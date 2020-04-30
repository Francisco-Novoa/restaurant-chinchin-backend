from flask import jsonify
from flask_mail import Mail, Message
mail = Mail()

def sendMailNew(subject, to_email):
    msg = Message(subject, sender=['yana', 'fineukraine94@gmail.com'], recipients=[to_email])
    mail.send(msg)
    return jsonify({"msg": "Email send successfully"}), 200 

    