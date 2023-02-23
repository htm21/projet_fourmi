import tkinter as tk

#Dimensions
HEIGHT = 700
WIDTH = 700

nombre_case = 50


#Initiation liste 2D de la grille

cases = []
for ligne in range(nombre_case):
    sous_liste = []
    for colonne in range(nombre_case) :             #liste en 2D qui contient 50 lignes et 50 colonnes
        sous_liste.append(0)
    cases.append(sous_liste)








#Partie graphique 
racine = tk.Tk()
racine.title("La Fourmi de Langton")
Canvas = tk.Canvas(racine, height=HEIGHT, width=WIDTH, bg="white")
Canvas.grid()
racine.mainloop()