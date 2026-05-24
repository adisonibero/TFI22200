from pydantic import BaseModel


# Tg User Data | Base Model
class Sch8ce97668Base(BaseModel):
    id_register: int
    id_universal: str
    cd_email: str
    cd_login: str
    cd_password: str
    # tg_30158e10: list[]

# Tg User Data | Base Create
class Sch8ce97668Create(Sch8ce97668Base):
    cd_password: str

# Tg User Data | Clase Main
class Sch8ce97668Main(Sch8ce97668Base):
    id_register: int
    id_universal: str
    cd_email: str
    cd_login: str
    cd_password: str
    tg_30158e10: list[Sch30158e10Main] = []

    class Config:
        orm_mode = True
