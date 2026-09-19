# epsi-module-dataops

Repo contenant les TD que je dispense à l'école EPSI pour les étudiants en Master d'informatique, pour le module DataOps.

## Prérequis techniques

Pour mener à bien le TD, vous trouverez d'abord les prérequis technique.

### 1. Comptes et accès
* **GitHub :** Un compte personnel.
* **AWS :** Je vous fournirai un accès au début du TD à mon compte AWS.

### 2. Système d'exploitation
* **macOS / Linux :** Vous n'avez rien à faire.
* **Windows :** Il est **fortement recommandé** d'installer et d'utiliser **WSL 2** (Windows Subsystem for Linux) avec une distribution Ubuntu.

### 3. "Toolkit" DataOps
Installez les outils suivants et assurez-vous qu'ils sont accessibles depuis votre terminal (ajoutés au `PATH`) :
* **Git :** Outil de versionnement de code. (Configurez votre identité via `git config --global`).
* **Python 3.10+ :** Avec le gestionnaire de paquets `pip` fonctionnel.
* **Docker & Docker Compose :** Indispensable pour faire tourner localement l'orchestrateur et les outils de transformation.
* **Terraform CLI :** (Version >= 1.5). Le moteur d'IaC pour déployer nos environnements Cloud.
* **AWS CLI (v2) :** L'interface en ligne de commande pour interagir avec le cloud AWS.
* **GNU Make :** Pour exécuter nos raccourcis d'automatisation.

### 4. L'environnement de développement (IDE)
L'éditeur standard recommandé pour ce cours est **Visual Studio Code (VS Code)**. Installez impérativement les extensions suivantes :
* **Python** + **Pylance**
* **HashiCorp Terraform**
* **Docker**
* *(Optionnel)* **GitHub Actions** et **dbt Power User**

**✅ Le test de validation**
Exécutez ces commandes dans votre terminal. Si aucune ne renvoie d'erreur, vous êtes prêts pour la mission :
`git --version`, `python --version`, `pip --version`, `docker --version`, `docker-compose --version`, `terraform --version`, `aws --version`, `make --version`.

<br><br>

---
<br><br>

## TD -  Mission DataOps : Opération "ShopOps"

### Contexte de la mission

Bienvenue chez **ShopOps**, une plateforme e-commerce française en hyper-croissance opérant à l'international (Europe, US, UK).
Jusqu'à la semaine dernière, notre infrastructure data tenait sur des scripts artisanaux. La catastrophe redoutée a fini par arriver : une mise à jour d'un développeur backend a silencieusement corrompu nos données de ventes. Le CEO a présenté un tableau de bord financier totalement faux aux investisseurs. **La confiance envers la donnée est brisée.**

En tant que nouvelle recrue Data Engineer, vous intégrez la nouvelle "Task Force DataOps". Votre mission : reprendre l'architecture de zéro, instaurer une rigueur logicielle à notre chaîne de traitement de données, et ramener la confiance.

<br>

### Exigence de la direction Financière (CFO)

> <br>
>Équipe Data,
>
> Depuis notre expansion internationale, notre tableau de bord des revenus est incompréhensible. Le montant total additionne des dollars, des livres sterling et des euros sans aucune logique ! En tant qu'entreprise dont le siège est à Paris, j'exige une vision consolidée de notre chiffre d'affaires quotidien dans notre devise de référence.
>
> De plus, notre catalogue tarifaire évolue souvent. J'ai de sérieux doutes sur notre calcul de marge : j'ai l'impression que le système applique les prix actuels du catalogue sur des commandes qui ont été passées il y a 6 mois.
>
> Réglez ça avec l'aide du nouveau Data Engineer, et assurez-vous qu'aucune donnée aberrante ne puisse plus jamais polluer mes rapports.
> <br>



<br>

### Dictionnaire des sources (couche Bronze)

L'API du site web vous livre 5 flux de données brutes :
1. **`raw_customers`** : Base CRM clients (`id`, `name`, `country`, `signup_date`).
2. **`raw_orders`** : Transactions (`order_id`, `customer_id`, `product_id`, `quantity`, `order_date`, `status`).
3. **`raw_payments`** : Flux financiers (`payment_id`, `order_id`, `amount`, `currency` ,`payment_method`).
4. **`products_scd2`** : Historique du catalogue tarifaire (`product_id`, `price`, `start_date`, `end_date`).
5. **`exchange_rates`** : Taux de change (`date`, `currency_from`, `currency_to`, `rate`). *Attention : Les marchés financiers ferment le week-end.*

