import tkinter as tk

#LES DIFFÉRENTES CONSTANTES

#POUR LE CANVAS
HEIGHT = 700
WIDTH = 700

#POUR LES CASES
case = []                   #varia
nombre_case = 50


#Initiation liste 2D de la grille

for ligne in range(nombre_case):
    sous_liste = []
    for colonne in range(nombre_case) :             #liste en 2D qui contient 50 lignes et 50 colonnes
        sous_liste.append(0)                                #[[0,0,0,...,0,0,0,0],[0,0,0,...,0,0,0,0],...]
    case.append(sous_liste)

def JeuEnCours():
    global boutton_start_stop

    if boutton_start_stop["text"] == "START" :
        boutton_start_stop.config(text="STOP")
    else :
        boutton_start_stop.config(text="START")

    



#Partie graphique 
racine = tk.Tk()
racine.title("La Fourmi de Langton")
racine.geometry("1000x800")     

Canvas = tk.Canvas(racine, height=HEIGHT, width=WIDTH)

#création de la grille de base avec les cases apparantes
        #-> liste en compréhension : https://python.doctor/page-comprehension-list-listes-python-cours-debutants

                        #(HEIGHT/HAUTEUR)/nombre_case permet la création de case proportionnelle au Canvas
                                #-> https://docs.python.org/3/library/tkinter.html (Partie sur les Canvas)

[[Canvas.create_rectangle(colonnes*(HEIGHT/nombre_case),lignes*(WIDTH/nombre_case),(colonnes+1)*(HEIGHT/nombre_case),(lignes+1)*(WIDTH/nombre_case),
                          fill="white",outline="black")
  for lignes in range(nombre_case)] for colonnes in range(nombre_case)]                

boutton_start_stop = tk.Button(racine, text="START", font=("Arial",40,"bold"),
                       fg="#DF0101", bg="#0404B4",activeforeground="#DF0101",
                       relief="raised",bd=10,pady=10,padx=20,command=JeuEnCours)



boutton_start_stop.grid(row= 0,column=0)
Canvas.grid()
racine.mainloop()