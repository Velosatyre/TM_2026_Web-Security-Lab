# Web Server Vulnerability Lab

Ce projet a été conçu dans le cadre d'un Travail de Maturité afin d'illustrer plusieurs vulnérabilités web classiques et leurs solutions associées.

L'objectif est de comprendre concrètement le fonctionnement de certaines failles de sécurité web, tout en présentant des versions corrigées qui montrent comment les remédiations peuvent être mises en place.

## Objectif du projet

Le projet présente plusieurs exercices de sécurité web basés sur des vulnérabilités réelles, notamment :

- Path Traversal
- Authentification
- Injections SQL

---

## Exercices disponibles

Le projet contient les exercices suivants :

- `brute-force-vuln`, `brute-force-solution`
- `cookies-vuln`, `cookies-solution`
- `path-traversal-vuln`, `path-traversal-solution`
- `blind-sql-vuln`, `blind-sql-solution`
- `password-sql-vuln`, `password-sql-solution`
- `union-sql-vuln`, `union-sql-solution`

---

## Description des vulnérabilités

### 1. Path Traversal

Cette vulnérabilité permet d'accéder à des fichiers du système qui ne sont pas censés être accessibles depuis le serveur web.

Exemple : un utilisateur peut demander un fichier arbitraire via l'URL, et le serveur le lit sans vérifier si le chemin est bien contenu dans le répertoire autorisé.

### 2. Authentification

#### Brute Force

Le serveur n'impose pas de limite au nombre de tentatives de connexion. Un attaquant peut donc tester un grand nombre de combinaisons de mots de passe.

#### Cookies

Le serveur utilise des cookies de manière non sécurisée. Un utilisateur peut modifier la valeur d'un cookie pour se faire passer pour un autre compte ou pour réussir une connexion non autorisée.

### 3. Injections SQL

#### Password retrieving

Les informations de connexion sont directement concaténées dans des requêtes SQL, sans filtrage ni validation.

#### UNION-based SQL injection

Une injection SQL peut être utilisée pour modifier la structure d'une requête et récupérer des informations supplémentaires depuis la base de données.

#### Blind SQL injection

Le serveur ne renvoie pas directement le résultat de la requête SQL, mais son comportement ou ses réponses diffèrent selon le résultat. Cela permet de réaliser une attaque par tâtonnement.

---

## Prérequis

Assurez-vous d'avoir Docker et Docker Compose installés sur votre machine.

Vérification :

```bash
docker compose version
```

Si cette commande fonctionne, le projet est prêt à être lancé.

---

## Lancer un exercice

Depuis le dossier principal du projet, choisissez un exercice avec la variable `EX` et lancez le conteneur :

```bash
EX=path-traversal-vuln docker compose up --build
```

Si vous avez un doute sur la syntaxe des noms des exercices, il vous suffit de ne pas mettre la variable Ex et vous verrez une liste des exercices.


Ensuite, ouvrez le site dans votre navigateur :

```text
http://localhost:8080
```

---

## Exemples de lancement

### Exemple 1 : exercice vulnérable

```bash
EX=cookies-vuln docker compose up --build
```

### Exemple 2 : version corrigée

```bash
EX=cookies-solution docker compose up --build
```

### Changer le port

```bash
WEB_PORT=8081 EX=cookies-vuln docker compose up --build
```

Puis ouvrir :

```text
http://localhost:8081
```

### Utiliser une autre adresse d'écoute

```bash
WEB_HOST=194.35.21.1 EX=cookies-vuln docker compose up --build
```

Puis ouvrir :

```text
http://194.35.21.1:8080
```

---

## Arrêter les conteneurs

Pour arrêter le serveur et supprimer les conteneurs associés :

```bash
docker compose down -v
```

---

## Structure du projet

- `Authentification/` : Exercices liés à l'authentification et aux cookies
- `Path_Traversal/` : Exercices de path traversal
- `SQL_injections/` : Exercices sur les injections SQL
- `docker/` : Fichiers de configuration Docker et initialisation de la base de données
- `docker-compose.yml` : Configuration des services applicatifs
- `Dockerfile` : Image applicative Python

---

> [!IMPORTANT] 
> La majorité de la partie docker a été généré par IA
> Cela est dû au manque de temps, mais surtout car le sujet principal du TM n'est pas l'utilisation de Docker.
> En conséquence, mes connaissances en Docker ne sont pas suffisantes pour certains éléments

> [!TIP]
> Chaque code généré par IA contiendra en haut de page un commentaire soulignant sa provenance.