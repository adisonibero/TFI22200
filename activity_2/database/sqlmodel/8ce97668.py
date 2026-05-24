from sqlalchemy import Column, Integer, String
# from sqlmodel import Column, Integer, String
# from .database import Base


class Tg1390fc69d057(Base):
    __tablename__ = "tg_1390fc69d057"

    id_register = Column(Integer, primary_key = True, index = True)
    id_universal = Column(String, unique = True, index = True)
    cd_email = Column(String, unique = True, index = True)
    cd_login = Column(String, unique = True, index = True)
    cd_password = Column(String, unique = True, index = True)