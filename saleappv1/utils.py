import json, os
from saleappv1 import app
from saleappv1.models import *
from datetime import datetime
from flask_login import current_user
from sqlalchemy import func
from sqlalchemy.sql import extract
import hashlib
from saleappv1 import db
from sqlalchemy.sql import extract
from saleappv1.models import ListDetail


def read_json(path):
    with open(path, "r") as f:
        return json.load(f)


def add_user(name, username, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name.strip(),
                username=username.strip(),
                password=password,
                email=kwargs.get('email'),
                avatar=kwargs.get('avatar'))

    db.session.add(user)
    db.session.commit()


def check_login(username, password, role=UserRole.USER):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password),
                                 User.user_role.__eq__(role)).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def add_schedule(created_date, name, **kwargs):
    list = ListSchedule(created_date=created_date)
    db.session.add(list)
    db.session.commit()

    d = ListDetail(list_schedule_id=list.id, user=current_user,
                   name=name.strip(),
                   gender=kwargs.get('gender'),
                   year_born=kwargs.get('year_born'),
                   address=kwargs.get('address'))
    db.session.add(d)
    db.session.commit()


def read_medicine():
    return Medicine.query.all()


def get_created_date():
    return db.session.query(extract('created_day', ListSchedule.created_date))


def count_schedule_by_date(created_date='1212-12-12'):
    return db.session.query(ListSchedule.id, ListSchedule.created_date) \
        .join(ListDetail, ListDetail.list_schedule_id.__eq__(ListSchedule.id)) \
        .filter(ListSchedule.created_date == created_date) \
        .group_by(ListSchedule.id, ListSchedule.created_date).all()


# chức năng 3
def sum_money(tien_kham, tien_thuoc):
    return tien_kham + tien_thuoc


def load_list_bills(user_id=1):
    return Bills.query.filter(Bills.user_id.__eq__(user_id))


def reload_state_pay(bill_id):
    p = Bills.query.filter(Bills.id.__eq__(bill_id)).first()
    p.state_pay = True
    db.session.commit()

def count_cart(cart):
    total_amount = 0

    if cart:
        for c in cart.values():
            total_amount += c['quantity'] * c['TienThuoc']

    return total_amount


def add_Bills(medicalBill):
    user = get_user_by_id(medicalBill.user_id)
    bill = Bills(name=user.name, examined_date=medicalBill.created_day,
                 TienThuoc=medicalBill.total_amount,
                 user_id=user.id,
                 medical_bill_id=medicalBill.id)
    db.session.add(bill)
    db.session.commit()


def add_MedicalBill(name, created_date, symptom, prognostication, cart):
    total_amount = count_cart(cart)

    medicinalBill = MedicalBill(name=name, created_day=created_date,
                                symptom=symptom,
                                prognostication=prognostication,
                                total_amount=total_amount,
                                user_id=current_user.id)
    db.session.add(medicinalBill)
    db.session.commit()
    # tạo một cái bill
    add_Bills(medicalBill=medicinalBill)

    # tạo những cái details
    for c in cart.values():
        medicalBillDetail = MedicallBillDetail(medicalbill_id=medicinalBill.id,
                                               medicine_id=c['id'],
                                               quantity=c['quantity'])
    db.session.add(medicalBillDetail)
    db.session.commit()


def get_medicine_by_id(id):
    return Medicine.query.get(id)


def bill_stats(kw=None, from_date=None, to_date=None):
    p = db.session.query(Bills.id, Bills.name,
                         func.sum(Bills.TienKham + Bills.TienThuoc))

    if kw:
        p = p.filter(Bills.name.contains(kw))
    if from_date:
        p = p.filter(Bills.Adate1.__ge__(from_date))
    if to_date:
        p = p.filter(Bills.Adate1.__ge__(to_date))
    return p.all()


def bill_month_stats(year):
    return db.session.query(extract('month', Bills.examined_date), func.sum(Bills.TienKham + Bills.TienThuoc)) \
        .filter(extract('year', Bills.examined_date) == year) \
        .group_by(extract('month', Bills.examined_date))\
        .order_by(extract('month', Bills.examined_date)).all()


def medicine_month_stats(kw =None,from_date=None, to_date=None):
    p = db.session.query(Medicine.id, Medicine.name, func.sum(MedicallBillDetail.quantity * Medicine.TienThuoc))\
                    .join(MedicallBillDetail, MedicallBillDetail.medicine_id.__eq__(Medicine.id), isouter=True)\
                    .join(MedicalBill, MedicalBill.id.__eq__(MedicallBillDetail.medicalbill_id))\
                    .group_by(Medicine.id, Medicine.name)

    if kw:
        p = p.filter(Medicine.name.contains(kw))
    if from_date:
        p = p.filter(MedicalBill.created_day.__eq__(from_date))
    if to_date:
        p = p.filter(MedicalBill.created_day.__eq__(to_date))
    return p.all()