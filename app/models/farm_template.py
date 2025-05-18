from sqlalchemy import Column, Integer, String, BigInteger, Float, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

class FarmTemplate(Base):
    __tablename__ = 'farm_templates'
    
    farm_id = Column(BigInteger, primary_key=True)
    name = Column(String(100), nullable=False)
    image_url = Column(String(500), nullable=False)
    base_price = Column(BigInteger, nullable=False)
    price_multiplier = Column(Float, nullable=False)
    base_income = Column(BigInteger, nullable=False)
    income_multiplier = Column(Float, nullable=False)
    is_visible = Column(Boolean, default=False)
    clicks_needed = Column(BigInteger, nullable=False)

    
    user_farms = relationship("UserFarm", back_populates="farm_template", lazy="raise")