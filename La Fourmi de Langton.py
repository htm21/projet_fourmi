import ctypes, platform, json, tkinter as tk, time as t
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
taille_grille   = [21,51, 101, 201] # Types de comportement de la fourmie

fourmi_objs   = [{"sym" : 0, "pos" : [nombre_case // 2,nombre_case // 2], "direction" : directions[0], "case_actuelle" : "w", "couleur" : "red", "obj" : "None"}] # l'object/dictionaire fourmi = symbole | position | direction | case actuelle | couleur | canvas.rectangle int

symbol         = fourmi_objs[-1]["sym"] + 1 if fourmi_objs else 0
pos            = [nombre_case // 2,nombre_case // 2]
direction      = directions[0]
fourmi_color  = "red"

for fourmi in fourmi_objs: # Pose les symboles des fourmis dans la grille
    field[fourmi["pos"][0]][fourmi["pos"][1]] = fourmi["sym"]

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
    
    if not args or args[0].keysym == "Up":
        vitesse_jeu = vitesses[0] if vitesse_jeu == vitesses[-1] else vitesses[vitesses.index(vitesse_jeu) + 1]
        bouton_Vitesse.config(text = vitesse_jeu[1])
    elif args[0].keysym == "Down":
        vitesse_jeu = vitesses[-1] if vitesse_jeu == vitesses[0] else vitesses[vitesses.index(vitesse_jeu) - 1]
        bouton_Vitesse.config(text = vitesse_jeu[1])

def sauvegarder(*args): 
    with open("game_state.txt", "w") as file:
        file.write(str(grid) + "\n")
        file.write(str(ant_pos[0]) + "," + str(ant_pos[1]) + "\n")
        file.write(ant_dir)
       
def charger(*args):
    with open("game_state.txt", "r") as file:
        # Lire la grille et la position de la fourmi depuis le fichier
        grid_str = file.readline().rstrip()
        ant_pos_str = file.readline().rstrip()
        ant_dir_str = file.readline().rstrip() # fenetre pour charger un fichier txt qui a une sauvegarede d'un jeu'''
    file_path = filedialog.askopenfilename(title = "Charger une partie", filetypes = (("Fichiers textes", "*.txt"),("Tous les fichiers", "*.*"))).name       

def avancer(*args):
    '''Fait avencer le jeu d'une unité de temps'''
    if Running: pass
    else: fourmi_update()

def retour(*args):
    '''Fait retourner le jeu d'une unité de temps'''
    global directions, refesh_counter, total_steps

    if Running or refesh_counter == 0: return
    else : 
        for ant in fourmi_objs:

            #a faire
        
            
            Canvas.update()
        
        refesh_counter -= 1

def start(*args):
    '''Fait tourner le jeu'''
    global Running
    
    if Running: pause()
    else:
        Running = True
        bouton_Start.config(text = "Pause")
        while Running:
            fourmi_update()
            t.sleep(vitesse_jeu[0])

def pause():
    '''Met en pause le jeu'''
    global Running
    bouton_Start.config(text = "Play")
    Running = False

def tk_key_control(event):
    '''Takes control of Keyboard Input'''
    if event.char == "g":
        toggle_grid_lines()

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

def change_type_case(y, x):
    '''Change la couleur de la case en fonction de sa couleur precedente'''
    if fourmi["case_actuelle"] == "w":
        field[y][x] = "b"
        Canvas.create_rectangle(x * (Height / nombre_case), y * (Width / nombre_case), (x + 1) * (Height / nombre_case), (y + 1) * (Width / nombre_case), outline = Grid_Line, fill = "black")
    else:
        field[y][x] = "w"
        Canvas.create_rectangle(x * (Height / nombre_case), y * (Width / nombre_case), (x + 1) * (Height / nombre_case), (y + 1) * (Width / nombre_case), outline = Grid_Line, fill = "white")

def fourmi_update():
    '''Met a jour le positionnement de la fourmi et les cases dans la liste "field" et canvas'''
    global directions, refesh_counter, total_steps, Grid_Line 

    for ant in fourmi_objs:
        # Change la directionde la fourmi
        if ant["case_actuelle"] == "b": ant["direction"] = directions[-1] if ant["direction"] == directions[0] else directions[directions.index(ant["direction"]) - 1]
        else:                           ant["direction"] = directions[0] if ant["direction"] == directions[-1] else directions[directions.index(ant["direction"]) + 1]
    
        # Change la couleur de la case en fonction de sa couleur precedente 
        change_type_case(*ant["pos"])

        # Bouge la fourmi en fonction de son orientation
        if   ant["direction"] == "0":   ant["pos"][0] = nombre_case - 1 if ant["pos"][0] == 0 else ant["pos"][0] - 1 # Up
        # si pos y de ant est toute en haut elle redecnends tout en bas sinon elle monte d'une case
        elif ant["direction"] == "180": ant["pos"][0] = 0 if ant["pos"][0] == nombre_case - 1 else ant["pos"][0] + 1 # Down
        # si pos y de ant est toute en bas elle remonte toute n haut sinon elle desends d'une case 
        elif ant["direction"] == "90":  ant["pos"][1] = 0 if ant["pos"][1] == nombre_case - 1 else ant["pos"][1] + 1 # Left
        #  si pos x de ant est toute a gauche elle repasse toute a droite sinon elle bouge d'une case vers la gauche
        elif ant["direction"] == "-90": ant["pos"][1] = nombre_case - 1 if ant["pos"][1] == 0 else ant["pos"][1] - 1 # Right
        # si pos x de ant est toute a droite elle repasse toute a gauche sinon elle bouge d'une case vers la droite

        # Met a jour le canvas et suvegarde la case actuelle
        ant["case_actuelle"] = field[ant["pos"][0]][ant["pos"][1]]
        ant["obj"] = Canvas.create_rectangle(ant["pos"][1] * (Height / nombre_case), ant["pos"][0] * (Width / nombre_case), (ant["pos"][1] + 1) * (Height / nombre_case), (ant["pos"][0] + 1) * (Width / nombre_case), outline = Grid_Line, fill = ant["couleur"])
        # Canvas.tag_bind(ant["obj"],"<Button-1>", lambda event, fourmi = ant: fourmi_config(fourmi))
        Canvas.update()
    
    total_steps += 1; refesh_counter += 1
    if refesh_counter > 1000: canvas_refresh(); refesh_counter = 0
    label_steps.configure(text = f"Steps: {total_steps}")


def canvas_refresh():
    '''Met a jour TOUT le canvas'''
    global fourmi_objs

    Canvas.delete("all")
    for y, line in enumerate(field):
        for x, cell in enumerate(line):
            if cell == "b":   Canvas.create_rectangle(x * (Height / nombre_case), y * (Width / nombre_case), (x + 1) * (Height / nombre_case), (y + 1) * (Width / nombre_case), outline = Grid_Line, fill = "black")
            elif cell == "w": Canvas.create_rectangle(x * (Height / nombre_case), y * (Width / nombre_case), (x + 1) * (Height / nombre_case), (y + 1) * (Width / nombre_case), outline = Grid_Line, fill = "white")
    for fourmi in fourmi_objs:
        fourmi["obj"] = Canvas.create_rectangle(fourmi["pos"][1] * (Height / nombre_case), fourmi["pos"][0] * (Width / nombre_case), (fourmi["pos"][1] + 1) * (Height / nombre_case), (fourmi["pos"][0] + 1) * (Width / nombre_case), outline = Grid_Line, fill = fourmi["couleur"])
    
def reset_field(*args):
    '''Resets the field with no ants'''
    global Running, field, fourmi_objs

    pause()
    fourmi_objs = []
    field        = [["w" for _ in range(nombre_case)] for _ in range(nombre_case)]
    Canvas.delete("all"); canvas_refresh()


def configure_creation_fourmi(*config_type):
    global symbol, pos, direction, fourmi_color

    if config_type[0] == "color":
        fourmi_color = colorchooser.askcolor()[1]
        config_type[1].config(bg = fourmi_color, activebackground = fourmi_color)

    elif config_type[0] == "add":
        try: 
            if int(config_type[1].get()) > nombre_case or int(config_type[1].get()) < 0: pass
            else: pos[0] = int(config_type[1].get())
        except ValueError: pass
        try: 
            if int(config_type[2].get()) > nombre_case or int(config_type[2].get()) < 0: pass
            else: pos[1] = int(config_type[2].get())
        except ValueError: pass

        if not config_type[3].get(): pass
        else: direction = directions[directions.index(config_type[3].get())]
        

        fourmi_objs.append({"sym" : symbol, "pos" : pos, "direction" : direction, "case_actuelle" : "w", "couleur" : fourmi_color, "obj" : "None"})
        config_type[4].destroy()
        symbol         = fourmi_objs[-1]["sym"] + 1 if fourmi_objs else 0
        pos            = [nombre_case // 2,nombre_case // 2]
        direction      = directions[0]
        fourmi_color  = "red"
        
        canvas_refresh()

def ajout_fourmi(*args):
    '''Ouvre une fenetre separee pour configurer et ajouter une fourmi au terrain'''
    global fourmi_color, pos, nombre_case, directions

    pause()
    fourmi_create_window = tk.Tk()
    fourmi_create_window.title("Configuration de la Fourmi")
    width, height = 1000, 700
    screen_width, screen_height  = fourmi_create_window.winfo_screenwidth(), fourmi_create_window.winfo_screenheight()
    x, y = (screen_width/2) - (width/2), (screen_height/2) - (height/2)
    fourmi_create_window.geometry('%dx%d+%d+%d' % (width, height, x, y))
    fourmi_create_window.resizable(False,False)
    if platform.system() == "Windows": fourmi_create_window.overrideredirect(1); fourmi_create_window.wm_attributes("-topmost", 1); ctypes.windll.shcore.SetProcessDpiAwareness(1)

    main_frame      = tk.Frame(fourmi_create_window, bg = "#1b1b1b", highlightbackground = "#3b3b3b", highlightthickness = 7)

    menu_top_bar     = tk.Frame(main_frame,      bg = "#3b3b3b")
    menu_creation    = tk.Frame(main_frame,      bg = "#1b1b1b")
    menu_bottom_bar  = tk.Frame(main_frame,      bg = "#1b1b1b")
    pos_frame        = tk.Frame(menu_creation,   bg = "#1b1b1b")
    pos_framel       = tk.Frame(pos_frame,       bg = "#1b1b1b")
    pos_framer       = tk.Frame(pos_frame,       bg = "#1b1b1b")
    color_frame      = tk.Frame(menu_creation,   bg = "#1b1b1b")
    color_framel     = tk.Frame(color_frame,     bg = "#1b1b1b")
    color_framer     = tk.Frame(color_frame,     bg = "#1b1b1b")
    direction_frame  = tk.Frame(menu_creation,   bg = "#1b1b1b")
    direction_framel = tk.Frame(direction_frame, bg = "#1b1b1b")
    direction_framer = tk.Frame(direction_frame, bg = "#1b1b1b")

    main_frame.pack       (side = None,     anchor = None,     fill = "both", expand = 1)
    menu_top_bar.pack     (side = None,     anchor = "n",      fill = "both", expand = 0)
    menu_creation.pack    (side = None,     anchor = "center", fill = "both", expand = 1)
    menu_bottom_bar.pack  (side = None,     anchor = "s",      fill = "both", expand = 0)
    pos_frame.pack        (side = None,     anchor = "center", fill = "both", expand = 1, pady = 10)
    pos_framel.pack       (side = "left",   anchor = None,     fill = "x",    expand = 1,)
    pos_framer.pack       (side = "right",  anchor = None,     fill = "x",    expand = 1,)
    color_frame.pack      (side = None,     anchor = "center", fill = "both", expand = 1, pady = 10)
    color_framel.pack     (side = "left",   anchor = None,     fill = "x",    expand = 1,)
    color_framer.pack     (side = "right",  anchor = None,     fill = "x",    expand = 1,)
    direction_frame.pack  (side = None,     anchor = "center", fill = "both", expand = 1, pady = 10)
    direction_framel.pack (side = "left",   anchor = None,     fill = "x",    expand = 1,)
    direction_framer.pack (side = "right",  anchor = None,     fill = "x",    expand = 1,)


    title_bar       = tk.Label      (menu_top_bar, text = f"Creation de la fourmi : {symbol + 1}", font = ("Helvetica 15 bold"), fg = "white", bg = "#3b3b3b")
    exitbutton      = tk.Button     (menu_top_bar, width = 2, height = 1, bg = "#1b1b1b", fg = "white", activebackground = "red", activeforeground = "black",relief = "sunken", bd = 0, text = "X", command = fourmi_create_window.destroy)
    
    position_label  = tk.Label      (pos_framel, text = "Position Fourmi :", font = ("Helvetica 25 bold"), fg = "white", bg = "#1b1b1b")
    posx_entry      = tk.Entry      (pos_framer, width = 10,  bg = "#3b3b3b", fg =  "white", cursor = "xterm", font = ("Helvetica 15 bold"), justify = "center", bd = 0, relief = "flat")
    posy_entry      = tk.Entry      (pos_framer, width = 10, bg = "#3b3b3b", fg = "white",  cursor = "xterm", font = ("Helvetica 15 bold"), justify = "center", bd = 0, relief = "flat")
    
    couleur_label   = tk.Label      (color_framel, text = "Couleur Fourmi :", font = ("Helvetica 25 bold"), fg = "white", bg = "#1b1b1b")
    couleur_box     = tk.Button     (color_framer, width = 6, height = 3, cursor = "hand2", relief = "sunken", bd = 0, activebackground = fourmi_color, bg = fourmi_color, command = lambda: configure_creation_fourmi("color", couleur_box))
    
    direction_label = tk.Label      (direction_framel, text = "Direction Fourmi :", font = ("Helvetica 25 bold"), fg = "white", bg = "#1b1b1b")
    direction_entry = ttk.Combobox  (direction_framer, text = "Position De La Fourmi:", font = ("Helvetica 10 bold"), state = "readonly", cursor = "hand2", justify = "center", values = directions)    

    cancel          = tk.Button     (menu_bottom_bar, width = 8, height = 2, cursor = "hand2", relief = "flat", font = ("Helvetica 10 bold"), text = "Cancel", command = fourmi_create_window.destroy)
    create          = tk.Button     (menu_bottom_bar, width = 8, height = 2, cursor = "hand2", relief = "flat", font = ("Helvetica 10 bold"), text = "Create", command = lambda: configure_creation_fourmi("add", posy_entry, posx_entry, direction_entry, fourmi_create_window))


    exitbutton.pack      (side = "right", anchor = None,padx = 5, pady = 5)
    title_bar.pack       (side = None,    anchor = "center", fill = "x")
    position_label.pack  (side = "left",padx = 30)
    posx_entry.pack      (side = "left",  fill = "x", expand = 1, ipady = 10)
    posy_entry.pack      (side = "right", fill = "x", expand = 1, ipady = 10, padx = 30)
    couleur_label.pack   (side = "left",padx = 30)
    couleur_box.pack     (side = None,    anchor = "center",padx = 145)
    direction_label.pack (side = "left",padx = 30)
    direction_entry.pack (side = None,    anchor = "center", ipady = 10, fill = "y", expand = 1)
    create.pack          (side = "right", anchor = None,padx = 5, pady = 3)
    cancel.pack          (side = "right", anchor = None,padx = 5, pady = 3)

    fourmi_create_window.mainloop()




# ========== Tkinter GUI ==========

if platform.system() == "Windows": ctypes.windll.shcore.SetProcessDpiAwareness(1)

racine = tk.Tk()
racine.title("La Fourmi de Langton")
racine.state("zoomed")
racine.protocol("WM_DELETE_WINDOW", quitter)
racine.minsize(1600, 900)

# FRAMES CREATION:

menu_du_haut             = tk.Frame (racine,       bg = "#1b1b1b", highlightbackground = "#3b3b3b", highlightthickness = 5)
menu_lateral             = tk.Frame (racine,       bg = "#1b1b1b", highlightbackground = "#3b3b3b", highlightthickness = 5)
terrain_jeu_frame        = tk.Frame (racine,       bg = "#1b1b1b", highlightbackground = "#3b3b3b", highlightthickness = 5)
menu_lateral_defaut      = tk.Frame (menu_lateral, bg = "#1b1b1b", highlightbackground = "#3b3b3b", highlightthickness = 5)
menu_lateral_fourmi      = tk.Frame (menu_lateral, bg = "#1b1b1b", highlightbackground = "#3b3b3b", highlightthickness = 5)

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

bouton_Start           = tk.Button    (menu_du_haut,             text = "Play",                        font = ("Helvetica 25 bold"), cursor = "hand2", fg = "#1b1b1b", bg = "white",  activeforeground = "#1b1b1b", activebackground = "white", bd = 7, pady = 5, padx = 20, width = 10, command = start)
bouton_Quitter         = tk.Button    (menu_du_haut,             text = "Quit",                        font = ("Helvetica 25 bold"), cursor = "hand2", fg = "#1b1b1b", bg = "white",  activeforeground = "#1b1b1b", activebackground = "white", bd = 7, pady = 5, padx = 20, width = 10, command = quitter)

label_Texte            = tk.Label     (menu_titre_frame,         text = "Les Commandes Avancées",      font = ("Helvetica 25 bold"),                   fg = "white",   bg = "#1b1b1b")   
bouton_Vitesse         = tk.Button    (vitesse_frame,            text = vitesse_jeu[1],                font = ("Helvetica 25 bold"), cursor = "hand2", fg = "#1b1b1b", bg = "white",  activeforeground = "#1b1b1b", activebackground = "white", bd = 7, pady = 5, padx = 20, width = 10, command = changer_vitesse)
bouton_Retour          = tk.Button    (controles_etat_jeu_frame, text = "Retour",                      font = ("Helvetica 25 bold"), cursor = "hand2", fg = "#1b1b1b", bg = "white",  activeforeground = "#1b1b1b", activebackground = "white", bd = 7, pady = 5, padx = 20, width = 10, command = retour)
bouton_Avancer         = tk.Button    (controles_etat_jeu_frame, text = "Avancer",                     font = ("Helvetica 25 bold"), cursor = "hand2", fg = "#1b1b1b", bg = "white",  activeforeground = "#1b1b1b", activebackground = "white", bd = 7, pady = 5, padx = 20, width = 10, command = avancer)
bouton_Sauvegarder     = tk.Button    (game_file_control,        text = "Sauvegarder",                 font = ("Helvetica 25 bold"), cursor = "hand2", fg = "#1b1b1b", bg = "white",  activeforeground = "#1b1b1b", activebackground = "white", bd = 7, pady = 5, padx = 20, width = 10, command = sauvegarder)
bouton_Charger         = tk.Button    (game_file_control,        text = "Charger",                     font = ("Helvetica 25 bold"), cursor = "hand2", fg = "#1b1b1b", bg = "white",  activeforeground = "#1b1b1b", activebackground = "white", bd = 7, pady = 5, padx = 20, width = 10, command = charger)

Label_Text2            = tk.Label     (menu_titre_PAPL,          text = "Les Pour allez plus loin",    font = ("Helvetica 25 bold"),                   fg = "white",   bg = "#1b1b1b")
Bouton_fourmi2         = tk.Button    (couleur_comportement,     text = "+ Fourmi",                    font = ("Helvetica 25 bold"), cursor = "hand2", fg = "#1b1b1b", bg = "white",  activeforeground = "#1b1b1b", activebackground = "white", bd = 7, pady = 5, padx = 20, width = 10, command = ajout_fourmie)
ComboBox_taille_grille = ttk.Combobox (couleur_comportement,     values = taille_grille, state="readonly")

label_steps            = tk.Label     (terrain_jeu_frame,        text =  f"Step: {total_steps}",       font = ("Helvetica 18 bold"), cursor = "hand2", fg = "white",   bg = "#2b2b2b")

# BOUTTONS/LABEL PACK:

bouton_Start.pack          (padx = 5, pady = 5, side = "left", expand = 1)
bouton_Quitter.pack        (padx = 5, pady = 5, side = "left", expand = 1)

label_Texte.pack           (padx = 5, pady = 5, side = "top")
bouton_Vitesse.pack        (padx = 5, pady = 5, side = "top")
bouton_Avancer.pack        (padx = 5, pady = 5, side = "left")
bouton_Retour.pack         (padx = 5, pady = 5, side = "right")
bouton_Sauvegarder.pack    (padx = 5, pady = 5, side = "left")
bouton_Charger.pack        (padx = 5, pady = 5, side = "right")

Label_Text2.pack           (padx = 5, pady = 5, side = "top")
Bouton_fourmi2.pack        (padx = 5, pady = 5, side = "left")
ComboBox_taille_grille.pack (padx = 5, pady = 5, side = "right")

label_steps.place          (x = 10, y = 10)


# CANVAS CREATION / PACK:

Canvas = tk.Canvas(terrain_jeu_frame, height = Height, width = Width, highlightthickness = 0, bg = "#1b1b1b")
Canvas.pack(expand = 1, anchor = "center")
canvas_refresh() # Affiche le canvas pour la premiere fois


# ========== Raccourcis Clavier ==========

racine.bind('<Escape>',    quitter)
racine.bind("<space>",     start)

racine.bind("<Up>",       changer_vitesse)
racine.bind("<Down>",     changer_vitesse)

racine.bind("<Right>",     avancer)
racine.bind("<Left>",      retour)

racine.bind("<Control-s>", sauvegarder)
racine.bind("<Control-l>", charger)

racine.bind("<MouseWheel>", zoom_canvas)
racine.bind("<KeyPress>",   tk_key_control)
racine.bind("<BackSpace>", reset_field)

# ========== Autres ==========

ComboBox_taille_grille.set("Choisie la taille")

racine.mainloop()
