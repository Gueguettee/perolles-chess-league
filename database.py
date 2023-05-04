from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine, select, exists, Enum, ForeignKey, Table
from sqlalchemy.orm import Session, declarative_base, relationship, sessionmaker, object_session
from datetime import datetime


Base = declarative_base()


class PlayersTournaments(Base):
    __tablename__ = "players_tournaments_table"
    player_id = Column(ForeignKey("players_table.id"), primary_key=True)
    tournament_id = Column(ForeignKey("tournaments_table.id"), primary_key=True)
    # association between Assocation -> Child
    players_ass = relationship("Player", back_populates="tournaments_associations")
    # association between Assocation -> Parent
    tournaments_ass = relationship("Tournament", back_populates="players_associations")
    #extra_data:
    score = Column(Integer, default=0)

class Player(Base):
    __tablename__ = 'players_table'
    id = Column(Integer, nullable=False, primary_key=True)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    school = school = Column(Enum('HEIA-FR', 'UNI-FR', 'Autre'))
    elo = Column(Integer, default=0)
    tournaments = relationship("Tournament", secondary="players_tournaments_table", back_populates="players", viewonly=True)
    tournaments_associations = relationship("PlayersTournaments", back_populates="players_ass")
    matches = relationship("Match", primaryjoin="or_(Player.id == Match.white_player_id, Player.id == Match.black_player_id)", viewonly=True)

class Tournament(Base):
    __tablename__ = 'tournaments_table'
    id = Column(Integer,nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    matchs = relationship("Match", back_populates="tournament")
    players = relationship("Player", secondary="players_tournaments_table", back_populates="tournaments", overlaps="players_ass,tournaments_associations,tournaments_ass")
    players_associations = relationship("PlayersTournaments", back_populates="tournaments_ass", overlaps="players")

class Match(Base):
    __tablename__ = 'matchs_table'
    id = Column(Integer, primary_key=True)
    white_player_id = Column(Integer, ForeignKey('players_table.id'), nullable=False)
    black_player_id = Column(Integer, ForeignKey('players_table.id'), nullable=False)
    tournament_id = Column(Integer, ForeignKey('tournaments_table.id'), nullable=False)
    tournament = relationship("Tournament", back_populates="matchs")
    winner_id = Column(Integer, ForeignKey('players_table.id'))
    winner = relationship("Player", foreign_keys=[winner_id])
    white_player = relationship("Player", foreign_keys=[white_player_id])
    black_player = relationship("Player", foreign_keys=[black_player_id])


class Database():
        
    def __init__(self, nameOfDatabase="db"):
        self.engine = create_engine(f"sqlite:///{nameOfDatabase}.sqlite", echo=False)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def CreateDatabase(self):
        Base.metadata.create_all(self.engine)
        
    def AddData(self, data):
        with self.Session() as session:
            session.add(data)
            session.commit()
            id = data.id
        return id

    def AddDataList(self, dataList: list):
        with self.Session() as session:
            session.add_all(dataList)
            session.commit()

    def AddPlayerID2ToTournament(self, tournament_id, player_id):
        with self.Session() as session:
            tournament = session.query(Tournament).get(tournament_id)
            if not(tournament):
                tournament = Tournament("error", tournament_id)
                session.add(tournament)
            player = self.ReadPlayer_byID(player_id)
            tournament.players.append(player)
            session.commit()

    def AddPlayerIDToTournament(self, tournament_id, player_id):
        with self.Session() as session:
            tournament = session.query(Tournament).get(tournament_id)
            player = session.query(Player).get(player_id)
            tournament.players.append(player)
            session.commit()

    def ReadAllData(self, column):
        session = self.Session()
        data = session.query(column).all()
        return data

    def ReadData_bySelection(self, selection):
        session = self.Session()
        data = session.scalars(selection).one()
        session.close()
        return data

    def ReadDataList_bySelection(self, selection):
        session = self.Session()
        dataList = []
        for data in session.scalars(selection):
            dataList.append(data)
        return dataList

    def ReadTournament_byDate(self, date: datetime):
        return self.ReadData_bySelection(select(self.Balance).where(self.Balance.date == date))

    def ReadTournament_byID(self, id: int):
        return self.ReadData_bySelection(select(Tournament).where(Tournament.id == id))

    def ReadTournamentPlayers_byID(self, id: int):
        return self.ReadData_bySelection(select(Player).where(Player.tournaments_associations == id))
    
    def GetAllPlayers(self):
        with self.Session() as session:
            return session.query(Player).all()
    
    def GetPlayersByTournamentID(self, tournament_id):
        with self.Session() as session:
            tournament = session.query(Tournament).filter_by(id=tournament_id).first()
            if tournament:
                return tournament.players
            else:
                return []
    
    def UpdateScoreFromPlayerTournament(self, tournament_id, player_id, score):
        with self.Session() as session:   
            player_tournament = session.query(PlayersTournaments).filter_by(player_id=player_id, tournament_id=tournament_id).first()
            player_tournament.score = score
            session.commit()

    
    def ReadPlayer_byID(self, id: int):
        return self.ReadData_bySelection(select(Player).where(Player.id == id))
    
    def TestIfTradeExist(self, id: int):
        session = self.Session()
        b = session.query(exists().where(self.Trade.id == id)).scalar()
        return b
    
    def ModifyScorePlayer(self, firstName: str, elo: int):
        session = self.Session()
        trade = session.query(Player).filter_by(firstName=firstName).first()
        trade.elo = elo
        session.commit()

if __name__ == "__main__":
    db=Database()
    db.CreateDatabase()
