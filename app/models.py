from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base
from typing import Optional
from pydantic import BaseModel
from typing import Optional, Dict


class Sport(Base):
    __tablename__ = 'sports'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    tournament_types = relationship("TournamentType", back_populates="sport")

class TournamentType(Base):
    __tablename__ = 'tournament_types'
    id = Column(Integer, primary_key=True, index=True)
    sport_id = Column(Integer, ForeignKey("sports.id"), nullable=False)
    gender = Column(String(10), nullable=False)  # Men, Women, Mixed
    format = Column(String(50), nullable=False)  # e.g., T20, ODI, etc.
    sport = relationship("Sport", back_populates="tournament_types")
    tournaments = relationship("Tournament", back_populates="tournament_type")


class Tournament(Base):
    __tablename__ = 'tournaments'
    id = Column(Integer, primary_key=True, index=True)
    tournament_id = Column(String(50), nullable=False)
    tournament_type_id = Column(Integer, ForeignKey("tournament_types.id"), nullable=False)
    host = Column(String(50))
    venue = Column(String(100))
    winner = Column(String(50))
    runner_up = Column(String(50))
    player_of_the_match = Column(String(100))
    tournament_type = relationship("TournamentType", back_populates="tournaments")
    stats = relationship("Stat", back_populates="tournament")
    
    # Composite unique constraint
    __table_args__ = (UniqueConstraint('tournament_id', 'tournament_type_id', name='uq_tournament_id_type'),)


class Stat(Base):
    __tablename__ = 'stats'
    id = Column(Integer, primary_key=True, index=True)
    tournament_id = Column(Integer, ForeignKey("tournaments.id"), nullable=False)
    key = Column(String(50), nullable=False)  # goals_scored, runs_scored
    value = Column(String(100), nullable=False)
    tournament = relationship("Tournament", back_populates="stats")


# Schema definitions
class StatsSchema(BaseModel):
    runs: Optional[int] = None
    goals: Optional[int] = None
    points: Optional[int] = None

class TournamentSchema(BaseModel):
    sport_id: int
    sport_name: Optional[str] = None
    tournament_id: str
    format: str
    host: str
    venue: str
    winner: str
    runner_up: str
    player_of_the_match: str
    stats: Optional[Dict[str, int]] = None