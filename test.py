import tkinter as tk

#LES DIFFÉRENTES CONSTANTES

#POUR LE CANVAS
HEIGHT = 700
WIDTH = 700

#POUR LES CASES
case = []
nombre_case = 50


#Initiation liste 2D de la grille

for ligne in range(nombre_case):
    sous_liste = []
    for colonne in range(nombre_case) :             #liste en 2D qui contient 50 lignes et 50 colonnes
        sous_liste.append(0)                                #[[0,0,0,...,0,0,0,0],[0,0,0,...,0,0,0,0],...]
    case.append(sous_liste)




#Partie graphique 
racine = tk.Tk()
racine.title("La Fourmi de Langton")

Canvas = tk.Canvas(racine, height=HEIGHT, width=WIDTH)

#création de la grille de base avec les cases apparantes
        #-> liste en compréhension : https://python.doctor/page-comprehension-list-listes-python-cours-debutants

                        #(HEIGHT/HAUTEUR)/nombre_case permet la création de case proportionnelle au Canvas

[[Canvas.create_rectangle(colonnes*(HEIGHT/nombre_case),lignes*(WIDTH/nombre_case),(colonnes+1)*(HEIGHT/nombre_case),(lignes+1)*(WIDTH/nombre_case),
                          fill="white",outline="black")
  for lignes in range(nombre_case)] for colonnes in range(nombre_case)]                


Canvas.grid()
racine.mainloop()