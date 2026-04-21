from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from src.database.connection import Base

# Represent tables in PostgresSQL
# Each class = one table

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    clothing_items = relationship("ClothingItem", back_populates="user", cascade="all, delete")
    outfits = relationship("Outfit", back_populates="user", cascade="all, delete")


class ClothingItem(Base):
    __tablename__ = "clothing_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    item_name = Column(String(100))
    category = Column(String(50), nullable=False)
    subcategory = Column(String(50))
    color = Column(String(50))
    season = Column(String(30))
    occasion = Column(String(50))
    image_url = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User", back_populates="clothing_items")
    detection_results = relationship("DetectionResult", back_populates="clothing_item", cascade="all, delete")
    outfit_items = relationship("OutfitItem", back_populates="clothing_item", cascade="all, delete")


class DetectionResult(Base):
    __tablename__ = "detection_results"

    id = Column(Integer, primary_key=True, index=True)
    clothing_item_id = Column(Integer, ForeignKey("clothing_items.id", ondelete="CASCADE"), nullable=False)
    detected_label = Column(String(50), nullable=False)
    detected_color = Column(String(50))
    confidence = Column(Numeric(4, 3))
    created_at = Column(TIMESTAMP, server_default=func.now())

    clothing_item = relationship("ClothingItem", back_populates="detection_results")


class Outfit(Base):
    __tablename__ = "outfits"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    outfit_name = Column(String(100), nullable=False)
    occasion = Column(String(50))
    season = Column(String(30))
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User", back_populates="outfits")
    outfit_items = relationship("OutfitItem", back_populates="outfit", cascade="all, delete")


class OutfitItem(Base):
    __tablename__ = "outfit_items"

    id = Column(Integer, primary_key=True, index=True)
    outfit_id = Column(Integer, ForeignKey("outfits.id", ondelete="CASCADE"), nullable=False)
    clothing_item_id = Column(Integer, ForeignKey("clothing_items.id", ondelete="CASCADE"), nullable=False)

    outfit = relationship("Outfit", back_populates="outfit_items")
    clothing_item = relationship("ClothingItem", back_populates="outfit_items")