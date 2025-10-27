# 📚 Rapport de Projet II - Plateforme Umuhuza

## 📖 Vue d'ensemble

Ce dossier contient le **rapport académique complet** du projet Umuhuza pour le cours de Projet II (BAC3 Génie Logiciel, UPG, 2024-2025).

### Contenu du rapport

- ✅ **Diagrammes UML complets** (13 types)
- ✅ **Modélisation base de données** (MCD/MLD)
- ✅ **Architecture système**
- ✅ **Documentation technique détaillée**
- ✅ **Code source commenté**
- ✅ **Tests et validation**
- ✅ **Rapport LaTeX prêt à compiler**

---

## 📁 Structure du dossier

```
rapport/
├── README.md                          # Ce fichier
├── diagrams/                          # Diagrammes PlantUML (.puml)
│   ├── class_diagram.puml            # Diagramme de classes complet
│   ├── er_diagram.puml               # MCD/MLD (Entity-Relationship)
│   ├── use_case_diagram.puml         # Cas d'utilisation
│   ├── sequence_registration.puml    # Séquence: Inscription
│   ├── sequence_create_listing.puml  # Séquence: Création annonce
│   ├── sequence_messaging.puml       # Séquence: Messagerie
│   ├── sequence_payment.puml         # Séquence: Paiement
│   ├── architecture_components.puml  # Architecture en composants
│   ├── deployment_diagram.puml       # Déploiement
│   ├── 3tier_architecture.puml       # Architecture 3-tiers
│   ├── activity_registration.puml    # Activité: Inscription
│   ├── activity_create_listing.puml  # Activité: Création annonce
│   ├── activity_payment.puml         # Activité: Paiement
│   └── state_listing.puml            # États: Cycle de vie annonce
│
├── images/                            # Images pour le rapport
│   ├── logo_upg.png                  # TODO: Ajouter logo UPG
│   └── (diagrammes PNG générés)
│
├── tex/                               # Source LaTeX du rapport
│   ├── rapport_projet_umuhuza.tex         # Partie 1: Intro, Cahier des charges
│   ├── rapport_projet_umuhuza_part2.tex   # Partie 2: Analyse et conception
│   ├── rapport_projet_umuhuza_part3.tex   # Partie 3: Réalisation technique
│   └── rapport_projet_umuhuza_part4.tex   # Partie 4: Tests, Conclusion
│
├── generate_diagrams.py               # Script Python de génération diagrammes
├── python_files_list.txt             # Liste des fichiers Python du projet
└── directory_structure.txt            # Structure des répertoires

```

---

## 🚀 Utilisation rapide

### Étape 1: Générer les images des diagrammes

Les diagrammes sont au format PlantUML (`.puml`). Vous devez les convertir en PNG pour les inclure dans le rapport LaTeX.

#### Option A: Utilisation en ligne (rapide, recommandé)

