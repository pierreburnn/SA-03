import pandas as pd
import matplotlib.pyplot as plt


### CHEMIN DU FICHIER GÉNÉRÉ PAR LE PROGRAMME PRÉCÉDENT ###
chemin_fichier_csv = 'Questions/Question 4/Seances R107.csv'

### CHEMIN DU FICHIER GÉNÉRÉ EN SORTIE ###
chemin_fichier_sortie = 'Questions/Question 4/GraphiqueTP.png'
df = pd.read_csv(chemin_fichier_csv, sep=";")



### CONVERTION DE LA DATE ###
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')



### MOIS + ANNÉE ###
df['Mois'] = df['Date'].dt.to_period('M')


nombre_de_cours_par_mois = df.groupby('Mois').size()


### GRAPHIQUE ###
plt.figure(figsize=(10, 6))
ax = nombre_de_cours_par_mois.plot(kind='bar', color='royalblue', width=0.8, edgecolor='darkblue')



### ON AJOUTE LES TITRES ###
plt.xlabel('Mois', fontsize=14, weight='bold', color='darkblue')
plt.ylabel('Nombre de cours', fontsize=14, weight='bold', color='darkblue')




### ON SAUVEGARDE LE GRAPHIQUE ###
plt.tight_layout()
plt.savefig(chemin_fichier_sortie, dpi=300)
