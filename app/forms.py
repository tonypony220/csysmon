from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('<h3>Логин</h3>', validators=[DataRequired()])
    password = PasswordField('<h3>Пароль</h3>', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class EditProfileForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=1, max=64)])
    name = StringField('Ф.И.О.', validators=[DataRequired(), Length(min=1, max=200)])
    email = StringField('email', validators=[DataRequired(), Email(), Length(min=1, max=120)])
    phone_num = StringField('Номер телефона', validators=[DataRequired(), Length(min=1, max=30)])

    submit = SubmitField('Сохранить')


class AddDeviceForm(FlaskForm):
    serial_num = StringField('Серийный номер', validators=[DataRequired()])
    device_type = StringField('Тип устройства', validators=[DataRequired()])
    addition = TextAreaField('Примечание')
    submit = SubmitField('Добавить устройство')
    
class EditDeviceForm(FlaskForm):
    serial_num = StringField('Серийный номер', validators=[DataRequired()])
    device_type = StringField('Тип устройства', validators=[DataRequired()])
    addition = TextAreaField('Примечание')

    apikey_poolbtccom = StringField('API KEY pool.btc.com', validators=[Length(min=1, max=256)])
    puid_poolbtccom = StringField('PUID pool.btc.com', validators=[Length(min=1, max=256)])
    
    apikey_antpool = StringField('API KEY antpool.com', validators=[Length(min=1, max=256)])
    secret_antpool = StringField('SECRET antpool.com', validators=[Length(min=1, max=256)])
    userid_antpool = StringField('USERID antpool.com', validators=[Length(min=1, max=256)])
    coin_antpool = StringField('COIN antpool.com', validators=[Length(min=1, max=256)])

    apikey_viabtc = StringField('API KEY viabtc.com', validators=[Length(min=1, max=256)])

    apikey_f2pool = StringField('Имя пользователя f2pool.com', validators=[Length(min=1, max=256)])

    worker_slushpool  = StringField('WORKER slushpool.com', validators=[Length(min=1, max=256)])
    apikey_slushpool = StringField('API KEY slushpool.com', validators=[Length(min=1, max=256)])

    url_sensor_device = StringField('URL адрес устройства мониторинга', validators=[Length(min=1, max=256)])
    url_relay_device = StringField('URL адрес реле', validators=[Length(min=1, max=256)])

    submit = SubmitField('Применить изменения')

class ContactUsForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired(), Length(min=1, max=200)])
    email = StringField('Email (для ответа на обращение)', validators=[DataRequired(), Email()])
    email_text = TextAreaField('Написать нам', validators=[DataRequired()])
    submit = SubmitField('Написать нам')