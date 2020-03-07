from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
def send_email(aircraft, RUL):
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    IP = os.getenv("IP")
    message = Mail(
        from_email='alaeddine-13@live.fr',
        to_emails='ala2017eddine@gmail.com',
        subject='Alert, Aircraft {} is in danger state'.format(aircraft),
        html_content='Aircraft is in <span style="color:red;">danger</span> state, with <strong>RUL={}</strong>. <br>Click the button below to see details. <a href="http://{}/aircraft-status/{}"><button style="background:green;color:black;">See Dashboard</button></a>'.format(round(RUL, 3), IP, aircraft))
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)