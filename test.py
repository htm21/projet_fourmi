import tkinter as tk


racine = tk.Tk()
racine.title("La Fourmi de Langton")
Canvas1 = tk.Canvas(racine, height=700, width=700, bg="grey")
Canvas1.pack(padx=15,pady=15)

cases = []
for i in range(100) :
    liste_case = []
    for j in range(100) :
        case = Canvas1.create_rectangle(i*8+2,j*8+2,i*8+15,j*8+15, fill="white")   #pour les multiplications, inspiré par un site
        liste_case.append(case)
    cases.append(liste_case)

#donc jusqu'ici, on a la fenêtre : racine ; le canvas : Canvas 1 ; et la création de la grille avec la bougle for()

racine.mainloop()