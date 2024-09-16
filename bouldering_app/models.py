from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Text, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base() 

class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    age = Column(String, nullable=False)
    profile_picture = Column(String)
    highest_grade_climbed = Column(Integer, default=0)
    highest_grade_flased = Column(Integer, default=0)
    
    #relationships
    boulders = relationship('Boulder', back_populates='creator')
    attempts = relationship('Attempt', back_populates='user')
    

class Boulder(Base):
    __tablename__ = 'boulder'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    color = Column(String, nullable=False)
    difficulty = Column(Integer, nullable=False)
    numberofmoves = Column(Integer, nullable=False)
    set_date = Column(Date)
    description = Column(Text)
    image = Column(String)
    created_by = Column(Integer, ForeignKey('user.id'), nullable=False)

    # Relationship
    creator = relationship('User', back_populates='boulders')
    attempts = relationship('Attempt', back_populates='boulder')

class Attempt(Base):
    __tablename__ = 'attempt'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    number_of_attempts = Column(Integer, nullable=False)
    status = Column(String, CheckConstraint("status IN ('incomplete', 'completed', 'flashed')"), nullable=False)
    attempt_date = Column(Date, default='CURRENT_DATE')
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    boulder_id = Column(Integer, ForeignKey('boulder.id'), nullable=False)
    moves_completed = Column(Integer)
    difficulty = Column(Integer, nullable=False)

    # Relationships
    user = relationship('User', back_populates='attempts')
    boulder = relationship('Boulder', back_populates='attempts')

# Example of creating the database engine and session
def create_db_engine_and_session(database_url):
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return engine, Session