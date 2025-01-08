import csv
from datetime import datetime

### CHEMIN DU FICHIER DE MOODLE 
chemin_fichier_ics = 'Questions/Question 2/ADE_RT1_Septembre2023_Decembre2023.ics'
### CHEMMIN DU FICHIER CSV 
chemin_fichier_csv = 'Questions/Question 2/Fichier de trie.csv'



### ON LIT LE FICHIER PRÉCEDENT 
def lire_fichier_ics(chemin_fichier):

    with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
        return fichier.readlines()



def extraire_evenements_ics(contenu_ics):

    evenements = []
    evenement = {}


    for ligne in contenu_ics:
        ligne = ligne.strip()
        if ligne.startswith('BEGIN:VEVENT'):
            evenement = {}

        elif ligne.startswith('UID:'):
            evenement['uid'] = ligne.split(':', 1)[1].strip()

        elif ligne.startswith('DTSTART:'):
            evenement['date_debut'] = ligne.split(':', 1)[1].strip()

        elif ligne.startswith('DTEND:'):
            evenement['date_fin'] = ligne.split(':', 1)[1].strip()

        elif ligne.startswith('SUMMARY:'):
            evenement['intitule'] = ligne.split(':', 1)[1].strip()

        elif ligne.startswith('LOCATION:'):
            evenement['salle'] = ligne.split(':', 1)[1].strip()

        elif ligne.startswith('DESCRIPTION:'):
            evenement['description'] = ligne.split(':', 1)[1].strip()

        elif ligne.startswith('END:VEVENT'):
            evenements.append(evenement)

    return evenements



def convertir_vers_pseudo_csv(evenement):

    date = datetime.strptime(evenement['date_debut'][:8], '%Y%m%d').strftime('%d-%m-%Y')
    heure_debut = datetime.strptime(evenement['date_debut'][9:15], '%H%M%S').strftime('%H:%M')
    heure_fin = datetime.strptime(evenement['date_fin'][9:15], '%H%M%S')
    heure_debut_dt = datetime.strptime(evenement['date_debut'][9:15], '%H%M%S')
    duree = heure_fin - heure_debut_dt
    duree_formatee = f"{duree.seconds // 3600:02}:{(duree.seconds // 60) % 60:02}"

    groupes = "|".join(evenement['description'].split('\\n')) if 'description' in evenement else "vide"
    salle = evenement.get('salle', 'vide').replace('\\,', '|')

    return [
        evenement['uid'], 
        date, 
        heure_debut, 
        duree_formatee, 
        "CM",  
        evenement['intitule'], 
        salle, 
        "vide",  
        groupes
    ]


### ON EXECUTE LES FONCTIONS ET L'ON MET LE RETURN DANS LA VARIBALE 
contenu_ics = lire_fichier_ics(chemin_fichier_ics)
evenements = extraire_evenements_ics(contenu_ics)
tableau_pseudo_csv = [convertir_vers_pseudo_csv(e) for e in evenements]


### ON TRIE LES ÉVENTS PAR DATE ET HEURE
tableau_pseudo_csv.sort(key=lambda x: (x[1], x[2]))


### ON OUVRE OU CRÉER LE FICHIER CSC AVEC "mode = 'w' " ET ON CRÉÉ LES DIFÉRENTES COLLONNES 
with open(chemin_fichier_csv, mode='w', newline='', encoding='utf-8') as fichier_csv:

    writer = csv.writer(fichier_csv, delimiter=';') #quand dans le code il y'a une point virgule on change de ligne, on passe à la suivante
    writer.writerow(["UID", "Date", "Heure Début", "Durée", "Modalité", "Intitulé", "Salle", "Professeurs", "Groupes"])
    writer.writerows(tableau_pseudo_csv)

print(tableau_pseudo_csv)


