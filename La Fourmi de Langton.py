import ctypes, os, platform, json, tkinter as tk, time as t
from tkinter import ttk, filedialog, colorchooser

print("\033c")

# =============== initiation Tk =============
if platform.system() == "Windows": ctypes.windll.shcore.SetProcessDpiAwareness(1)
racine = tk.Tk()

# ========== Chargement des Icones ==========
program_icons  = {"Logo" : None, "Backwards" : None, "Cross" : None, "Forwards" : None,  "Load" : None,  "Pause" : None,  "Play" : None,  "Stop" : None,  "Save" : None,  "Zoom In" : None,  "Zoom Out" : None, "Speed 1" : None, "Speed 2" : None, "Speed 3" : None, "Add Ant" : None, "Escape" : None}

program_folder_path = os.path.dirname(__file__)
for icon in program_icons:
    icon_file = icon + ".png"
    program_icons[icon] = tk.PhotoImage(file = os.path.join(program_folder_path, "Icons", icon_file))

# ================== VAR ====================

Running        = False
create_window  = False

refesh_counter = 0
total_steps    = 0
Height, Width  = 700, 700 # Dimensions du canvas
taille_grille  = [20, 50, 100, 200] # Tailles Du Terrain
nombre_case    = taille_grille[1] + 1 # Nombre de cases dans le jeu | Doit etre impaire si on veut un milieu
field          = [["w" for _ in range(nombre_case)] for cell in range(nombre_case)] # liste 2D 40x40 remplie de "0"
grid_l_types   = ["", "black"]
Grid_Line      = grid_l_types[1]

vitesses       = [(0.5, program_icons["Speed 1"]), (0.1, program_icons["Speed 2"]), (0, program_icons["Speed 3"])] # Les differantes vitesses du jeu | num = temps de sleep, txt = text du boutton
vitesse_jeu    = vitesses[0] # Vitesse du jeu
directions     = ["0", "90", "180", "-90"] # Directions de la fourmie

