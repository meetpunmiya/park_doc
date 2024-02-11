
Conversation opened. 1 unread message.

Skip to content
Using Karnavati University Mail with screen readers

1 of 2,185
(no subject)
Inbox

Pratham Savaliya
05:58 (0 minutes ago)
to me

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import date, datetime
from urllib.parse import quote
from sqlalchemy.exc import IntegrityError
import requests
import vonage

app = Flask(__name__)
password = 'Pratham123123@'
encoded_password = quote(password, safe='')
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{encoded_password}@localhost:3306/park_automation'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class VehicleRegister(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_number = db.Column(db.String(20), nullable=False)
    date = db.Column(db.Date, nullable=False)
    intime = db.Column(db.Time, nullable=False)
    in_status = db.Column(db.Boolean, nullable=False)
    outtime = db.Column(db.Time, nullable=True)
    out_status = db.Column(db.Boolean, nullable=True)

class UserRegister(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    mobile_number = db.Column(db.String(20), nullable=False)
    vehicle_number = db.Column(db.String(20), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return render_template('index.html', error='No file part')

    file = request.files['file']

    if file.filename == '':
        return render_template('index.html', error='No selected file')

    api_key = '33784bb65249af222949eee9998cabc54e9a5fce'
    url = 'https://api.platerecognizer.com/v1/plate-reader/'
    files = {'upload': file.read()}
    headers = {'Authorization': f'Token {api_key}'}

    response = requests.post(url, files=files, headers=headers)
    response.raise_for_status()
    result = response.json()

    plate_info = 'No license plate detected.'
    if 'results' in result and result['results']:
        plate_info = result['results'][0].get('plate', 'N/A')

    try:
        existing_entry = VehicleRegister.query.filter_by(vehicle_number=plate_info, date=date.today(), in_status=True).first()
        ## if no entry found for the vehicle number, create a new entry
        if not existing_entry:
            new_entry = VehicleRegister(vehicle_number=plate_info, date=date.today(), intime=datetime.now().time(), in_status=True, outtime=None, out_status=False)
            db.session.add(new_entry)
            db.session.commit()

            # if UserRegister.query.filter_by(vehicle_number=plate_info).first() and new_entry.in_status:
            client = vonage.Client(key="adc25a78", secret="6UbB1dm2zi3kEZPS")
            sms = vonage.Sms(client)
            car_number = plate_info
            message = f"Your car {car_number} is parked at park_smart at {new_entry.intime}"
            responseData = sms.send_message({"from": "Vonage APIs",
                                             "to": "919104961321",
                                              "text": message})
            if responseData["messages"][0]["status"] == "0":
                print("Message sent successfully.")
            else:
                print(f"Message failed with error: {responseData['messages'][0]['error-text']}")

            print("Message sent successfully.")
        else:
            # if entry found for the vehicle number, update the outtime and out_status
            existing_entry.outtime = datetime.now().time()
            existing_entry.out_status = True
            existing_entry.in_status = False
            db.session.commit()

            # if UserRegister.query.filter_by(vehicle_number=plate_info).first() and existing_entry.out_status:
            client = vonage.Client(key="adc25a78", secret="6UbB1dm2zi3kEZPS")
            sms = vonage.Sms(client)
            car_number = plate_info
            time_difference = datetime.combine(date.today(), existing_entry.outtime) - datetime.combine(date.today(), existing_entry.intime)
            message = f"Your car {car_number} was parked at park_doc for {time_difference}"
            responseData = sms.send_message({"from": "Vonage APIs", "to": "919104961321", "text": message})
            if responseData["messages"][0]["status"] == "0":
                print("Message sent successfully.")
            else:
                print(f"Message failed with error: {responseData['messages'][0]['error-text']}")
    except IntegrityError as e:
        db.session.rollback()
        print(f"IntegrityError: {e}")

    ret = {'plate_info': plate_info,
           'date': date.today().strftime('%Y-%m-%d'),
           'time': datetime.now().strftime('%H:%M:%S')}

    return render_template('result.html', ret=ret)

@app.route('/view_entries')
def view_entries():
    entries = VehicleRegister.query.all()
    return render_template('view_entries.html', entries=entries)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        migrate.init_app(app, db)
    app.run(debug=True)

