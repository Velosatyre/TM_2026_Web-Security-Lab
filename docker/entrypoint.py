import os
import sys
from pathlib import Path


DEMOS = {
    "brute-force-vuln": "Authentification/Brute force/vuln.py",
    "brute-force-solution": "Authentification/Brute force/Soultion.py",
    "cookies-vuln": "Authentification/cookies_Vuln/cookies_Vuln.py",
    "cookies-solution": "Authentification/cookies_Vuln/cookies_Solution.py",
    "path-traversal-vuln": "Path_Traversal/server_Vuln.py",
    "path-traversal-solution": "Path_Traversal/server_Solution.py",
    "blind-sql-vuln": "SQL injections/Blind SQL/Vuln.py",
    "blind-sql-solution": "SQL injections/Blind SQL/solution.py",
    "password-sql-vuln": "SQL injections/Password_retrieving/SQL_injection_Vuln.py",
    "password-sql-solution": "SQL injections/Password_retrieving/SQL_injection_Solution.py",
    "union-sql-vuln": "SQL injections/Union based/Vuln.py",
    "union-sql-solution": "SQL injections/Union based/solution.py",
    "xss-vuln": "XSS/Vuln.py",
    "xss-solution": "XSS/Solution.py",
}


def main() -> None:
    demo_name = os.environ.get("DEMO", "path-traversal-vuln")
    try:
        relative_script = DEMOS[demo_name]
    except KeyError:
        available = ", ".join(sorted(DEMOS))
        raise SystemExit(f"Unknown DEMO={demo_name!r}. Choose one of: {available}")

    project_root = Path(__file__).resolve().parents[1]
    script = project_root / relative_script
    os.chdir(script.parent)
    os.execv(sys.executable, [sys.executable, script.name])


if __name__ == "__main__":
    main()
