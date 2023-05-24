import csv
from database import Database, Player

db = Database()

with open('players.csv', 'r', encoding='latin-1') as file:
    reader = csv.reader(file)
    headers = next(reader)
    players = [row for row in reader]

print(headers)
print(players)

for player in players:

    player_data = player[0].split(';')
    date_time = player_data[0]
    email = player_data[1]
    lastName = player_data[2]
    firstName = player_data[3]
    school = player_data[4]
    elo = player_data[5]
    if not elo:
        elo = 0

    player = Player(firstName=firstName, lastName=lastName, school=school, elo=elo)
    db.AddData(player)
