# 📸 Raw Image Pipeline - Reconstruction et Amélioration d’Images RAW

## 🌟 Description
**Raw Image Pipeline** est un projet Python permettant de reconstruire et d’améliorer des images RAW (DNG, Bayer) en appliquant un pipeline de traitement avancé. Il permet d’obtenir une image couleur exploitable à partir d’une capture brute du capteur.

## 🚀 Fonctionnalités
✔️ **Chargement d’images RAW** (DNG) et extraction de la matrice de Bayer.  
✔️ **Dématriçage avancé** (Malvar-He-Cutler) pour reconstruire les couleurs.  
✔️ **Balance des blancs automatique** avec `rawpy` pour des couleurs fidèles.  
✔️ **Débruitage intelligent** pour conserver les détails tout en réduisant le bruit.  
✔️ **Correction gamma adaptative** pour un rendu réaliste.  
✔️ **Filtre de netteté** pour renforcer les contours et les détails.  
✔️ **Affichage et sauvegarde** de l’image finale.  

## 🛠 Technologies utilisées
- **Python** 🐍   
- **RawPy** 📷  
- **Matplotlib** 📊  
- **NumPy** 🔢  

## 📌 Installation & Utilisation
### 1️⃣ Cloner le repo
```bash
git clone https://github.com/pinhero/raw-image-pipeline.git
cd raw-image-pipeline
```
### 2️⃣ Installer les dépendances
```bash
pip install scipy PIL rawpy numpy matplotlib
```
### 3️⃣ Exécuter le script
```bash
python projet.py chemin/vers/ton/image.dng -o output.png
```

## 📸 Exemple d’Image Avant / Après
| **RAW (DNG)** | **Image reconstruite** |
|--------------|----------------------|
| ![RAW Image](https://github.com/pinhero/raw-image-pipeline/blob/main/Images/colorchart-iphone7plus-cloudy.png) | ![Processed Image](https://github.com/pinhero/raw-image-pipeline/blob/main/Images/output.png) |

## 💡 Améliorations futures
- Ajouter un **mode HDR** 📷  
- Comparer différents algorithmes de **dématriçage** 🔬  
- Intégrer du **deep learning pour la reconstruction d’image** 🤖  

## 📩 Contributions
Les contributions sont les bienvenues ! Forkez le projet et ouvrez une pull request.  

---

## 🧑‍💻Auteurs

- **Ronaldo Adikpeto**
- **Ayoub Belachmi**
- **Mohamed Taga**
- **Iba Wade**

## 🧑‍💼Encadrant

- **Antoine Guennec**


📧 **Contact** :  ronaldo.adikpeto@etu.u-bordeaux.fr | [LinkedIn](https://www.linkedin.com/in/ronaldo-adikpeto-5a02b8204) | [GitHub](https://github.com/pinhero)

