from sqlalchemy import Column, Integer, Float, ForeignKey, func, event
from sqlalchemy.orm import relationship
from app.core.database import Base, UnixTimestamp

class UserFarm(Base):
    __tablename__ = 'user_farms'
    
    telegram_id = Column(Integer, ForeignKey('users.telegram_id'), primary_key=True)
    farm_id = Column(Integer, ForeignKey('farm_templates.farm_id'), primary_key=True)
    level = Column(Integer, default=1)
    last_collected = Column(UnixTimestamp, onupdate=func.extract('epoch', func.now()))
    current_income = Column(Integer)
    current_upgrade_cost = Column(Integer)
    
    user = relationship("User", back_populates="farms")
    farm_template = relationship("FarmTemplate", back_populates="user_farms")

@event.listens_for(UserFarm, 'before_insert')
@event.listens_for(UserFarm, 'before_update')
def calculate_values(mapper, connection, target):
    if target.farm_template:
        target.current_upgrade_cost = int(target.farm_template.base_price * (target.farm_template.price_multiplier ** target.level))
        target.current_income = int(target.farm_template.base_income * (target.farm_template.income_multiplier ** target.level))