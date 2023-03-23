import tkinter as tk
from tkinter import filedialog
import time as t

#LES DIFFÉRENTES VARIABLES

#POUR LE CANVAS
HEIGHT = 700
WIDTH = 700



nombre_case   = 40
field         = [[0 for _ in range(nombre_case)] for cell in range(nombre_case)] # liste 2D 40x40 remplie de "0"

Running       = False
fourmie_pos   = [nombre_case // 2, nombre_case // 2] # Position de la fourmie | [5, 3] = [y (ligne), x (colone)]
directions    = ["0", "90", "180", "-90"]
case_actuelle = 0 # Memoire de la cellule actuelle


vitesses      = [(0.5,"Speed: x 1"), (0.1, "Speed: x 2"), (0, "Speed: CPU"), (0.7, "Speed: x 0.5")] # Les differantes vitesses du jeu | num = temps de sleep, txt = text du boutton
vitesse_jeu   = vitesses[0] # Vitesse du jeu

direction_fourmie = directions[0]
field[nombre_case // 2][nombre_case // 2] = 3 # 3 c'est le symbol de la fourmie


#FONCTIONS 

def quitter():
    racine.destroy()

def changer_vitesse():
    '''Change la vitesse du jeu'''
    global vitesses, vitesse_jeu
    vitesse_jeu = vitesses[0] if vitesse_jeu == vitesses[-1] else vitesses[vitesses.index(vitesse_jeu) + 1]
    boutton_Vitesse.config(text = vitesse_jeu[1])


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

def start():
    '''Fait commencer le jeu'''
    global Running
    Running = True
    while Running:
        fourmie_update()
        t.sleep(vitesse_jeu[0])


def load():
    chemin_acces = file_path = filedialog.askopenfilename(initialdir='/Users/Ahmad/Desktop/UNI - UVSQ/L1 BI/S2/projet_fourmi',
                                                           title="Charger une partie", filetypes=(("Fichiers textes", "*.txt"),
                                                                                                   ("Tous les fichiers", "*.*"))
                                                        )

def save():                                                               #https://www.geeksforgeeks.org/python-asksaveasfile-function-in-tkinter/
    fichier = [('All Files', '*.*'),                                                    #en cours de dev 
             ('Python Files', '*.py'),                      
             ('Text Document', '*.txt')]
    fichier = filedialog.asksaveasfile(filetypes = fichier, defaultextension = fichier)



# ========== Tkinter GUI ========== 
racine = tk.Tk()
racine.title("La Fourmi de Langton")
racine.geometry("1300x800")
racine.configure(bg="black")


Canvas = tk.Canvas(racine, height=HEIGHT, width=WIDTH)

# création de la grille de base avec les cases apparantes
# (HEIGHT/HAUTEUR)/nombre_case permet la création de case proportionnelle au Canvas

boutton_Start = tk.Button(racine, text="PLAY", font=("Arial",20,"bold"),
                       fg="black", activeforeground="black",activebackground="white",
                       bd=10,pady=5,padx=20,width=10,command=start
                    )

boutton_Pause = tk.Button(racine, text="PAUSE", font=("Arial",20,"bold"),
                       fg="black", activeforeground="black",activebackground="white",
                       bd=10,pady=5,padx=20,width=10,
                    )

boutton_Quitter = tk.Button(racine, text="QUITTER", font=("Arial",20,"bold"),
                       fg="black", activeforeground="black",activebackground="white",
                       bd=10,pady=5,padx=20,width=10,command=quitter
                    )


label_Texte = tk.Label(racine, text="LES COMMANDES AVANCÉES", font=("Metropolis",30,"bold"),
                       fg="#8f6745",bg="black",activeforeground="black"
                    )

boutton_Vitesse = tk.Button(racine, text="VITESSE : x1",font=("Airial Black",20,"bold"),
                       fg="black", activeforeground="black",activebackground="white",
                       bd=10,pady=5,padx=20,width=10,
                       command=changer_vitesse
                       )

boutton_Retour = tk.Button(racine, text="RETOUR",font=("Poppins",20,"bold"),
                       fg="black", activeforeground="black",activebackground="white",
                       bd=10,pady=5,padx=20,width=10,
                       )

boutton_Avancer = tk.Button(racine, text="AVANCER",font=("Poppins",20,"bold"),
                       fg="black", activeforeground="black",activebackground="white",
                       bd=10,pady=5,padx=20,width=10,
                        )

boutton_Sauvegarder = tk.Button(racine,text="SAUVEGARDER",font=("Poppins",20,"bold"),
                       fg="black", activeforeground="black",activebackground="white",
                       bd=10,pady=5,padx=20,width=10,
                       command=save
                       )

boutton_Ouvrir = tk.Button(racine, text="CHARGER",font=("Poppins",20,"bold"),
                           fg="black", activeforeground="black",activebackground="white",
                       bd=10,pady=5,padx=20,width=10,
                       command=load
                        )

#PLACEMENTS 
    #-> BOUTONS

#AU DESSUS DE LA GRILLE
boutton_Start.grid(row=0,column=0)
boutton_Pause.grid(row=0,column=1)
boutton_Quitter.grid(row=0,column=2)

#Côté droit (3 Blocs)

boutton_Vitesse.grid(row=1, column=4,pady=10,padx=20,columnspan=2)


boutton_Avancer.grid(row=2,column=4,pady=10,padx=20)
boutton_Retour.grid(row=2,column=5,pady=10,padx=20)

boutton_Sauvegarder.grid(row=3,column=4,pady=20,padx=10)
boutton_Ouvrir.grid(row=3,column=5,padx=10,pady=20)

    #-> TEXTE
label_Texte.grid(row = 0, column=4,pady=10,padx=20,columnspan=4)

    #-> CANEVAS
Canvas.grid(row=1,column=0,columnspan=4,rowspan=4,padx=25)


canvas_refresh()

racine.mainloop()