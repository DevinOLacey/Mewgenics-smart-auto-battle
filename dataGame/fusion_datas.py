import os
from pathlib import Path

# Nom du méga-fichier qui sera généré
FICHIER_SORTIE = "Toutes_Les_Datas_Mewgenics.txt"

# Les extensions de fichiers que l'on veut récupérer. 
# J'ai ajouté .gon, mais tu peux en ajouter d'autres si besoin.
EXTENSIONS_VALIDE = {'.gon'}

# Récupère le dossier où se trouve ce script
dossier_racine = Path(__file__).parent

print("Début de la fusion des fichiers...")

with open(FICHIER_SORTIE, 'w', encoding='utf-8') as fichier_final:
    # rglob('*') permet de fouiller dans TOUS les sous-dossiers automatiquement
    for chemin_fichier in dossier_racine.rglob('*'):
        
        # On vérifie que c'est bien un fichier et qu'il a la bonne extension
        if chemin_fichier.is_file() and chemin_fichier.suffix.lower() in EXTENSIONS_VALIDE:
            
            # On ignore le fichier de sortie s'il existe déjà pour ne pas créer de boucle
            if chemin_fichier.name == FICHIER_SORTIE:
                continue
            
            # On calcule le chemin relatif (ex: abilities\armor.gon)
            chemin_relatif = chemin_fichier.relative_to(dossier_racine)
            
            # On écrit l'en-tête visuel avec le chemin du fichier
            fichier_final.write(f"\n{'='*60}\n")
            fichier_final.write(f"/// PATH: {chemin_relatif} ///\n")
            fichier_final.write(f"{'='*60}\n\n")
            
            # On lit et on copie le contenu du fichier
            try:
                with open(chemin_fichier, 'r', encoding='utf-8') as fichier_a_lire:
                    fichier_final.write(fichier_a_lire.read())
            except UnicodeDecodeError:
                # Si le fichier a un encodage bizarre, on gère l'erreur pour ne pas planter le script
                try:
                    with open(chemin_fichier, 'r', encoding='latin-1') as fichier_a_lire:
                        fichier_final.write(fichier_a_lire.read())
                except Exception as e:
                    fichier_final.write(f"// ERREUR DE LECTURE DU FICHIER : {e}\n")
            
            # On ajoute un saut de ligne pour aérer avant le prochain fichier
            fichier_final.write("\n")

print(f"✅ Terminé ! Le fichier '{FICHIER_SORTIE}' a été créé à la racine.")