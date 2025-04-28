from sqlalchemy import Column, Integer, String, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from app.core.database import Base, UnixTimestamp

class User(Base):
    __tablename__ = 'users'
    
    telegram_id = Column(Integer, primary_key=True)
    username = Column(String)
    created_at = Column(UnixTimestamp, server_default=func.extract('epoch', func.now()))
    referrer_id = Column(Integer, ForeignKey('users.telegram_id'), nullable=True)
    
    referrer = relationship('User', remote_side=[telegram_id], backref=backref('referrals'))
    clicks = relationship("Clicks", uselist=False, back_populates="user")
    farms = relationship("UserFarm", back_populates="user")