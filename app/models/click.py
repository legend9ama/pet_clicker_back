from sqlalchemy import Column, ForeignKey, Integer, BigInteger,  func
from sqlalchemy.orm import relationship
from app.core.database import Base, UnixTimestamp

class Clicks(Base):
    __tablename__ = 'clicks'
    
    telegram_id = Column(Integer, ForeignKey('users.telegram_id'), primary_key=True)
    clicks_count = Column(BigInteger, default=0)
    updated_at = Column(UnixTimestamp, server_default=func.extract('epoch', func.now()), onupdate=func.extract('epoch', func.now()))
    
    user = relationship("User", back_populates="clicks")