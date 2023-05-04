"""players_tournaments = Table(
    "players_tournaments_table",
    Base.metadata,
    Column("players_id", ForeignKey("players_table.id"), primary_key=True),
    Column("tournaments_table_id", ForeignKey("tournaments_table.id"), primary_key=True),
)

class Player(Base):
    __tablename__ = 'players_table'
    id = Column(Integer, primary_key=True)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    school = school = Column(Enum('HEIA-FR', 'UNI-FR', 'Autre'))
    elo = Column(Integer, default=0)
    #matchs = relationship('Match', backref='players', foreign_keys="[Match.whitePlayer_id, Match.blackPlayer_id]")
    #tournaments = relationship('Player', secondary='players_tournament', backref='tournaments_of_player')

    tournaments = relationship("Tournament", secondary=players_tournaments, back_populates="players")

class Tournament(Base):
    __tablename__ = 'tournaments_table'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    #idForPlayers = relationship("Tournament", secondary='players_tournament', backref='tournament_of_players')
    #matchs = relationship("Match", secondary='matchs_tournament', backref='tournament_of_matchs')

    matchs = relationship("Match", back_populates="tournament")
    players = relationship("Player", secondary=players_tournaments, back_populates="tournaments")

class Match(Base):
    __tablename__ = 'matchs_table'
    id = Column(Integer, primary_key=True)
    #whitePlayer_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    #blackPlayer_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    #tournament = relationship("Tournament", secondary='matchs_tournament', backref='matchs_of_tournament')

    tournament_id = Column(Integer, ForeignKey('tournaments_table.id'))
    tournament = relationship("Tournament", back_populates="matchs")"""