fourmi_objs    = [{"sym" : 0, "pos" : [nombre_case // 2,nombre_case // 2], "direction" : directions[0], "case_actuelle" : "w", "couleur" : "red", "obj" : "None"}] # l'object/dictionaire fourmi = symbole | position | direction | case actuelle | couleur | canvas.rectangle int

symbol         = fourmi_objs[-1]["sym"] + 1 if fourmi_objs else 0
pos            = [nombre_case // 2,nombre_case // 2]
direction      = directions[0]
fourmi_color   = "red"

for fourmi in fourmi_objs: # Pose les symboles des fourmis dans la grille
    field[fourmi["pos"][0]][fourmi["pos"][1]] = fourmi["sym"]   

# ========== FUNC ==========

def quitter(*args):
    '''Ferme le programme'''
    global Running, create_window
    
    if Running: Running = False
    if create_window:
        create_window.destroy()
    racine.destroy()


def changer_vitesse(*args):
    '''Change la vitesse du jeu'''
    global vitesses, vitesse_jeu

    if not args or args[0].keysym == "Up":
        vitesse_jeu = vitesses[0] if vitesse_jeu == vitesses[-1] else vitesses[vitesses.index(vitesse_jeu) + 1]  
    elif args[0].keysym == "Down":
        vitesse_jeu = vitesses[-1] if vitesse_jeu == vitesses[0] else vitesses[vitesses.index(vitesse_jeu) - 1]
    bouton_Vitesse.config(image = vitesse_jeu[1])


def sauvegarder(file_name, position, couleurs):
    mon_fichier = open(file_name,"w")
    text = [str(position) + "\n", str(couleurs)]
    mon_fichier.writelines(text)
    mon_fichier.close()

    print(text)

def recuperer_tuple(text):
    ## Retirer les parentheses et les virgules
    text = text.replace("(", "")
    text = text.replace(")", "")

    text = text.split(", ")

    text = (int(text[0]), int(text[1]))

    return text

def recuperer_list(text):
    ## Retirer les crochets
    text = text.replace("[", "")
    text = text.replace("]", "")

    liste = text.split(", ")
    for i in range(len(liste)):
        liste[i] = eval(liste[i])

    return liste

def charger(file_name):
    mon_fichier = open(file_name,"r")
    text = mon_fichier.readlines()
    mon_fichier.close()

    position, couleurs = text
    
    position = recuperer_tuple(position)
    couleurs = recuperer_list(couleurs)

    return position, couleurs
     


def avancer(*args):
    '''Fait avencer le jeu d'une unité de temps'''
    if Running: pass
    else: fourmi_update()


def retour(*args):
    '''Fait retourner le jeu d'une unité de temps'''
    global directions, refesh_counter, total_steps, fourmi_objs
    
    if total_steps == 0 or not fourmi_objs: return
    else:
        for ant in fourmi_objs:
            
            if ant["case_actuelle"] == "b":Canvas.create_rectangle(ant["pos"][1] * (Height / nombre_case), ant["pos"][0] * (Width / nombre_case), (ant["pos"][1] + 1) * (Height / nombre_case), (ant["pos"][0] + 1) * (Width / nombre_case), outline = Grid_Line, fill = "black")
            else:                          Canvas.create_rectangle(ant["pos"][1] * (Height / nombre_case), ant["pos"][0] * (Width / nombre_case), (ant["pos"][1] + 1) * (Height / nombre_case), (ant["pos"][0] + 1) * (Width / nombre_case), outline = Grid_Line, fill = "white")

            if   ant["direction"] == "0"  : ant ["pos"][0] = 0 if ant ["pos"][0] == nombre_case - 1 else ant ["pos"][0] + 1 # Down
            elif ant["direction"] == "180": ant ["pos"][0] = nombre_case - 1 if ant ["pos"][0] == 0 else ant ["pos"][0] - 1 # Up
            elif ant["direction"] == "90" : ant ["pos"][1] = nombre_case - 1 if ant ["pos"][1] == 0 else ant ["pos"][1] - 1 # Left
            elif ant["direction"] == "-90": ant ["pos"][1] = 0 if ant ["pos"][1] == nombre_case - 1 else ant ["pos"][1] + 1 # Right

            ant["case_actuelle"] = field[ant["pos"][0]][ant["pos"][1]]
            change_type_case(ant, *ant["pos"])
            ant["case_actuelle"] = field[ant["pos"][0]][ant["pos"][1]]

            if ant["case_actuelle"] == "b": ant["direction"] = directions[0] if ant["direction"] == directions[-1] else directions[directions.index(ant["direction"]) + 1]
            else:                           ant["direction"] = directions[-1] if ant["direction"] == directions[0] else directions[directions.index(ant["direction"]) - 1]
                                    

            ant["obj"] = Canvas.create_rectangle(ant["pos"][1] * (Height / nombre_case), ant["pos"][0] * (Width / nombre_case), (ant["pos"][1] + 1) * (Height / nombre_case), (ant["pos"][0] + 1) * (Width / nombre_case), outline = Grid_Line, fill = ant["couleur"])
            Canvas.update()  
        total_steps -= 1; refesh_counter += 1
        if refesh_counter > 1000: canvas_refresh(); refesh_counter = 0
        label_steps.configure(text = f"Steps: {total_steps}")

def start(*args):
    '''Fait tourner le jeu'''
    global Running
    
    if Running: pause()
    else:
        Running = True
        bouton_Start.config(image = program_icons["Pause"])
        while Running:
            fourmi_update()
            t.sleep(vitesse_jeu[0])


def pause():
    '''Met en pause le jeu'''
    global Running
    bouton_Start.config(image = program_icons["Play"])
    Running = False


def tk_key_control(event):
    '''Takes control of Keyboard Input'''
    if event.char == "g":
        toggle_grid_lines()


def zoom_canvas(event):
    '''Zooms in or out of the canvas for better visability'''
    global Width, Height

    try:
        if event == "zoom in" or event.num == 4 or event.delta == 120: # Zoom In Canvas
            if Canvas.winfo_reqwidth() >= (field_frame.winfo_width() - 150) or Canvas.winfo_reqheight() >= (field_frame.winfo_height() - 150):
                Width, Height = Canvas.winfo_reqwidth(), Canvas.winfo_reqheight()
            else: 
                Width += 50; Height += 50
    except AttributeError: pass
    try:
        if event == "zoom out" or event.num == 5 or event.delta == -120: # Zoom Out Canvas
            if Canvas.winfo_reqwidth() <= nombre_case or Canvas.winfo_reqheight() <= nombre_case:
                Width, Height = nombre_case, nombre_case
            else:
                Width -= 50; Height -= 50
    except AttributeError: pass
    Canvas.configure(width = Width, height = Height); canvas_refresh()


def toggle_grid_lines():
    '''Toggles the grid lines of the Canvas'''
    global Grid_Line

    Grid_Line = grid_l_types[0] if Grid_Line == grid_l_types[-1] else grid_l_types[grid_l_types.index(Grid_Line) + 1] 
    Canvas.update(); canvas_refresh()


def change_field_size(*args):
    global field, fourmi_objs, nombre_case, pos, symbol, total_steps, refesh_counter


    nombre_case = int(cbox_field_taille.get()) + 1
    field = []
    field = [["w" for _ in range(nombre_case)] for _ in range(nombre_case)]
    fourmi_objs = []
    symbol = fourmi_objs[-1]["sym"] + 1 if fourmi_objs else 0
    pos = [nombre_case // 2,nombre_case // 2]
    cbox_field_taille.set(f"Taille Terrain: {cbox_field_taille.get()}x{cbox_field_taille.get()}")
    total_steps, refesh_counter = 0, 0
    label_steps.configure(text = f"Steps: {total_steps}")
    Main_Frame.focus() 
    
    canvas_refresh(); Canvas.update()


def change_type_case(fourmi, y, x):
    '''Change la couleur de la case en fonction de sa couleur precedente'''
    global nombre_case

    if fourmi["case_actuelle"] == "w":
        field[y][x] = "b"
        Canvas.create_rectangle(x * (Height / nombre_case), y * (Width / nombre_case), (x + 1) * (Height / nombre_case), (y + 1) * (Width / nombre_case), outline = Grid_Line, fill = "black")
    else:
        field[y][x] = "w"
        Canvas.create_rectangle(x * (Height / nombre_case), y * (Width / nombre_case), (x + 1) * (Height / nombre_case), (y + 1) * (Width / nombre_case), outline = Grid_Line, fill = "white")


def fourmi_update():
    '''Met a jour le positionnement de la fourmi et les cases dans la liste "field" et canvas'''
    global directions, refesh_counter, total_steps, Grid_Line, Running
    
    if fourmi_objs:
        for ant in fourmi_objs:
            # Change la directionde la fourmi
            if ant["case_actuelle"] == "b": ant["direction"] = directions[-1] if ant["direction"] == directions[0] else directions[directions.index(ant["direction"]) - 1]
            else:                           ant["direction"] = directions[0] if ant["direction"] == directions[-1] else directions[directions.index(ant["direction"]) + 1]
        
            # Change la couleur de la case en fonction de sa couleur precedente 
            change_type_case(ant, *ant["pos"])

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
            Canvas.update()
    
        total_steps += 1; refesh_counter += 1
        if refesh_counter > 1000: canvas_refresh(); refesh_counter = 0
        label_steps.configure(text = f"Steps: {total_steps}")
    else: 
        Running = False
        bouton_Start.config(image = program_icons["Play"])
        return


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
    global symbol, pos, direction, fourmi_color, nombre_case, field

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
        

        fourmi_objs.append({"sym" : symbol, "pos" : pos, "direction" : direction, "case_actuelle" : field[pos[0]][pos[1]], "couleur" : fourmi_color, "obj" : "None"})
        config_type[4].destroy()
        symbol         = fourmi_objs[-1]["sym"] + 1 if fourmi_objs else 0
        pos            = [nombre_case // 2, nombre_case // 2]
        direction      = directions[0]
        fourmi_color  = "red"
        
        canvas_refresh()


def ajout_fourmi(*args):
    '''Ouvre une fenetre separee pour configurer et ajouter une fourmi au terrain'''
    global fourmi_color, pos, nombre_case, directions, create_window

    pause()
    fourmi_create_window = tk.Tk()
    create_window = fourmi_create_window
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
    exitbutton      = tk.Button     (menu_top_bar, width = 2, height = 1, bg = "#1b1b1b", fg = "white", activebackground = "red", activeforeground = "black", relief = "sunken", bd = 0, text = "X", command = fourmi_create_window.destroy)
    
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

racine.title("La Fourmi de Langton")
racine.iconphoto(False, program_icons["Logo"])
racine.state("zoomed")
racine.protocol("WM_DELETE_WINDOW", quitter)
racine.minsize(1920, 1000)

# FRAMES CREATION:

Main_Frame      = tk.Frame (racine,       bg = "#1b1b1b", highlightbackground = "#3b3b3b", highlightthickness = 5)
menu_du_haut    = tk.Frame (Main_Frame,   bg = "#1b1b1b", highlightbackground = "#3b3b3b", highlightthickness = 5)
field_frame     = tk.Frame (Main_Frame,   bg = "#1b1b1b", highlightbackground = "#3b3b3b", highlightthickness = 5)
separator_frame = tk.Frame (menu_du_haut, bg = "#1b1b1b")

# FRAMES PACK:

Main_Frame.pack   (anchor = "center", fill = "both", expand = 1)
menu_du_haut.pack (anchor = "n", fill = "x",    expand = 0)
field_frame.pack  (anchor = "s", fill = "both", expand = 1)


# BOUTTONS/LABEL CREATION:

bouton_Start           = tk.Button    (menu_du_haut, image = program_icons["Play"],      relief = "sunken", bd = 0, cursor = "hand2", bg = "light green",  activebackground = "light green",  command = start)
bouton_Retour          = tk.Button    (menu_du_haut, image = program_icons["Backwards"], relief = "sunken", bd = 0, cursor = "hand2", bg = "cyan",   activebackground = "cyan",   command = retour)
bouton_Avancer         = tk.Button    (menu_du_haut, image = program_icons["Forwards"],  relief = "sunken", bd = 0, cursor = "hand2", bg = "cyan",   activebackground = "cyan",   command = avancer)
bouton_Vitesse         = tk.Button    (menu_du_haut, image = program_icons["Speed 1"],   relief = "sunken", bd = 0, cursor = "hand2", bg = "purple", activebackground = "purple", text = "Vitesse ",          compound = "right",font = ("Impact 20"), command = changer_vitesse)
bouton_ajout_fourmie   = tk.Button    (menu_du_haut, image = program_icons["Add Ant"],   relief = "sunken", bd = 0, cursor = "hand2", bg = "yellow", activebackground = "yellow", text = "  Ajout Fourmie  ", compound = "left", font = ("Impact 20"), command = ajout_fourmi)
bouton_zoomin          = tk.Button    (menu_du_haut, image = program_icons["Zoom In"],   relief = "sunken", bd = 0, cursor = "hand2", bg = "white",  activebackground = "white",  command = lambda a = "zoom in" : zoom_canvas(a))
bouton_zoomout         = tk.Button    (menu_du_haut, image = program_icons["Zoom Out"],  relief = "sunken", bd = 0, cursor = "hand2", bg = "white",  activebackground = "white",  command = lambda a = "zoom out": zoom_canvas(a))
bouton_Charger         = tk.Button    (menu_du_haut, image = program_icons["Load"],      relief = "sunken", bd = 0, cursor = "hand2", bg = "orange", activebackground = "orange", text = "Charger ",          compound = "right", font = ("Impact 20"),command = charger)
bouton_Sauvegarder     = tk.Button    (menu_du_haut, image = program_icons["Save"],      relief = "sunken", bd = 0, cursor = "hand2", bg = "orange", activebackground = "orange", text = "Sauvegarder ",      compound = "right", font = ("Impact 20"), command = sauvegarder)
bouton_Quitter         = tk.Button    (menu_du_haut, image = program_icons["Escape"],    relief = "sunken", bd = 0, cursor = "hand2", bg = "red",    activebackground = "red",    command = quitter)
cbox_field_taille      = ttk.Combobox (menu_du_haut, text = "Choisie la taille",         justify = "center", values = taille_grille, font = ("Impact 23"), state = "readonly")

label_steps            = tk.Label     (field_frame,  text =  f"Step: {total_steps}", font = ("Impact 18"), fg = "white",   bg = "#2b2b2b")

# BOUTTONS/LABEL PACK:

bouton_Start.pack          (side = "left",  padx = 10, pady = 10, ipadx = 5, ipady = 5, expand = 1)
bouton_Retour.pack         (side = "left",  padx = 10, pady = 10, ipadx = 5, ipady = 5, expand = 0)
bouton_Avancer.pack        (side = "left",  padx = 10, pady = 10, ipadx = 5, ipady = 5, expand = 0)
bouton_Vitesse.pack        (side = "left",  padx = 10, pady = 10, ipadx = 5, ipady = 5, expand = 1)
bouton_ajout_fourmie.pack  (side = "left",  padx = 10, pady = 10, ipadx = 5, ipady = 5, expand = 1, anchor = "center")
bouton_zoomin.pack         (side = "left",  padx = 10, pady = 10, ipadx = 5, ipady = 5, expand = 0)
bouton_zoomout.pack        (side = "left",  padx = 10, pady = 10, ipadx = 5, ipady = 5, expand = 0)
cbox_field_taille.pack     (side = "left",  padx = 10, pady = 10, ipadx = 5, ipady = 15, expand = 0)
separator_frame.pack       (side = "left", expand = 1, fill = "both")
bouton_Quitter.pack        (side = "right", padx = 10, pady = 10, ipadx = 5, ipady = 5, expand = 1, anchor = "e")
bouton_Sauvegarder.pack    (side = "right", padx = 10, pady = 10, ipadx = 5, ipady = 5, expand = 0)
bouton_Charger.pack        (side = "right", padx = 10, pady = 10, ipadx = 5, ipady = 5, expand = 0)
cbox_field_taille.set      (f"Taille Terrain: {nombre_case - 1}x{nombre_case - 1}")
label_steps.place          (x = 10, y = 10)

# CANVAS CREATION / PACK:

Canvas = tk.Canvas(field_frame, height = Height, width = Width, highlightthickness = 0, bg = "#1b1b1b")
Canvas.pack(expand = 1, anchor = "center")
canvas_refresh() # Affiche le canvas pour la premiere fois


# ========== Raccourcis Clavier ==========

racine.bind("<Up>",         changer_vitesse)
racine.bind("<Down>",       changer_vitesse)
racine.bind("<Right>",      avancer)
racine.bind("<Left>",       retour)
racine.bind("<space>",      start)
racine.bind('<Escape>',     quitter)
racine.bind("<KeyPress>",   tk_key_control)
racine.bind("<Control-s>",  sauvegarder)
racine.bind("<Control-l>",  charger)
racine.bind("<MouseWheel>", zoom_canvas)
racine.bind("<BackSpace>",  reset_field)
cbox_field_taille.bind("<<ComboboxSelected>>", change_field_size)

racine.mainloop()
