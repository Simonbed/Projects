import pandas as pd
import numpy as np

db = pd.read_excel("Processus gestion de commandes clients (1).xlsx")


db = db.transpose()

db = db[4:28]

#print(db)

db = db.transpose()

db.columns =["Poste", "Departement", "Acteur participant au processus",
"Info Client" , "Info Commis d’entrepôt", "Info Représentant des ventes",
"Info technicien comptable", "Info Contrôleur comptable", "Info vp ventes",
"Info livreur", "Info Fournisseur", "Info Préposé à la prise de commande",
"Info Autre", "Elements les plus pertinent",
"Elément à rattacher au bon de commande",
"Elément à rattacher à la soumission client",
"Elément à rattacher à la soumission fournisseur",
"Elément à rattacher au bon de livraison", "Elément à rattacher à la facture",
"Elément à rattache au produit", "Réponse à autre`",
"Activite complétant le processus gestion commande",
"Affirmation vraie au sujet du processus", "Info complémentaires" ]
list_col = list(db.columns.values)

db = db.transpose()
list_rep = list(db.columns.values)

temp = 0
for i in (list_rep):
    if temp == 0:
        db1 = db[db.columns[0]].str.split(";", expand=True)
        temp = temp + 1
    else :
        if temp == 1 :
            db2 = db[db.columns[temp]].str.split(";", expand=True)
            db_row = pd.concat([db1, db2], axis=1)
            temp = temp + 1
        else :
            db2 = db[db.columns[temp]].str.split(";", expand=True)
            db_row = pd.concat([db_row, db2], axis=1)
            temp = temp + 1

db_fin = db_row.transpose()
db_fin.to_excel("essaie_output.xlsx")
