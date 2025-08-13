from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, Boolean, DateTime, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str | None] = mapped_column(String(80))
    last_name: Mapped[str | None] = mapped_column(String(80))
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, server_default=func.now())

    posts = relationship("Post", back_populates="author",
                         cascade="all, delete-orphan")
    comments = relationship(
        "Comment", back_populates="author", cascade="all, delete-orphan")
    favorite_planets = relationship(
        "FavoritePlanet", back_populates="user", cascade="all, delete-orphan")
    favorite_characters = relationship(
        "FavoriteCharacter", back_populates="user", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Post(db.Model):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    author = relationship("User", back_populates="posts")
    comments = relationship(
        "Comment", back_populates="post", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "user_id": self.user_id,
        }


class Comment(db.Model):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)

    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "body": self.body,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "user_id": self.user_id,
            "post_id": self.post_id,
        }


class Planet(db.Model):
    __tablename__ = "planet"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    climate: Mapped[str | None] = mapped_column(String(80))
    terrain: Mapped[str | None] = mapped_column(String(80))
    population: Mapped[int | None] = mapped_column(Integer)

    favorites = relationship(
        "FavoritePlanet", back_populates="planet", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population,
        }


class Character(db.Model):
    __tablename__ = "character"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    gender: Mapped[str | None] = mapped_column(String(30))
    birth_year: Mapped[str | None] = mapped_column(String(20))
    height_cm: Mapped[int | None] = mapped_column(Integer)
    mass_kg: Mapped[int | None] = mapped_column(Integer)
    homeworld_id: Mapped[int | None] = mapped_column(ForeignKey("planet.id"))

    homeworld = relationship("Planet")
    favorites = relationship(
        "FavoriteCharacter", back_populates="character", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "birth_year": self.birth_year,
            "height_cm": self.height_cm,
            "mass_kg": self.mass_kg,
            "homeworld_id": self.homeworld_id,
        }


class FavoritePlanet(db.Model):
    __tablename__ = "favorite_planet"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    planet_id: Mapped[int] = mapped_column(
        ForeignKey("planet.id"), nullable=False)

    __table_args__ = (UniqueConstraint(
        "user_id", "planet_id", name="uq_user_planet"),)

    user = relationship("User", back_populates="favorite_planets")
    planet = relationship("Planet", back_populates="favorites")

    def serialize(self):
        return {"id": self.id, "user_id": self.user_id, "planet_id": self.planet_id}


class FavoriteCharacter(db.Model):
    __tablename__ = "favorite_character"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    character_id: Mapped[int] = mapped_column(
        ForeignKey("character.id"), nullable=False)

    __table_args__ = (UniqueConstraint(
        "user_id", "character_id", name="uq_user_character"),)

    user = relationship("User", back_populates="favorite_characters")
    character = relationship("Character", back_populates="favorites")

    def serialize(self):
        return {"id": self.id, "user_id": self.user_id, "character_id": self.character_id}