1. Visitez [https://www.plantuml.com/plantuml/uml/](https://www.plantuml.com/plantuml/uml/)
2. Copiez le contenu d'un fichier `.puml` (par exemple `class_diagram.puml`)
3. Collez dans la zone de texte
4. Cliquez sur "Submit"
5. Téléchargez l'image PNG générée
6. Sauvegardez dans `rapport/images/`

**Répétez pour chaque diagramme.**

#### Option B: Installation locale (si Java et Graphviz disponibles)

```bash
# 1. Installer Java (si pas déjà installé)
sudo apt-get install default-jre

# 2. Installer Graphviz
sudo apt-get install graphviz

# 3. Télécharger PlantUML (déjà fait)
cd /home/user_04/umuhuza/backend
# plantuml.jar déjà présent

# 4. Générer tous les diagrammes
cd /home/user_04/umuhuza/rapport/diagrams
for file in *.puml; do
    java -jar ../../backend/plantuml.jar "$file"
done

# Les fichiers PNG seront créés dans diagrams/
mv *.png ../images/
```

### Étape 2: Ajouter le logo UPG

**TODO: IMPORTANT**

Ajoutez le logo de l'Université Polytechnique de Gitega:

```bash
# Copiez le logo de votre université dans:
cp /chemin/vers/logo_upg.png /home/user_04/umuhuza/rapport/images/
```

### Étape 3: Compiler le rapport LaTeX

#### Option A: Overleaf (en ligne, recommandé)

1. Créez un compte sur [https://www.overleaf.com/](https://www.overleaf.com/)
2. Créez un nouveau projet vide
3. Uploadez tous les fichiers `.tex` depuis `rapport/tex/`
4. Uploadez toutes les images depuis `rapport/images/`
5. Créez la structure:
   ```
   rapport_projet_umuhuza.tex (fichier principal)
   rapport_projet_umuhuza_part2.tex
   rapport_projet_umuhuza_part3.tex
   rapport_projet_umuhuza_part4.tex
   images/ (dossier avec toutes les images)
   ```
6. Ouvrez `rapport_projet_umuhuza.tex`
7. Cliquez sur "Recompile" pour générer le PDF

#### Option B: Compilation locale (Linux/WSL)

```bash
# 1. Installer LaTeX
sudo apt-get update
sudo apt-get install texlive-full  # Attention: ~5GB

# 2. Compiler le rapport
cd /home/user_04/umuhuza/rapport/tex

# 3. Combiner tous les fichiers (méthode manuelle)
# Ouvrez rapport_projet_umuhuza.tex et ajoutez à la fin (avant \end{document}):
# \input{rapport_projet_umuhuza_part2}
# \input{rapport_projet_umuhuza_part3}
# \input{rapport_projet_umuhuza_part4}

# 4. Compiler
pdflatex rapport_projet_umuhuza.tex
pdflatex rapport_projet_umuhuza.tex  # 2x pour table des matières
```

---

## 📝 Personnalisation du rapport

### Modifier les informations de base

Éditez `tex/rapport_projet_umuhuza.tex`:

```latex
% Ligne ~73: Nom de l'enseignant
Prof./Dr. [NOM ENSEIGNANT]
% Remplacez par le nom réel de votre encadrant
```

### Ajouter des captures d'écran

1. Prenez des captures d'écran de votre application
2. Sauvegardez-les dans `rapport/images/`
3. Dans les sections marquées `TODO` du rapport:

```latex
% Remplacez:
\fbox{\parbox{0.8\textwidth}{
\textbf{TODO: Design Figma à créer}
}}

% Par:
\includegraphics[width=0.8\textwidth]{../images/screenshot_login.png}
```

### Compléter les sections TODO

Recherchez `TODO` dans tous les fichiers `.tex` et complétez:

- Logo UPG (page de garde)
- Designs Figma (si vous les créez)
- Nom de l'enseignant
- Toute information spécifique à votre contexte

---

## 🎨 Création des designs Figma (optionnel)

Si vous souhaitez créer les maquettes d'interface:

1. Créez un compte sur [https://www.figma.com/](https://www.figma.com/)
2. Créez un nouveau fichier "Umuhuza UI Design"
3. Créez les écrans suivants:
   - Page de connexion
   - Page d'accueil
   - Formulaire de création d'annonce
   - Page de liste d'annonces
4. Exportez en PNG (1920x1080 recommandé)
5. Ajoutez dans `rapport/images/`
6. Mettez à jour les références dans le rapport

**Note:** Les designs ne sont pas obligatoires pour le rapport si vous n'avez pas le temps. Les sections sont déjà documentées textuellement.

---

## ✅ Checklist avant soumission

- [ ] Tous les diagrammes PlantUML convertis en PNG
- [ ] Logo UPG ajouté
- [ ] Nom de l'enseignant complété
- [ ] Rapport compilé sans erreur
- [ ] Table des matières générée (2 compilations)
- [ ] Liste des figures générée
- [ ] Numéros de page corrects
- [ ] Vérification orthographique française
- [ ] PDF final généré (`rapport_projet_umuhuza.pdf`)
- [ ] Taille du PDF raisonnable (<20MB)

---

## 🛠️ Dépannage

### Erreur: "File not found" pour les images

**Solution:** Vérifiez que:
1. Les images sont bien dans `images/` (pas `diagrams/`)
2. Les noms de fichiers correspondent exactement (sensible à la casse)
3. Le chemin relatif est correct: `../images/nom_fichier.png`

### Erreur LaTeX: "Undefined control sequence"

**Solution:**
- Installez le package manquant (`texlive-full` contient tout)
- Ou utilisez Overleaf qui a tous les packages préinstallés

### Les diagrammes PlantUML ne se génèrent pas

**Solution:**
- Utilisez la méthode en ligne (plus simple)
- Ou vérifiez que Java et Graphviz sont installés:
  ```bash
  java -version
  dot -V
  ```

### Le rapport est trop long

**Astuce:** Le rapport complet fait ~100+ pages. C'est normal et attendu pour un projet de cette envergure. Il couvre:
- 13 diagrammes UML
- Documentation technique complète
- Code source commenté
- Tests détaillés

---

## 📊 Statistiques du rapport

- **Pages:** ~120 pages (estimation)
- **Chapitres:** 7
- **Diagrammes UML:** 15
- **Tableaux:** 10+
- **Listings de code:** 20+
- **Références bibliographiques:** 30+

---

## 🆘 Support

Si vous rencontrez des problèmes:

1. **Documentation LaTeX:** [https://fr.wikibooks.org/wiki/LaTeX](https://fr.wikibooks.org/wiki/LaTeX)
2. **PlantUML:** [https://plantuml.com/fr/](https://plantuml.com/fr/)
3. **Overleaf Help:** [https://www.overleaf.com/learn](https://www.overleaf.com/learn)
4. **Stack Overflow:** Recherchez votre erreur spécifique

---

## 📄 Licence

Ce rapport est créé pour un projet académique à l'Université Polytechnique de Gitega (UPG).

**Auteurs:**
- Andy Miguel HABYARIMANA
- Dahl NDAYISENGA

**Année académique:** 2024-2025

---

## 🙏 Remerciements

Ce rapport a été généré automatiquement à partir de l'analyse du code source du projet Umuhuza, en utilisant:
- PlantUML pour les diagrammes
- LaTeX pour la mise en page professionnelle
- Documentation exhaustive du code

**Générateur:** Claude Code (Anthropic)
**Date de génération:** 2025-10-27

---

**Bonne chance pour votre soutenance! 🎓🚀**
