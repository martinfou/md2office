---
title: Formation Microsoft Copilot 365 - Prompt Engineering
author: Institution Financière Québécoise
subtitle: Prompt Engineering pour les Équipes Agiles
---

# Formation Microsoft Copilot 365

Prompt Engineering pour les Équipes Agiles

**Public cible** : QA, Analystes fonctionnels, Product Owners, Gestionnaires, Scrum Masters  
**Durée totale** : 5 heures et 20 minutes (8 modules)  
**Contexte** : Institution financière québécoise

## Objectifs de la Formation

### Objectifs Principaux

1. Structurer des prompts efficaces avec CTF et CRISPE
2. Itérer et raffiner ses prompts
3. Utiliser le few-shot learning
4. Appliquer des contraintes et critères de qualité
5. Adapter le ton et utiliser des personas
6. Créer de la documentation Confluence avec Mermaid
7. Rédiger des épics, stories et tâches Jira de qualité
8. Améliorer la productivité quotidienne

## Vue d'Ensemble de la Formation

### Modules et Durées

| Module | Titre | Durée |
|--------|-------|-------|
| Module 01 | Introduction et CTF | 45 min |
| Module 02 | Itération et Raffinement | 40 min |
| Module 03 | Few-Shot Learning | 40 min |
| Module 04 | Contraintes et Critères de Qualité | 35 min |
| Module 05 | Personas et Ton | 35 min |
| Module 06 | Framework CRISPE Complet | 45 min |
| Module 07 | Confluence et Mermaid | 50 min |
| Module 08 | Jira | 50 min |
| **Total** | **8 modules** | **5h20** |

## Public Cible

### Rôles Visés

- **QA** (Quality Assurance)
- **Analystes fonctionnels**
- **Product Owners**
- **Gestionnaires**
- **Scrum Masters**

### Prérequis

- Utilisation basique de Copilot 365
- Connaissance des outils agiles (Jira, Confluence)
- Aucune compétence technique en développement requise

## Module 01 : Introduction et CTF

### Module 01 - Introduction

**Durée** : 45 minutes

**Objectifs d'apprentissage** :

1. Identifier les trois composants essentiels d'un prompt efficace
2. Structurer un prompt de base en utilisant CTF
3. Distinguer un prompt efficace d'un prompt basique
4. Appliquer CTF dans Confluence et Jira

### Qu'est-ce que CTF ?

**CTF : Context, Task, Format**

- **Context** : Informations de contexte nécessaires
- **Task** : Tâche précise à accomplir
- **Format** : Format de sortie souhaité

Ces trois composants travaillent ensemble pour créer un prompt efficace et structuré.

### Exemple Avant/Après - CTF

**Exemple : Amélioration d'une Story Jira**

**Avant** (prompt inefficace) :
```
Améliore cette story Jira
```

**Après** (prompt avec CTF) :
- **Contexte** : Product Owner, institution financière, backend Spring Boot
- **Tâche** : Améliorer la story pour qu'elle soit claire et actionnable
- **Format** : Story avec Description, Critères d'acceptation, Notes techniques

### Bonnes Pratiques CTF

1. Toujours commencer par le contexte
2. Être spécifique dans la tâche
3. Demander un format structuré
4. Adapter le contexte au public cible
5. Inclure les contraintes métier

## Module 02 : Itération et Raffinement

### Module 02 - Introduction

**Durée** : 40 minutes

**Objectifs** :

1. Reconnaître les signes qu'un prompt nécessite un raffinement
2. Itérer sur un prompt initial
3. Utiliser le feedback de Copilot
4. Appliquer des techniques de raffinement

### Le Cycle d'Itération

**Processus d'amélioration continue** :

1. **Prompt Initial** → Génère un résultat
2. **Résultat** → Évaluation de la qualité
3. **Évaluation** → Identification des améliorations
4. **Feedback** → Ajustements spécifiques
5. **Prompt Amélioré** → Nouveau cycle

Ce cycle se répète jusqu'à obtenir le résultat souhaité.

### Techniques de Raffinement

1. Ajouter des détails au contexte
2. Clarifier et préciser la tâche
3. Renforcer le format avec des exemples
4. Utiliser le feedback de Copilot
5. Itérer sur des aspects spécifiques

## Module 03 : Few-Shot Learning

### Module 03 - Introduction

**Durée** : 40 minutes

**Objectifs** :

1. Comprendre le concept de few-shot learning
2. Identifier les situations où fournir des exemples est bénéfique
3. Structurer des exemples efficaces
4. Utiliser des exemples pour guider Copilot

### Qu'est-ce que le Few-Shot Learning ?

**Définition** : Technique où vous fournissez à Copilot quelques exemples (2-5) de ce que vous voulez obtenir.

**Analogie** : "C'est comme montrer des photos plutôt que de décrire avec des mots"

