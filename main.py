import random
import tkinter as tk
from datetime import datetime
from tkinter import ttk
from telegramAPI import Telegram

from database import Database, Match, Player, PlayersTournaments, Tournament

N_ROUNDS = 3
TOKEN_TOURNAMENT_TELEGRAM = '6189666655:AAGyjZ7dkgqQtobYR3j3AHlIYPwNdeDusR8'
CHAT_ID_TELEGRAM = '1646128337'

te = Telegram(
    token = TOKEN_TOURNAMENT_TELEGRAM,
    chat_id = CHAT_ID_TELEGRAM
    )

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


allPlayers = db.GetAll(Player)
inTournamentVar = {player.id: tk.BooleanVar(value=False) for player in allPlayers}

selected_count = tk.IntVar(value=0)
def selection_callback():
    n = 0
    for player in allPlayers:
        if inTournamentVar[player.id].get():
            n += 1
    selected_count.set(n)

for player in allPlayers:
    playerVar = tk.StringVar()
    playerVar.set(f"{player.firstName} {player.lastName}")
    buttonPlayerIn = tk.Checkbutton(root, textvariable = playerVar, variable=inTournamentVar[player.id], command=selection_callback).pack(anchor = tk.W)
    #buttonPlayerIn.pack()

selected_label = tk.Label(root, text="Nombre actuel : ", textvariable=selected_count).pack(anchor = tk.W)

