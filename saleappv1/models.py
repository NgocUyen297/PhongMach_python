import json
from sqlalchemy import Column, Integer, String, Float, Enum, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from saleappv1 import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from enum import Enum as UserEnum


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class UserRole(UserEnum):
    ADMIN = 1
    USER = 2


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100))
    email = Column(String(50))
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    details = relationship('ListDetail', backref='user', lazy=True)
    bills = relationship('Bills', backref='user', lazy=True)

    def __str__(self):
        return self.name


class ListSchedule(BaseModel):
    __tablename__ = 'listschedule'
    created_date = Column(DateTime, default=datetime.now(), nullable=False)
    details = relationship('ListDetail', backref='listschedule', lazy=True)


class ListDetail(db.Model):
    list_schedule_id = Column(Integer, ForeignKey(ListSchedule.id), nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False, primary_key=True)
    name = Column(String(50), nullable=False)
    gender = Column(String(20), default='Nam')
    year_born = Column(String(20))
    address = Column(String(100))



# Yêu cầu 2

class MedicallBillDetail(db.Model): # bảng sinh ra từ Medicine và MedicalBil
    medicine_id = Column(Integer, ForeignKey('medicine.id'), nullable=False, primary_key=True) #id thuốc
    medicalbill_id = Column(Integer, ForeignKey('medicalbill.id'), nullable=False, primary_key=True) #id phiếu thuốc
    quantity = Column(Integer, nullable=False, default=1) #số lượng thuốc

    def __str__(self):
        return self.name


class Medicine(BaseModel): # thuốc
    __tablename__ = 'medicine'
    name = Column(String(50), nullable=False) #tên thuốc
    unit = Column(String(20), nullable=False) #đơn vị thuốc
    TienThuoc = Column(Float, default=0)
    how_to_use = Column(String(500))
    details = relationship('MedicallBillDetail', backref='medicine', lazy=True)

    def __str__(self):
        return self.name


class MedicalBill(BaseModel): # phiếu khám bệnh
    __tablename__ = 'medicalbill'
    name = Column(String(50), nullable=False) # tên của người bệnh
    created_day = Column(DateTime, default=datetime.now()) #ngày lập
    symptom = Column(String(100))  # triệu chứng
    prognostication = Column(String(100)) # dự đoán bệnh
    total_amount = Column(Float, default=0)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('MedicallBillDetail', backref='medicalbill', lazy=True)

    def __str__(self):
        return self.name

#hết yêu cầu 2

class Bills(BaseModel):
    __tablename__ = 'bills'

    name = Column(String(50), nullable=False) #tên của bệnh nhân
    examined_date = Column(DateTime, nullable=False) #ngày khám bệnh
    TienKham = Column(Float, default=100.000)
    TienThuoc = Column(Float, default=0)
    state_pay = Column(Boolean, default=False)  # true là thanh toán rồi, false là chưa thanh toán
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    medical_bill_id = Column(Integer, ForeignKey(MedicalBill.id), nullable=False)


if __name__ == '__main__':
    db.create_all()

