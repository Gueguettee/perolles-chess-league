from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine, select, exists, Enum, ForeignKey, Table
from sqlalchemy.orm import Session, declarative_base, relationship, sessionmaker
from datetime import datetime


Base = declarative_base()

class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    school = school = Column(Enum('HEIA-FR', 'UNI-FR', 'Autre'))
    elo = Column(Integer, default=0)
    #matchs = relationship('Match', backref='players', foreign_keys="[Match.whitePlayer_id, Match.blackPlayer_id]")
    tournaments = relationship('Player', secondary='players_tournament', backref='tournaments_of_player')

class Tournament(Base):
    __tablename__ = 'tournaments'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    idForPlayers = relationship("Tournament", secondary='players_tournament', backref='tournament_of_players')
    #matchs = relationship("Match", secondary='matchs_tournament', backref='tournament_of_matchs')

"""class Match(Base):
    __tablename__ = 'matchs'
    id = Column(Integer, primary_key=True)
    whitePlayer_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    blackPlayer_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    tournament = relationship("Tournament", secondary='matchs_tournament', backref='matchs_of_tournament')"""

class PlayersTournaments(Base):
    __tablename__ = 'players_tournament'
    player_id = Column('player_id', Integer, ForeignKey('players.id'), primary_key=True)
    tournament_id = Column('tournament_id', Integer, ForeignKey('tournaments.id'), primary_key=False)

"""class MatchsTournaments(Base):
    __tablename__ = 'matchs_tournament'
    match_id = Column('match_id', Integer, ForeignKey('matchs_of_tournament.id'), primary_key=True)
    tournament_id = Column('tournament_id', Integer, ForeignKey('tournament_of_matchs.id'), primary_key=True)"""


class Database():
        
    def __init__(self, nameOfDatabase="db"):
        self.engine = create_engine(f"sqlite:///{nameOfDatabase}.sqlite", echo=False)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def CreateDatabase(self):
        Base.metadata.create_all(self.engine)
        
    def AddData(self, data):
        session = self.Session()
        session.add(data)
        session.commit()

    def AddDataList(self, dataList: list):
        session = self.Session()
        session.add_all(dataList)
        session.commit()

    def ReadAllData(self, column):
        session = self.Session()
        data = session.query(column).all()
        return data

    def ReadData_bySelection(self, selection):
        session = self.Session()
        data = session.scalars(selection).one()
        return data

    def ReadDataList_bySelection(self, selection):
        session = self.Session()
        dataList = []
        for data in session.scalars(selection):
            dataList.append(data)
        return dataList

    def ReadBalance_byDate(self, date: datetime):
        return Database.ReadData_bySelection(select(self.Balance).where(self.Balance.date == date))

    def ReadTrade_byID(self, id: int):
        return Database.ReadData_bySelection(select(self.Trade).where(self.Trade.id == id))

    def ReadTrade_byIDs(self, ids: list[int]):
        return Database.ReadDataList_bySelection(select(self.Trade).where(self.Trade.id.in_(ids)))
    
    def TestIfTradeExist(self, id: int):
        session = self.Session()
        b = session.query(exists().where(self.Trade.id == id)).scalar()
        return b
    
    def ModifyScorePlayer(self, firstName: str, elo: int):
        session = self.Session()
        trade = session.query(Player).filter_by(firstName=firstName).first()
        trade.elo = elo
        session.commit()

    """def readData_relationship(self):
        with Session(self.engine) as session:

            stmt = (
                select(Address)
                .join(Address.user)
                .where(User.name == "sandy")
                .where(Address.email_address == "sandy@sqlalchemy.org")
            )
            sandy_address = session.scalars(stmt).one()"""

    """def changeData(self, selection):
        with Session(self.engine) as session:
            patrick = session.scalars(stmt).one()
            patrick.addresses.append(Address(email_address="patrickstar@sqlalchemy.org"))
            sandy_address.email_address = "sandy_cheeks@sqlalchemy.org"
            session.commit()"""

if __name__ == "__main__":
    db=Database()
    db.CreateDatabase()