<br>

### Évaluation et critères de succès (score sur 20)

Votre infrastructure sera évaluée par le système CI/CD présent dans le projet.

*   **Standardisation et infra (4 points)** : Exécution propre du pre-commit local et isolation stricte des environnements cloud.
*   **Contrats de données (4 points)** : Blocage effectif des données aberrantes à l'ingestion.
*   **Versionnement (4 points)** : Capacité prouvée à restaurer une table corrompue à un instant précis dans le passé.
*   **Observabilité et résilience (4 points)** : Orchestration fluide et relance automatique fonctionnelle en cas d'erreur.
*   **Déploiement continu (4 points)** : Validation stricte des tests dans le pipeline CI avant tout déploiement simulé.

<br>

### Niveaux de la mission

<br>

#### Niveau 1 : Mettre en place les fondations (DevOps)
Actuellement, tout le monde manipule le même dossier S3. L'équipe sécurité exige une séparation physique étanche entre les données de développement et les données de production.

**Votre objectif :**
* Déployez l'infrastructure de stockage Cloud via du code de manière isolée pour votre environnement.
* Instaurez une politique stricte sur votre dépôt Git local : aucun code mal formaté ou contenant des erreurs de syntaxe de base ne doit pouvoir être validé (commit).

#### Niveau 2 : Qualité et contrats de données
Notre partenaire est instable. Il arrive que des commandes soient annulées mais remontent avec des montants de paiement négatifs, ou que des paiements soient orphelins (sans client associé).

Directive du Tech Lead :
"Le CFO veut son tableau de bord à 6h00 précises. Il est hors de question de stopper tout le pipeline pour 5 commandes aberrantes.
Cependant, nous avons deux exigences contradictoires :
1. L'équipe d'Audit Logistique exige de pouvoir consulter toutes les commandes corrompues (montants négatifs, clients fantômes) pour facturer des pénalités au fournisseur.
2. Le CFO exige que les modèles analytiques finaux soient impossibles à polluer, même par erreur.

Votre mission :
Implémentez la stratégie d'architecture DataOps qui répond à ces deux besoins de manière automatisée."

**Votre objectif :**
* Mettez en place un rempart logiciel (via `dbt`) entre la donnée brute (Bronze) et la donnée nettoyée (Silver).
* Implémentez la stratégie d'architecture DataOps qui répond à ces deux besoins de manière automatisée."

#### Niveau 3 : Consolidation des données et fonctionnalité de Rollback
Vous devez créer la table finale `gold_revenue_daily` réclamée par le CFO, en résolvant le problème de tarification historique et de standardisation de devise.

**Votre objectif :**
* Modélisez cette table finale.
* **Alerte :** Pendant votre développement, un script s'emballe et supprime accidentellement tout l'historique des revenus de 2025. Vous n'avez pas de backup classique sous la main. Exploitez les métadonnées de votre format de table (Iceberg) pour annuler cette action et ramener la table exactement telle qu'elle était juste avant votre erreur. Fournissez la requête SQL de sauvetage.

#### Niveau 4 : Orchestration
Les flux de données arrivent à des heures imprévisibles au milieu de la nuit.

**Votre objectif :**
* Automatisez l'enchaînement de vos validations et de vos transformations.
* Le système d'ingestion des taux de change subit souvent des micro-coupures réseau à 2h du matin. Configurez votre orchestrateur pour qu'il encaisse ces échecs temporaires de manière résiliente, sans que vous n'ayez à vous lever pour relancer le système manuellement.

#### Niveau 5 : CI/CD et lignage
La direction refuse de consulter vos données si la documentation n'est pas à jour et si le code n'est pas testé par un tiers de confiance.

**Votre objectif :**
* Liez votre code de transformation à sa documentation technique.
* Configurez le dépôt Git pour que chaque nouvelle modification pousse un automate à vérifier la syntaxe et la logique des tests de données avant d'autoriser le déploiement de l'infrastructure.
