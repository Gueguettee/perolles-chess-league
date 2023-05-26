import random
import tkinter as tk
from tkinter.messagebox import askyesno
from datetime import datetime
from tkinter import ttk
from telegramAPI import Telegram
import math
import random
import time

from database import Database, Match, Player, PlayersTournaments, Tournament

N_ROUNDS = 3

TIME_BETWEEN_ROUND = 15 #* 60

TOKEN_TOURNAMENT_TELEGRAM = '6189666655:AAGyjZ7dkgqQtobYR3j3AHlIYPwNdeDusR8'
CHAT_ID_TELEGRAM = '1646128337'

te = Telegram(
    token = TOKEN_TOURNAMENT_TELEGRAM,
    chat_id = CHAT_ID_TELEGRAM
    )

db = Database()

root = tk.Tk()
H = 600
L = 1000
root.geometry(f"{L}x{H}")
root.title("Pérolles Chess Tournament")

N_MAX_ROW = math.floor(H/26)
N_MAX_COLUMN = math.floor(L/150)

def addPlayer():
    player = playerEntry.get().strip()
    if player:
        db.AddData(Player(firstName=player, lastName=player, school='HEIA-FR', elo=100))
        menu = playerSelectDrowdown['menu']
        menu.add_command(label=player, command=tk._setit(varPlayerSelect, player))

def updateScore():
    player = varPlayerSelect.get()
    score = score_entry.get()
    if player and score.isdigit():
        db.ModifyScorePlayer(player, int(score))
        score_entry.delete(0, tk.END)

def selection_callback():
    n = 0
    for player in allPlayers:
        if inTournamentVar[player.id].get():
            n += 1
    selected_count.set(n)

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

    def establishmentTournament():
        nonlocal tournamentID
        resumeTournament = False
        if tournamentID == None:
            nameTournament = entryNameTournament.get()
            n_rounds = int(entryNRoundTournament.get())

            if n_rounds < 1:
                n_rounds = N_ROUNDS

            te.PostMessage(f"Bienvenue au premier tournoi d'échecs de Pérolles !")

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
            roundT = round(len(db.GetMatchsByTournamentID(tournamentID)) / math.floor(len(db.GetPlayersTournamentsByTournamentID(tournamentID))/2))
            resumeTournament = True

        nonlocal root2
        root2.destroy()
        root2 = tk.Toplevel(root)
        
        def startRound(round):

            print(round)

            def update_timer():
                nonlocal paused
                nonlocal lastIdMessage
                if not paused:
                    elapsedTime = update_timer.elapsed_time
                    timeRemaining = TIME_BETWEEN_ROUND - elapsedTime
                    minutes = timeRemaining // 60
                    seconds = timeRemaining % 60
                    string = f"Temps restant avant le début de la manche :\n{minutes:02d}:{seconds:02d}"
                    timer_label.config(text=string)
                    if timeRemaining <= 5:
                        lastIdMessage = te.EditMessageId(string, lastIdMessage)
                        if timeRemaining > 0:
                            string = f"{seconds}"
                            after_id = root2.after(1000, update_timer)  # Update every second (1000 milliseconds)
                        else:
                            string = "Lancez les clocks et bon match !"
                        te.PostMessage(string)
                    else:
                        if update_timer.elapsed_time == 0:
                            lastIdMessage = te.PostMessage(string)
                        else:
                            lastIdMessage = te.EditMessageId(string, lastIdMessage)
                        after_id = root2.after(1000, update_timer)  # Update every second (1000 milliseconds)
                    update_timer.elapsed_time = elapsedTime + 1
                else:
                    after_id = root2.after(1000, update_timer)  # Update every second (1000 milliseconds)
            
            update_timer.elapsed_time = 0
            paused = False
            lastIdMessage = None

            nonlocal root2
            if round == 1:
                string1 = "Joueurs :\n\n"
            else:
                root2.destroy()
                root2 = tk.Toplevel(root)
                if round <= n_rounds:
                    string1 = "Classement actuel :\n\n"
                else:
                    # Finish Tournament
                    string1 = "Classement Final :\n\n"

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
            nonlocal resumeTournament
            if not resumeTournament:
                if len(playersTournamentsMatchID)%2 != 0:
                    playerSolo_id = playersTournamentsMatchID[random.randrange(0,len(playersTournamentsMatchID))]
                    playersTournamentsMatchID.remove(playerSolo_id)

                matchsTournament = db.GetMatchsByTournamentID(tournamentID)
                for i in range(0, int(len(playersTournamentsMatchID)/2)):
                    whitePlayer_id = playersTournamentsMatchID[0]
                    playersTournamentsMatchID.remove(whitePlayer_id)
                    for ii in range(0, len(playersTournamentsMatchID)):
                        blackPlayer_id = playersTournamentsMatchID[ii]
                        n = 0
                        for match in matchsTournament:
                            if((match.white_player_id == whitePlayer_id and match.black_player_id == blackPlayer_id) 
                            or (match.white_player_id == blackPlayer_id and match.black_player_id == whitePlayer_id)):
                                n += 1
                                break
                        if n == 0:
                            break
                    if n != 0:  # if déjà toute façon joué ensemble, inverse white black
                        n = {ii : 0 for ii in range(0,  len(playersTournamentsMatchID))}
                        for ii in range(0, len(playersTournamentsMatchID)):
                            blackPlayer_id = playersTournamentsMatchID[ii]
                            for match in matchsTournament:
                                if((match.white_player_id == whitePlayer_id and match.black_player_id == blackPlayer_id) 
                                or (match.white_player_id == blackPlayer_id and match.black_player_id == whitePlayer_id)):
                                    n[ii] += 1
                        pos = 0
                        min = n[0]
                        for ii in range(1, len(playersTournamentsMatchID)):
                            if n[ii] < min:
                                min = n[ii]
                                pos = ii
                        blackPlayer_id = playersTournamentsMatchID[pos]
                        playersTournamentsMatchID.remove(blackPlayer_id)
                        if min%2 == 0:
                            matchsTournament = matchsTournament[::-1]
                        for match in matchsTournament:
                            if ((match.white_player_id == whitePlayer_id and match.black_player_id == blackPlayer_id) 
                            or (match.white_player_id == blackPlayer_id and match.black_player_id == whitePlayer_id)):
                                if match.white_player_id == whitePlayer_id:
                                    whitePlayer_id = blackPlayer_id
                                    blackPlayer_id = match.white_player_id
                                break
                    else:
                        playersTournamentsMatchID.remove(blackPlayer_id)
                        # random white black player
                        random_number = random.randint(0, 1)
                        if random_number != 0:
                            temp = whitePlayer_id
                            whitePlayer_id = blackPlayer_id
                            blackPlayer_id = temp
                    #whitePlayer = db.GetPlayerByID(whitePlayer_id)
                    #blackPlayer = db.GetPlayerByID(blackPlayer_id)
                    db.AddData(Match(tournament_id=tournamentID, white_player_id=whitePlayer_id, black_player_id=blackPlayer_id, round=round))

            else:
                resumeTournament = False
                if len(playersTournamentsMatchID)%2 != 0:
                    matchsRound = db.GetMatchsByRound(tournamentID, round)
                    for match in matchsRound:
                        playersTournamentsMatchID.remove(match.white_player_id)
                        playersTournamentsMatchID.remove(match.black_player_id)
                    playerSolo_id = playersTournamentsMatchID[0]

            if round==1:
                string2 = "Premiers matchs\n"
            else:
                string2 = "Prochains matchs\n"
            string2 += ("Le numéro correspond à la table,\nLe premier joueur prend les blancs,\nLe second prend les noirs :\n")
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
                string = f"\n{str(n)}) Pas de match pour {player.firstName} {player.lastName}"
                string2 += string
                labelPlayerSolo = tk.Label(root2, text=string, justify="left")
                labelPlayerSolo.pack()

            def show_confirmation():
                confirm = askyesno("Confirmation", "Voulez-vous vraiment afficher les prochains matchs ?")
                if confirm:
                    finishRound(winners)
            
            if round == n_rounds:
                string = "Classement Final"
            else:
                string = "Prochains matchs"
            button_submit = tk.Button(root2, text=string, command=show_confirmation)
            button_submit.pack(side="bottom")

            te.PostMessage(string2)

            def toggle_pause():
                nonlocal paused
                if paused:
                    paused = False
                else:
                    paused = True
                pause_button.config(text="Relancer le timer" if paused else "Stopper le timer")

            pause_button = tk.Button(root2, text="Stopper le temps", command=toggle_pause)
            pause_button.pack(side="bottom")

            timer_label = tk.Label(root2, text="")
            timer_label.pack(side="bottom")

            update_timer()

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

