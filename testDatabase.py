from database import Database, Player, Tournament
from datetime import datetime

db = Database()

db.AddData(Player(firstName='fdashgzswh', lastName='fdsa', school='HEIA-FR', elo=100))
db.AddData(Tournament(name="hfaddfas", date=datetime.now()))
db.AddPlayerIDToTournament(1, 1)

db.UpdateScoreFromPlayerTournament(1,1, 10)

