from flask import render_template, url_for, request, redirect
from flaskr import app
from flaskr.models import *
from flaskr import db
from datetime import datetime


@app.route('/')
@app.route('/statistics')
def index():
    protocols = Protocol.query.order_by(Protocol.aspiration_date).all()
    return render_template('index.html', protocols=protocols)


@app.route('/enter_protocol', methods=['POST', 'GET'])
def enter_protocol():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        embryologist_id = request.form['embryologist_id']
        doctor_id = request.form['doctor_id']
        oocytes_number = request.form['oocytes_number']
        fert_oocytes_number = request.form['fert_oocytes_number']
        fertilization_rate = int(fert_oocytes_number)/int(oocytes_number) * 100
        aspiration_date = datetime.strptime(
            request.form['aspiration_date'],
            '%Y-%m-%d')

        protocol = Protocol(
            patient_id=patient_id,
            embryologist_id=embryologist_id,
            doctor_id=doctor_id,
            aspiration_date=aspiration_date,
            oocytes_number=oocytes_number,
            fert_oocytes_number=fert_oocytes_number,
            fertilization_rate=fertilization_rate
        )

        try:
            db.session.add(protocol)
            db.session.commit()
            return redirect('/statistics')
        except Exception as e:
            return str(e)
    else:
        patients = Patient.query.order_by(Patient.id).all()
        embryologists = Embryologist.query.order_by(Embryologist.id).all()
        doctors = Doctor.query.order_by(Doctor.id).all()
        return render_template('enter_protocol.html', patients=patients, embryologists=embryologists, doctors=doctors)


@app.route('/statistics/<int:id>/update', methods=['POST', 'GET'])
def update_protocol(id):
    protocol = Protocol.query.get(id)
    if request.method == 'POST':
        protocol.patient_id = request.form['patient_id']
        protocol.embryologist_id = request.form['embryologist_id']
        protocol.doctor_id = request.form['doctor_id']
        protocol.oocytes_number = request.form['oocytes_number']
        protocol.fert_oocytes_number = request.form['fert_oocytes_number']
        protocol.fertilization_rate = int(protocol.fert_oocytes_number) / int(protocol.oocytes_number) * 100
        protocol.aspiration_date = datetime.strptime(
            request.form['aspiration_date'],
            '%Y-%m-%d')

        try:
            db.session.commit()
            return redirect('/statistics')
        except Exception as e:
            return str(e)
    else:
        patients = Patient.query.order_by(Patient.id).all()
        embryologists = Embryologist.query.order_by(Embryologist.id).all()
        doctors = Doctor.query.order_by(Doctor.id).all()
        protocol = Protocol.query.get(id)
        return render_template('edit_protocol.html', protocol=protocol, patients=patients, embryologists=embryologists, doctors=doctors)


@app.route('/protocol_deleting/<int:id>/del')
def delete_protocol(id):
    protocol = Protocol.query.get_or_404(id)
    try:
        db.session.delete(protocol)
        db.session.commit()
        return redirect('/statistics')
    except Exception as e:
        return str(e)


@app.route('/patients')
def patients():
    patients = Patient.query.order_by(Patient.id).all()
    return render_template('patients.html', patients=patients)


@app.route('/embryologists')
def embryologists():
    embryologists = Embryologist.query.order_by(Embryologist.id).all()
    return render_template('embryologists.html', embryologists=embryologists)


@app.route('/doctors')
def doctors():
    doctors = Doctor.query.order_by(Doctor.id).all()
    return render_template('doctors.html', doctors=doctors)


@app.route('/enter_doctor', methods=['POST', 'GET'])
def enter_doctor():
    if request.method == 'POST':
        name = request.form['name']
        medical_specialty = request.form['medical_specialty']

        if name == '' or medical_specialty == '':
            return redirect('/enter_doctor')

        doctor = Doctor(name=name, medical_specialty=medical_specialty)

        try:
            db.session.add(doctor)
            db.session.commit()
            return redirect('/doctors')
        except Exception as e:
            return str(e)
    else:
        return render_template('enter_doctor.html')


@app.route('/doctors/<int:id>/update', methods=['POST', 'GET'])
def update_doctor(id):
    doctor = Doctor.query.get(id)
    if request.method == 'POST':
        doctor.name = request.form['name']
        doctor.medical_specialty = request.form['medical_specialty']

        if doctor.name == '' or doctor.medical_specialty == '':
            return redirect(f'/doctors/{id}/update')

        try:
            db.session.commit()
            return redirect('/doctors')
        except Exception as e:
            return str(e)
    else:
        return render_template('edit_doctor.html', doctor=doctor)


@app.route('/d_deleting/<int:id>/del')
def delete_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    try:
        db.session.delete(doctor)
        db.session.commit()
        return redirect('/doctors')
    except Exception as e:
        return str(e)


@app.route('/enter_embryologist', methods=['POST', 'GET'])
def enter_embryologist():
    if request.method == 'POST':
        name = request.form['name']
        work_clinic = request.form['work_clinic']
        education = request.form['education']

        if name == '' or work_clinic == '' or education == '':
            return redirect('/enter_embryologist')

        embryologist = Embryologist(name=name, work_clinic=work_clinic, education=education)

        try:
            db.session.add(embryologist)
            db.session.commit()
            return redirect('/embryologists')
        except Exception as e:
            return str(e)
    else:
        return render_template('enter_embryologist.html')


@app.route('/embryologists/<int:id>/update', methods=['POST', 'GET'])
def update_embryologist(id):
    embryologist = Embryologist.query.get(id)
    if request.method == 'POST':
        embryologist.name = request.form['name']
        embryologist.work_clinic = request.form['work_clinic']
        embryologist.education = request.form['education']

        if embryologist.name == '' or embryologist.work_clinic == '' or embryologist.education == '':
            return redirect(f'/embryologists/{id}/update')

        try:
            db.session.commit()
            return redirect('/embryologists')
        except Exception as e:
            return str(e)
    else:
        return render_template('edit_embryologist.html', embryologist=embryologist)


@app.route('/e_deleting/<int:id>/del')
def delete_embryologist(id):
    embryologist = Embryologist.query.get_or_404(id)
    try:
        db.session.delete(embryologist)
        db.session.commit()
        return redirect('/embryologists')
    except Exception as e:
        return str(e)


@app.route('/enter_patient', methods=['POST', 'GET'])
def enter_patient():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']

        if name == '' or age == '':
            return redirect('/enter_patient')

        patient = Patient(name=name, age=age)

        try:
            db.session.add(patient)
            db.session.commit()
            return redirect('/patients')
        except Exception as e:
            return str(e)
    else:
        return render_template('enter_patient.html')


@app.route('/patients/<int:id>/update', methods=['POST', 'GET'])
def update_patient(id):
    patient = Patient.query.get(id)
    if request.method == 'POST':
        patient.name = request.form['name']
        patient.age = request.form['age']

        if patient.name == '' or patient.age == '':
            return redirect(f'/patients/{id}/update')

        try:
            db.session.commit()
            return redirect('/patients')
        except Exception as e:
            return str(e)
    else:
        return render_template('edit_patient.html', patient=patient)


@app.route('/p_deleting/<int:id>/del')
def delete_patient(id):
    patient = Patient.query.get_or_404(id)
    try:
        db.session.delete(patient)
        db.session.commit()
        return redirect('/patients')
    except Exception as e:
        return str(e)







