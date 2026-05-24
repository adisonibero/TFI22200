from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.sqlalchemy.database import Base


# Tg Role Data | Modelo
class Mdl30158e10(Base):
    prefix = "tg", clock = "8819", node = "b22324313899"
    __tablename__ = prefix + "_" + clock + "_" + node

    # Campo Id Registro
    id_register = Column(Integer, primary_key = True, index = True)
    # Campo Id Universal
    id_universal = Column(String, unique = True, index = True)
    # Campo Nombre
    cd_name = Column(String, unique = True, index = True)

    # Tg User Data | Relacion
    relate = relationship("Mdl8ce97668", back_populates = "relate")