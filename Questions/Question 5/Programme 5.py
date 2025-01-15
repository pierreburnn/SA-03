import pandas as pd
import matplotlib.pyplot as plt
import markdown
from markdown import markdown
import os




### CHEMIN DU FICHIER GÉNÉRÉ PAR LE PROGRAMME PRÉCÉDENT ###
chemin_fichier_csv = 'Questions/Question 4/Seances R107.csv'

### CHEMIN DU FICHIER GÉNÉRÉ EN SORTIE ###
chemin_fichier_sortie = 'Questions\Question 5\GraphiqueTP2.png'

### CHEMIN DU FICHIER HTML FINAL ###
chemin_fichier_html = 'Questions\Question 5\Travaux.html'




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


def generer_tableau_html(df):


    tableau_html = df.to_html(index=False, 
                              classes="tableau-seances", 
                              border=1)
    
    return tableau_html



def creer_fichier_html(df, nombre_de_cours_par_mois, chemin_fichier_sortie, chemin_fichier_html):

    tableau_html = generer_tableau_html(df)
    




    contenu_html = f"""

    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        
        <style>
            body {{
                font-family: Arial, sans-serif;
                color: #333;
                margin: 40px;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 30px;
            }}

            th, td {{
                padding: 8px 12px;
                text-align: center;
                border: 1px solid #ddd;
            }}

            th {{
                background-color: #f4f4f4;
                color: #333;
            }}

            img {{
                display: block;
                margin: 0 auto;
            }}
        </style>
    </head>
    <body>
        <h2>Tableau des Séances de R1.07</h2>
        {tableau_html}
    </body>
    </html>
    """





    with open(chemin_fichier_html, 'w', encoding='utf-8') as fichier_html:
        
        fichier_html.write(contenu_html)



### ON EXECUTE ICI LES FONCTIONS ###
def principal():

    df = lire_fichier_csv(chemin_fichier_csv)
    df = convertir_date(df)
    


    # ON GENERE LE GRAPHIQUE EN FORME DE CERCLE
    nombre_de_cours_par_mois = ajouter_mois_annee(df)
    graphique_cercle(nombre_de_cours_par_mois, chemin_fichier_sortie)
    

    ### CREATION D UN FIHCIER HTML ###
    creer_fichier_html(df, nombre_de_cours_par_mois, chemin_fichier_sortie, chemin_fichier_html)




### DEBUT DU PROGRAMME ###
if __name__ == "__main__":
    principal()
