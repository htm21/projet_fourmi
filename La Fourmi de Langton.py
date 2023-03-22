<<<<<<< HEAD
import time as t
from tkinter import filedialog
=======
>>>>>>> 75d33904a3d7899f334e60b38526524eb18c09e6
import tkinter as tk
from tkinter import filedialog
import time as t

# ========== VAR ==========

HEIGHT, WIDTH = 950, 950 # Dimensions du canvas
nombre_case   = 51 # Nombre de cases dans le jeu | Doit etre impaire si on veut un milieu
field         = [[0 for _ in range(nombre_case)] for cell in range(nombre_case)] # liste 2D 40x40 remplie de "0"

vitesses      = [(0.5,"Speed: x 1"), (0.1, "Speed: x 2"), (0.7, "Speed: x 0.5")] # Les differantes vitesses du jeu | num = temps de sleep, txt = text du boutton
vitesse_jeu   = vitesses[0] # Vitesse du jeu

Running       = False
fourmie_pos   = [nombre_case // 2, nombre_case // 2] # Position de la fourmie | [5, 3] = [y (ligne), x (colone)]
directions    = ["0", "90", "180", "-90"]
case_actuelle = 0 # Memoire de la cellule actuelle

direction_fourmie = directions[0]
field[nombre_case // 2][nombre_case // 2] = 3 # 3 c'est le symbol de la fourmie

# ========== FUNC ==========

def quitter():
    '''Ferme le programme'''
    global Running
    if Running: Running = False
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
    global Running
    Running = True
    while Running:
        fourmie_update()
        t.sleep(vitesse_jeu[0])

def pause():
    '''Met en pause le jeu'''
    pass

def change_type_case(y, x):
    '''Change la couleur de la case en fonction de sa couleur precedente'''
    if case_actuelle == 0:
        field[y][x] = 1
        Canvas.create_rectangle(x * (HEIGHT / nombre_case), y * (WIDTH / nombre_case), (x + 1) * (HEIGHT / nombre_case), (y + 1) * (WIDTH / nombre_case), outline = "black", fill = "black")
    else:
        field[y][x] = 0
        Canvas.create_rectangle(x * (HEIGHT / nombre_case), y * (WIDTH / nombre_case), (x + 1) * (HEIGHT / nombre_case), (y + 1) * (WIDTH / nombre_case), outline = "black", fill = "white")

def fourmie_update():
    '''Met a jour le positionnement de la fourmie et les cases dans la liste "field" et canvas'''
    global case_actuelle, direction_fourmie

    # Change la directionde la fourmie
    if case_actuelle: direction_fourmie = directions[-1] if direction_fourmie == directions[0] else directions[directions.index(direction_fourmie) - 1]
    else:             direction_fourmie = directions[0] if direction_fourmie == directions[-1] else directions[directions.index(direction_fourmie) + 1]
    
    # Change la couleur de la case en fonction de sa couleur precedente 
    change_type_case(*fourmie_pos)

    # Bouge la fourmie en fonction de son orientation
    if direction_fourmie == "0":   fourmie_pos[0] = nombre_case - 1 if fourmie_pos [0] == 0 else fourmie_pos[0] - 1 # Up
    if direction_fourmie == "180": fourmie_pos[0] = 0 if fourmie_pos [0] == nombre_case - 1 else fourmie_pos[0] + 1 # Down
    if direction_fourmie == "90":  fourmie_pos[1] = 0 if fourmie_pos [1] == nombre_case - 1 else fourmie_pos[1] + 1 # Left
    if direction_fourmie == "-90": fourmie_pos[1] = nombre_case - 1 if fourmie_pos [1] == 0 else fourmie_pos[1] - 1 # Right

    # Met a jour le canvas et suvegarde
    case_actuelle = field[fourmie_pos[0]][fourmie_pos[1]]
    field[fourmie_pos[0]][fourmie_pos[1]] = 3
    Canvas.create_rectangle(fourmie_pos[1] * (HEIGHT / nombre_case), fourmie_pos[0] * (WIDTH / nombre_case), (fourmie_pos[1] + 1) * (HEIGHT / nombre_case), (fourmie_pos[0] + 1) * (WIDTH / nombre_case), outline = "black", fill = "red")
    racine.update()


def canvas_refresh():
    '''Met a jour tout le canvas'''
    for y, line in enumerate(field):
        for x, cell in enumerate(line):
            if cell == 1:
                Canvas.create_rectangle(x * (HEIGHT / nombre_case), y * (WIDTH / nombre_case), (x + 1) * (HEIGHT / nombre_case), (y + 1) * (WIDTH / nombre_case), outline = "black", fill = "black")
            if cell == 0:
                Canvas.create_rectangle(x * (HEIGHT / nombre_case), y * (WIDTH / nombre_case), (x + 1) * (HEIGHT / nombre_case), (y + 1) * (WIDTH / nombre_case), outline = "black", fill = "white")
            if cell == 3:
                Canvas.create_rectangle(x * (HEIGHT / nombre_case), y * (WIDTH / nombre_case), (x + 1) * (HEIGHT / nombre_case), (y + 1) * (WIDTH / nombre_case), outline = "black", fill = "red")


# ========== Tkinter GUI ==========

print("\033c")

racine = tk.Tk()
racine.title("La Fourmi de Langton")
racine.configure(bg = "black")

width, height = 1920, 1080
screen_width  = racine.winfo_screenwidth()
screen_height = racine.winfo_screenheight()
x, y          = (screen_width/2) - (width/2), (screen_height/2) - (height/2)
racine.geometry('%dx%d+%d+%d' % (width, height, x, y))

# FRAMES CREATION:

menu_du_haut_frame       = tk.Frame (racine, bg = "#1b1b1b", highlightbackground = "#3b3b3b", highlightthickness = 5)
terrain_jeu_frame        = tk.Frame (racine, bg = "#1b1b1b", highlightbackground = "#3b3b3b", highlightthickness = 5)
menu_lateral_frame       = tk.Frame (racine, bg = "#1b1b1b", highlightbackground = "#3b3b3b", highlightthickness = 5)

menu_titre_frame         = tk.Frame (menu_lateral_frame, bg = "#1b1b1b")
vitesse_frame            = tk.Frame (menu_lateral_frame, bg = "#1b1b1b")
controles_etat_jeu_frame = tk.Frame (menu_lateral_frame, bg = "#1b1b1b")
game_file_control        = tk.Frame (menu_lateral_frame, bg = "#1b1b1b")

# FRAMES PACK:

menu_lateral_frame.pack       (anchor = "e", fill = "y",    expand = 0, side = "right")
menu_du_haut_frame.pack       (anchor = "n", fill = "x",    expand = 0, side = "top")
terrain_jeu_frame.pack        (anchor = "s", fill = "both", expand = 1, side = None)

menu_titre_frame.pack         (padx = 10, pady = 30, expand = 0, fill = "both")
vitesse_frame.pack            (padx = 10, pady = 30, expand = 0, fill = "both")
controles_etat_jeu_frame.pack (padx = 10, pady = 30, expand = 0, fill = "both")
game_file_control.pack        (padx = 10, pady = 30, expand = 0, fill = "both") 

# BOUTTONS CREATION:

boutton_Start       = tk.Button(menu_du_haut_frame,       text = "Play",                    font = ("Arial 25 bold"), fg = "#1b1b1b", bg = "white",  activeforeground = "#1b1b1b", activebackground = "white", bd = 7, pady = 5, padx = 20, width = 10, command = start)
boutton_Pause       = tk.Button(menu_du_haut_frame,       text = "Pause",                   font = ("Arial 25 bold"), fg = "#1b1b1b", bg = "white",  activeforeground = "#1b1b1b", activebackground = "white", bd = 7, pady = 5, padx = 20, width = 10, command = pause)                
boutton_Quitter     = tk.Button(menu_du_haut_frame,       text = "Quit",                    font = ("Arial 25 bold"), fg = "#1b1b1b", bg = "white",  activeforeground = "#1b1b1b", activebackground = "white", bd = 7, pady = 5, padx = 20, width = 10, command = quitter)

label_Texte         = tk.Label (menu_titre_frame,         text = "LES COMMANDES AVANCÉES",  font = ("Arial 25 bold"), fg = "white",   bg = "#1b1b1b")   
boutton_Vitesse     = tk.Button(vitesse_frame,            text = vitesse_jeu[1],            font = ("Arial 25 bold"), fg = "#1b1b1b", bg = "white",  activeforeground = "#1b1b1b", activebackground = "white", bd = 7, pady = 5, padx = 20, width = 10, command = changer_vitesse)
boutton_Retour      = tk.Button(controles_etat_jeu_frame, text = "Back",                    font = ("Arial 25 bold"), fg = "#1b1b1b", bg = "white",  activeforeground = "#1b1b1b", activebackground = "white", bd = 7, pady = 5, padx = 20, width = 10, command = retour)
boutton_Avancer     = tk.Button(controles_etat_jeu_frame, text = "Forward",                 font = ("Arial 25 bold"), fg = "#1b1b1b", bg = "white",  activeforeground = "#1b1b1b", activebackground = "white", bd = 7, pady = 5, padx = 20, width = 10, command = avencer)
boutton_Sauvegarder = tk.Button(game_file_control,        text = "Save",                    font = ("Arial 25 bold"), fg = "#1b1b1b", bg = "white",  activeforeground = "#1b1b1b", activebackground = "white", bd = 7, pady = 5, padx = 20, width = 10, command = save)
boutton_Ouvrir      = tk.Button(game_file_control,        text = "Load",                    font = ("Arial 25 bold"), fg = "#1b1b1b", bg = "white",  activeforeground = "#1b1b1b", activebackground = "white", bd = 7, pady = 5, padx = 20, width = 10, command = load)

# BOUTTONS PACK:

boutton_Start.pack        (padx = 5, pady = 5, side = "left", expand = 1)
boutton_Pause.pack        (padx = 5, pady = 5, side = "left", expand = 1)
boutton_Quitter.pack      (padx = 5, pady = 5, side = "left", expand = 1)


label_Texte.pack          (padx = 5, pady = 5, side = "top")
boutton_Vitesse.pack      (padx = 5, pady = 5, side = "top")
boutton_Avancer.pack      (padx = 5, pady = 5, side = "left")
boutton_Retour.pack       (padx = 5, pady = 5, side = "right")
boutton_Sauvegarder.pack  (padx = 5, pady = 5, side = "left")
boutton_Ouvrir.pack       (padx = 5, pady = 5, side = "right")

# CANVAS CREATION / PACK:

# création de la grille de base avec les cases apparantes
# (HEIGHT/HAUTEUR)/nombre_case permet la création de case proportionnelle au Canvas

<<<<<<< HEAD
Canvas = tk.Canvas(terrain_jeu_frame, height = HEIGHT, width = WIDTH, highlightthickness = 0, bg = "#1b1b1b")
Canvas.pack (expand = 1, fill = None, anchor = "center")
canvas_refresh()
=======

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
>>>>>>> 75d33904a3d7899f334e60b38526524eb18c09e6


racine.mainloop()