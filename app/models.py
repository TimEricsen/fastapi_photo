from .database import Base

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String, unique=True)

    photos = relationship('Photo', back_populates='owner')


class Photo(Base):
    __tablename__ = 'photos'

    id = Column(Integer, autoincrement=True, index=True, primary_key=True)
    title = Column(String, unique=True)
    creating_date = Column(Date)
    location = Column(String)
    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship('User', back_populates='photos')
    people = relationship('PeopleOnPhoto', back_populates='photo')


class PeopleOnPhoto(Base):
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    full_name = Column(String)
    photo_title = Column(String, ForeignKey('photos.title'))

    photo = relationship('Photo', back_populates='people')


