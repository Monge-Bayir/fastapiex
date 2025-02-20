from database import Base
from sqlalchemy import Column, String, Integer, Text


class Recipes(Base):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    views = Column(Integer, default=0)
    time_cooking = Column(Integer)
    description = Column(Text)
    ingredients = Column(Text)
