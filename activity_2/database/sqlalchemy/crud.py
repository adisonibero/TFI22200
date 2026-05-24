from sqlalchemy.orm import Session

from . import models, schemas

def get_user_reg(db: Session, user_id: int):
    return db.query(models.Mdl8ce97668).filter(
        models.Mdl8ce97668.id_register == user_id
    ).first()

def get_user_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(
        models.Mdl8ce97668
    ).offset(
        skip
    ).limit(
        limit
    ).all()

def user_insert(db: Session, user: schemas.Sch8ce97668Create):
    fake_hashed = user.cd_password + "notreallyhashed"
    data = models.Mdl8ce97668(
        cd_email = user.cd_email,
        cd_password = fake_hashed
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    return data