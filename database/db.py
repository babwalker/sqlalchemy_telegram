import asyncio
from typing import List
from sqlalchemy import ForeignKey, create_engine, String
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship, sessionmaker, Session
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData
from config import engine_url

metadata_obj = MetaData()

engine = create_engine(engine_url, echo=True)

# sess = sessionmaker(engine)
session = Session(engine)

class Base(DeclarativeBase):
    pass

class CategoryCards(Base):
    __tablename__ = "category"
    id: Mapped[int] = mapped_column(primary_key=True)
    category_name: Mapped[str] = mapped_column(String(255))
    card: Mapped[List["Card"]] = relationship(back_populates="category")

class Card(Base):
    __tablename__ = "card"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(4000))
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    category: Mapped[List["CategoryCards"]] = relationship(back_populates="card")
        
# # Base.metadata.drop_all(engine)
# # Base.metadata.create_all(engine)
# with session as session:
#     # Пример добавления данных в таблицу CategoryCards
#     category = session.query(Card).filter(CategoryCards.category_name == "Credits").all()
    
#     for card in category:
#         print(f"Card ID: {card.id}, Name: {card.name}, Description: {card.description}")
        
#     # session.commit()