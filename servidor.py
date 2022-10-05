# d-230f67b8e83449ad95965ac4bfb65907 Id plantilla de Registro Usuario

# save this as app.py
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask import Flask, request
from twilio.rest import Client

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello"


@app.route("/email", methods=['POST'])
def email():
    hash = request.form['hash_validator']
    print("estoy aqui")
    print(request.form['hash_validator'])
    print(os.environ.get('HASH_VALIDATOR'))
    if (hash == os.environ.get('HASH_VALIDATOR')):
        try:
            email_sender = os.environ.get("EMAIL_SENDER")
            to = request.form['destination']
            subject = request.form['subject']
            message_content = request.form['message']
            message = Mail(
                from_email=email_sender,
                to_emails=to,
                subject=subject,
                html_content=message_content)
            try:
                sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                response = sg.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
                return "OK"
            except Exception as e:
                print(e)
                return "KO"
        except:
            return "Faltan datos para el mensaje"
    else:
        return "Hash Error"


@app.route("/sms", methods=['POST'])
def sms():
    hash = request.form['hash_validator']
    if (hash == os.environ.get('HASH_VALIDATOR')):
        try:
            account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
            auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                messaging_service_sid=os.environ.get(
                    'TWILIO_MESSAGING_SERVICE_SID'),
                body=request.form['message'],
                to=request.form['destination']
            )
            print(message.sid)
            return "Enviado"
        except:
            return "Error: SMS no enviado."
    else:
        return "Error de Hash"


if __name__ == '__main__':
    app.run()
