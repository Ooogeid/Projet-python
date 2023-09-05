'''import os
 
directory = 'sous_titres\sous-titres'
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        print(f)
        

'''

'''
from os import listdir
from os.path import isfile, join
fichiers = [f for f in listdir('sous_titres\sous-titres\*') if isfile(join('sous_titres\sous-titres\*', f))]
print(fichiers)
'''

'''
from os import walk
listeFichiers = []
repertoire = 'sous_titres'
sousRepertoires = 'sous_titres\sous-titres'
for (repertoire, sousRepertoires, fichiers) in walk(sousRepertoires):
 print(listeFichiers.extend(fichiers))
 '''

import os

# Starting directory
root_directory = 'sous_titres\sous-titres'  # Replace with the root directory path

# Walk through all directories and subdirectories
for root, _, files in os.walk(root_directory):
    # Print the list of files in the current directory
    #print(f"Files in '{root}':")
    for file in files:
        print(os.path.join(root, file))
