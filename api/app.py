
from sqlalchemy_utils import ChoiceType
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, json
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
    name = db.Column(db.String(80), unique=True, nullable=False)
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

# ########### ROUTES #############
@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


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

# @api.route('/setAppt', methods={'POST'})
# class SetAppt(Resource):
#     def post():
#         if(request.method == 'POST'):
#             client = request.form.get("client")
#             console.log(client)
#             return {"client":client}


@app.route("/setAppt", methods=["POST"])
def setAppt():
    if request.method == "POST":
        request_data = json.loads(request.data)
        #print(request_data['content'])
        
        #logging shift details in log file
        append_new_line('log.txt', request_data.get('client') + " scheduled " + request_data.get('cleaner') + " from "
        + request_data.get('start') + " for " + request_data.get('hours')+ " hours on " + request_data.get('date'))
        
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