def startTournament(tournamentID = None):
    root2 = tk.Toplevel(root)
    if tournamentID == None:
        labelNameTournament = tk.Label(root2, text="Nom du tournoi :")
        labelNameTournament.pack()
        entryNameTournament = tk.Entry(root2)
        entryNameTournament.pack()

        labelNRoundTournament = tk.Label(root2, text="\n\nNombre de rounds :")
        labelNRoundTournament.pack()
        entryNRoundTournament = tk.Entry(root2)
        entryNRoundTournament.bind('<Return>', lambda event: establishmentTournament())
        entryNRoundTournament.pack()
    else:
        labelIdTournament = tk.Label(root2, text="ID du tournoi :")
        labelIdTournament.pack()
        entryIdTournament = tk.Entry(root2)
        entryIdTournament.bind('<Return>', lambda event: establishmentTournament())
        entryIdTournament.pack()

    """labelNRoundTournament = tk.Label(root2, text="\n\nNombre de rounds :")
    labelNRoundTournament.pack()
    entryNRoundTournament = tk.Entry(root2)
    entryNRoundTournament.bind('<Return>', lambda event: establishmentTournament())
    entryNRoundTournament.pack()"""

    def establishmentTournament():
        nonlocal tournamentID
        resumeTournament = False
        if tournamentID == None:
            nameTournament = entryNameTournament.get()
            n_rounds = int(entryNRoundTournament.get())

            if n_rounds < 1:
                n_rounds = N_ROUNDS

            tournament = Tournament(name=nameTournament, nRounds=n_rounds, date=datetime.now())
            tournamentID = db.AddData(data=tournament)

            players = db.GetAll(Player)
            for player in players:
                if inTournamentVar[player.id].get():
                    db.AddPlayerIDToTournament(tournament_id=tournamentID, player_id=player.id)

            roundT = 1

        else:
            tournamentID = entryIdTournament.get()
            tournament = db.GetTournament(id = tournamentID)
            n_rounds = tournament.nRounds
            roundT = round(len(db.GetMatchsByTournamentID(tournamentID)) / len(db.GetPlayersTournamentsByTournamentID(tournamentID)))
            print(roundT)
            resumeTournament = True

        nonlocal root2
        root2.destroy()
        root2 = tk.Toplevel(root)
        
        def startRound(round):

            nonlocal root2
            if round == 1:
                string1 = "Players :\n\n"
            else:
                root2.destroy()
                root2 = tk.Toplevel(root)
                if round <= n_rounds:
                    string1 = "Current ranking :\n\n"
                else:
                    string1 = "Final ranking :\n\n"

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
                    n_sous = 0
                    if i != 0:
                        ok = False
                        for i2 in range(0, i):
                            if table_classement[i][1] == table_classement[i-i2-1][1]:
                                n_sous += 1
                            else:
                                break
                    string1 += f"{n-n_sous}) {player.firstName} {player.lastName} : {table_classement[i][1]}\n"
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

            te.PostMessage(string1)

            labelPlayersTournament = tk.Label(root2, text=string1, justify="left")
            labelPlayersTournament.pack(side="left", padx=(10,50),  anchor="nw")

            if round > n_rounds:
                return 0
            
            playerSolo_id = None
            if len(playersTournamentsMatchID)%2 != 0:
                playerSolo_id = playersTournamentsMatchID[random.randrange(0,len(playersTournamentsMatchID))]
                playersTournamentsMatchID.remove(playerSolo_id)

            nonlocal resumeTournament
            if not resumeTournament:
                matchsTournament = db.GetMatchsByTournamentID(tournamentID)
                for i in range(0, int(len(playersTournamentsMatchID)/2)):
                    whitePlayer_id = playersTournamentsMatchID[0]
                    playersTournamentsMatchID.remove(whitePlayer_id)
                    print("w"+str(whitePlayer_id))
                    ok = False
                    for i in range(0, len(playersTournamentsMatchID)):
                        blackPlayer_id = playersTournamentsMatchID[i]
                        print("b" + str(blackPlayer_id))
                        ok = True
                        for match in matchsTournament:
                            if((match.white_player_id == whitePlayer_id and match.black_player_id == blackPlayer_id) 
                            or (match.white_player_id == blackPlayer_id and match.black_player_id == whitePlayer_id)):
                                ok = False
                                break
                        if ok:
                            break
                    print(ok)
                    if not ok:
                        blackPlayer_id = playersTournamentsMatchID[0]
                        for match in matchsTournament:
                            if ((match.white_player_id == whitePlayer_id and match.black_player_id == blackPlayer_id) 
                            or (match.white_player_id == blackPlayer_id and match.black_player_id == whitePlayer_id)):
                                if match.white_player_id == whitePlayer_id:
                                    whitePlayer_id = blackPlayer_id
                                    blackPlayer_id = match.white_player_id
                                break
                        playersTournamentsMatchID.remove(whitePlayer_id)
                    else:
                        playersTournamentsMatchID.remove(blackPlayer_id)
                    #whitePlayer = db.GetPlayerByID(whitePlayer_id)
                    #blackPlayer = db.GetPlayerByID(blackPlayer_id)
                    db.AddData(Match(tournament_id=tournamentID, white_player_id=whitePlayer_id, black_player_id=blackPlayer_id, round=round))

            if round==1:
                string2 = "First matchs :\n"
            else:
                string2 = "Next matchs :\n"
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

                string = f"\n{str(n)}) {white_player.firstName} {white_player.lastName} vs {black_player.firstName} {black_player.lastName}"
                string2 += string
                label = tk.Label(match_frame, text=string, justify="left")
                label.grid(row=n, column=0)

                winner_options = [f"{white_player.firstName} {white_player.lastName}", f"{black_player.firstName} {black_player.lastName}", "Draw"]
                winner_var = tk.StringVar(value="None")
                winner_dropdown = ttk.Combobox(match_frame, textvariable=winner_var, values=winner_options)
                winner_dropdown.grid(row=n, column=1)

                winners.append([match.id, winner_var, winner_options])

                n += 1

            if playerSolo_id:
                player = db.GetPlayerByID(playerSolo_id)
                string = f"\n{str(n)}) No match for {player.firstName} {player.lastName}"
                string2 += string
                labelPlayerSolo = tk.Label(root2, text=string, justify="left")
                labelPlayerSolo.pack()
            
            if round == n_rounds:
                string = "Final ranking"
            else:
                string = "Next match"
            button_submit = tk.Button(root2, text=string, command=lambda: finishRound(winners))
            button_submit.pack(side="bottom")

            te.PostMessage(string2)

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

        startRound(roundT)
            
updateScoreButton = tk.Button(root, text="Mettre à jour le score", command=updateScore)
updateScoreButton.pack()

startTournamentButton = tk.Button(root, text="Lancer un tournoi", command=startTournament)
startTournamentButton.pack()


resumeTournamentButton = tk.Button(root, text="Resume Tournament", command=lambda: startTournament(1))
resumeTournamentButton.pack()

root.mainloop()
