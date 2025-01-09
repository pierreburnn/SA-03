import csv
from datetime import datetime


### CHEMIN DU FICHIER GÉNÉRÉ PAR LE PROGRAMME PRÉCÉDENT ###
chemin_fichier_csv = 'Questions/Question 3/Fichier de trie.csv'

### CHEMIN DU FICHIER GÉNÉRÉ EN SORTIE ###
chemin_fichier_sortie = 'Questions/Question 3/Seances R107.csv'


### Groupe QUE L'ON VEUT FILTRER ###
groupe_recherche = "B2"  


### ON LIT LE FICHIER CSV (chemin qu'on a défini avant) ###
def lirefichiercsv(chemin_fichier):

    with open(chemin_fichier, 'r', encoding='utf-8') as fichier:

        reader = csv.reader(fichier, delimiter=';')
        next(reader)

        return list(reader)



### ON GARDE SEULEMENT LES SÉANCES DE R1.07 POUR LE GROUPE QUE L'ON CHOISIT PRÉCEDEMENT ###
def filtrer_seances_r107(tableauCSV, groupe_recherche):

    filtre_seance = []

    for ligne in tableauCSV:

        uid, date, heure, duree, modalite, intitule, salle, professeurs, groupes = ligne

        # On enlève les choses qui ne nous interessent pas à partir de filtrer les groupes
        # On décompose en liste tous les '|' et on supprime tous les autres choses inutiles
        groupes_corriges = "|".join([part.strip() for part in groupes.split('|') if groupe_recherche in part])

        
        if "R1.07" in intitule and groupe_recherche in groupes_corriges:
            filtre_seance.append([date, duree, modalite])

    return filtre_seance




### ON ÉCRIT LE TABLEAU ###
def ecrire_tableau_resultat(chemin_fichier_sortie, filtre_seance):

    with open(chemin_fichier_sortie, mode='w', newline='', encoding='utf-8') as fichier_csv:

        # On écrit les colonnes
        writer = csv.writer(fichier_csv, delimiter=';')
        writer.writerow(["Date", "Durée", "Type de Séance"])
        writer.writerows(filtre_seance)




tableauCSV = lirefichiercsv(chemin_fichier_csv)


### FILTRER LES SÉANCES DE R1.07 POUR LE GROUPE QUE L'ON VEUT ###
filtre_seance = filtrer_seances_r107(tableauCSV, groupe_recherche)


### ON ÉCRIT LES RESULTATS DANS UN FICHIER CSV ###
ecrire_tableau_resultat(chemin_fichier_sortie, filtre_seance)



# Afficher les résultats
print(f"Voici les séances filtrées pour la ressource R1.07 et le groupe {groupe_recherche} :")

for seance in filtre_seance:
    print(seance)

