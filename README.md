> [!IMPORTANT] 
> #Toute la partie docker a été généré par IA
> Cela est dû au manque de temps, mais surtout car le sujet principal du TM n'est pas l'utilisation de Docker.
> En conséquence, mes connaissances en Docker ne sont pas suffisantes pour certains éléments
> [!TIP]
> Chaque code généré par IA contiendra en haut de page un commentaire soulignant sa provenance.

## Exigences

Installer Docker en suivant le tutoriel [ici](https://docs.docker.com/engine/).

Vérifier avec:

```bash
docker compose version
```
## Lancer un des exercices

Depuis le dossier principal du projet, choisir un des exercices avec `EX` et lancer:

```bash
EX=path-traversal-vuln docker compose up --build
```

Ouvrir le site <http://localhost:8080> sur lequel se trouve l'exercice.

## Exercices disponibles

- `brute-force-vuln`, `brute-force-solution`
- `cookies-vuln`, `cookies-solution`
- `path-traversal-vuln`, `path-traversal-solution`
- `blind-sql-vuln`, `blind-sql-solution`
- `password-sql-vuln`, `password-sql-solution`
- `union-sql-vuln`, `union-sql-solution`
- `xss-vuln`, `xss-solution`

Par exemple:

```bash
EX=xss-vuln docker compose up --build
```

Pour lancer sur un autre port:

```bash
WEB_PORT=8081 EX=xss-vuln docker compose up --build
```

Ouvrir ensuite <http://localhost:8081>.

## Pour terminer

Arrêter le serveur et supprimer le container Docker

```bash
docker compose down -v
```
