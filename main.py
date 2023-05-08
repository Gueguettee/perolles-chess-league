from database import Database, Player, Tournament, PlayersTournaments, Match
from datetime import datetime
import tkinter as tk
from tkinter import ttk
import random
import math

N_ROUNDS = 3

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
if players:
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
    labelNameTournament = tk.Label(root2, text="Nom du tournoi :")
    labelNameTournament.pack()
    entryNameTournament = tk.Entry(root2)
    entryNameTournament.pack()

    labelNRoundTournament = tk.Label(root2, text="\n\nNombre de rounds :")
    labelNRoundTournament.pack()
    entryNRoundTournament = tk.Entry(root2)
    entryNRoundTournament.bind('<Return>', lambda event: establishmentTournament())
    entryNRoundTournament.pack()

    def establishmentTournament():
        nameTournament = entryNameTournament.get()
        n_rounds = int(entryNRoundTournament.get())
        if n_rounds < 1:
            n_rounds = N_ROUNDS
        
        nonlocal root2
        root2.destroy()
        root2 = tk.Toplevel(root)

        tournament = Tournament(name=nameTournament, date=datetime.now())
        tournamentID = db.AddData(data=tournament)
        players = db.GetAll(Player) # Tous les players en l'occurence
        for player in players:
            db.AddPlayerIDToTournament(tournament_id=tournamentID, player_id=player.id)

        roundT = 1
        startFirstRoundButton = tk.Button(root2, text="Start First Round", command=lambda: startRound(roundT))
        startFirstRoundButton.pack()
        
        def startRound(round):

            nonlocal root2
            if round == 1:
                startFirstRoundButton.destroy()
                string1 = "Players :\n\n"
            else:
                root2.destroy()
                root2 = tk.Toplevel(root)
                if round <= n_rounds:
                    string1 = "Actual classement :\n\n"
                else:
                    string1 = "Final classement :\n\n"

            playersTournament = db.GetPlayersTournamentsByTournamentID(tournamentID)
            n = 1
            playersTournamentsMatchID = []
            table_classement = [None] * len(playersTournament)
            i = 0
            if round != 1:
                for playerTournament in playersTournament:
                    table_classement[i] = [playerTournament.player_id, playerTournament.score]
                    i += 1
                while i != 0:
                    i = 0
                    for j in range(0, len(table_classement)-1):
                        if table_classement[j+1][1] > table_classement[j][1]:
                            temp = table_classement[j]
                            table_classement[j] = table_classement[j+1]
                            table_classement[j+1] = temp
                            i += 1

                for i in range(0, len(table_classement)):
                    player = db.GetPlayerByID(table_classement[i][0])
                    playersTournamentsMatchID.append(player.id)
                    string1 += f"{n}) {player.firstName} {player.lastName} : {table_classement[i][1]}\n"
                    n += 1

            else:
                for playerTournament in playersTournament:
                    table_classement[i] = [playerTournament.player_id, db.GetPlayerByID(playerTournament.player_id).elo]
                    i += 1
                while i != 0:
                    i = 0
                    for j in range(0, len(table_classement)-1):
                        if table_classement[j+1][1] > table_classement[j][1]:
                            temp = table_classement[j]
                            table_classement[j] = table_classement[j+1]
                            table_classement[j+1] = temp
                            i += 1

                for i in range(0, len(table_classement)):
                    player = db.GetPlayerByID(table_classement[i][0])
                    playersTournamentsMatchID.append(player.id)
                    string1 += f"{n}) {player.firstName} {player.lastName} : {0}\n"
                    n += 1

            labelPlayersTournament = tk.Label(root2, text=string1, justify="left")
            labelPlayersTournament.pack(side="left", padx=(10,50),  anchor="nw")

            if round > n_rounds:
                return 0
            
            playerSolo_id = None
            if len(playersTournamentsMatchID)%2 != 0:
                playerSolo_id = playersTournamentsMatchID[random.randrange(0,len(playersTournamentsMatchID))]
                playersTournamentsMatchID.remove(playerSolo_id) #sauf si déjà en pause  ##################################3

            for i in range(0, len(playersTournamentsMatchID)/2):
                whitePlayer_id = playersTournamentsMatchID[0]
                playersTournamentsMatchID.remove(whitePlayer_id)    #sauf si déjà joué contre ###################################
                blackPlayer_id = playersTournamentsMatchID[1]
                playersTournamentsMatchID.remove(blackPlayer_id)
                #whitePlayer = db.GetPlayerByID(whitePlayer_id)
                #blackPlayer = db.GetPlayerByID(blackPlayer_id)
                db.AddData(Match(tournament_id=tournamentID, white_player_id=whitePlayer_id, black_player_id=blackPlayer_id, round=round))

            string2 = "First matchs :"
            labelPlayersFirstMatch = tk.Label(root2, text=string2, justify="left")
            labelPlayersFirstMatch.pack(side="top", padx=(50,10),  anchor="nw")

            n = 1
            winners = []
            matchsRound = db.GetMatchsByRound(tournamentID, round)
            for match in matchsRound:
                match_frame = tk.Frame(root2)
                match_frame.pack(side="top", padx=(50,10), anchor="nw")

                white_player = db.GetPlayerByID(match.white_player_id)
                black_player = db.GetPlayerByID(match.black_player_id)

                label = tk.Label(match_frame, text=f"\n{str(n)}) {white_player.firstName} {white_player.lastName} vs {black_player.firstName} {black_player.lastName}", justify="left")
                label.grid(row=n, column=0)

                winner_options = [f"{white_player.firstName} {white_player.lastName}", f"{black_player.firstName} {black_player.lastName}", "Draw"]
                winner_var = tk.StringVar(value="None")
                winner_dropdown = ttk.Combobox(match_frame, textvariable=winner_var, values=winner_options)
                winner_dropdown.grid(row=n, column=1)

                winners.append([match.id, winner_var, winner_options])

                n += 1

            if playerSolo_id:
                player = db.GetPlayerByID(playerSolo_id)
                labelPlayerSolo = tk.Label(root2, text=f"\n{str(n)}) No match for {player.firstName} {player.lastName}", justify="left")
                labelPlayerSolo.pack()
            
            button_submit = tk.Button(root2, text="Next match", command=lambda: finishRound(winners))
            button_submit.pack(side="bottom")

            def finishRound(winners):
                for winner in winners:
                    if winner[1].get() == winner[2][0]:
                        playerID = db.GetMatchByID(winner[0]).white_player_id
                        db.AddWinnerToMatch(winner[0], playerID)
                        db.UpgradeScoreFromPlayerTournament(tournament_id=tournamentID, player_id=playerID, increment=1)
                    elif winner[1].get() == winner[2][1]:
                        playerID = db.GetMatchByID(winner[0]).black_player_id
                        db.AddWinnerToMatch(winner[0], playerID)
                        db.UpgradeScoreFromPlayerTournament(tournament_id=tournamentID, player_id=playerID, increment=1)
                    else:
                        playerID = db.GetMatchByID(winner[0]).white_player_id
                        db.UpgradeScoreFromPlayerTournament(tournament_id=tournamentID, player_id=playerID, increment=0.5)
                        playerID = db.GetMatchByID(winner[0]).black_player_id
                        db.UpgradeScoreFromPlayerTournament(tournament_id=tournamentID, player_id=playerID, increment=0.5)
                
                nonlocal round

                round += 1
                startRound(round=round)
            
updateScoreButton = tk.Button(root, text="Mettre à jour le score", command=updateScore)
updateScoreButton.pack()

startTournamentButton = tk.Button(root, text="Lancer un tournoi", command=startTournament)
startTournamentButton.pack()

root.mainloop()
