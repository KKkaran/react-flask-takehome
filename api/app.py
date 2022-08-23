
from crypt import methods
from wsgiref.validate import validator
from sqlalchemy_utils import ChoiceType
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, json, render_template
from flask_restx import Resource, fields, Api
from flask_cors import CORS
from loggingFile import *
from utils.sendEmail import *

app = Flask(__name__)
api = Api(app)

CORS(app, resources={r"*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

TYPES = [
    ('available', 'Available'),
    ('not available', 'Not available')
]

########### MODELS #############
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email_address = db.Column(db.String(120), unique=True, nullable=False)
    availability_status = db.Column(
        ChoiceType(TYPES), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey(
        'company.id'), nullable=False)
    company = db.relationship(
        'Company', backref=db.backref('company', lazy=True))

    def __repr__(self):
        return '<User %r>' % self.name


class Schedule(db.Model):
    __tablename__ = 'schedule'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(
        'User', backref=db.backref('user', lazy=True))
    client_id = db.Column(db.Integer, db.ForeignKey(
        'client.id'), nullable=False)
    client = db.relationship(
        'Client', backref=db.backref('client', lazy=True))
    date_range = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<Schedule %r>' % self.id


class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<Schedule %r>' % self.id


class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email_address = db.Column(db.String(120), unique=True, nullable=False)

    def _repr__(self):
        return '<Client %r>' % self.name


# ########### SERIALIZERS #############
company_serializer = api.model('Model', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a company'),
    'name': fields.String(required=True, description='The name of the company')
})

user_serializer = api.model('Model', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of user'),
    'name': fields.String(required=True, description='The name of user'),
    'email_address': fields.String(required=True, description='The email address of user'),
    'availability_status': fields.String(required=True, description='The availability status of user'),
    'company': fields.Nested(company_serializer)

})

client_serializer = api.model('Model', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of client'),
    'name': fields.String(required=True, description='The name of client'),
    'email_address': fields.String(required=True, description='The email address of user'),
})

schedule_serializer = api.model('Model', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of schedule'),
    'user_id': fields.Integer(required=True, description='The unique identifier of cleaner'),
    'client_id': fields.Integer(required=True, description='The unique identifier of client'),
    'date_range': fields.String(required=True, description='The details of the shift')
})

# ########### ROUTES #############

#return me all the scheduled shifts in db
@api.route("/shifts")
class Shifts(Resource):
    @api.marshal_with(schedule_serializer, envelope='resource')
    def get(self):
        return Schedule.query.all();

@api.route("/client/<string:email>")
class ClientsByEmail(Resource):
    @api.marshal_with(client_serializer, envelope='resource')
    def get(self, email):
        return Client.query.filter_by(email_address=email).all()

#returns me all the clients in db
@api.route("/clients")
class Clients(Resource):
    @api.marshal_with(client_serializer, envelope='resource')
    def get(self):
        return Client.query.all();

@api.route('/companies')
class Companies(Resource):
    @api.marshal_with(company_serializer, envelope='resource')
    def get(self):
        return Company.query.all()


@api.route('/users/<int:company_id>')
class Users(Resource):
    @api.marshal_with(user_serializer, envelope='resource')
    def get(self, company_id):
        return User.query.filter_by(company_id=company_id).all()

# client route creating new clients uniquely identified by their email ids
@app.route("/createClient", methods=['POST'])
def createClient():
    if request.method == 'POST':
        request_data = json.loads(request.data)
        client = Client(name=request_data.get('name'),email_address=request_data.get('email'))
        db.session.add(client)
        db.session.commit()
        
        return str(client.id);

#shift route creating new shift schedule using client and user ids and the schedule
@app.route("/createShift", methods=['POST'])
def createShift():
    if request.method == 'POST':
        request_data = json.loads(request.data)
        shift = Schedule(user_id=request_data.get('user_id'),client_id=request_data.get('client_id'),date_range=request_data.get('date_range'))
        db.session.add(shift)
        db.session.commit()
        
        return str(shift.id);


@app.route("/setAppt", methods=["POST"])
def setAppt():
    if request.method == "POST":
        request_data = json.loads(request.data)
        #print(request_data['content'])
        
        #create new entitiy in db for the schedule
        #logging shift details in log file
        append_new_line('log.txt', request_data.get('client') + " scheduled " + request_data.get('cleaner') + " from "
        + request_data.get('start') + " for " + request_data.get('hours')+ " hours on " + request_data.get('date'))
        


        # db.session.add(Client(name=request_data.get('client').split("@")[0],email_address=request_data.get('client')))
        # db.session.commit()

        #send the confirmation email to the client and the cleaner
        sendConfirmationEmail(request_data.get('client'),request_data.get('cleaner').split(":")[1],
            {
                "start":request_data.get('start'),
                "end":request_data.get('hours'),
                "date":request_data.get('date')
                # "messagae":f'This is a reminder email for the scheduled Cleaning shift starting in 2 hrs scheduled on {schedule["date"]} starting at {schedule["start"]} for {schedule["end"]} hours.',
                # "purpose":"confirmation"
            }); 

        #sedning it back to the front end as response...
        return request_data
    else:
        return "nothing to send"

