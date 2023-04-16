import ctypes, json, tkinter as tk, time as t
from tkinter import ttk, filedialog, colorchooser

print("\033c")

# ========== VAR ==========

Running        = False
create_window  = False
refesh_counter = 0
total_steps    = 0
Height, Width  = 900, 900 # Dimensions du canvas
nombre_case    = 51 # Nombre de cases dans le jeu | Doit etre impaire si on veut un milieu
field          = [["w" for _ in range(nombre_case)] for cell in range(nombre_case)] # liste 2D 40x40 remplie de "0"
grid_l_types   = ["", "black"]
Grid_Line      = grid_l_types[1]

vitesses       = [(0.5,"Speed: x 1"), (0.1, "Speed: x 2"), (0, "Speed: CPU"), (0.7, "Speed: x 0.5")] # Les differantes vitesses du jeu | num = temps de sleep, txt = text du boutton
vitesse_jeu    = vitesses[0] # Vitesse du jeu
directions     = ["0", "90", "180", "-90"] # Directions de la fourmie
comportement   = ["GGDD", "GDGD", "GDDG", "DGGD", "DGDD", "DDGG"] # Types de comportement de la fourmie

fourmie_objs   = [{"sym" : 0, "pos" : [nombre_case // 2,nombre_case // 2], "direction" : directions[0], "case_actuelle" : "w", "couleur" : "red", "obj" : "None"},] # l'object/dictionaire fourmie = symbole | position | direction | case actuelle | couleur | canvas.rectangle int

for fourmie in fourmie_objs: # Pose les symboles des fourmies dans la grille
    field[fourmie["pos"][0]][fourmie["pos"][1]] = fourmie["sym"]

# ========== FUNC ==========

def quitter(*args):
    '''Ferme le programme'''
    global Running, create_window
    
    if Running: Running = False
    if create_window: create_window = False
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
    if Running: pass
    else: fourmie_update()

def retour(*args):
    '''Fait retourner le jeu d'une unité de temps'''
    global directions, refesh_counter, total_steps

    if Running or refesh_counter == 0: return
    else : 
        for ant in fourmie_objs:

            #a faire
        
            
            Canvas.update()
        
        refesh_counter -= 1

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

def tk_key_control(event):
    '''Takes control of Keyboard Input'''
    if event.char == "g":
        toggle_grid_lines()

def change_menu(*args):
    menu_lateral_fourmie.pack_forget()
    menu_lateral_defaut.pack(fill = "y", expand = 1)

def zoom_canvas(event):
    '''Zooms in or out of the canvas for better visability'''
    global Width, Height
    
    if event.num == 4 or event.delta == 120: # Zoom In Canvas
        if Canvas.winfo_width() > terrain_jeu_frame.winfo_width() or Canvas.winfo_height() > terrain_jeu_frame.winfo_height():
            Width, Height = terrain_jeu_frame.winfo_width(), terrain_jeu_frame.winfo_height()
        else: 
            Width += 100; Height += 100  
    elif event.num == 5 or event.delta == -120: # Zoom Out Canvas
        if Canvas.winfo_width() <= nombre_case or Canvas.winfo_height() <= nombre_case:
            Width, Height = nombre_case, nombre_case
        else:
            Width -= 100; Height -= 100
    Canvas.configure(width = Width, height = Height); canvas_refresh()

def toggle_grid_lines():
    '''Toggles the grid lines of the Canvas'''
    global Grid_Line

    Grid_Line = grid_l_types[0] if Grid_Line == grid_l_types[-1] else grid_l_types[grid_l_types.index(Grid_Line) + 1] 
    Canvas.update(); canvas_refresh()

def change_type_case(fourmie, y, x):
    '''Change la couleur de la case en fonction de sa couleur precedente'''
    if fourmie["case_actuelle"] == "w":
        field[y][x] = "b"
        Canvas.create_rectangle(x * (Height / nombre_case), y * (Width / nombre_case), (x + 1) * (Height / nombre_case), (y + 1) * (Width / nombre_case), outline = Grid_Line, fill = "black")
    else:
        field[y][x] = "w"
        Canvas.create_rectangle(x * (Height / nombre_case), y * (Width / nombre_case), (x + 1) * (Height / nombre_case), (y + 1) * (Width / nombre_case), outline = Grid_Line, fill = "white")

def fourmie_update():
    '''Met a jour le positionnement de la fourmie et les cases dans la liste "field" et canvas'''
    global directions, refesh_counter, total_steps, Grid_Line 

    for ant in fourmie_objs:
        # Change la directionde la fourmie
        if ant["case_actuelle"] == "b": ant["direction"] = directions[-1] if ant["direction"] == directions[0] else directions[directions.index(ant["direction"]) - 1]
        else:                           ant["direction"] = directions[0] if ant["direction"] == directions[-1] else directions[directions.index(ant["direction"]) + 1]
    
        # Change la couleur de la case en fonction de sa couleur precedente 
        change_type_case(ant, *ant["pos"])

        # Bouge la fourmie en fonction de son orientation
        if   ant["direction"] == "0":   ant["pos"][0] = nombre_case - 1 if ant["pos"][0] == 0 else ant["pos"][0] - 1 # Up
        elif ant["direction"] == "180": ant["pos"][0] = 0 if ant["pos"][0] == nombre_case - 1 else ant["pos"][0] + 1 # Down
        elif ant["direction"] == "90":  ant["pos"][1] = 0 if ant["pos"][1] == nombre_case - 1 else ant["pos"][1] + 1 # Left
        elif ant["direction"] == "-90": ant["pos"][1] = nombre_case - 1 if ant["pos"][1] == 0 else ant["pos"][1] - 1 # Right

        # Met a jour le canvas et suvegarde la case actuelle
        ant["case_actuelle"] = field[ant["pos"][0]][ant["pos"][1]]
        ant["obj"] = Canvas.create_rectangle(ant["pos"][1] * (Height / nombre_case), ant["pos"][0] * (Width / nombre_case), (ant["pos"][1] + 1) * (Height / nombre_case), (ant["pos"][0] + 1) * (Width / nombre_case), outline = Grid_Line, fill = ant["couleur"])
        # Canvas.tag_bind(ant["obj"],"<Button-1>", lambda event, fourmie = ant: fourmie_config(fourmie))
        Canvas.update()
    
    total_steps += 1; refesh_counter += 1
    if refesh_counter > 1000: canvas_refresh(); refesh_counter = 0
    label_steps.configure(text = f"Steps: {total_steps}")
    

def fourmie_config(fourmie, *args):
    '''Opens a configuration window for the ant object'''

    if Running: return
    menu_lateral_defaut.pack_forget()
    menu_lateral_fourmie.pack(fill = "y", expand = 1)
    label_fourmie.config(text = f"Fourmie: {fourmie['sym'] + 1}")


def canvas_refresh():
    '''Met a jour TOUT le canvas'''
    global fourmie_objs

    Canvas.delete("all")
    for y, line in enumerate(field):
        for x, cell in enumerate(line):
            if cell == "b":   Canvas.create_rectangle(x * (Height / nombre_case), y * (Width / nombre_case), (x + 1) * (Height / nombre_case), (y + 1) * (Width / nombre_case), outline = Grid_Line, fill = "black")
            elif cell == "w": Canvas.create_rectangle(x * (Height / nombre_case), y * (Width / nombre_case), (x + 1) * (Height / nombre_case), (y + 1) * (Width / nombre_case), outline = Grid_Line, fill = "white")
    for fourmie in fourmie_objs:
        fourmie["obj"] = Canvas.create_rectangle(fourmie["pos"][1] * (Height / nombre_case), fourmie["pos"][0] * (Width / nombre_case), (fourmie["pos"][1] + 1) * (Height / nombre_case), (fourmie["pos"][0] + 1) * (Width / nombre_case), outline = Grid_Line, fill = fourmie["couleur"], tags = str(fourmie["sym"]))
        Canvas.tag_bind(fourmie["obj"], "<Button-1>", lambda event, fourmie = fourmie: fourmie_config(fourmie))
    
def reset_field(*args):
    '''Resets the field with no ants'''
    global Running, field, fourmie_objs

    pause()
    fourmie_objs = []
    field        = [["w" for _ in range(nombre_case)] for _ in range(nombre_case)]
    Canvas.delete("all"); canvas_refresh()

def ajout_fourmie(*args):
    
    pause()
    fourmie_create_window = tk.Tk()
    width, height = 800, 600
    screen_width, screen_height  = racine.winfo_screenwidth(), racine.winfo_screenheight()
    x, y = (screen_width/2) - (width/2), (screen_height/2) - (height/2)
    fourmie_create_window.geometry('%dx%d+%d+%d' % (width, height, x, y))
    fourmie_create_window.resizable(False,False)
    fourmie_create_window.overrideredirect(True)
    
    exitbutton = tk.Button(fourmie_create_window, relief = "flat", text = "X", command = fourmie_create_window.destroy).pack(ipadx = 10, ipady = 0, side = "right", anchor = "n")

    fourmie_create_window.mainloop()


# ========== Tkinter GUI ==========

ctypes.windll.shcore.SetProcessDpiAwareness(1)

racine = tk.Tk()
racine.title("La Fourmi de Langton")
racine.state("zoomed")
racine.protocol("WM_DELETE_WINDOW", quitter)
racine.minsize(1280,720)

# FRAMES CREATION:

menu_du_haut             = tk.Frame (racine,       bg = "#1b1b1b", highlightbackground = "#3b3b3b", highlightthickness = 5)
menu_lateral             = tk.Frame (racine,       bg = "#1b1b1b", highlightbackground = "#3b3b3b", highlightthickness = 5)
terrain_jeu_frame        = tk.Frame (racine,       bg = "#1b1b1b", highlightbackground = "#3b3b3b", highlightthickness = 5)
menu_lateral_defaut      = tk.Frame (menu_lateral, bg = "#1b1b1b", highlightbackground = "#3b3b3b", highlightthickness = 5)
menu_lateral_fourmie     = tk.Frame (menu_lateral, bg = "#1b1b1b", highlightbackground = "#3b3b3b", highlightthickness = 5)

menu_titre_frame         = tk.Frame (menu_lateral_defaut, bg = "#1b1b1b")
vitesse_frame            = tk.Frame (menu_lateral_defaut, bg = "#1b1b1b")
controles_etat_jeu_frame = tk.Frame (menu_lateral_defaut, bg = "#1b1b1b")
game_file_control        = tk.Frame (menu_lateral_defaut, bg = "#1b1b1b")

menu_titre_PAPL          = tk.Frame (menu_lateral_defaut, bg = "#1b1b1b")
couleur_comportement     = tk.Frame (menu_lateral_defaut, bg = "#1b1b1b")

# FRAMES PACK:

menu_du_haut.pack             (anchor = "n", fill = "x",    expand = 0, side = "top")
menu_lateral.pack             (anchor = "e", fill = "y",    expand = 0, side = "right")
terrain_jeu_frame.pack        (anchor = "s", fill = "both", expand = 1, side = None)
menu_lateral_defaut.pack      (anchor = "n", fill = "y",    expand = 1, side = None)

menu_titre_frame.pack         (padx = 10, pady = 30, expand = 0, fill = "both")
vitesse_frame.pack            (padx = 10, pady = 30, expand = 0, fill = "both")
controles_etat_jeu_frame.pack (padx = 10, pady = 30, expand = 0, fill = "both")
game_file_control.pack        (padx = 10, pady = 30, expand = 0, fill = "both") 

menu_titre_PAPL.pack          (padx = 10, pady = 30, expand = 0, fill = "both")
couleur_comportement.pack     (padx = 10, pady = 30, expand = 0, fill = "both") 


# BOUTTONS/LABEL CREATION:

bouton_Start          = tk.Button    (menu_du_haut,             text = "Play",                        font = ("Helvetica 25 bold"), fg = "#1b1b1b", bg = "white",  activeforeground = "#1b1b1b", activebackground = "white", bd = 7, pady = 5, padx = 20, width = 10, command = start)
bouton_Pause          = tk.Button    (menu_du_haut,             text = "Pause",                       font = ("Helvetica 25 bold"), fg = "#1b1b1b", bg = "white",  activeforeground = "#1b1b1b", activebackground = "white", bd = 7, pady = 5, padx = 20, width = 10, command = pause)                
bouton_Quitter        = tk.Button    (menu_du_haut,             text = "Quit",                        font = ("Helvetica 25 bold"), fg = "#1b1b1b", bg = "white",  activeforeground = "#1b1b1b", activebackground = "white", bd = 7, pady = 5, padx = 20, width = 10, command = quitter)

label_Texte           = tk.Label     (menu_titre_frame,         text = "Les Commandes Avancées",      font = ("Helvetica 25 bold"), fg = "white",   bg = "#1b1b1b")   
bouton_Vitesse        = tk.Button    (vitesse_frame,            text = vitesse_jeu[1],                font = ("Helvetica 25 bold"), fg = "#1b1b1b", bg = "white",  activeforeground = "#1b1b1b", activebackground = "white", bd = 7, pady = 5, padx = 20, width = 10, command = changer_vitesse)
bouton_Retour         = tk.Button    (controles_etat_jeu_frame, text = "Retour",                      font = ("Helvetica 25 bold"), fg = "#1b1b1b", bg = "white",  activeforeground = "#1b1b1b", activebackground = "white", bd = 7, pady = 5, padx = 20, width = 10, command = retour)
bouton_Avancer        = tk.Button    (controles_etat_jeu_frame, text = "Avancer",                     font = ("Helvetica 25 bold"), fg = "#1b1b1b", bg = "white",  activeforeground = "#1b1b1b", activebackground = "white", bd = 7, pady = 5, padx = 20, width = 10, command = avancer)
bouton_Sauvegarder    = tk.Button    (game_file_control,        text = "Sauvegarder",                 font = ("Helvetica 25 bold"), fg = "#1b1b1b", bg = "white",  activeforeground = "#1b1b1b", activebackground = "white", bd = 7, pady = 5, padx = 20, width = 10, command = sauvegarder)
bouton_Charger        = tk.Button    (game_file_control,        text = "Charger",                     font = ("Helvetica 25 bold"), fg = "#1b1b1b", bg = "white",  activeforeground = "#1b1b1b", activebackground = "white", bd = 7, pady = 5, padx = 20, width = 10, command = charger)

Label_Text2           = tk.Label     (menu_titre_PAPL,          text = "Les Pour allez plus loin",    font = ("Helvetica 25 bold"), fg = "white",   bg = "#1b1b1b")
Bouton_fourmi2        = tk.Button    (couleur_comportement,     text = "+ Fourmi",                    font = ("Helvetica 25 bold"), fg = "#1b1b1b", bg = "white",  activeforeground = "#1b1b1b", activebackground = "white", bd = 7, pady = 5, padx = 20, width = 10, command = ajout_fourmie)
ComboBox_Comportement = ttk.Combobox (couleur_comportement,     values = comportement)

label_fourmie         = tk.Label     (menu_lateral_fourmie,     text = "Fourmie",                     font = ("Helvetica 25 bold"), fg = "white",   bg = "#1b1b1b")
retour_defaut_menu    = tk.Button    (menu_lateral_fourmie,     text = "X",                           font = ("Helvetica 25 bold"), fg = "#1b1b1b", bg = "white",  activeforeground = "#1b1b1b", activebackground = "white", bd = 7, pady = 5, padx = 20, width = 10, command = change_menu)
label_steps           = tk.Label     (terrain_jeu_frame,        text =  f"Step: {total_steps}",       font = ("Helvetica 18 bold"), fg = "white",   bg = "#2b2b2b")

# BOUTTONS/LABEL PACK:

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
label_steps.place          (x = 10, y = 10)


# CANVAS CREATION / PACK:

Canvas = tk.Canvas(terrain_jeu_frame, height = Height, width = Width, highlightthickness = 0, bg = "#1b1b1b")
Canvas.pack(expand = 1, anchor = "center")
canvas_refresh() # Affiche le canvas pour la premiere fois


# ========== Raccourcis Clavier ==========

racine.bind('<Escape>',    quitter)
racine.bind("<space>",     start)

racine.bind("<Tab>",       changer_vitesse)

racine.bind("<Right>",     avancer)
racine.bind("<Left>",      retour)

racine.bind("<Control-s>", sauvegarder)
racine.bind("<Control-l>", charger)

racine.bind("<MouseWheel>", zoom_canvas)
racine.bind("<KeyPress>",   tk_key_control)
racine.bind("<BackSpace>", reset_field)

# ========== Autres ==========

ComboBox_Comportement.set("Teste d'autres directions !")
racine.mainloop()