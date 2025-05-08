from sqlalchemy import Column, Integer, ForeignKey, BigInteger, func
from sqlalchemy.orm import relationship
from app.core.database import Base, UnixTimestamp

class UserFarm(Base):
    __tablename__ = 'user_farms'
    
    telegram_id = Column(BigInteger, ForeignKey('users.telegram_id'), primary_key=True)
    farm_id = Column(BigInteger, ForeignKey('farm_templates.farm_id'), primary_key=True)
    level = Column(BigInteger, default=1)
    last_collected = Column(UnixTimestamp, onupdate=func.extract('epoch', func.now()))
    current_income = Column(BigInteger)
    current_upgrade_cost = Column(BigInteger)
    
    user = relationship("User", back_populates="farms")
    farm_template = relationship("FarmTemplate", back_populates="user_farms", lazy="joined")
