from StorageInterface import StorageInterface
import os
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from dotenv import load_dotenv
from schemas import Base, Roll, RollTable
from sqlalchemy.orm import Session
import uuid
from datetime import date
import statistics


class PgService(StorageInterface):

    def __init__(self, dotenv_path):

        self.dotenv_path = dotenv_path
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)

        self.engine = self.connect()
        self.engine.connect()
        Base.metadata.create_all(self.engine, checkfirst=True)

    def connect(self):
        url = f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_HOST")}/warehouse'
        if not database_exists(url):
            create_database(url)

        url = URL.create(
            drivername="postgresql",
            username=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            host=os.getenv('POSTGRES_HOST'),
            database="warehouse"
        )

        engine = create_engine(url)
        return engine

    def get(self, rollSortModel: dict):

        with Session(self.engine) as session:
            result = session.query(RollTable).filter_by(**rollSortModel).all()
            return result

    def insert(self, roll: Roll):

        if roll.id:
            with Session(self.engine) as session:
                record = session.query(RollTable).get(roll.id)

            if not record:
                with Session(self.engine) as session:
                    if roll.id:
                        session.add(
                            RollTable(
                                id=roll.id,
                                length=roll.length,
                                weight=roll.weight
                            )
                        )
                        session.commit()
                        with Session(self.engine) as session:
                            record_id = session.query(RollTable).get(roll.id)

                if record_id:
                    return record_id
                else:
                    return "Something wrong"

            else:
                return "Its alredy exist"

        else:
            key = str(uuid.uuid4())
            with Session(self.engine) as session:
                session.add(
                    RollTable(
                        id=key,
                        length=roll.length,
                        weight=roll.weight
                    )
                )
                session.commit()
            with Session(self.engine) as session:
                record_uuid = session.query(RollTable).get(key)

            if record_uuid:
                return record_uuid
            else:
                return "Something wrong"

    def delete(self, id: str):

        with Session(self.engine) as session:
            record = session.query(RollTable).filter(RollTable.id == id).first()
            if record:
                record.status = False
                session.commit()
                return record
            else:
                return "No record with this ID"

    def statistics(self, put_date: date, delete_date: date):
        with Session(self.engine) as session:
            records = session.query(RollTable).filter(RollTable.put_date >= put_date,
                                                      RollTable.delete_date <= delete_date).all()
            if records:
                count_of_Rolls = len(records)
                count_of_delete_Rolls = len([roll for roll in records if roll.status == False])
                avg_length = statistics.mean([int(roll.length) for roll in records])
                avg_weight = statistics.mean([int(roll.weight) for roll in records])
                max_length = max([int(roll.length) for roll in records])
                min_length = min([int(roll.length) for roll in records])
                max_weight = max([int(roll.weight) for roll in records])
                min_weight = min([int(roll.weight) for roll in records])
                sum_weight = sum([int(roll.weight) for roll in records])
                return {"count_of_Rolls": count_of_Rolls,
                        "count_of_delete_Rolls": count_of_delete_Rolls,
                        "avg_length": avg_length,
                        "avg_weight": avg_weight,
                        "max_length": max_length,
                        "min_length": min_length,
                        "max_weight": max_weight,
                        "min_weight": min_weight,
                        "sum_weight": sum_weight}

            else:
                return "No records for the period"

    def update(self):
        pass