**Avantages** :
- Clarté visuelle
- Apprentissage par pattern
- Adaptation au contexte
- Réduction de l'ambiguïté

### Exemple Few-Shot Learning

**Exemple : User Story avec Format Spécifique**

**Structure du prompt avec exemples** :
- Contexte
- Tâche
- Format
- **Exemples** (2-3 user stories existantes)
- Demande spécifique

**Résultat** : User story qui suit exactement le format des exemples fournis.

## Module 04 : Contraintes et Critères de Qualité

### Module 04 - Introduction

**Durée** : 35 minutes

**Objectifs** :

1. Définir des contraintes appropriées
2. Établir des critères de qualité mesurables
3. Appliquer des contraintes métier
4. Utiliser des contraintes pour garantir la conformité

### Types de Contraintes

1. **Format** : Structure, longueur, style
2. **Contenu** : Éléments à inclure/exclure
3. **Style** : Ton, langage, niveau technique
4. **Longueur** : Nombre de mots, sections, points
5. **Conformité** : Standards, réglementations
6. **Technique** : Outils, technologies, intégrations

### Critères de Qualité

1. **Clarté** : Résultat clair et compréhensible
2. **Complétude** : Tous les éléments requis présents
3. **Pertinence** : Adapté au contexte et besoins
4. **Mesurabilité** : Peut être évalué objectivement

## Module 05 : Personas et Ton

### Module 05 - Introduction

**Durée** : 35 minutes

**Objectifs** :

1. Comprendre l'impact des personas
2. Sélectionner un persona approprié
3. Adapter le ton selon le contexte
4. Utiliser des personas pour créer de la documentation

### Qu'est-ce qu'un Persona ?

**Définition** : Rôle ou identité que vous assignez à Copilot.

**Exemples de personas** :
- Expert en sécurité bancaire
- Product Owner expérimenté
- Rédacteur technique spécialisé
- Analyste fonctionnel expérimenté

**Impact** :
- Perspective spécialisée
- Adaptation au public
- Cohérence du style

### Adaptation du Ton

**Types de ton** :

- **Professionnel** : Formel, respectueux, institutionnel
- **Technique** : Spécialisé, précis, avec jargon approprié
- **Accessible** : Clair, simple, adapté aux non-experts
- **Conversationnel** : Informel, amical, engageant

**Adaptation selon le public cible** : Choisir le ton approprié selon le contexte et les destinataires.

## Module 06 : Framework CRISPE Complet

### Module 06 - Introduction

**Durée** : 45 minutes

**Objectifs** :

1. Maîtriser les six composants de CRISPE
2. Structurer un prompt complet avec CRISPE
3. Intégrer tous les concepts précédents
4. Appliquer CRISPE dans Confluence et Jira

### Les Six Composants de CRISPE

**CRISPE : Les Six Composants**

- **C** - Context (Contexte)
- **R** - Role (Rôle/Persona)
- **I** - Instructions (Instructions/Tâche)
- **S** - Style (Style/Ton)
- **P** - Parameters (Paramètres/Contraintes)
- **E** - Examples (Exemples)

Ces composants travaillent ensemble pour créer un prompt complet et précis.

### CRISPE vs CTF

**Comparaison** :

- **CTF** : Context, Task, Format (base)
- **CRISPE** : Ajoute Role, Style, Examples (avancé)

**Avantages de CRISPE** :
- Intégration complète
- Précision accrue
- Cohérence
- Flexibilité

### Exemple CRISPE Complet

**Exemple : User Story avec CRISPE**

**Structure complète du prompt CRISPE** :
- **Context** : Détaillé avec informations métier
- **Role** : Product Owner expérimenté
- **Instructions** : Détaillées et spécifiques
- **Style** : Professionnel mais accessible
- **Parameters** : Contraintes complètes
- **Examples** : 2-3 user stories existantes

**Résultat** : User story complète et précise qui respecte tous les critères.

## Module 07 : Confluence et Mermaid

### Module 07 - Introduction

**Durée** : 50 minutes

**Objectifs** :

1. Créer des prompts efficaces pour Confluence
2. Générer des diagrammes Mermaid via prompts
3. Mettre à jour la documentation existante
4. Structurer la documentation selon les meilleures pratiques

### Application de CTF à Confluence

**Template CTF pour documentation** :

- **Contexte** : Rôle, organisation, contexte métier
- **Tâche** : Ce que vous voulez créer ou mettre à jour
- **Format** : Structure Confluence souhaitée

**Exemple** : Documentation de processus avec sections structurées.

### Types de Diagrammes Mermaid

**Six types principaux** :

1. **Flowchart** : Flux de processus
2. **Sequence Diagram** : Interactions entre composants
3. **Class Diagram** : Structure de classes
4. **State Diagram** : Transitions d'état
5. **Gantt Chart** : Planning et échéances
6. **Git Graph** : Branches et commits

### Exemple : Génération de Flowchart

