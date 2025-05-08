from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger, func
from sqlalchemy.orm import relationship, backref
from app.core.database import Base, UnixTimestamp

class User(Base):
    __tablename__ = 'users'
    
    telegram_id = Column(BigInteger, primary_key=True)
    first_name = Column(String)
    username = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    photo_url = Column(String, nullable=True)
    created_at = Column(UnixTimestamp, server_default=func.extract('epoch', func.now()))
    referrer_id = Column(BigInteger, ForeignKey('users.telegram_id'), nullable=True)
    
    referrer = relationship('User', remote_side=[telegram_id], backref=backref('referrals'))
    clicks = relationship("Clicks", uselist=False, back_populates="user")
    farms = relationship("UserFarm", back_populates="user")