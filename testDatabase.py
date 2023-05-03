from database import Database, Player, Tournament, PlayersTournaments
from datetime import datetime

db = Database()

db.AddData(Player(firstName='fdsa', lastName='fdsa', school='HEIA-FR', elo=100))
db.AddData(Tournament(name="test", date=datetime.now()))

db.AddData(PlayersTournaments(player_id=2,tournament_id=1))
