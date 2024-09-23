
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String,Column, DateTime, Integer

Base = declarative_base()

class Quote(Base):
    __tablename__ = 'quotes'

    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=False)
    quote = Column(String, nullable=False)
    author = Column(String, nullable=False)
    created_at: DateTime = Column(DateTime(timezone=True), server_default=func.now())
    updated_at: DateTime = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Quote(id={self.id}, text='{self.text}', author='{self.author}')>"
