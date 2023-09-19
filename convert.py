import os

# dossier source
root_directory = 'sous_titres\sous-titres'  

# parcourir les fichiers dans les dossiers
for root, _, files in os.walk(root_directory):
    for file in files:
        print(os.path.join(root, file))



