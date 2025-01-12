import pandas as pd
import matplotlib.pyplot as plt
import markdown
from markdown import markdown
import os




### CHEMIN DU FICHIER GÉNÉRÉ PAR LE PROGRAMME PRÉCÉDENT ###
chemin_fichier_csv = 'Questions/Question 4/Seances R107.csv'

### CHEMIN DU FICHIER GÉNÉRÉ EN SORTIE ###
chemin_fichier_sortie = 'Questions/Question 5/GraphiqueTP2.png'

### CHEMIN DU FICHIER HTML FINAL ###
chemin_fichier_html = 'Questions/Question 5/Travaux.html'




### ON LIT LE FICHIER DU PROGRAMME PRECEDENT ###
def lire_fichier_csv(chemin_fichier_csv):

    return pd.read_csv(chemin_fichier_csv, sep=";")


### CONVERTION DE LA DATE ###
def convertir_date(df):

    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
    return df


### MOIS + ANNÉE ###
def ajouter_mois_annee(df):

    df['Mois'] = df['Date'].dt.to_period('M')
    return df.groupby('Mois').size()



### GRAPHIQUE EN FORME DE CERCLE ###
def graphique_cercle(nombre_de_cours_par_mois, chemin_fichier_sortie):

    plt.figure(figsize=(8, 8))

    ax = nombre_de_cours_par_mois.plot(kind='pie', autopct='%1.1f%%', startangle=90)

    plt.title('Pourcentage de cours par mois', fontsize=16, weight='bold')



    ### ON SAUVEGARDE LE GRAPHIQUE ###
    plt.tight_layout()
    plt.savefig(chemin_fichier_sortie)



### ON EXECUTE ICI LES FONCTIONS ###
def principal():
    df = lire_fichier_csv(chemin_fichier_csv)
    df = convertir_date(df)
    


    # On génère le graphique en cercle
    nombre_de_cours_par_mois = ajouter_mois_annee(df)
    graphique_cercle(nombre_de_cours_par_mois, chemin_fichier_sortie)
    



if __name__ == "__main__":
    principal()
