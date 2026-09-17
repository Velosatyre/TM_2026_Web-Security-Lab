import os
import socket
import subprocess
import sys
import time
import unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import urlopen


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PORT = 8080
STARTUP_TIMEOUT = 10


SERVER_SCRIPTS = [
	path
	for path in sorted(PROJECT_ROOT.rglob("*.py"))
	if path.name.endswith(("_Vuln.py", "_Solution.py"))
]


def server_host():
	with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as connection:
		connection.connect(("8.8.8.8", 80))
		return connection.getsockname()[0]


def wait_for_server(process):
	host = server_host()
	deadline = time.monotonic() + STARTUP_TIMEOUT
	while time.monotonic() < deadline:
		if process.poll() is not None:
			output = process.stdout.read()
			raise AssertionError(
				f"Server exited before accepting requests (exit code "
				f"{process.returncode}):\n{output}"
			)

		try:
			with socket.create_connection((host, PORT), timeout=0.2):
				return
		except OSError:
			time.sleep(0.1)

	output = process.stdout.read()
	raise AssertionError(
		f"Server did not start within {STARTUP_TIMEOUT} seconds:\n{output}"
	)


class WebServerSmokeTests(unittest.TestCase):
	def test_every_server_accepts_a_get_request(self):
		self.assertTrue(SERVER_SCRIPTS, "No server scripts were found")
		host = server_host()

		failures = []
		for script in SERVER_SCRIPTS:
			process = subprocess.Popen(
				[sys.executable, script.name],
				cwd=script.parent,
				env={**os.environ, "BROWSER": "/bin/true"},
				stdout=subprocess.PIPE,
				stderr=subprocess.STDOUT,
				text=True,
			)
			try:
				wait_for_server(process)
				try:
					with urlopen(f"http://{host}:{PORT}/", timeout=3) as response:
						body = response.read()
						status = response.status
				except HTTPError as error:
					status = error.code
					body = error.read()

				self.assertGreaterEqual(status, 200)
				self.assertLess(status, 500)
				self.assertTrue(body, f"{script} returned an empty response")
			except (AssertionError, OSError) as error:
				failures.append(f"{script.relative_to(PROJECT_ROOT)}: {error}")
			finally:
				process.terminate()
				try:
					process.wait(timeout=3)
				except subprocess.TimeoutExpired:
					process.kill()
					process.wait()
				process.stdout.close()

		if failures:
			self.fail("\n".join(failures))


if __name__ == "__main__":
	unittest.main()
