from tkinter import *  
from tkinter import ttk


root = Tk()
root.geometry("350x170")

# Voir solution Exercice 49-50: https://www.tresfacile.net/solution-exercice-49-pgcd-ppcm-en-python/
def pgcd(m,n):
    d = min(m,n)
    while(m%d != 0 or n%d != 0):
        d = d - 1
    return d

# Voir solution Exercice 49-50: https://www.tresfacile.net/solution-exercice-49-pgcd-ppcm-en-python/
def ppcm(m,n):
    M = max(m,n)
    while(M%m !=0 or M%n != 0):
        M = M + 1
    return M

def action(event):
    # on récupère la valeur sélectionnée de la liste cobobox
    select = listeCombo.get()
    
    # récupération de la valeur de m depuis le champ de saisie 
    m = int(entry_m.get())
    # récupération de la valeur de n depuis le champ de saisie
    n = int(entry_n.get())
    
    if(select == "PGCD"):
        lblResult['text'] = "PGCD  = "  + str(pgcd(m , n))
    else:
        lblResult['text'] = "PPCM   = " + str(ppcm(m , n))
        
    

# Création du label et champ de saisie pour l'entier m
lbl_m = Label(root , text ="Enter value of m :  ")
entry_m = Entry(root)
lbl_m.place( x = 10 , y =20)
entry_m.place( x = 150 , y = 20)

# Création du label et champ de saisie pour l'entier n
lbl_n = Label(root , text ="Enter value of n :  ")
lbl_n.place(x = 10 , y = 50 )
entry_n = Entry(root)
entry_n.place( x = 150 , y = 50)

lblChoose = Label(root , text ="Choose function :  ")
lblChoose.place(x = 10 , y = 80)

# Création de la liste combobox pour sélectionner la fonction
listeCombo = ttk.Combobox(root, values=[ "PGCD" , "PPCM" ] )
listeCombo.place(x = 150 , y = 80 , width = 165)
listeCombo.bind("<<ComboboxSelected>>", action)

# Création d'un label qui affiche le résultat
lblResult = Label(root , text ="Result :  ")
lblResult.place(x = 150 , y = 110)

root.mainloop()