**Exemple : Processus de Déploiement**

**Prompt pour générer un flowchart** :
- **Contexte** : DevOps, institution financière
- **Tâche** : Créer un diagramme Mermaid flowchart
- **Format** : Flowchart avec étapes et décisions

**Résultat** : Diagramme Mermaid complet prêt à être intégré dans Confluence.

## Module 08 : Jira

### Module 08 - Introduction

**Durée** : 50 minutes

**Objectifs** :

1. Rédiger des épics de qualité
2. Créer des user stories efficaces
3. Définir des tâches claires
4. Améliorer des artefacts Jira existants

### Types d'Artefacts Jira

**Trois types principaux** :

1. **Epic** : Grande initiative contenant plusieurs stories
2. **User Story** : Fonctionnalité du point de vue utilisateur
3. **Task** : Tâche technique ou de travail

**Hiérarchie** : Epic → Story → Task

### Format INVEST pour User Stories

**INVEST** :

- **I** - Independent (Indépendante)
- **N** - Negotiable (Négociable)
- **V** - Valuable (Valuable)
- **E** - Estimable (Estimable)
- **S** - Small (Petite)
- **T** - Testable (Testable)

Une user story de qualité respecte tous ces critères.

### Exemple : Amélioration d'une User Story

**Exemple : Amélioration avec CRISPE**

**Avant** :
```
Permettre aux utilisateurs de payer
```

**Après** : User story complète avec :
- Titre format "En tant que... je veux... afin de..."
- Description détaillée
- Critères d'acceptation mesurables
- Notes techniques
- Définition de "Terminé"

## Récapitulatif de la Formation

### Concepts Clés Appris

1. **CTF** : Structure de base
2. **Itération** : Amélioration progressive
3. **Few-Shot Learning** : Utilisation d'exemples
4. **Contraintes** : Définir des limites
5. **Personas et Ton** : Adapter au contexte
6. **CRISPE** : Framework complet
7. **Confluence** : Documentation professionnelle
8. **Jira** : Artefacts de qualité

## Prochaines Étapes

### Actions Recommandées

1. Pratiquer avec les quiz interactifs
2. Compléter les exercices pratiques
3. Appliquer les techniques dans votre travail quotidien
4. Partager vos apprentissages avec l'équipe
5. Continuer à raffiner vos prompts

## Ressources et Support

### Ressources Disponibles

- Templates Confluence et Jira
- Exemples de prompts
- Documentation de référence
- Support et questions

**Contact** : Informations de contact disponibles

## Questions et Réponses

Merci pour votre attention !

Questions ou commentaires ?

---

## Notes de Design (Référence)

### Palette de Couleurs

- **Bleu principal** : #003366 (institutionnel)
- **Bleu secondaire** : #0066CC (accents)
- **Bleu clair** : #E1F5FF (arrière-plans)
- **Blanc** : #FFFFFF (texte sur fond sombre)
- **Gris foncé** : #333333 (texte principal)
- **Gris clair** : #F5F5F5 (arrière-plans alternatifs)

### Typographie

- **Titres** : Calibri Bold, 44pt (titre principal), 36pt (titres de section), 28pt (sous-titres)
- **Corps** : Calibri Regular, 18pt (texte principal), 16pt (listes)
- **Code/Prompts** : Consolas ou Courier New, 14pt

### Éléments Visuels

- **Icônes** : Utiliser des icônes cohérentes (Flaticon, Icons8, ou bibliothèque Microsoft)
- **Diagrammes** : Créer des diagrammes dans PowerPoint ou utiliser des outils externes
- **Captures d'écran** : Ajouter des captures d'écran de Copilot 365, Confluence, Jira
- **Exemples de code** : Utiliser des code blocks avec syntax highlighting

### Animations et Transitions

- **Transitions entre slides** : "Fondu" ou "Poussée" (subtiles)
- **Animations** : Apparition progressive pour les listes à puces
- **Timing** : Animations rapides (0.5-1 seconde)

### Mise en Page

- **Marges** : Respecter les marges standards
- **Espacement** : Espacement généreux entre les éléments
- **Alignement** : Alignement cohérent (gauche pour texte, centré pour titres)
- **Hiérarchie visuelle** : Utiliser la taille, la couleur et l'espacement pour créer une hiérarchie claire

### Notes pour le Créateur de la Présentation

1. **Créer un template de base** avec les couleurs et polices définies
2. **Utiliser des masques de diapositives** pour maintenir la cohérence
3. **Ajouter des logos** institutionnels si disponibles
4. **Créer des diagrammes** directement dans PowerPoint ou utiliser des outils externes
5. **Tester les animations** pour s'assurer qu'elles sont fluides
6. **Vérifier la lisibilité** sur différents écrans et projecteurs
7. **Ajouter des notes** pour le présentateur si nécessaire
8. **Optimiser les images** pour réduire la taille du fichier

*End of presentation*
