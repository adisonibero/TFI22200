from pydantic import BaseModel


# Tg Role Data | Base Model
class Sch30158e10Base(BaseModel):
    id_register: int
    id_universal: str
    cd_name: str

# Tg Role Data | Base Create
class Sch30158e10Create(Sch30158e10Base):
    pass

# Tg Role Data | Clase Main
class Sch30158e10Main(Sch30158e10Base):
    id_register: int
    id_universal: str
    cd_name: str

    class Config:
        orm_mode = True