import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String,Enum,Table
from sqlalchemy.orm import relationship, declarative_base
# from sqlalchemy.types import Enum
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

tabla_users_characters = Table('tabla_users_characters',Base.metadata,
    Column('user_id',ForeignKey('users.id'),primary_key = True),             
    Column('character_id',ForeignKey('characters.id'),primary_key = True)                   
)

tabla_users_planets = Table('tabla_users_planets',Base.metadata,
    Column('user_id',ForeignKey('users.id')),             
    Column('planet_id',ForeignKey('planets.id'))                   
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True)
    nick = Column(String(30),nullable=False,unique=True)
    email = Column(String(30),nullable=False,unique=True)
    password = Column(String(20),nullable=False)


class Planet(Base):
    __tablename__ = 'planets'
    id = Column(Integer, primary_key=True)
    name = Column(String(30),nullable= False,unique = True)
    biome = Column(Enum('Dessert','Forest','Frozen','Volcanic'))
    # cuando yo llame a  cities, con backref me trae todo la informacion del planeta
    # la propiedad cities nos va a guardar todas las cities que tiene este planeta
    cities = relationship('City',back_populates = 'planet')
    races = relationship('Race', back_populates = 'planet')
    characters = relationship('Character', back_populates = 'planet')
    users = relationship('User',secondary = tabla_users_planets)

class City(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True)
    name = Column(String(30),nullable=False,unique = True)
    population = Column(Integer)

    planet_id = Column(Integer,ForeignKey('planets.id'))
    planet = relationship('Planet',back_populates = 'cities')

    characters = relationship('Character',back_populates = 'city')

class Battleship(Base):
    __tablename__ = 'battleships'
    id = Column(Integer, primary_key=True)
    name = Column(String(30),nullable=False,unique=True)
    strength = Column(Integer)
    size = Column(Integer)

    character = relationship('Character',back_populates = 'battleship',uselist = False)

class Character(Base):
    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True)
    name = Column(String(30),nullable=False)
    age = Column(Integer)

    users = relationship('User',secondary = tabla_users_characters)

    planet_id = Column(Integer,ForeignKey('planets.id'))
    planet = relationship('Planet',back_populates = 'characters')

    race_id = Column(Integer,ForeignKey('races.id'))
    race = relationship('Race',back_populates = 'characters')

    city_id = Column(Integer,ForeignKey('cities.id'))
    city = relationship('City',back_populates = 'characters')

    battleship_id = Column(Integer,ForeignKey('battleships.id'))
    battleship = relationship('Battleship',back_populates = 'character')

class Race(Base):
    __tablename__ = 'races'
    id = Column(Integer, primary_key=True)
    name = Column(String(30),nullable=False)
    avg_height = Column(Integer)
    skin_color = Column(String)
    
    planet_id = Column(Integer,ForeignKey('planets.id'))
    planet = relationship('Planet',back_populates = 'races')



# backref y back_populates -> automaticamente te crea la relaccion en la otra tabla
# back_populates te crea una relaccion bidireccional

## Draw from SQLAlchemy base
render_er(Base, 'diagram.png')
