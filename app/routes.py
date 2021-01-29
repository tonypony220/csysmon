# -*- coding: utf-8 -*-
import requests
import json
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db, errors
from app.forms import LoginForm, EditProfileForm, AddDeviceForm, ContactUsForm, EditDeviceForm
from app.models import User, Device, Indicator, Alert
from app.email import send_email
from flask import jsonify

import time
import hmac,hashlib
import ssl

import json
#from flask_mail import Mail, Message

@app.route('/device')
@login_required
def device():
    return render_template('index.html', title='Home')


@app.route('/')
@app.route('/index')
@login_required
def index():
    devices = Device.query.all()
    return render_template("device.html", title='Список устройств', devices=devices)

# Добавление устройства в БД
@app.route('/add_device', methods=['GET', 'POST'])
@login_required
def add_device():
    form = AddDeviceForm()
    if form.validate_on_submit():
        device = Device(serial_num=form.serial_num.data, device_type=form.device_type.data, addition=form.addition.data, status=False)
        try:
            # Пробуем добавить устройство в БД
            db.session.add(device)
            db.session.commit()
            flash('Устройство успешно добавлено')
        except:
            # Если устройство уже существует
            flash('Ошибка: Устройство уже существует')
            return redirect(url_for('device'))
    
	# Загружаем шаблон Устройства
    return render_template('add_device.html', action ="Добавить", add_device=add_device, form=form, title="Добавление устройства")
    

#@app.route('/json')
#def json():
#    return render_template('json.html')   

@app.route('/change_device_status/<device_id>')
def change_device_status(device_id):
    dstatus = Device.query.filter_by(id=device_id).first()
    if dstatus.status == True:
        dstatus.status = False
        dstatus.relay1_state = False
        dstatus.relay2_state = False
        dstatus.relay3_state = False
        dstatus.relay4_state = False
        dstatus.relay5_state = False
        dstatus.relay6_state = False
    else:
        dstatus.status = True
        dstatus.relay1_state = True
        dstatus.relay2_state = True
        dstatus.relay3_state = True
        dstatus.relay4_state = True
        dstatus.relay5_state = True
        dstatus.relay6_state = True
    db.session.commit()

    return redirect(request.referrer)

@app.route('/change_device_status/<device_id>/<relay_id>')
def change_device_relay_status(device_id, relay_id):
    dstatus = Device.query.filter_by(id=device_id).first()
    if relay_id == "1":
        dstatus.relay1_state = not dstatus.relay1_state    
    if relay_id == "2":
        dstatus.relay2_state = not dstatus.relay2_state    
    if relay_id == "3":
        dstatus.relay3_state = not dstatus.relay3_state    
    if relay_id == "4":
        dstatus.relay4_state = not dstatus.relay4_state    
    if relay_id == "5":
        dstatus.relay5_state = not dstatus.relay5_state    
    if relay_id == "6":
        dstatus.relay6_state = not dstatus.relay6_state    
    db.session.commit()

    return redirect(request.referrer)
    
@app.route('/change_subscription_status/<user_id>')
def change_subscription_status(user_id):
    sstatus = User.query.filter_by(id=user_id).first()
    if sstatus.alerts == True:
        sstatus.alerts = False
    else:
        sstatus.alerts = True
    db.session.commit()

    return redirect(url_for('user', username=sstatus.username))

