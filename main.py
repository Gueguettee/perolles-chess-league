from database import Database, Player, Tournament, PlayersTournaments, Match
from datetime import datetime
import tkinter as tk

db = Database()

root = tk.Tk()
root.geometry("1000x600")
root.title("Pérolles Chess Tournament")

def plotPlayers():
    players = db.ReadAllData(Player)
    for j in players:
        print(f"{j.firstName}: {j.elo}")

def addPlayer():
    player = playerEntry.get().strip()
    if player:
        db.AddData(Player(firstName=player, lastName=player, school='HEIA-FR', elo=100))
        plotPlayers()
        menu = playerSelectDrowdown['menu']
        menu.add_command(label=player, command=tk._setit(varPlayerSelect, player))

varPlayerSelect = tk.StringVar()
varPlayerSelect.set("Sélectionner un player")

labelPlayer = tk.Label(root, text="Nom du joueur :")
labelPlayer.pack()

playerEntry = tk.Entry(root)
playerEntry.pack()

addPlayerButton = tk.Button(root, text="Ajouter un joueur", command=addPlayer)
addPlayerButton.pack()

players = [j.firstName for j in db.ReadAllData(Player)]
playerSelectDrowdown = tk.OptionMenu(root, varPlayerSelect, *players, command=varPlayerSelect.set)
playerSelectDrowdown.pack()

def updateScore():
    player = varPlayerSelect.get()
    score = score_entry.get()
    if player and score.isdigit():
        db.ModifyScorePlayer(player, int(score))
        plotPlayers()
        score_entry.delete(0, tk.END)

score_label = tk.Label(root, text="Score à ajouter :")
score_label.pack()

score_entry = tk.Entry(root)
score_entry.pack()

def startTournament():
    root2 = tk.Toplevel(root)
    labelNameTournament = tk.Label(root2, text="Nom du tournoi:")
    labelNameTournament.pack()

    entryNameTournament = tk.Entry(root2)
    entryNameTournament.bind('<Return>', lambda event: startTournament2())
    entryNameTournament.pack()

    def startTournament2():
        nameTournament = entryNameTournament.get()
        entryNameTournament.destroy()
        labelNameTournament.destroy()

        tournament = Tournament(name=nameTournament, date=datetime.now())
        tournamentID = db.AddData(data=tournament)
        players = db.GetAllPlayers()
        for player in players:
            db.AddPlayerIDToTournament(tournament_id=tournamentID, player_id=player.id)
        
        playersTournament = 
        db.AddData(Match(tournament_id=tournamentID, white_player_id=, black_player_id=))

updateScoreButton = tk.Button(root, text="Mettre à jour le score", command=updateScore)
updateScoreButton.pack()

startTournamentButton = tk.Button(root, text="Lancer un tournoi", command=startTournament)
startTournamentButton.pack()

root.mainloop()
