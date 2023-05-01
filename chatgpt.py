import tkinter as tk
import sqlite3

# Créez une connexion à la base de données
conn = sqlite3.connect('tournoi.db')

# Créez une table pour stocker les joueurs et leurs scores
conn.execute('''CREATE TABLE IF NOT EXISTS Joueurs
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             nom TEXT NOT NULL,
             score INTEGER NOT NULL);''')

# Créez une fenêtre principale pour l'interface graphique
root = tk.Tk()

# Ajoutez un label pour les nouveaux joueurs
new_player_label = tk.Label(root, text="Nouveau joueur:")
new_player_label.pack()

# Ajoutez une zone de texte pour saisir le nom du joueur
new_player_entry = tk.Entry(root)
new_player_entry.pack()

# Ajoutez un bouton pour ajouter un nouveau joueur
def ajouter_joueur():
    nom = new_player_entry.get()
    conn.execute("INSERT INTO Joueurs (nom, score) VALUES (?, ?)", (nom, 0))
    conn.commit()
    new_player_entry.delete(0, tk.END)

ajouter_joueur_button = tk.Button(root, text="Ajouter joueur", command=ajouter_joueur)
ajouter_joueur_button.pack()

# Ajoutez un label pour les scores des joueurs
scores_label = tk.Label(root, text="Scores:")
scores_label.pack()

# Ajoutez une liste déroulante pour sélectionner les joueurs
joueur_selection = tk.StringVar(root)
joueur_selection.set("Sélectionnez un joueur")

joueurs = conn.execute("SELECT nom FROM Joueurs").fetchall()
joueurs = [joueur[0] for joueur in joueurs]

joueur_selection_dropdown = tk.OptionMenu(master=root, value=joueur_selection, *joueurs)
joueur_selection_dropdown.pack()

# Ajoutez une zone de texte pour saisir le score du joueur
score_entry = tk.Entry(root)
score_entry.pack()

# Ajoutez un bouton pour mettre à jour le score du joueur sélectionné
def mettre_a_jour_score():
    nom = joueur_selection.get()
    score = int(score_entry.get())
    conn.execute("UPDATE Joueurs SET score=? WHERE nom=?", (score, nom))
    conn.commit()
    score_entry.delete(0, tk.END)

mettre_a_jour_score_button = tk.Button(root, text="Mettre à jour score", command=mettre_a_jour_score)
mettre_a_jour_score_button.pack()

# Ajoutez un bouton pour afficher les matchs à venir
def afficher_matchs():
    joueurs = conn.execute("SELECT nom, score FROM Joueurs ORDER BY score DESC").fetchall()
    matchs = []
    for i in range(0, len(joueurs), 2):
        if i+1 < len(joueurs):
            matchs.append((joueurs[i][0], joueurs[i+1][0]))
    match_label = tk.Label(root, text="Matchs à venir:")
    match_label.pack()
    for match in matchs:
        match_string = match[0] + " contre " + match[1]
        match_display = tk.Label(root, text=match_string)
        match_display.pack()

afficher_matchs_button = tk.Button(root, text="Afficher matchs à venir", command=afficher_matchs)
afficher_matchs_button.pack()

# Lancez la fenêtre principale
root.mainloop()

# Fermez la connexion à la base de données
conn.close()

