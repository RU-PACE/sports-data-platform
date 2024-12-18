# from sqlalchemy.orm import Session
# from sqlalchemy.exc import NoResultFound
# from models import Sport, Tournament, Stat
# from typing import Optional

# def create_sport(db: Session, name: str):
#     sport = Sport(name=name)
#     db.add(sport)
#     db.commit()
#     return sport

# def create_tournament(db: Session, data: dict):
#     tournament = Tournament(**data)
#     db.add(tournament)
#     db.commit()
#     return tournament

# def upsert_tournament(db: Session, data: dict):
#     """
#     Update an existing tournament if it exists, otherwise create a new one.
#     """
#     existing_tournament = db.query(Tournament).filter_by(tournament_id=data["tournament_id"]).first()
#     if existing_tournament:
#         for key, value in data.items():
#             setattr(existing_tournament, key, value)
#         db.commit()
#     else:
#         create_tournament(db, data)

# def add_stat(db: Session, data: dict):
#     stat = Stats(**data)
#     db.add(stat)
#     db.commit()
#     return stat

# def query_stats(db: Session, tournament_id: str, sport_id: Optional[int] = None, format: Optional[str] = None):
#     """
#     Query stats with filtering options.
#     """
#     # query = db.query(Stats).join(Tournament).filter(Tournament.id == tournament_id)

#     query = db.query(Stats).join(Tournament).join(Sport)

#     # Filter by required tournament_id
#     query = query.filter(Tournament.tournament_id == tournament_id)

#     if sport_id:
#         query = query.filter(Tournament.sport_id == sport_id)
#     if format:
#         query = query.filter(Tournament.format == format)
#     return query.all()

# def delete_record(db: Session, tournament_id: int):
#     """
#     Delete a record by tournament_id.
#     """
#     record = db.query(Tournament).filter_by(tournament_id=tournament_id).first()
#     if record:
#         db.delete(record)
#         db.commit()
#         return True
#     return False


# def query_s(db: Session, tournament_id: str, sport_id: Optional[int], format: Optional[str]):
#     """
#     Fetch stats with details from related tables: Sport, Tournament, and Stats.
#     """
#     # Base query joining Stats, Tournament, and Sport tables
#     query = (
#         db.query(
#             Sport.name.label("sport"), 
#             Tournament.tournament_id, 
#             Tournament.format, 
#             Tournament.host, 
#             Tournament.venue, 
#             Tournament.winner, 
#             Tournament.runner_up, 
#             Tournament.player_of_the_match, 
#             Stats.key, 
#             Stats.value
#         )
#         .join(Tournament, Tournament.id == Stats.tournament_id)
#         .join(Sport, Sport.id == Tournament.sport_id)
#     )

#     # Required filter: tournament_id
#     query = query.filter(Tournament.tournament_id == tournament_id)

#     # Optional filters: sport_id and format
#     if sport_id:
#         query = query.filter(Tournament.sport_id == sport_id)
#     if format:
#         query = query.filter(Tournament.format == format)

#     return query.all()

