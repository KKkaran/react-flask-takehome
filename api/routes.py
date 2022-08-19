
import app
from flask_restx import Resource
from app import Company, User, api
########### ROUTES #############


@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


@api.route('/companies')
class Companies(Resource):
    def get(self):
        return Company.query.all()


@api.route('/users/<int:company_id>')
class Users(Resource):
    def get(self, company_id):
        return User.query.filter_by(company_id).all()