@app.route('/get_set_relay_parms/<device_id>')
def get_set_relay_parms(device_id):
    device = Device.query.filter_by(id=device_id).first_or_404()
    i = Indicator.query.filter_by(device_id=device_id).first_or_404()
    
    relay_1 = request.args.get('relay_1', default = 0, type = int)
    relay_2 = request.args.get('relay_2', default = 0, type = int)
    relay_3 = request.args.get('relay_3', default = 0, type = int)
    sensor_1 = request.args.get('sensor_1', default = 0, type = float)
    sensor_2 = request.args.get('sensor_2', default = 0, type = float)
    sensor_3 = request.args.get('sensor_3', default = 0, type = float)
    updt = request.args.get('updt', default = 'N')
    
    if (device.relay1_state == True):
        drel1 = 1
    else:
        drel1 = 0
    if (device.relay2_state == True):
        drel2 = 1
    else:
        drel2 = 0
    if (device.relay3_state == True):
        drel3 = 1
    else:
        drel3 = 0
    
    str1 = ''
    if (drel1 == 0):
        str1 = '1'
    if (drel2 == 0):
        str1 = '2'
    if (drel3 == 0):
        str1 = '3'
    if (drel1 == 0 and drel2 == 0):
        str1 = '4'
    if (drel1 == 0 and drel3 == 0):
        str1 = '5'
    if (drel2 == 0 and drel3 == 0):
        str1 = '6'
    if (drel1 == 0 and drel2 == 0 and drel3 == 0):
        str1 = '7'
    if (drel1 == 1 and drel2 == 1 and drel3 == 1):
        str1 = '0'
        
    #str2 = str(drel1)  + ' ' + str(drel2) + ' ' + str(drel3)
        
    #if (updt == 'Y'):
        #if relay_1 == 0:
        #    i.relay1_state = False
        #else:
        #    i.relay1_state = True
        #if relay_2 == 0:
        #    i.relay2_state = False
        #else:
        #    i.relay2_state = True
        #if relay_3 == 0:
        #    i.relay3_state = False
        #else:
        #    i.relay3_state = True
            
        #if device.relay1_state is None:
        #    device.relay1_state =  i.relay1_state

        #if device.relay2_state is None:
        #    device.relay2_state =  i.relay2_state

        #if device.relay3_state is None:
         #   device.relay3_state =  i.relay3_state
            
        #device.status = True if device.relay1_state or device.relay2_state or device.relay3_state else False
  
    current_mult =  1.0 / 1024 * 30 / 2 * 1.2 #5.0 / 1024.0 * 0.707 / 66 * 1000

    i.relay1_current = 0 if float(sensor_1) <= 120 else float(sensor_1) * current_mult
    i.relay2_current = 0 if float(sensor_2) <= 120 else float(sensor_2) * current_mult
    i.relay3_current = 0 if float(sensor_3) <= 120 else float(sensor_3) * current_mult

    db.session.add(i)
    db.session.commit()
    
    return str1 #+ '   ' + str2
    
