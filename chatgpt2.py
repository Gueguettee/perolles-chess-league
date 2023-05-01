import tkinter as tk
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Initialiser la base de données SQLite
engine = create_engine('sqlite:///chess.db', echo=False)
Base = declarative_base()

# Définir la classe Joueur pour mapper la table "joueurs" en Python
class Joueur(Base):
    __tablename__ = 'joueurs'

    id = Column(Integer, primary_key=True)
    nom = Column(String)
    score = Column(Integer, default=0)

# Créer la table "joueurs" dans la base de données si elle n'existe pas
Base.metadata.create_all(engine)

# Créer une session SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()

# Ajouter des joueurs à la base de données
joueurs = [("Alice", 0), ("Bob", 0), ("Charlie", 0), ("David", 0)]
for nom, score in joueurs:
    j = Joueur(nom=nom, score=score)
    session.add(j)
session.commit()

# Fonction pour afficher les joueurs dans la console
def afficher_joueurs():
    joueurs = session.query(Joueur).all()
    for j in joueurs:
        print(f"{j.nom}: {j.score}")

afficher_joueurs()

# Interface graphique avec Tkinter
root = tk.Tk()
root.title("Tournoi d'échecs")

# Ajouter un joueur à la base de données
def ajouter_joueur():
    joueur = joueur_entry.get().strip()
    if joueur:
        j = Joueur(nom=joueur)
        session.add(j)
        session.commit()
        afficher_joueurs()
        joueur_selection['menu'].add_command(label=joueur, command=tk._setit(joueur_selection, joueur))

joueur_label = tk.Label(root, text="Nom du joueur :")
joueur_label.pack()

joueur_entry = tk.Entry(root)
joueur_entry.pack()

ajouter_joueur_button = tk.Button(root, text="Ajouter un joueur", command=ajouter_joueur)
ajouter_joueur_button.pack()

# Sélectionner un joueur pour mettre à jour son score
def selectionner_joueur(value):
    joueur_selection.set(value)

joueur_selection = tk.StringVar()
joueur_selection.set("Sélectionner un joueur")

joueurs = [j.nom for j in session.query(Joueur).all()]
joueur_selection_dropdown = tk.OptionMenu(root, joueur_selection, *joueurs, command=selectionner_joueur)
joueur_selection_dropdown.pack()

# Mettre à jour le score du joueur sélectionné
def mettre_a_jour_score():
    joueur = joueur_selection.get()
    score = score_entry.get()
    if joueur and score.isdigit():
        j = session.query(Joueur).filter_by(nom=joueur).first()
        j.score += int(score)
        session.commit()
        afficher_joueurs()
        score_entry.delete(0, tk.END)

score_label = tk.Label(root, text="Score à ajouter :")
score_label.pack()

score_entry = tk.Entry(root)
score_entry.pack()

mettre_a_jour_score_button = tk.Button(root, text="Mettre à jour le score", command=mettre_a_jour_score)
mettre_a_jour_score_button.pack()

# Lancer la boucle principale Tkinter
root.mainloop()
