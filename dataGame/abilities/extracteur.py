import re
import os

# Configuration
FICHIER_SOURCE = "Toutes_Les_Datas_Mewgenics.txt"
DOSSIER_SORTIE = "Listes_Extraites"

# Liste des mots à ignorer absolument (mots-clés de structure)
IGNORED_KEYS = {
    'meta', 'graphics', 'sounds', 'cost', 'target', 'damage_instance', 
    'temporary_effects', 'spawn', 'editor', 'passives', 'stat_mods',
    'consumable', 'item', 'breakdown', 'stock_fill_order', 'variant_of'
}

if not os.path.exists(DOSSIER_SORTIE):
    os.makedirs(DOSSIER_SORTIE)

def extract_from_mega_file():
    current_file_name = "inconnu"
    extracted_data = {}

    # Regex pour le chemin : /// PATH: dossier\fichier.gon ///
    path_regex = re.compile(r"/// PATH: (.+?) ///")
    
    # Regex pour le nom du sort : Doit être en début de ligne, suivi d'un espace/newline et d'une accolade
    # On autorise les lettres, chiffres et underscores
    ability_regex = re.compile(r"^([a-zA-Z0-9_]+)\s*\{", re.MULTILINE)

    print(f"Lecture de {FICHIER_SOURCE}...")

    with open(FICHIER_SOURCE, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # On découpe le fichier par sections "PATH"
    sections = path_regex.split(content)
    
    # sections[0] est vide ou contient l'en-tête avant le premier PATH
    for i in range(1, len(sections), 2):
        path_str = sections[i]
        file_content = sections[i+1]
        
        # On nettoie le nom du fichier pour Windows (enlever les slashs)
        clean_name = path_str.replace('\\', '_').replace('/', '_')
        
        # Extraction des noms de sorts dans cette section
        matches = ability_regex.findall(file_content)
        
        # Filtrage : On garde uniquement si c'est pas dans IGNORED_KEYS
        valid_abilities = [m for m in matches if m not in IGNORED_KEYS]
        
        if valid_abilities:
            output_path = os.path.join(DOSSIER_SORTIE, f"sorts_{clean_name}.txt")
            with open(output_path, 'w', encoding='utf-8') as out:
                for ability in valid_abilities:
                    out.write(f"{ability}\n")
            print(f"✅ Créé : {output_path} ({len(valid_abilities)} noms)")

if __name__ == "__main__":
    if os.path.exists(FICHIER_SOURCE):
        extract_from_mega_file()
        print(f"\nTerminé ! Regarde dans le dossier '{DOSSIER_SORTIE}'.")
    else:
        print(f"Erreur : Le fichier {FICHIER_SOURCE} est introuvable.")