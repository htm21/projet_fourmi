import tkinter as tk

#LES DIFFÉRENTES CONSTANTES

#POUR LE CANVAS
HEIGHT = 700
WIDTH = 700

#POUR LES CASES
case = []                   #variable de la liste 2D
nombre_case = 50


#Initiation liste 2D de la grille
#inspiration pour les 0 / 1 : http://pascal.ortiz.free.fr/contents/tkinter/projets_tkinter/langton/langton.html

for ligne in range(nombre_case):
    sous_liste = []
    for colonne in range(nombre_case):             #liste en 2D qui contient 50 lignes et 50 colonnes
        sous_liste.append(0)                                #[[0,0,0,...,0,0,0,0],[0,0,0,...,0,0,0,0],...]
    case.append(sous_liste)

#def JeuEnCours():
    #global boutton_start_stop

    #if boutton_start_stop["text"] == "START" :
        #boutton_start_stop.config(text="STOP")
    #else :
        #boutton_start_stop.config(text="START")

#Partie graphique 
racine = tk.Tk()
racine.title("La Fourmi de Langton")
racine.geometry("1000x800")

vitesse = 1

def changer_vitesse():
    global vitesse
    if vitesse == 1:
        boutton_accelerer.config(text="Vitesse x 2")
        vitesse = 2
    elif vitesse == 2:
        boutton_accelerer.config(text="Vitesse x 0.5")
        vitesse = 0.5
    elif vitesse == 0.5:
        boutton_accelerer.config(text="Vitesse x 1")
        vitesse = 1


Canvas = tk.Canvas(racine, height=HEIGHT, width=WIDTH)

#création de la grille de base avec les cases apparantes
        #-> liste en compréhension : https://python.doctor/page-comprehension-list-listes-python-cours-debutants

                        #(HEIGHT/HAUTEUR)/nombre_case permet la création de case proportionnelle au Canvas
                                #-> https://docs.python.org/3/library/tkinter.html (Partie sur les Canvas)

[[Canvas.create_rectangle(colonnes*(HEIGHT/nombre_case),lignes*(WIDTH/nombre_case),(colonnes+1)*(HEIGHT/nombre_case),(lignes+1)*(WIDTH/nombre_case),
                          fill="white",outline="black")

  for lignes in range(nombre_case)] for colonnes in range(nombre_case)]                

boutton_start = tk.Button(racine, text="START", font=("Arial",20,"bold"),
                       fg="#DF0101", bg="#0404B4",activeforeground="#DF0101",
                       relief="raised",bd=10,pady=10,padx=20
                    )

boutton_stop = tk.Button(racine, text="RESET", font=("Arial",20,"bold"),
                       fg="#DF0101", bg="#0404B4",activeforeground="#DF0101",
                       relief="raised",bd=10,pady=10,padx=20
                    )

boutton_pause = tk.Button(racine, text="STOP", font=("Arial",20,"bold"),
                       fg="#DF0101", bg="#0404B4",activeforeground="#DF0101",
                       relief="raised",bd=10,pady=10,padx=20
                    )

label_text = tk.Label(racine, text="LES COMMANDES AVANCÉES", font=("Poppins",15,"bold"),
                       fg="black", activeforeground="black"
                    )

boutton_accelerer = tk.Button(racine, text="Vitesse : x1",font=("Poppins",20,"bold"),
                       fg="black", activeforeground="black",command=changer_vitesse
                       )

boutton_retour = tk.Button(racine, text="RETOUR",font=("Poppins",20,"bold"),
                       fg="black", activeforeground="black"
                       )

boutton_start.grid(row=0,column=0)
boutton_pause.grid(row=0,column=1)
boutton_stop.grid(row=0,column=2)
boutton_accelerer.grid(row=1, column=4)
boutton_retour.grid(row=2,column=4)

label_text.grid(row = 0, column=4)

Canvas.grid(row=1,column=0,columnspan=4,rowspan=4,padx=25)
racine.mainloop()