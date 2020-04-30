from flask import jsonify
from flask_mail import Mail, Message
mail = Mail()

def sendMail(subject, to_email, html):
    msg = Message(subject, sender=['yana', 'fineukraine94@gmail.com'], recipients=[to_email])
    msg.html = html
    mail.send(msg)
    return jsonify({"msg": "Email send successfully"}), 200 

def allowed_file(filename,ALLOWED_EXTENSIONS):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS