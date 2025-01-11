import pandas as pd
import matplotlib.pyplot as plt



### CHEMIN DU FICHIER GÉNÉRÉ PAR LE PROGRAMME PRÉCÉDENT ###
chemin_fichier_csv = 'Questions/Question 4/Seances R107.csv'

### CHEMIN DU FICHIER GÉNÉRÉ EN SORTIE ###
chemin_fichier_sortie = 'Questions/Question 4/GraphiqueTP.png'




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




### GRAPHIQUE ###
def creer_graphique(nombre_de_cours_par_mois, chemin_fichier_sortie):

    plt.figure(figsize=(10, 6))

    ax = nombre_de_cours_par_mois.plot(kind='bar', color='royalblue', width=0.8, edgecolor='darkblue')



    ### ON AJOUTE LES TITRES ###
    plt.xlabel('Mois', fontsize=14, weight='bold', color='darkblue')
    plt.ylabel('Nombre de cours', fontsize=14, weight='bold', color='darkblue')




    ### ON SAUVEGARDE LE GRAPHIQUE ###
    plt.tight_layout()
    plt.savefig(chemin_fichier_sortie) # on peut ajouter les DPI si on le souhaite mais ce n'est pas obligatiore sur unn graphique puisqe on ne cherche pas unen qualilté optimal



### ON EXECUTE ICI LES FONCTIONS ###
def principal():

    df = lire_fichier_csv(chemin_fichier_csv)
    df = convertir_date(df)

    nombre_de_cours_par_mois = ajouter_mois_annee(df)
    creer_graphique(nombre_de_cours_par_mois, chemin_fichier_sortie)



if __name__ == "__main__":
    principal()
