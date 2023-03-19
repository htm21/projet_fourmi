import tkinter as tk
from tkinter import filedialog
import time as t

# ========== VAR ==========

HEIGHT, WIDTH = 700, 700 # Dimensions du canvass
nombre_case   = 40 # Nombre de cases dans le jeu
case          = [[0 for _ in range(nombre_case)] for cell in range(nombre_case)] # liste 2D 40x40 remplie de "0"
vitesses      = [(0.5,"VITESSE : x 1"), (0, "VITESSE : x 2"), (1, "VITESSE : x 0.5")] # Les differantes vitesses du jeu | num = temps de sleep, txt = text du boutton
vitesse_jeu   = vitesses[0] # Vitesse du jeu




# ========== FUNC ==========

def quitter():
    '''Ferme le programme'''
    racine.destroy()

def changer_vitesse():
    '''Change la vitesse du jeu'''
    global vitesses, vitesse_jeu
    vitesse_jeu = vitesses[0] if vitesse_jeu == vitesses[-1] else vitesses[vitesses.index(vitesse_jeu) + 1]
    boutton_Vitesse.config(text = vitesse_jeu[1])

def load():
    '''Ouvre une fenetre pour charger un fichier txt qui a une sauvegarede d'un jeu'''
    file_path = filedialog.askopenfilename(title = "Charger une partie", filetypes = (("Fichiers textes", "*.txt"),("Tous les fichiers", "*.*"))).name

def save(): 
    '''Ouvre une fenetre pour '''
    fichier = [('Text Document', '*.txt')]
    fichier = filedialog.asksaveasfile(filetypes = fichier, defaultextension = fichier)

def avencer():
    '''Fait avencer le jeu d'une unité de temps'''
    pass

def retour():
    '''Fait retourner le jeu d'une unité de temps'''
    pass

def start():
    '''Fait commencer le jeu'''
    pass

def pause():
    '''Met en pause le jeu'''
    pass




# ========== Tkinter GUI ==========
racine = tk.Tk()
racine.title("La Fourmi de Langton")
racine.geometry("1300x800")
racine.configure(bg = "black")

Canvas = tk.Canvas(racine, height=HEIGHT, width=WIDTH)

# création de la grille de base avec les cases apparantes
# (HEIGHT/HAUTEUR)/nombre_case permet la création de case proportionnelle au Canvas
[[Canvas.create_rectangle(colonnes*(HEIGHT/nombre_case), lignes*(WIDTH/nombre_case), (colonnes+1) * (HEIGHT/nombre_case), (lignes+1) * (WIDTH/nombre_case), fill = "white", outline = "black") for lignes in range(nombre_case)] for colonnes in range(nombre_case)]


boutton_Start       = tk.Button(racine, text = "PLAY",                   font = ("Arial 20 bold"),           fg = "black",   activeforeground = "black", activebackground = "white", bd = 10, pady = 5, padx = 20, width = 10, command = start)
boutton_Pause       = tk.Button(racine, text = "PAUSE",                  font = ("Arial 20 bold"),           fg = "black",   activeforeground = "black", activebackground = "white", bd = 10, pady = 5, padx = 20, width = 10, command = pause)                

label_Texte         = tk.Label (racine, text = "LES COMMANDES AVANCÉES", font = ("Metropolis 20 bold"),      fg = "#8f6745", activeforeground = "black",  bg="black")   
boutton_Quitter     = tk.Button(racine, text = "QUITTER",                font = ("Arial 20 bold"),           fg = "black",   activeforeground = "black", activebackground = "white", bd = 10, pady = 5, padx = 20, width = 10, command = quitter)
boutton_Vitesse     = tk.Button(racine, text = vitesse_jeu[1],           font = ("Airial 20 bold"),          fg = "black",   activeforeground = "black", activebackground = "white", bd = 10, pady = 5, padx = 20, width = 10, command = changer_vitesse)
boutton_Retour      = tk.Button(racine, text = "RETOUR",                 font = ("Poppins 20 bold"),         fg = "black",   activeforeground = "black", activebackground = "white", bd = 10, pady = 5, padx = 20, width = 10, command = retour)
boutton_Avancer     = tk.Button(racine, text = "AVANCER",                font = ("Poppins 20 bold"),         fg = "black",   activeforeground = "black", activebackground = "white", bd = 10, pady = 5, padx = 20, width = 10, command = avencer)
boutton_Sauvegarder = tk.Button(racine, text = "SAUVEGARDER",            font = ("Poppins 20 bold"),         fg = "black",   activeforeground = "black", activebackground = "white", bd = 10, pady = 5, padx = 20, width = 10, command = save)
boutton_Ouvrir      = tk.Button(racine, text = "CHARGER",                font = ("Poppins 20 bold"),         fg = "black",   activeforeground = "black", activebackground = "white", bd = 10, pady = 5, padx = 20, width = 10, command = load)


# PLACEMENTS BOUTONS:

boutton_Start.grid       (row = 0, column = 0)
boutton_Pause.grid       (row = 0, column = 1)
boutton_Quitter.grid     (row = 0, column = 2)

boutton_Vitesse.grid     (row = 1, column = 4, pady = 10, padx = 20, columnspan=2)
boutton_Avancer.grid     (row = 2, column = 4, pady = 10, padx = 20)
boutton_Retour.grid      (row = 2, column = 5, pady = 10, padx = 20)

boutton_Sauvegarder.grid (row = 3, column = 4, pady = 20, padx = 10)
boutton_Ouvrir.grid      (row = 3, column = 5, padx = 10, pady = 20)

# PLACEMENTS LABEL
label_Texte.grid         (row = 0, column = 4, pady = 10, padx=20, columnspan=4)

# PLACEMENTS CANVAS
Canvas.grid              (row = 1, column = 0, columnspan = 4, rowspan = 4, padx = 25)


racine.mainloop()