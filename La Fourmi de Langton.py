import os, tkinter as tk, time as t
from tkinter import ttk, filedialog

print("\033c")

# ========== VAR ==========

Running       = False
steps         = 0
total_steps   = 0
HEIGHT, WIDTH = 900, 900 # Dimensions du canvas
nombre_case   = 51 # Nombre de cases dans le jeu | Doit etre impaire si on veut un milieu
field         = [["w" for _ in range(nombre_case)] for cell in range(nombre_case)] # liste 2D 40x40 remplie de "0"

vitesses      = [(0.5,"Speed: x 1"), (0.1, "Speed: x 2"), (0, "Speed: CPU"), (0.7, "Speed: x 0.5")] # Les differantes vitesses du jeu | num = temps de sleep, txt = text du boutton
vitesse_jeu   = vitesses[0] # Vitesse du jeu
directions    = ["0", "90", "180", "-90"] # Directions de la fourmie
comportement  = ["GGDD", "GDGD", "GDDG", "DGGD", "DGDD", "DDGG"] # Types de comportement de la fourmie

fourmie_objs  = []
fourmie_objs.append({"sym" : 0, "pos" : [nombre_case // 2,nombre_case // 2], "direction" : directions[0], "func" : None, "case_actuelle" : "w", "couleur" : "red", "obj" : None}) # l'object/dictionaire fourmie = symbole | position | direction | case actuelle | couleur |canvas.rectangle obj

for fourmie in fourmie_objs: # Pose les symboles des fourmies dans la grille
    field[fourmie["pos"][0]][fourmie["pos"][1]] = fourmie["sym"]

# ========== FUNC ==========

def quitter(*args):
    '''Ferme le programme'''
    global Running
    if Running: Running = False
    racine.destroy()

def changer_vitesse(*args):
    '''Change la vitesse du jeu'''
    global vitesses, vitesse_jeu
    vitesse_jeu = vitesses[0] if vitesse_jeu == vitesses[-1] else vitesses[vitesses.index(vitesse_jeu) + 1]
    bouton_Vitesse.config(text = vitesse_jeu[1])

def sauvegarder(*args): 
    '''Ouvre une fenetre pour savegarder la parie en cours'''
    fichier = [('Text Document', '*.txt')]
    fichier = filedialog.asksaveasfile(filetypes = fichier, defaultextension = fichier)
   
def charger(*args):
    '''Ouvre une fenetre pour charger un fichier txt qui a une sauvegarede d'un jeu'''
    file_path = filedialog.askopenfilename(title = "Charger une partie", filetypes = (("Fichiers textes", "*.txt"),("Tous les fichiers", "*.*"))).name    

def avancer(*args):
    '''Fait avencer le jeu d'une unité de temps'''
    if Running: return
    else: fourmie_update()

def start(*args):
    '''Fait tourner le jeu'''
    global Running
    if Running: Running = False
    else:
        Running = True
        while Running:
            fourmie_update()
            t.sleep(vitesse_jeu[0])

def pause():
    '''Met en pause le jeu'''
    global Running
    Running = False

def change_menu(*args):
    menu_lateral_fourmie.pack_forget()
    menu_lateral_defaut.pack(fill = "y", expand = 1)

def change_type_case(fourmie, y, x):
    '''Change la couleur de la case en fonction de sa couleur precedente'''
    if fourmie["case_actuelle"] == "w":
        field[y][x] = "b"
        Canvas.create_rectangle(x * (HEIGHT / nombre_case), y * (WIDTH / nombre_case), (x + 1) * (HEIGHT / nombre_case), (y + 1) * (WIDTH / nombre_case), outline = "", fill = "black")
    else:
        field[y][x] = "w"
        Canvas.create_rectangle(x * (HEIGHT / nombre_case), y * (WIDTH / nombre_case), (x + 1) * (HEIGHT / nombre_case), (y + 1) * (WIDTH / nombre_case), outline = "", fill = "white")

def fourmie_update():
    '''Met a jour le positionnement de la fourmie et les cases dans la liste "field" et canvas'''
    global directions, steps, total_steps 
    if fourmie_objs:
        for ant in fourmie_objs:
            # Change la directionde la fourmie
            if ant["case_actuelle"] == "b": ant["direction"] = directions[-1] if ant["direction"] == directions[0] else directions[directions.index(ant["direction"]) - 1]
            else:                           ant["direction"] = directions[0] if ant["direction"] == directions[-1] else directions[directions.index(ant["direction"]) + 1]
        
            # Change la couleur de la case en fonction de sa couleur precedente 
            change_type_case(ant, *ant["pos"])

            # Bouge la fourmie en fonction de son orientation
            if ant["direction"] == "0":     ant["pos"][0] = nombre_case - 1 if ant["pos"][0] == 0 else ant["pos"][0] - 1 # Up
            elif ant["direction"] == "180": ant["pos"][0] = 0 if ant["pos"][0] == nombre_case - 1 else ant["pos"][0] + 1 # Down
            elif ant["direction"] == "90":  ant["pos"][1] = 0 if ant["pos"][1] == nombre_case - 1 else ant["pos"][1] + 1 # Left
            elif ant["direction"] == "-90": ant["pos"][1] = nombre_case - 1 if ant["pos"][1] == 0 else ant["pos"][1] - 1 # Right

            # Met a jour le canvas et suvegarde la case actuelle
            ant["case_actuelle"] = field[ant["pos"][0]][ant["pos"][1]]
            ant["obj"] = Canvas.create_rectangle(ant["pos"][1] * (HEIGHT / nombre_case), ant["pos"][0] * (WIDTH / nombre_case), (ant["pos"][1] + 1) * (HEIGHT / nombre_case), (ant["pos"][0] + 1) * (WIDTH / nombre_case), outline = "", fill = ant["couleur"])
            # Canvas.tag_bind(ant["obj"],"<Button-1>", lambda event, fourmie = ant: fourmie_config(fourmie))
            Canvas.update()
    else: return
    total_steps += 1; steps += 1
    if steps > 1000: canvas_refresh(); steps = 0
         
def retour(*args):
    '''Fait retourner le jeu d'une unité de temps'''
    global directions, steps, total_steps

    if Running or steps == 0: return
    else : 
        for ant in fourmie_objs:

            #a faire
        
            
            Canvas.update()
        
        steps -= 1
    

def fourmie_config(fourmie, *args):
    if Running: return
    menu_lateral_defaut.pack_forget()
    menu_lateral_fourmie.pack(fill = "y", expand = 1)
    label_fourmie.config(text = f"Fourmie: {fourmie['sym'] + 1}")


def canvas_refresh():
    '''Met a jour TOUT le canvas'''
    Canvas.delete("all")
    for y, line in enumerate(field):
        for x, cell in enumerate(line):
            if cell == "b":   Canvas.create_rectangle(x * (HEIGHT / nombre_case), y * (WIDTH / nombre_case), (x + 1) * (HEIGHT / nombre_case), (y + 1) * (WIDTH / nombre_case), outline = "", fill = "black")
            elif cell == "w": Canvas.create_rectangle(x * (HEIGHT / nombre_case), y * (WIDTH / nombre_case), (x + 1) * (HEIGHT / nombre_case), (y + 1) * (WIDTH / nombre_case), outline = "", fill = "white")
            elif type(cell) == int:
                fourmie_objs[cell]["obj"] = Canvas.create_rectangle(x * (HEIGHT / nombre_case), y * (WIDTH / nombre_case), (x + 1) * (HEIGHT / nombre_case), (y + 1) * (WIDTH / nombre_case), outline = "", fill = fourmie_objs[cell]["couleur"], tags = str(fourmie_objs[cell]["sym"]))
                Canvas.tag_bind(fourmie_objs[cell]["obj"], "<Button-1>", lambda event, fourmie = fourmie_objs[cell]: fourmie_config(fourmie))

def couleur_fourmi():
    #fourmi?.config(bg = colorchooser.askcolor()[1])           -----> En Développement
    pass


# ========== Tkinter GUI ==========

racine = tk.Tk()
racine.title("La Fourmi de Langton")
racine.state("zoomed")
racine.protocol("WM_DELETE_WINDOW", quitter)

dirname    = os.path.dirname(__file__)
image_path = os.path.join(dirname, "ICONS", "logo.png")                     #https://stackoverflow.com/questions/61485360/opening-a-file-from-other-directory-in-python
logo       = tk.PhotoImage(file=image_path)
racine.iconphoto(True, logo)

racine.minsize(1280,720)

# FRAMES CREATION:

menu_du_haut             = tk.Frame (racine,       bg = "#1b1b1b", highlightbackground = "#3b3b3b", highlightthickness = 5)
terrain_jeu_frame        = tk.Frame (racine,       bg = "#1b1b1b", highlightbackground = "#3b3b3b", highlightthickness = 5)

menu_lateral             = tk.Frame (racine,       bg = "#1b1b1b", highlightbackground = "#3b3b3b", highlightthickness = 5)
menu_lateral_defaut      = tk.Frame (menu_lateral, bg = "#1b1b1b", highlightbackground = "#3b3b3b", highlightthickness = 5)
menu_lateral_fourmie     = tk.Frame (menu_lateral, bg = "#1b1b1b", highlightbackground = "#3b3b3b", highlightthickness = 5)


menu_titre_frame         = tk.Frame (menu_lateral_defaut, bg = "#1b1b1b")
vitesse_frame            = tk.Frame (menu_lateral_defaut, bg = "#1b1b1b")
controles_etat_jeu_frame = tk.Frame (menu_lateral_defaut, bg = "#1b1b1b")
game_file_control        = tk.Frame (menu_lateral_defaut, bg = "#1b1b1b")

menu_titre_PAPL          = tk.Frame (menu_lateral_defaut, bg = "#1b1b1b")
couleur_comportement     = tk.Frame (menu_lateral_defaut, bg = "#1b1b1b")

# FRAMES PACK:

menu_lateral.pack             (anchor = "e", fill = "y",    expand = 0, side = "right")
menu_lateral_defaut.pack      (anchor = "n", fill = "y",    expand = 1, side = None)
menu_du_haut.pack             (anchor = "n", fill = "x",    expand = 0, side = "top")
terrain_jeu_frame.pack        (anchor = "s", fill = "both", expand = 1, side = None)

menu_titre_frame.pack         (padx = 10, pady = 30, expand = 0, fill = "both")
vitesse_frame.pack            (padx = 10, pady = 30, expand = 0, fill = "both")
controles_etat_jeu_frame.pack (padx = 10, pady = 30, expand = 0, fill = "both")
game_file_control.pack        (padx = 10, pady = 30, expand = 0, fill = "both") 
menu_titre_PAPL.pack          (padx = 10, pady = 30, expand = 0, fill = "both")
couleur_comportement.pack     (padx = 10, pady = 30, expand = 0, fill = "both") 


# BOUTTONS CREATION:

bouton_Start          = tk.Button    (menu_du_haut,             text = "Play",                        font = ("Arial 25 bold"), fg = "#1b1b1b", bg = "white",  activeforeground = "#1b1b1b", activebackground = "white", bd = 7, pady = 5, padx = 20, width = 10, command = start)
bouton_Pause          = tk.Button    (menu_du_haut,             text = "Pause",                       font = ("Arial 25 bold"), fg = "#1b1b1b", bg = "white",  activeforeground = "#1b1b1b", activebackground = "white", bd = 7, pady = 5, padx = 20, width = 10, command = pause)                
bouton_Quitter        = tk.Button    (menu_du_haut,             text = "Quit",                        font = ("Arial 25 bold"), fg = "#1b1b1b", bg = "white",  activeforeground = "#1b1b1b", activebackground = "white", bd = 7, pady = 5, padx = 20, width = 10, command = quitter)

label_Texte           = tk.Label     (menu_titre_frame,         text = "Les Commandes Avancées",      font = ("Arial 25 bold"), fg = "white",   bg = "#1b1b1b")   
bouton_Vitesse        = tk.Button    (vitesse_frame,            text = vitesse_jeu[1],                font = ("Arial 25 bold"), fg = "#1b1b1b", bg = "white",  activeforeground = "#1b1b1b", activebackground = "white", bd = 7, pady = 5, padx = 20, width = 10, command = changer_vitesse)
bouton_Retour         = tk.Button    (controles_etat_jeu_frame, text = "Retour",                      font = ("Arial 25 bold"), fg = "#1b1b1b", bg = "white",  activeforeground = "#1b1b1b", activebackground = "white", bd = 7, pady = 5, padx = 20, width = 10, command = retour)
bouton_Avancer        = tk.Button    (controles_etat_jeu_frame, text = "Avancer",                     font = ("Arial 25 bold"), fg = "#1b1b1b", bg = "white",  activeforeground = "#1b1b1b", activebackground = "white", bd = 7, pady = 5, padx = 20, width = 10, command = avancer)
bouton_Sauvegarder    = tk.Button    (game_file_control,        text = "Sauvegarder",                 font = ("Arial 25 bold"), fg = "#1b1b1b", bg = "white",  activeforeground = "#1b1b1b", activebackground = "white", bd = 7, pady = 5, padx = 20, width = 10, command = sauvegarder)
bouton_Charger        = tk.Button    (game_file_control,        text = "Charger",                     font = ("Arial 25 bold"), fg = "#1b1b1b", bg = "white",  activeforeground = "#1b1b1b", activebackground = "white", bd = 7, pady = 5, padx = 20, width = 10, command = charger)

Label_Text2           = tk.Label     (menu_titre_PAPL,          text = "Les Pour allez plus loin",    font = ("Arial 25 bold"), fg = "white",   bg = "#1b1b1b")
Bouton_fourmi2        = tk.Button    (couleur_comportement,     text = "+ Fourmi",                    font = ("Arial 25 bold"), fg = "#1b1b1b", bg = "white",  activeforeground = "#1b1b1b", activebackground = "white", bd = 7, pady = 5, padx = 20, width = 10, command = couleur_fourmi)
ComboBox_Comportement = ttk.Combobox (couleur_comportement,     values = comportement)

label_fourmie         = tk.Label     (menu_lateral_fourmie,     text = "Fourmie",                     font = ("Arial 25 bold"), fg = "white",   bg = "#1b1b1b")
retour_defaut_menu    = tk.Button    (menu_lateral_fourmie,     text = "X",                           font = ("Arial 25 bold"), fg = "#1b1b1b", bg = "white",  activeforeground = "#1b1b1b", activebackground = "white", bd = 7, pady = 5, padx = 20, width = 10, command = change_menu)

# BOUTTONS PACK:

bouton_Start.pack          (padx = 5, pady = 5, side = "left", expand = 1)
bouton_Pause.pack          (padx = 5, pady = 5, side = "left", expand = 1)
bouton_Quitter.pack        (padx = 5, pady = 5, side = "left", expand = 1)


label_Texte.pack           (padx = 5, pady = 5, side = "top")
bouton_Vitesse.pack        (padx = 5, pady = 5, side = "top")
bouton_Avancer.pack        (padx = 5, pady = 5, side = "left")
bouton_Retour.pack         (padx = 5, pady = 5, side = "right")
bouton_Sauvegarder.pack    (padx = 5, pady = 5, side = "left")
bouton_Charger.pack        (padx = 5, pady = 5, side = "right")

Label_Text2.pack           (padx = 5, pady = 5, side = "top")
Bouton_fourmi2.pack        (padx = 5, pady = 5, side = "left")
ComboBox_Comportement.pack (padx = 5, pady = 5, side = "right")

label_fourmie.pack         (padx = 5, pady = 5, side = "top")
retour_defaut_menu.pack    (padx = 5, pady = 5, side = "top")


# CANVAS CREATION / PACK:

Canvas = tk.Canvas(terrain_jeu_frame, height = HEIGHT, width = WIDTH, highlightthickness = 0, bg = "#1b1b1b")
Canvas.pack(expand = 1, anchor = "center")
canvas_refresh() # Affiche le canvas pour la premiere fois


# ========== Raccourcis Clavier ==========

racine.bind('<Escape>',        quitter)
racine.bind("<space>",         start)

racine.bind("<Tab>",           changer_vitesse)

racine.bind("<Right>",         avancer)
racine.bind("<Left>",          retour)

racine.bind("<Control-s>",     sauvegarder)
racine.bind("<Control-l>",     charger)

# ========== Autres ==========

ComboBox_Comportement.set("Teste d'autres directions !")


racine.mainloop()
