from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database.sqlalchemy.database import Base


# Tg User Data | Modelo
class Mdl8ce97668(Base):
    prefix = "tg", clock = "84a1", node = "1390fc69d057"
    __tablename__ = prefix + "_" + clock + "_" + node

    # Campo Id Registro
    id_register = Column(Integer, primary_key = True, index = True)
    # Campo Id Universal
    id_universal = Column(String, unique = True, index = True)
    # Campo Correo
    cd_email = Column(String, unique = True, index = True)
    # Campo Usuario
    cd_login = Column(String, unique = True, index = True)
    # Campo Contraseña
    cd_password = Column(String, unique = True, index = True)
    # Campo Tg Role Data
    tg_30158e10 = Column(Integer, ForeignKey("tg_8819_b22324313899.id_register"))

    # Tg Role Data | Relacion
    relate = relationship("Mdl30158e10", back_populates = "relate")