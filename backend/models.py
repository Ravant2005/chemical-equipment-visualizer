"""
SQLAlchemy models for equipment data.
"""
from sqlalchemy import Column, Integer, String, Float
from database import Base


class Equipment(Base):
    """
    Equipment model for storing equipment records.
    Table name: equipments
    """
    __tablename__ = "equipments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)  # NOT NULL constraint
    category = Column(String(100))
    material = Column(String(100))

    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "material": self.material,
        }

