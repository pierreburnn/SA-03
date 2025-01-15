import re
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import webbrowser
import os







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

    chemin = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

    if chemin:

        try:

            df = pd.DataFrame(problemes, columns=["Type", "Description", "Trame"])
            df.to_csv(chemin, index=False, sep=';', encoding='utf-8-sig')
            messagebox.showinfo("Succès", "Résultats sauvegardés dans un fichier CSV.") #on affiche un message de réussite comme quoi le fichier a bien été sauvegardé


        except Exception as e:

            messagebox.showerror("Erreur", f"Impossible de sauvegarder le fichier : {e}") #on affiche un message d'erreur si le fichier n'a pas pu être sauvegardé




### SAUVEGARDE DES RÉSULTATS DANS UN FICHIER HTML ###
def enregistrer_sous_HTML(problemes):

    contenu_html = """



    <html>
    <head>
        <title>Analyse TCP</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #4CAF50; color: white; }
            tr:nth-child(even) { background-color: #f2f2f2; }
            h1 { color: #4CAF50; }
        </style>
    </head>
    <body>
        <h1>Résultats de l'analyse TCP</h1>
        <table>
            <tr>
                <th>Type</th>
                <th>Description</th>
                <th>Trame</th>
            </tr>
    """
    
    for prob in problemes:
        contenu_html += f"""
            <tr>
                <td>{prob[0]}</td>
                <td>{prob[1]}</td>
                <td>{prob[2]}</td>
            </tr>
        """
    
    contenu_html += """
        </table>
    </body>
    </html>
    """
    




    ### SAUVEGARDE DU FICHIER HTML SUR LE BUREAU ###
    chemin = os.path.join(os.path.expanduser("~"), "Desktop", "analyse_tcp.html")

    with open(chemin, 'w', encoding='utf-8') as f:
        f.write(contenu_html)


    webbrowser.open('file://' + chemin) #on ouvre ici le fichier html dans le navigateur web






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




root = tk.Tk()
root.title("Analyseur TCP")




btn = tk.Button(root, text="Charger un fichier", command=chargement_fichier)
btn.pack(pady=20)



root.mainloop()
