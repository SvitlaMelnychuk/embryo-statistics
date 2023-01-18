from flaskr import db
from datetime import datetime


class Embryologist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    work_clinic = db.Column(db.String(300), nullable=False)
    education = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Embryologist %r>' % self.id


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Patient %r>' % self.id


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    medical_specialty = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Doctor %r>' % self.id


class Protocol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient = db.relationship('Patient', backref='protocol', lazy=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    embryologist = db.relationship('Embryologist', backref='protocol', lazy=False)
    embryologist_id = db.Column(db.Integer, db.ForeignKey('embryologist.id'))
    doctor = db.relationship('Doctor', backref='protocol', lazy=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    aspiration_date = db.Column(db.DateTime, default=datetime.utcnow())
    oocytes_number = db.Column(db.Integer, nullable=False)
    fert_oocytes_number = db.Column(db.Integer, nullable=False)
    fertilization_rate = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Protocol %r>' % self.id

