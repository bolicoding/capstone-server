from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
app = Flask(__name__)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)
class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(500), unique=False)
    def __init__(self, email):
        self.email = email
class EmailSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email')
email_schema = EmailSchema()
emails_schema = EmailSchema(many=True)
@app.route('/sign-up', methods=["POST"])
def add_quote():
    email = request.json['email']
    new_email = Email(email)
    db.session.add(new_email)
    db.session.commit()
    email = Email.query.get(new_email.id)
    return email_schema.jsonify(email)
@app.route("/get-emails", methods=["GET"])
def get_quotes():
    all_emails = Email.query.all()
    result = emails_schema.dump(all_emails)
    return jsonify(result)
if __name__ == '__main__':
    app.run(debug=True)
