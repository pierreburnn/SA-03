import re
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import webbrowser
import os
import markdown





def analyse_fichier(contenu_fichier):


    problemes = []
    
    ### RECHERHCE DES TRAMES UNE PAR UNE ###

    dns_frame = re.finditer(r".*NXDomain.*", contenu_fichier, re.MULTILINE)
    syn_frames = re.finditer(r".*SYN.*", contenu_fichier, re.MULTILINE)
    repeated_frames = re.finditer(r".*5858.*", contenu_fichier, re.MULTILINE)



    # Stockage de chaque trame
    for frame in dns_frame:
        problemes.append(["DNS erreur", "Problème de DNS", frame.group(0)])

    for frame in syn_frames:
        problemes.append(["SYN Flag", "Drapeau SYN suspect", frame.group(0)])

    for frame in repeated_frames:
        problemes.append(["Répétition", "Données répétées", frame.group(0)])

    return problemes




### GENERER UN TABLEAU EXCEL ###

def generer_excel(problemes):


    """
    Sauvegarde des problèmes dans un fichier CSV, en proposant 
    à l'utilisateur de choisir l'emplacement via une boîte de dialogue.
    """
    chemin = filedialog.asksaveasfilename(defaultextension=".csv", 
                                          filetypes=[("CSV files", "*.csv")])
    

    if chemin:

        try:

            df = pd.DataFrame(problemes, columns=["Type", "Description", "Trame"])

            df.to_csv(chemin, index=False, sep=';', encoding='utf-8-sig')

            messagebox.showinfo("Succès", "Résultats sauvegardés dans un fichier CSV.")


        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de sauvegarder le fichier : {e}") 






### SAUVEGARDE DES RÉSULTATS DANS UN FICHIER HTML ###
def enregistrer_sous_HTML(problemes):


    """
    Sauvegarde des résultats dans un fichier HTML, 
    mais en utilisant la librairie Markdown pour la génération du tableau.
    """
    

    contenu_markdown = "# Résultats de l'analyse TCP\n\n"
    contenu_markdown += "| Type | Description | Trame |\n"
    contenu_markdown += "| ---  | ---         | ---   |\n"



    # On ajoute chaque problème dans le tableau Markdown
    for prob in problemes:
        contenu_markdown += f"| {prob[0]} | {prob[1]} | {prob[2]} |\n"



    # Conversion du texte Markdown en HTML
    # On active l'extension 'tables' pour une meilleure gestion des tableaux

    contenu_html_converti = markdown.markdown(contenu_markdown, extensions=['tables'])


    # On va maintenant encapsuler ce contenu HTML dans un squelette 
    contenu_html_final = f"""
    <html>
    <head>
        <title>Analyse TCP</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #4CAF50; color: white; }}
            tr:nth-child(even) {{ background-color: #f2f2f2; }}
            h1 {{ color: #4CAF50; }}
        </style>
    </head>
    <body>
        {contenu_html_converti}
    </body>
    </html>
    """





    ### SAUVEGARDE DU FICHIER HTML SUR LE BUREAU ###
    chemin = os.path.join(os.path.expanduser("~"), "Desktop", "analyse_tcp.html")

    with open(chemin, 'w', encoding='utf-8') as f:
        
        f.write(contenu_html_final)


    # On ouvre le fichier HTML dans le navigateur web
    webbrowser.open('file://' + chemin)







def chargement_fichier():

    chemin = filedialog.askopenfilename()
    if chemin:


        try:

            with open(chemin, 'r') as f:

                contenu = f.read()
                resultats = analyse_fichier(contenu)
                afficher_resultat(resultats)


        except Exception as e:
            print("Erreur :", e)





def afficher_resultat(problemes):


    resultats_fenetre = tk.Toplevel()
    resultats_fenetre.title("Résultats")



    def filter_problemes(event):
        type_selectionner = filtre.get()
        for row in tree.get_children():
            tree.delete(row)



        for prob in problemes:

            if type_selectionner == "Tous" or prob[0] == type_selectionner:

                tree.insert("", tk.END, values=prob)




    # Ajout des filtres
    filter_frame = ttk.Frame(resultats_fenetre)

    filter_frame.pack(fill=tk.X, padx=10, pady=5)




    ttk.Label(filter_frame, text="Filtrer par type de problème :").pack(side=tk.LEFT, padx=5)
    filtre = tk.StringVar(value="Tous")
    filter_menu = ttk.Combobox(filter_frame, textvariable=filtre, state="readonly")
    filter_menu['values'] = ["Tous"] + list(set(prob[0] for prob in problemes))
    filter_menu.pack(side=tk.LEFT, padx=5)
    filter_menu.bind("<<ComboboxSelected>>", filter_problemes)



    # liste des résultats avec colonne modifiée
    tree = ttk.Treeview(resultats_fenetre)
    tree["columns"] = ("Type", "Description", "Trame")
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("Type", anchor=tk.W, width=120)
    tree.column("Description", anchor=tk.W, width=200)
    tree.column("Trame", anchor=tk.W, width=400)  # la colonne est plus large pour les trames



    tree.heading("#0", text="", anchor=tk.W)
    tree.heading("Type", text="Type", anchor=tk.W)
    tree.heading("Description", text="Description", anchor=tk.W)
    tree.heading("Trame", text="Trame suspecte", anchor=tk.W)
    tree.pack(fill=tk.BOTH, expand=True)




    for prob in problemes:

        tree.insert("", tk.END, values=prob)



    # Boutons de sauvegarde
    boutton_frame = ttk.Frame(resultats_fenetre)
    boutton_frame.pack(pady=10)
    
    sauvegarder_csv_boutton = tk.Button(boutton_frame, text="Sauvegarder en CSV", 
                               command=lambda: generer_excel(problemes))
    


    sauvegarder_csv_boutton.pack(side=tk.LEFT, padx=5)
    

    sauvegarder_html_boutton = tk.Button(boutton_frame, text="Ouvrir dans le navigateur", 
                                command=lambda: enregistrer_sous_HTML(problemes))
    

    sauvegarder_html_boutton.pack(side=tk.LEFT, padx=5)



# Création de la fenêtre principale
root = tk.Tk()
root.title("Analyseur TCP")


btn = tk.Button(root, text="Charger un fichier", command=chargement_fichier)
btn.pack(pady=20)




root.mainloop()
