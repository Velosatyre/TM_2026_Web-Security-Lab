import os
import sys
from pathlib import Path


EXs = {
    "brute-force-vuln": "Authentification/Brute_force/Brute_Vuln.py",
    "brute-force-solution": "Authentification/Brute_force/Brute_Solution.py",

    "cookies-vuln": "Authentification/cookies_Vuln/cookies_Vuln.py",
    "cookies-solution": "Authentification/cookies_Vuln/cookies_Solution.py",

    "path-traversal-vuln": "Path_Traversal/Path_Vuln.py",
    "path-traversal-solution": "Path_Traversal/Path_Solution.py",

    "blind-sql-vuln": "SQL_injections/Blind_SQL/Blind_Vuln.py",
    "blind-sql-solution": "SQL_injections/Blind_SQL/Blind_Solution.py",

    "password-sql-vuln": "SQL_injections/Password_retrieving/SQL_injection_Vuln.py",
    "password-sql-solution": "SQL_injections/Password_retrieving/SQL_injection_Solution.py",
    
    "union-sql-vuln": "SQL_injections/Union_based/Union_Vuln.py",
    "union-sql-solution": "SQL_injections/Union_based/Union_Solution.py",
}

# Code généré par Copilot de VS code, le 9.9.2026
def main():
    """
    Gère le lancement de l'exercice demandé.

    - Prend le nom contenu dans la variable EX.
    Regarde si le fichier est présent dans le dictionnaire EXs.

    - Si oui, choisit le répertoire dans lequel se trouve le fichier demandé.
    Enfin, exécute le fichier demandé.

    """

    Ex_name = os.environ.get("EX")
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
