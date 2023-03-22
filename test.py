import tkinter as tk
from tkinter import filedialog

#LES DIFFÉRENTES VARIABLES

#POUR LE CANVAS
HEIGHT = 700
WIDTH = 700

#POUR LES CASES
case = []                   #variable de la liste 2D
nombre_case = 40

#POUR LA FOURMI



#Initiation liste 2D de la grille
#inspiration pour les 0 / 1 : http://pascal.ortiz.free.fr/contents/tkinter/projets_tkinter/langton/langton.html

for ligne in range(nombre_case):
    sous_liste = []
    for colonne in range(nombre_case):             #liste en 2D qui contient 40 lignes et 40 colonnes
        sous_liste.append(0)                                #[[0,0,0,...,0,0,0,0],[0,0,0,...,0,0,0,0],...]
    case.append(sous_liste)

#VARIABLES POUR LES FONCTIONS
vitesse = 1


#FONCTIONS 

def quitter():
    racine.destroy()

def changer_vitesse():
    global vitesse
    if vitesse == 1:
        boutton_Vitesse.config(text="VITESSE : x 2")
        vitesse = 2
    elif vitesse == 2:
        boutton_Vitesse.config(text="VITESSE : x 0.5")
        vitesse = 0.5
    elif vitesse == 0.5:
        boutton_Vitesse.config(text="VITESSE : x 1")
        vitesse = 1

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
[[Canvas.create_rectangle(colonnes*(HEIGHT/nombre_case), lignes*(WIDTH/nombre_case), (colonnes+1) * (HEIGHT/nombre_case), (lignes+1) * (WIDTH/nombre_case), fill = "white", outline = "black") for lignes in range(nombre_case)] for colonnes in range(nombre_case)]

boutton_Start = tk.Button(racine, text="PLAY", font=("Arial",20,"bold"),
                       fg="black", activeforeground="black",activebackground="white",
                       bd=10,pady=5,padx=20,width=10,
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
racine.mainloop()