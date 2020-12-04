from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_mail import Mail, Message
from flask_heroku import Heroku
# import sys
import os

# sys.setrecursionlimit(10**6) 

app = Flask(__name__)
heroku = Heroku(app)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL')
CORS(app)

app.config.update(
	# DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
  MAIL_DEFAULT_SENDER = os.environ.get("USERNAME"),
	MAIL_USERNAME =  os.environ.get("USERNAME"),
	MAIL_PASSWORD = os.environ.get("PASSWORD")
)
mail = Mail(app)


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
  
@app.route('/send', methods=['POST'])
def send_mail():
  try:
    msg = Message("Fast Garage Contact Page", sender = os.environ.get("USERNAME"), recipients = [os.environ.get("USERNAME")])
    msg.html = render_template("contact.html", message = request.json['message'], email = request.json['email'], name = request.json['name'])
    mail.send(msg)
    return jsonify('Mail Sent!!')
  except Exception as e:
    return jsonify(str(e))
  
  
if __name__ == '__main__':
    app.run(debug=True)