@app.route('/get_sensor_parms/<device_id>')      
def sget_sensor_parms(device_id):
    device = Device.query.filter_by(id=device_id).first_or_404()
    i = Indicator()
    
    temp_inside = request.args.get('temp_inside', default = -1, type = float)
    temp_outside_first = request.args.get('temp_outside_first', default = -1, type = float)
    temp_outside_second = request.args.get('temp_outside_second', default = -1, type = float)
    temp_outside_third = request.args.get('temp_outside_third', default = -1, type = float)
    if (temp_outside_second == 0):
        temp_outside_second = round((temp_outside_first+temp_outside_third)/2,1)
    temp_outside_fourth = request.args.get('temp_outside_fourth', default = -1, type = float)
    distance = request.args.get('distance', default = -1, type = float)
    power = request.args.get('power', default = -1, type = float)
    pressure = request.args.get('pressure', default = -1, type = float)
    if pressure != -1:
        pressure = int(float(pressure)) / 100
    else:
        pressure = pressure
    speed = request.args.get('speed', default = -1, type = float)
    temp_in = request.args.get('temp_in', default = -1, type = float)
    temp_out = request.args.get('temp_out', default = -1, type = float)
    temp_all = request.args.get('temp_all', default = -1, type = float)
    
    i.temp_inside = temp_inside
    i.temp_outside_first = temp_outside_first
    i.temp_outside_second = temp_outside_second
    i.temp_outside_third = temp_outside_third
    i.temp_outside_fourth = temp_outside_fourth
    i.distance = distance
    i.power = power
    i.pressure = pressure
    i.speed = speed
    i.temp_in = temp_in
    i.temp_out = temp_out
    i.temp_all = temp_all
    
    i.device_id = device_id
    
    #получаеми хэшрейты
    i.hashrate_poolbtccom = 0
    if (not device.apikey_poolbtccom is None and device.apikey_poolbtccom != ""):
        r = requests.get("https://eu-pool.api.btc.com/v1/realtime/hashrate?access_key="+device.apikey_poolbtccom+"&puid="+device.puid_poolbtccom)
        if r.status_code == 200:
            print(r.text)
            r = r.json()
            if (r["err_no"] == 0):
                i.hashrate_poolbtccom = float(r["data"]["shares_15m"])
            

    

    #antpool
    i.hashrate_antpool = 0
    if (not device.apikey_antpool is None and device.apikey_antpool != ""):
        nonce=int(time.time()*1000)
        msgs=device.userid_antpool+device.apikey_antpool+str(nonce)
        api_sign=[]
        api_sign.append(hmac.new(device.secret_antpool.encode(encoding="utf-8"), msg=msgs.encode(encoding="utf-8"), digestmod=hashlib.sha256).hexdigest().upper())
        api_sign.append(nonce)

        post_data = {'key': device.apikey_antpool, 'nonce': api_sign[1],'signature': api_sign[0],'coin': device.coin_antpool}
        r = requests.post("https://antpool.com/api/hashrate.htm", data=post_data)

        if r.status_code == 200:
            r = r.json()
            if r["code"] == 0:
                try:
                    i.hashrate_antpool = int(r["data"]["last10m"])
                except:
                    pass

    i.hashrate_viabtc = 0

    i.hashrate_f2pool = 0
    if (not device.apikey_f2pool is None and device.apikey_f2pool != ""):
        r = requests.get("http://api.f2pool.com/bitcoin/"+device.apikey_f2pool)
        if r.status_code == 200:
            r = r.json()
            try:
                i.hashrate_f2pool = int(r["hashrate"])
            except:
                pass   

    i.hashrate_slushpool = 0

    if (not device.apikey_slushpool is None and device.apikey_slushpool != ""):
        r = requests.get("https://slushpool.com/accounts/profile/json/"+device.apikey_slushpool)
        if r.status_code == 200 and r.text != "Invalid token":
            r = r.json()
            try:
                i.hashrate_slushpool = int(r["workers"][r["username"] + "." + device.worker_slushpool]["hashrate"])
            except:
                pass

    i.hashrate_total = i.hashrate_poolbtccom + i.hashrate_antpool + i.hashrate_viabtc + i.hashrate_f2pool + i.hashrate_slushpool 
    device.hash_rate = i.hashrate_total

    db.session.add(i)
    db.session.commit()

    # Некоторое количество говнокода
    a = Alert()
    if float(i.temp_inside) > 75.0:
        a.text = "Внутренняя температура превышает пороговое значение в 75 градусов на " + str(float(temp_inside)-75.0) + "градусов"
        a.device_id = i.device_id
        db.session.add(a)
        db.session.commit()
        #send_email('Превышение температуры!', 'no-reply@tpai.ru', ['ekochetkov@tpai.ru'], "Внутренняя температура превышает пороговое значение в 75 градусов на " + str(float('temp_inside)-75.0) + "градусов")
    if float(i.temp_outside_first) > 70.0:
        a.text = "Температура первого датчика превышает пороговое значение в 70 градусов на " + str(float(temp_outside_first)-70.0) + "градусов"
        a.device_id = i.device_id
        db.session.add(a)
        db.session.commit()
        #send_email('Превышение температуры!', 'no-reply@tpai.ru', ['ekochetkov@tpai.ru'], "Температура первого датчика превышает пороговое значение в 70 градусов на " + str(float('temp_outside_first)-70.0) + "градусов")
    if float(i.temp_outside_second) > 65.0:
        a.text = "Температура второго датчика превышает пороговое значение в 65 градусов на " + str(float(temp_outside_second)-65.0) + "градусов"
        a.device_id = i.device_id
        db.session.add(a)
        db.session.commit()
        #send_email('Превышение температуры!', 'no-reply@tpai.ru', ['ekochetkov@tpai.ru'], "Температура второго датчика превышает пороговое значение в 65 градусов на " + str(float(temp_outside_second)-65.0) + "градусов")
    if float(i.temp_outside_third) > 60.0:
        a.text = "Температура третьего датчика превышает пороговое значение в 60 градусов на " + str(float(temp_outside_third)-60.0) + "градусов"
        a.device_id = i.device_id
        db.session.add(a)
        db.session.commit()
        #send_email('Превышение температуры!', 'no-reply@tpai.ru', ['ekochetkov@tpai.ru'], "Температура третьего датчика превышает пороговое значение в 60 градусов на " + str(float(temp_outside_third)-60.0) + "градусов")
    if float(i.temp_outside_fourth) > 60.0:
        a.text = "Температура четвёртого датчика превышает пороговое значение в 60 градусов на " + str(float(temp_outside_fourth)-60.0) + "градусов"
        a.device_id = i.device_id
        db.session.add(a)
        db.session.commit()
        #send_email('Превышение температуры!', 'no-reply@tpai.ru', ['ekochetkov@tpai.ru'], "Температура четвёртого датчика превышает пороговое значение в 60 градусов на " + str(float(temp_outside_fourth)-60.0) + "градусов")
    if float(i.distance) > 199.0:
        a.text = "Расстояние до жидкости превышает пороговое значение 199 на " + str(float(distance)-199.0)
        a.device_id = i.device_id
        db.session.add(a)
        db.session.commit()
        #send_email('Расстояние до жидкости!', 'no-reply@tpai.ru', ['ekochetkov@tpai.ru'], "Расстояние до жидкости превышает пороговое значение 199 на " + str(float(distance)-199.0))
    if float(i.power) > 100.0:
        a.text = "Мощность превышает пороговое значение 100 на" + str(float(power)-100.0)
        a.device_id = i.device_id
        db.session.add(a)
        db.session.commit()
        #send_email('Мощность!', 'no-reply@tpai.ru', ['ekochetkov@tpai.ru'], "Мощность превышает пороговое значение 100 на" + str(float(power)-100.0))
    if float(i.pressure) > 200000.0:
        a.text = "Давление превышает пороговое значение 200000 на " + str(float(pressure)-200000.0)
        a.device_id = i.device_id
        db.session.add(a)
        db.session.commit()
        #send_email('Превышение давления!', 'no-reply@tpai.ru', ['ekochetkov@tpai.ru'], "Давление превышает пороговое значение 200000 на " + str(float(pressure)-200000.0))
        
    indicator = i.query.filter_by(device_id=1).first()
    return render_template('json_show.html', data=indicator.timestamp)
    
    #return "Finished"
    #return "Устройство " + device_id + "temp_insde " + str(temp_insde) + " temp_outside_first " + str(temp_outside_first) + " temp_outside_second " + str(temp_outside_second) + " temp_outside_third " + str(temp_outside_third) + " temp_outside_fourth " + str(temp_outside_fourth)
    
