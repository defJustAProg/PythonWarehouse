from sqlalchemy import Column, String, Date, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from pydantic import BaseModel, Field
from datetime import date

Base = declarative_base()

class Roll(BaseModel):
    id: str = Field(None)
    length: int = Field(...)
    weight: int = Field(...)
    put_date: date = Field(None)
    delete_date: date = Field(None)

class RollTable(Base):
    __tablename__ = 'Roll'
    id = Column(String(36), primary_key=True, nullable=False)
    length = Column(String(100), nullable=False)
    weight = Column(String(100), nullable=False)
    put_date = Column(Date, server_default=func.current_date(), nullable=False)
    delete_date = Column(Date, server_default=func.current_date(), nullable=False)
    status = Column(Boolean, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "length": self.length,
            "weight": self.weight,
            "put_date": str(self.put_date),
            "delete_date": str(self.delete_date),
            "status": self.status,
        }
