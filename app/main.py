from fastapi import FastAPI, Depends, UploadFile, HTTPException ,File ,Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from sqlalchemy.exc import IntegrityError
from typing import Optional
from enum import Enum
from sqlalchemy import and_
import csv
from database import SessionLocal, engine ,Base
from models import Sport, TournamentType, Tournament, Stat
from schemas import SportEnum , GenderEnum , FormatEnum
# from crud import create_sport, create_tournament, add_stat, query_stats, upsert_tournament, delete_record , query_s
from utils import parse_csv

# Initialize FastAPI app
Base.metadata.create_all(bind=engine)
app = FastAPI()

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/upload_csv/")
def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload CSV data into the database, ensuring relationships and handling composite unique constraints.
    """
    try:
        content = file.file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(content)

        for row in reader:
            # Insert or fetch Sport
            sport = db.query(Sport).filter(Sport.name == row['sport']).first()
            if not sport:
                sport = Sport(name=row['sport'])
                db.add(sport)
                db.commit()
                db.refresh(sport)

            # Insert or fetch TournamentType
            tournament_type = db.query(TournamentType).filter(
                TournamentType.sport_id == sport.id,
                TournamentType.gender == row['gender'],
                TournamentType.format == row['format']
            ).first()
            if not tournament_type:
                tournament_type = TournamentType(
                    sport_id=sport.id,
                    gender=row['gender'],
                    format=row['format']
                )
                db.add(tournament_type)
                db.commit()
                db.refresh(tournament_type)

            # Insert or fetch Tournament
            tournament = db.query(Tournament).filter(
                Tournament.tournament_id == row['tournament_id'],
                Tournament.tournament_type_id == tournament_type.id
            ).first()
            if not tournament:
                tournament = Tournament(
                    tournament_id=row['tournament_id'],
                    tournament_type_id=tournament_type.id,
                    host=row['host'],
                    venue=row['venue'],
                    winner=row['winner'],
                    runner_up=row['runner_up'],
                    player_of_the_match=row['player_of_the_match']
                )
                db.add(tournament)
                db.commit()
                db.refresh(tournament)

            # Insert or update Stats
            for key in ['runs', 'goals', 'points']:
                if key in row and row[key]:  # Only process non-null stats
                    stat = db.query(Stat).filter(
                        Stat.tournament_id == tournament.id,
                        Stat.key == key
                    ).first()
                    if not stat:
                        stat = Stat(
                            tournament_id=tournament.id,
                            key=key,
                            value=row[key]
                        )
                        db.add(stat)
                    else:
                        stat.value = row[key]  # Update the value if the stat already exists
            db.commit()

        return {"message": "CSV data uploaded successfully"}
    except Exception as e:
        db.rollback()
        return {"error": f"An error occurred: {str(e)}"}
    

@app.get("/tournaments/")
def get_tournament_details(
    tournament_id: str,
    sport: Optional[SportEnum] = Query(None, description="Filter by sport"),
    gender: Optional[GenderEnum] = Query(None, description="Filter by gender"),
    format: Optional[FormatEnum] = Query(None, description="Filter by format"),
    db: Session = Depends(get_db)
):
    """
    API to fetch tournament details by tournament_id, with optional filters for sport, gender, and format.
    """
    try:
        # Fetch the base query with `tournament_id`
        query = (
            db.query(Tournament)
            .join(TournamentType)
            .join(Sport)
            .filter(Tournament.tournament_id == tournament_id)
        )

        # Apply filters based on input
        if sport:
            query = query.filter(Sport.name == sport.value)
        if gender:
            query = query.filter(TournamentType.gender == gender.value)
        if format:
            query = query.filter(TournamentType.format == format.value)

        # Fetch results
        results = query.all()

        if not results:
            raise HTTPException(status_code=404, detail="No tournaments found for the given criteria")

        # Build response
        response = []
        for tournament in results:
            response.append({
                "tournament_id": tournament.tournament_id,
                "sport": tournament.tournament_type.sport.name,
                "gender": tournament.tournament_type.gender,
                "format": tournament.tournament_type.format,
                "host": tournament.host,
                "venue": tournament.venue,
                "winner": tournament.winner,
                "runner_up": tournament.runner_up,
                "player_of_the_match": tournament.player_of_the_match,
                "stats": [{"key": stat.key, "value": stat.value} for stat in tournament.stats]
            })

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    

# Define a Pydantic schema for input validation
class UpsertRecord(BaseModel):
    sport_name: str = Field(..., example="Football")
    gender: str = Field(..., example="Men")  # e.g., 'Men', 'Women', 'Mixed'
    format: str = Field(..., example="WorldCup")  # e.g., 'T20', 'ODI', 'WorldCup'
    tournament_id: str = Field(..., example="worldcup-2022")  # Unique ID for the tournament
    host: str = Field(..., example="Qatar")
    venue: str = Field(..., example="Lusail Stadium")
    winner: str = Field(..., example="Argentina")
    runner_up: str = Field(..., example="France")
    player_of_the_match: str = Field(..., example="Lionel Messi")
    stats: dict = Field(
        default={}, 
        example={"goals_scored": "35", "runs_scored": None, "points": None}
    )  # Dictionary of key-value stats

@app.post("/upsert_record/")
def upsert_record(record: UpsertRecord, db: Session = Depends(get_db)):
    """
    Upsert logic for adding or updating records in the database.
    Handles sports, tournament types, tournaments, and stats.
    """
    try:
        # Upsert Sport
        sport = db.query(Sport).filter(Sport.name == record.sport_name).first()
        if not sport:
            sport = Sport(name=record.sport_name)
            db.add(sport)
            db.commit()
            db.refresh(sport)

        # Upsert TournamentType
        tournament_type = db.query(TournamentType).filter(
            TournamentType.sport_id == sport.id,
            TournamentType.gender == record.gender,
            TournamentType.format == record.format
        ).first()

        if not tournament_type:
            tournament_type = TournamentType(
                sport_id=sport.id,
                gender=record.gender,
                format=record.format
            )
            db.add(tournament_type)
            db.commit()
            db.refresh(tournament_type)

        # Upsert Tournament # # Check if the tournament exists
        tournament = db.query(Tournament).filter(
            Tournament.tournament_id == record.tournament_id,
            Tournament.tournament_type_id == tournament_type.id
        ).first()

        if tournament:
            return {"message": "Data already exists for this combination of tournament ID, sport, gender, and format"}


        if not tournament:
            tournament = Tournament(
                tournament_id=record.tournament_id,
                tournament_type_id=tournament_type.id,
                host=record.host,
                venue=record.venue,
                winner=record.winner,
                runner_up=record.runner_up,
                player_of_the_match=record.player_of_the_match
            )
            db.add(tournament)
        else:
            # Update existing tournament
            tournament.host = record.host
            tournament.venue = record.venue
            tournament.winner = record.winner
            tournament.runner_up = record.runner_up
            tournament.player_of_the_match = record.player_of_the_match

        db.commit()
        db.refresh(tournament)

        # Upsert Stats
        for key, value in record.stats.items():
            if value:  # Only process non-null stats # # Only add non-null stats
                stat = db.query(Stat).filter(
                    Stat.tournament_id == tournament.id,
                    Stat.key == key
                ).first()

                if not stat:
                    stat = Stat(
                        tournament_id=tournament.id,
                        key=key,
                        value=value
                    )
                    db.add(stat)
                else:
                    # Update the value if stat already exists
                    stat.value = value

        db.commit()
        return {
            "message": "Record upserted successfully",
            #"data": record.dict()
            "data": record.model_dump()  # Use model_dump() instead of dict()
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.delete("/delete_record/")
def delete_record(
    tournament_id: str,
    sport: str,
    gender: str,
    format: str,
    db: Session = Depends(get_db),
):
    """
    Delete a tournament record along with its stats, tournament type, and sport if no dependencies exist.
    """
    try:
        # Find the Sport
        sport_record = db.query(Sport).filter(Sport.name == sport).first()
        if not sport_record:
            raise HTTPException(status_code=404, detail="Sport not found")

        # Find the TournamentType
        tournament_type = db.query(TournamentType).filter(
            and_(
                TournamentType.sport_id == sport_record.id,
                TournamentType.gender == gender,
                TournamentType.format == format
            )
        ).first()
        if not tournament_type:
            raise HTTPException(status_code=404, detail="Tournament type not found")

        # Find the Tournament
        tournament = db.query(Tournament).filter(
            and_(
                Tournament.tournament_id == tournament_id,
                Tournament.tournament_type_id == tournament_type.id
            )
        ).first()
        if not tournament:
            raise HTTPException(status_code=404, detail="Tournament not found")

        # Delete associated Stats
        db.query(Stat).filter(Stat.tournament_id == tournament.id).delete()

        # Delete the Tournament
        db.delete(tournament)
        db.commit()

        # Check if there are other Tournaments under the TournamentType
        remaining_tournaments = db.query(Tournament).filter(
            Tournament.tournament_type_id == tournament_type.id
        ).count()

        if remaining_tournaments == 0:
            # Delete the TournamentType
            db.delete(tournament_type)
            db.commit()

            # Check if there are other TournamentTypes under the Sport
            remaining_tournament_types = db.query(TournamentType).filter(
                TournamentType.sport_id == sport_record.id
            ).count()

            if remaining_tournament_types == 0:
                # Delete the Sport
                db.delete(sport_record)
                db.commit()

        return {"message": "Record deleted successfully"}

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
