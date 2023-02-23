import tkinter as tk

#Dimensions
HEIGHT = 700
WIDTH = 700








#Partie graphique 
racine = tk.Tk()
racine.title("La Fourmi de Langton")
Canvas = tk.Canvas(racine, height=HEIGHT, width=WIDTH, bg="white")
Canvas.grid()
racine.mainloop()