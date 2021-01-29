from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from datetime import datetime, timedelta
from app import db, login
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(120), index=True, unique=True)
    phone_num = db.Column(db.String(30), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    alerts = db.Column(db.Boolean)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serial_num = db.Column(db.String(100), index=True, unique=True)
    device_type = db.Column(db.String(260))
    addition = db.Column(db.String(500))
    hash_rate = db.Column(db.Float)
    status = db.Column(db.Boolean)

    apikey_poolbtccom = db.Column(db.String(256))
    puid_poolbtccom = db.Column(db.String(256))

    apikey_antpool = db.Column(db.String(256))
    secret_antpool = db.Column(db.String(256))
    userid_antpool = db.Column(db.String(256))
    coin_antpool = db.Column(db.String(256))

    apikey_viabtc = db.Column(db.String(256))

    apikey_f2pool = db.Column(db.String(256))

    apikey_slushpool = db.Column(db.String(256))
    worker_slushpool = db.Column(db.String(256))

    url_sensor_device = db.Column(db.String(256))
    url_relay_device = db.Column(db.String(256))

    relay1_state = db.Column(db.Boolean)
    relay2_state = db.Column(db.Boolean)
    relay3_state = db.Column(db.Boolean)
    relay4_state = db.Column(db.Boolean)
    relay5_state = db.Column(db.Boolean)
    relay6_state = db.Column(db.Boolean)

    def __repr__(self):
        return '<Post {}>'.format(self.serial_num)

class Indicator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temp_inside = db.Column(db.Float)
    temp_outside_first = db.Column(db.Float)
    temp_outside_second = db.Column(db.Float)
    temp_outside_third = db.Column(db.Float)
    temp_outside_fourth = db.Column(db.Float)
    distance = db.Column(db.Float)
    power = db.Column(db.Float)
    pressure = db.Column(db.Float)
    speed = db.Column(db.Float)
    temp_in = db.Column(db.Float)
    temp_out = db.Column(db.Float)
    temp_all = db.Column(db.Float)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    pressure_bmp180 = db.Column(db.Float)

    relay1_state = db.Column(db.Boolean)
    relay2_state = db.Column(db.Boolean)
    relay3_state = db.Column(db.Boolean)
    relay4_state = db.Column(db.Boolean)
    relay5_state = db.Column(db.Boolean)
    relay6_state = db.Column(db.Boolean)

    relay1_current = db.Column(db.Float)
    relay2_current = db.Column(db.Float)
    relay3_current = db.Column(db.Float)
    relay4_current = db.Column(db.Float)
    relay5_current = db.Column(db.Float)
    relay6_current = db.Column(db.Float)

    hashrate_total = db.Column(db.Float)
    hashrate_poolbtccom  = db.Column(db.Float)
    hashrate_antpool  = db.Column(db.Float)
    hashrate_viabtc  = db.Column(db.Float)
    hashrate_f2pool  = db.Column(db.Float)
    hashrate_slushpool  = db.Column(db.Float)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id': self.id,
           'temp_inside': self.temp_inside,
           'temp_outside_first': self.temp_outside_first,
           'temp_outside_second': self.temp_outside_second,
           'temp_outside_third': self.temp_outside_third,
           'temp_outside_fourth': self.temp_outside_fourth,
           'distance': self.distance,
           'power': self.power,
           'pressure': self.pressure,
           'speed': self.speed,
           'temp_in': self.temp_in,
           'temp_out': self.temp_out,
           'temp_all': self.temp_all,
           'device_id': self.device_id,
           'timestamp': (self.timestamp + timedelta(hours=3)).strftime("%H:%M:%S %d.%m.%Y"),

           'relay1_state': self.relay1_state,
           'relay2_state': self.relay2_state,
           'relay3_state': self.relay3_state,
           'relay4_state': self.relay4_state,
           'relay5_state': self.relay5_state,
           'relay6_state': self.relay6_state,

           'relay1_current': self.relay1_current,
           'relay2_current': self.relay2_current,
           'relay3_current': self.relay3_current,
           'relay4_current': self.relay4_current,
           'relay5_current': self.relay5_current,
           'relay6_current': self.relay6_current
       }   

    def __repr__(self):
        return '<Indicator {}>'.format(self.timestamp)

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1000))
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Alert {}>'.format(self.timestamp)