@app.route('/show_json/<device_id>')
def show_json(device_id):
    device = Device.query.filter_by(id=device_id).first_or_404()

    i = Indicator()
    r = requests.get(device.url_sensor_device)
    if r.status_code == 200:
        r = r.json()
        i.temp_inside = r['temp_inside']
        i.temp_outside_first = r['temp_outside_first']
        i.temp_outside_second = r['temp_outside_second']
        i.temp_outside_third = r['temp_outside_third']
        i.temp_outside_fourth = r['temp_outside_fourth']
        i.distance = r['distance']
        i.power = r['power']
        i.pressure = int(float(r['pressure_bmp180'])) / 100
        i.speed = r['speed']
        i.temp_in = r['temp_in']
        i.temp_out = r['temp_out']
        i.temp_all = r['temp_all']
    else:
        i.temp_inside = -1
        i.temp_outside_first = -1
        i.temp_outside_second = -1
        i.temp_outside_third = -1
        i.temp_outside_fourth = -1 
        i.distance =-1
        i.power = -1
        i.pressure = -1
        i.speed = -1
        i.temp_in = -1
        i.temp_out = -1
        i.temp_all = -1   

    i.device_id = device_id

    r = requests.get(device.url_relay_device)
    if r.status_code == 200:
        #TODO: костыль из-за старой версии прошивки реле
        r = r.text
        r = r.replace('"relay 6": 0 "sensor 1"', '"relay 6": 0, "sensor 1"').replace('"relay 6": 1 "sensor 1"', '"relay 6": 1, "sensor 1"')
        r = json.loads(r)

        i.relay1_state = False if r['relay 1'] == 1 else True
        i.relay2_state = False if r['relay 2'] == 1 else True
        i.relay3_state = False if r['relay 3'] == 1 else True
        i.relay4_state = False if r['relay 4'] == 1 else True
        i.relay5_state = False if r['relay 5'] == 1 else True
        i.relay6_state = False if r['relay 6'] == 1 else True

        current_mult =  1.0 / 1024 * 30 / 2 * 1.2 #5.0 / 1024.0 * 0.707 / 66 * 1000

        i.relay1_current = 0 if float(r['sensor 1']) <= 120 else float(r['sensor 1']) * current_mult
        i.relay2_current = 0 if float(r['sensor 2']) <= 120 else float(r['sensor 2']) * current_mult
        i.relay3_current = 0 if float(r['sensor 3']) <= 120 else float(r['sensor 3']) * current_mult
        i.relay4_current = 0 if float(r['sensor 4']) <= 120 else float(r['sensor 4']) * current_mult
        i.relay5_current = 0 if float(r['sensor 5']) <= 120 else float(r['sensor 5']) * current_mult
        i.relay6_current = 0 if float(r['sensor 6']) <= 120 else float(r['sensor 6']) * current_mult
    else:
        i.relay1_state = False
        i.relay2_state = False
        i.relay3_state = False
        i.relay4_state = False 
        i.relay5_state = False 
        i.relay6_state = False  

        i.relay1_current = 0 
        i.relay2_current = 0
        i.relay3_current = 0
        i.relay4_current = 0 
        i.relay5_current = 0 
        i.relay6_current = 0 

    if device.relay1_state is None:
        device.relay1_state =  i.relay1_state

    if device.relay2_state is None:
        device.relay2_state =  i.relay2_state

    if device.relay3_state is None:
        device.relay3_state =  i.relay3_state

    if device.relay4_state is None:
        device.relay4_state =  i.relay4_state

    if device.relay5_state is None:
        device.relay5_state =  i.relay5_state

    if device.relay6_state is None:
        device.relay6_state =  i.relay6_state

    device.status = True if device.relay1_state or device.relay2_state or device.relay3_state or device.relay4_state or device.relay5_state or device.relay6_state else False


    if (device.relay1_state != i.relay1_state):
        if (device.relay1_state):
            requests.get(device.url_relay_device + 'relay1on')    
        else:
            requests.get(device.url_relay_device + 'relay1off')

    if (device.relay2_state != i.relay2_state):
        if (device.relay2_state):
            requests.get(device.url_relay_device + 'relay2on')    
        else:
            requests.get(device.url_relay_device + 'relay2off')

    if (device.relay3_state != i.relay3_state):
        if (device.relay3_state):
            requests.get(device.url_relay_device + 'relay3on')    
        else:
            requests.get(device.url_relay_device + 'relay3off')

    if (device.relay4_state != i.relay4_state):
        if (device.relay4_state):
            requests.get(device.url_relay_device + 'relay4on')    
        else:
            requests.get(device.url_relay_device + 'relay4off')

    if (device.relay5_state != i.relay5_state):
        if (device.relay5_state):
            requests.get(device.url_relay_device + 'relay5on')    
        else:
            requests.get(device.url_relay_device + 'relay5off')

    if (device.relay6_state != i.relay6_state):
        if (device.relay6_state):
            requests.get(device.url_relay_device + 'relay6on')    
        else:
            requests.get(device.url_relay_device + 'relay6off')

    #получаеми хэшрейты
    i.hashrate_poolbtccom = 0
    if (not device.apikey_poolbtccom is None and device.apikey_poolbtccom != ""):
        r = requests.get("https://eu-pool.api.btc.com/v1/realtime/hashrate?access_key="+device.apikey_poolbtccom+"&puid="+device.puid_poolbtccom)
        if r.status_code == 200:
            print(r.text)
            r = r.json()
            if (r["err_no"] == 0):
                i.hashrate_poolbtccom = float(r["data"]["shares_15m"])
            

    

    #antpool
    i.hashrate_antpool = 0
    if (not device.apikey_antpool is None and device.apikey_antpool != ""):
        nonce=int(time.time()*1000)
        msgs=device.userid_antpool+device.apikey_antpool+str(nonce)
        api_sign=[]
        api_sign.append(hmac.new(device.secret_antpool.encode(encoding="utf-8"), msg=msgs.encode(encoding="utf-8"), digestmod=hashlib.sha256).hexdigest().upper())
        api_sign.append(nonce)

        post_data = {'key': device.apikey_antpool, 'nonce': api_sign[1],'signature': api_sign[0],'coin': device.coin_antpool}
        r = requests.post("https://antpool.com/api/hashrate.htm", data=post_data)

        if r.status_code == 200:
            r = r.json()
            if r["code"] == 0:
                try:
                    i.hashrate_antpool = int(r["data"]["last10m"])
                except:
                    pass

    i.hashrate_viabtc = 0

    i.hashrate_f2pool = 0
    if (not device.apikey_f2pool is None and device.apikey_f2pool != ""):
        r = requests.get("http://api.f2pool.com/bitcoin/"+device.apikey_f2pool)
        if r.status_code == 200:
            r = r.json()
            try:
                i.hashrate_f2pool = int(r["hashrate"])
            except:
                pass   

    i.hashrate_slushpool = 0

    if (not device.apikey_slushpool is None and device.apikey_slushpool != ""):
        r = requests.get("https://slushpool.com/accounts/profile/json/"+device.apikey_slushpool)
        if r.status_code == 200 and r.text != "Invalid token":
            r = r.json()
            try:
                i.hashrate_slushpool = int(r["workers"][r["username"] + "." + device.worker_slushpool]["hashrate"])
            except:
                pass

    i.hashrate_total = i.hashrate_poolbtccom + i.hashrate_antpool + i.hashrate_viabtc + i.hashrate_f2pool + i.hashrate_slushpool 
    device.hash_rate = i.hashrate_total

    db.session.add(i)
    db.session.commit()

    # Некоторое количество говнокода
    a = Alert()
    if float(i.temp_inside) > 75.0:
        a.text = "Внутренняя температура превышает пороговое значение в 75 градусов на " + str(float(r['temp_inside'])-75.0) + "градусов"
        a.device_id = i.device_id
        db.session.add(a)
        db.session.commit()
        send_email('Превышение температуры!', 'no-reply@tpai.ru', ['ekochetkov@tpai.ru'], "Внутренняя температура превышает пороговое значение в 75 градусов на " + str(float(r['temp_inside'])-75.0) + "градусов")
    if float(i.temp_outside_first) > 70.0:
        a.text = "Температура первого датчика превышает пороговое значение в 70 градусов на " + str(float(r['temp_outside_first'])-70.0) + "градусов"
        a.device_id = i.device_id
        db.session.add(a)
        db.session.commit()
        send_email('Превышение температуры!', 'no-reply@tpai.ru', ['ekochetkov@tpai.ru'], "Температура первого датчика превышает пороговое значение в 70 градусов на " + str(float(r['temp_outside_first'])-70.0) + "градусов")
    if float(i.temp_outside_second) > 65.0:
        a.text = "Температура второго датчика превышает пороговое значение в 65 градусов на " + str(float(r['temp_outside_second'])-65.0) + "градусов"
        a.device_id = i.device_id
        db.session.add(a)
        db.session.commit()
        send_email('Превышение температуры!', 'no-reply@tpai.ru', ['ekochetkov@tpai.ru'], "Температура второго датчика превышает пороговое значение в 65 градусов на " + str(float(r['temp_outside_second'])-65.0) + "градусов")
    if float(i.temp_outside_third) > 60.0:
        a.text = "Температура третьего датчика превышает пороговое значение в 60 градусов на " + str(float(r['temp_outside_third'])-60.0) + "градусов"
        a.device_id = i.device_id
        db.session.add(a)
        db.session.commit()
        send_email('Превышение температуры!', 'no-reply@tpai.ru', ['ekochetkov@tpai.ru'], "Температура третьего датчика превышает пороговое значение в 60 градусов на " + str(float(r['temp_outside_third'])-60.0) + "градусов")
    if float(i.temp_outside_fourth) > 60.0:
        a.text = "Температура четвёртого датчика превышает пороговое значение в 60 градусов на " + str(float(r['temp_outside_fourth'])-60.0) + "градусов"
        a.device_id = i.device_id
        db.session.add(a)
        db.session.commit()
        send_email('Превышение температуры!', 'no-reply@tpai.ru', ['ekochetkov@tpai.ru'], "Температура четвёртого датчика превышает пороговое значение в 60 градусов на " + str(float(r['temp_outside_fourth'])-60.0) + "градусов")
    if float(i.distance) > 199.0:
        a.text = "Расстояние до жидкости превышает пороговое значение 199 на " + str(float(r['distance'])-199.0)
        a.device_id = i.device_id
        db.session.add(a)
        db.session.commit()
        send_email('Расстояние до жидкости!', 'no-reply@tpai.ru', ['ekochetkov@tpai.ru'], "Расстояние до жидкости превышает пороговое значение 199 на " + str(float(r['distance'])-199.0))
    if float(i.power) > 100.0:
        a.text = "Мощность превышает пороговое значение 100 на" + str(float(r['power'])-100.0)
        a.device_id = i.device_id
        db.session.add(a)
        db.session.commit()
        send_email('Мощность!', 'no-reply@tpai.ru', ['ekochetkov@tpai.ru'], "Мощность превышает пороговое значение 100 на" + str(float(r['power'])-100.0))
    if float(i.pressure) > 200000.0:
        a.text = "Давление превышает пороговое значение 200000 на " + str(float(r['pressure'])-200000.0)
        a.device_id = i.device_id
        db.session.add(a)
        db.session.commit()
        send_email('Превышение давления!', 'no-reply@tpai.ru', ['ekochetkov@tpai.ru'], "Давление превышает пороговое значение 200000 на " + str(float(r['pressure'])-200000.0))
    #if float(r['speed']) > 0.0:
    #    a.text = "Скорость превышает пороговое значение в 0 на " + str(float(r['temp_outside_fourth'])-0.0)
    #    a.device_id = i.device_id
    #    db.session.add(a)
     #   db.session.commit()
    #if float(r['temp_in']) > 0.0:
    #    a.text = "Температура внутри превышает пороговое значение в 0 градусов на " + str(float(r['temp_in'])-0.0) + "градусов"
    #    a.device_id = i.device_id
    #    db.session.add(a)
    #    db.session.commit()
    #if float(r['temp_out']) > 0.0:
    #    a.text = "Температура снаружи превышает пороговое значение в 0 градусов на " + str(float(r['temp_out'])-0.0) + "градусов"
    #    a.device_id = i.device_id
    #    db.session.add(a)
    #    db.session.commit()
    #if float(r['temp_all']) > 0.0:
    #    a.text = "Температура общая превышает пороговое значение в 0 градусов на " + str(float(r['temp_all'])-0.0) + "градусов"
    #    a.device_id = i.device_id
    #    db.session.add(a)
    #    db.session.commit()
    
    indicator = i.query.filter_by(device_id=1).first()
    return render_template('json_show.html', data=indicator.timestamp)


