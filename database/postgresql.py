from sqlalchemy import create_engine, Column, Integer, String, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres@localhost:5432/machine_status"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class MachineStatus(Base):
    __tablename__ = "status"
    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(String)
    machine_name = Column(String)
    status = Column(String)
    time = Column(String)
    
Base.metadata.create_all(bind=engine)
