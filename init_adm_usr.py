from app import app, db
from app.models import User, Device, Indicator

u = User(username="admin")
u.set_password("ilikepussy")
db.session.add(u)
db.session.commit()
