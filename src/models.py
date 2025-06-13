from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "User"
    id: Mapped[int] = mapped_column(primary_key=True)
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    login_status: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email
    
    def serialize(self): 
        return {
            "id": self.id,
            "email": self.email
        }


class Person(db.Model):
    __tablename__ = "Person"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    gender: Mapped[str] = mapped_column(nullable=True)
    eye_color: Mapped[str] = mapped_column(nullable=True)
    hair_color: Mapped[str] = mapped_column(nullable=True)
    favorites = relationship("Favorites", backref="person", lazy=True)

    def serialize(self): 
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "eye_color": self.eye_color,
            "hair_color": self.hair_color,
            "favorites": self.favorites
        }

class Planet(db.Model):
    __tablename__ = "Planet"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    population: Mapped[str] = mapped_column(nullable=True)
    terrain: Mapped[str] = mapped_column(nullable=True)
    climate: Mapped[str] = mapped_column(nullable=True)
    favorites = relationship("Favorites", backref="planet", lazy=True)

    def serialize(self): 
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "terrain": self.terrain,
            "climate": self.climate,
            "favorites": self.favorites
        }

class Favorites(db.Model):
    __tablename__ = "Favorites"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("User.id"), nullable=False)
    person_id: Mapped[int] = mapped_column(
        ForeignKey("Person.id"))
    planet_id: Mapped[int] = mapped_column(
        ForeignKey("Planet.id"))
  
    def seralize(self): 
        return {
            "id": self.id,
            "user_id": self.user_id,
            "person_id": self.person_id,
            "planet_id": self.planet_id
        }
       