@app.route('/disallow')
@login_required
def disallow():
    return render_template('disallow.html', title='Недостаточно прав')

@app.route('/alert')
@login_required
def alert():
    alerts = Alert.query.all()
    page = request.args.get('page', 1, type=int)
    alerts = Alert.query.order_by(Alert.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('alert', page=alerts.next_num) \
        if alerts.has_next else None
    prev_url = url_for('alert', page=alerts.prev_num) \
        if alerts.has_prev else None
    return render_template("alert.html", title='Оповещения о событиях', alerts=alerts.items, next_url=next_url, prev_url=prev_url)
  
@app.route('/edit_device/<device_id>', methods=['GET', 'POST'])
@login_required
def edit_device(device_id):
    device = Device.query.filter_by(id=device_id).first_or_404()

    form = EditDeviceForm(request.form)
    if request.method == 'POST':
        device.serial_num = form.serial_num.data
        device.device_type = form.device_type.data
        device.addition = form.addition.data

        device.apikey_poolbtccom = form.apikey_poolbtccom.data
        device.puid_poolbtccom = form.puid_poolbtccom.data

        device.apikey_antpool = form.apikey_antpool.data
        device.secret_antpool = form.secret_antpool.data
        device.userid_antpool = form.userid_antpool.data
        device.coin_antpool = form.coin_antpool.data

        device.apikey_viabtc = form.apikey_viabtc.data
        device.apikey_f2pool = form.apikey_f2pool.data

        device.apikey_slushpool = form.apikey_slushpool.data
        device.worker_slushpool = form.worker_slushpool.data
        

        device.url_sensor_device = form.url_sensor_device.data
        device.url_relay_device = form.url_relay_device.data

        db.session.commit()
        flash('Ваши изменения применены')
        return redirect(url_for('device_info', device_id=device_id))
    elif request.method == 'GET':
        form.serial_num.data = device.serial_num
        form.device_type.data = device.device_type
        form.addition.data = device.addition

        form.apikey_poolbtccom.data = device.apikey_poolbtccom 
        form.puid_poolbtccom.data = device.puid_poolbtccom 

        form.apikey_antpool.data = device.apikey_antpool
        form.secret_antpool.data = device.secret_antpool
        form.userid_antpool.data = device.userid_antpool
        form.coin_antpool.data = device.coin_antpool
        

        form.apikey_viabtc.data = device.apikey_viabtc
        form.apikey_f2pool.data = device.apikey_f2pool

        form.apikey_slushpool.data = device.apikey_slushpool
        form.worker_slushpool.data = device.worker_slushpool

        form.url_sensor_device.data = device.url_sensor_device
        form.url_relay_device.data = device.url_relay_device

    return render_template('edit_device.html', title='Редактировать устройство',
                           form=form)

    
@app.route('/attribute/<device_id>')
@login_required
def attribute(device_id):
    page = request.args.get('page', 1, type=int)
    attributes = Indicator.query.filter_by(device_id=device_id).order_by(Indicator.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('attribute', device_id=device_id, page=attributes.next_num) \
        if attributes.has_next else None
    prev_url = url_for('attribute', device_id=device_id, page=attributes.prev_num) \
        if attributes.has_prev else None
    return render_template("indicator.html", title='Состояние устройств', attributes=attributes.items, next_url=next_url, prev_url=prev_url)

@app.route('/device_info/<device_id>')
@login_required
def device_info(device_id):
    attribute = Indicator.query.filter_by(device_id=device_id).order_by("timestamp desc").first()
    device = Device.query.filter_by(id=device_id).first_or_404()
    attribute.pressure = round(attribute.pressure / 1000, 4)
    return render_template("device_info.html", title='Информация об устройстве', attribute=attribute, device=device)
    
#@app.route('/relay_status/<device_id>')
#@login_required
#def relay_status(device_id):
#    device = Device.query.filter_by(id=device_id).first_or_404()
#    if (device.relay1_state == True):
#        rel1 = "1"
#    else:
#        rel1 = "0"
#    if (device.relay2_state == True):
#        rel2 = "1"
#    else:
#        rel2 = "0"
#    if (device.relay3_state == True):
#        rel3 = "1"
#    else:
#        rel3 = "0"
#    return "relay_1:" + rel1 + " relay_2:" + rel2 + " relay_3:" + rel3

@app.route('/device_info/<device_id>/attrs_json/<count>')
@login_required
def attrs_json(device_id, count):
    attribute = Indicator.query.order_by("timestamp desc").filter_by(device_id=device_id).limit(int(count)*100).all()
    attribute_new = []
    for idx, elem in enumerate(attribute):
        if idx % 100 == 0 or idx == len(attribute) - 1:
            attribute_new = [elem] + attribute_new
    return jsonify(json_list=[i.serialize for i in attribute_new])

@app.route('/user_info')
@login_required
def user_info():
    users = User.query.all()
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.id.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', page=users.next_num) \
        if users.has_next else None
    prev_url = url_for('alert', page=users.prev_num) \
        if users.has_prev else None
    return render_template("users.html", title='Списки пользователей', users=users.items, next_url=next_url, prev_url=prev_url)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(request.form)
    if request.method == 'POST':
        current_user.username = form.username.data
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.phone_num = form.phone_num.data

        db.session.commit()
        flash('Ваши изменения применены')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.phone_num.data = current_user.phone_num

    return render_template('edit_profile.html', title='Редактировать профиль',
                           form=form)

@app.route('/contact_request', methods=['GET', 'POST'])
@login_required
def contact_request():
    form = ContactUsForm()
    if form.validate_on_submit():
        send_email('Обратная связь с сайта', 'no-reply@tpai.ru', ['ekochetkov@tpai.ru', 'info@immersium.ru'], 
            form.name.data + ":" + form.email.data + ":" + form.email_text.data)
    
        return render_template('contactus.html',
                    title='Связаться с нами', form=form, message = "Сообщение успешно отправлено!")
    else:
        return render_template('contactus.html',
                    title='Связаться с нами', form=form)        

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.lower()).first()
        if user is None or not user.check_password(form.password.data):
            flash('Некорректное имя пользователя или пароль')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Вход в личный кабинет', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))