column = 0
elementsColumn = {c: [] for c in range(0, N_MAX_COLUMN)}

varPlayerSelect = tk.StringVar()
varPlayerSelect.set("Sélectionner un player")

labelPlayer = tk.Label(root, text="Nom du joueur :")
elementsColumn[column].append(labelPlayer)

playerEntry = tk.Entry(root)
elementsColumn[column].append(playerEntry)

addPlayerButton = tk.Button(root, text="Ajouter un joueur", command=addPlayer)
elementsColumn[column].append(addPlayerButton)

players = [f"{j.firstName} {j.lastName}" for j in db.ReadAllData(Player)]
if players:
    playerSelectDrowdown = tk.OptionMenu(root, varPlayerSelect, *players, command=varPlayerSelect.set)
    elementsColumn[column].append(playerSelectDrowdown)
            
updateScoreButton = tk.Button(root, text="Mettre à jour le score", command=updateScore)
elementsColumn[column].append(updateScoreButton)

startTournamentButton = tk.Button(root, text="Lancer un tournoi", command=startTournament)
elementsColumn[column].append(startTournamentButton)

resumeTournamentButton = tk.Button(root, text="Reprendre un tournoi", command=lambda: startTournament(1))
elementsColumn[column].append(resumeTournamentButton)

score_label = tk.Label(root, text="Score à ajouter :")
elementsColumn[column].append(score_label)

score_entry = tk.Entry(root)
elementsColumn[column].append(score_entry)

column += 1

allPlayers = db.GetAll(Player)
inTournamentVar = {player.id: tk.BooleanVar(value=False) for player in allPlayers}

selected_count = tk.IntVar(value=0)

for player in allPlayers:
    playerVar = tk.StringVar()
    playerVar.set(f"{player.firstName} {player.lastName}")
    buttonPlayerIn = tk.Checkbutton(root, textvariable=playerVar, variable=inTournamentVar[player.id], command=selection_callback)
    elementsColumn[column].append(buttonPlayerIn)

selected_label = tk.Label(root, text="Nombre actuel : ", textvariable=selected_count)
elementsColumn[column].append(selected_label)

supColumn = 0
for c in elementsColumn:
    row = 0
    for element in elementsColumn[c]:
        element.grid(row=row, column=c+supColumn)
        row += 1
        if row >= N_MAX_ROW:
            row = 0
            supColumn += 1

root.mainloop()
