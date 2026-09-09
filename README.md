# Web security demonstrations in Docker

This project contains intentionally vulnerable and corrected Python web-server examples. Run only on a local machine or an isolated lab network.

## Requirements

Install Docker with the Compose plugin. Verify with:

```bash
docker compose version
```

## Start a demo

From the project root, choose one demo with `DEMO` and start the stack:

```bash
DEMO=path-traversal-vuln docker compose up --build
```

Open the website in a local browser at <http://localhost:8080>. Stop it with `Ctrl+C`.

The container runs one server at a time because every original example uses port `8080`. The PostgreSQL container is started automatically for the SQL demos.

## Available demos

- `brute-force-vuln`, `brute-force-solution`
- `cookies-vuln`, `cookies-solution`
- `path-traversal-vuln`, `path-traversal-solution`
- `blind-sql-vuln`, `blind-sql-solution`
- `password-sql-vuln`, `password-sql-solution`
- `union-sql-vuln`, `union-sql-solution`
- `xss-vuln`, `xss-solution`

For example:

```bash
DEMO=xss-vuln docker compose up --build
```

To use another local port:

```bash
WEB_PORT=8081 DEMO=xss-vuln docker compose up --build
```

Then open <http://localhost:8081>.

To remove the database volume and reset its sample data:

```bash
docker compose down -v
```
