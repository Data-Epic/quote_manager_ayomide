from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Quote(Base):
    __tablename__ = 'quotes'

    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=False)
    quote = Column(String, nullable=False)
    author = Column(String, nullable=False)

    def __repr__(self):
        return f"<Quote(id={self.id}, text='{self.text}', author='{self.author}')>"