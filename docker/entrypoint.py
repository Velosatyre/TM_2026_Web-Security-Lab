# Code généré par IA

import os
import sys
from pathlib import Path


EXs = {
    "brute-force-vuln": "Authentification/Brute force/vuln.py",
    "brute-force-solution": "Authentification/Brute force/Solution.py",
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


def main():
    """
    Gère le lancement de l'exercice demandé.

    - Prend le nom contenu dans la variable EX.
    Regarde si le fichier est présent dans le dictionnaire EXs.

    - Si oui, choisit le répertoire dans lequel se trouve le fichier demandé.
    Enfin, exécute le fichier demandé.

    """

    Ex_name = os.environ.get("EX", "path-traversal-vuln")
    try:
        relative_script = EXs[Ex_name]
    except KeyError:
        available = ", ".join(sorted(EXs))
        raise SystemExit(f"Unknown Exercice={Ex_name!r}. Choose one of: {available}")

    project_root = Path(__file__).resolve().parents[1]
    script = project_root / relative_script
    os.chdir(script.parent)
    os.execv(sys.executable, [sys.executable, script.name])


if __name__ == "__main__":
    main()
