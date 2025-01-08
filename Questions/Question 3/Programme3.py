import csv
from datetime import datetime


### CHEMIN DU FICHIER GÉNÉRÉ PAR LE PROGRAMME PRÉCÉDENT ###
chemin_fichier_csv = 'Questions/Question 3/Fichier de trie.csv'


### CHEMIN DU FICHIER GÉNÉRÉ EN SORTIE ###
chemin_fichier_sortie = 'Questions/Question 3/Seances R107.csv'


### Groupe QUE L'ON VEUT FILTRER ###
groupe_recherche = "B2"  




### ON LIT LE FICHIER CSV ###
with open(chemin_fichier_csv, 'r', encoding='utf-8') as fichier:

    reader = csv.reader(fichier, delimiter=';')
    next(reader)  # On passe les définitions des collones dans le csv

    tableauCSV = list(reader)




### ON FILTRE LES SÉANCES ###
filtre_seance = []



for ligne in tableauCSV:


    uid, date, heure, duree, modalite, intitule, salle, professeurs, groupes = ligne


    # On enlève les choses qui ne nous intéressent pas à partir de filtrer les groupes
    # On décompose en liste tous les '|' et on supprime tous les autres choses inutiles
    groupes_corriges = "|".join([part.strip() for part in groupes.split('|') if groupe_recherche in part])


    
    if "R1.07" in intitule and groupe_recherche in groupes_corriges:

        filtre_seance.append([date, duree, modalite])





### ON ÉCRIT LE TABLEAU DANS LE FICHIER SORTIE ###
with open(chemin_fichier_sortie, mode='w', newline='', encoding='utf-8') as fichier_csv:


    # On écrit les colonnes
    writer = csv.writer(fichier_csv, delimiter=';')
    writer.writerow(["Date", "Durée", "Type de Séance"])
    writer.writerows(filtre_seance)





print(f"Voici les séances filtrées pour la ressource R1.07 et le groupe {groupe_recherche} :")


for seance in filtre_seance:
    print(seance)
