from datetime import datetime

chemin_fichier = "/Users/pierrehiltenbrand/Desktop/SAÉ03/Github/SA-03/Questions/Question 1/evenementSAE_15.ics" 


#on ouvre ici le fichier ics
def lire_fichier_ics(chemin_fichier):
    with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
        return fichier.readlines()


def extraire_evenement_ics(contenu_ics):

    evenement = {}
    for ligne in contenu_ics:
        if ligne.startswith('UID:'):
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
    return evenement



def convertir_vers_pseudo_csv(evenement):

    date = datetime.strptime(evenement['date_debut'][:8], '%Y%m%d').strftime('%d-%m-%Y')
    heure_debut = datetime.strptime(evenement['date_debut'][9:15], '%H%M%S').strftime('%H:%M')
    heure_fin = datetime.strptime(evenement['date_fin'][9:15], '%H%M%S')
    heure_debut_dt = datetime.strptime(evenement['date_debut'][9:15], '%H%M%S')
    duree = heure_fin - heure_debut_dt
    duree_formatee = f"{duree.seconds // 3600:02}:{(duree.seconds // 60) % 60:02}"

    groupes = "|".join(evenement['description'].split('\\n')) if 'description' in evenement else "vide"
    return f"{evenement['uid']};{date};{heure_debut};{duree_formatee};CM;{evenement['intitule']};{evenement['salle']};LACAN DAVID;S1"

def main():
    contenu_ics = lire_fichier_ics(chemin_fichier)
    evenement = extraire_evenement_ics(contenu_ics)
    pseudo_csv = convertir_vers_pseudo_csv(evenement)
    print(pseudo_csv)

if __name__ == "__main__":
    main()
