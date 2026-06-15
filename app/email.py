from threading import Thread
from flask import current_app, render_template
from flask_mail import Message


def send_async_email(app, msg):

    with app.app_context():      
        try:
            mail = app.extensions.get('mail')
            if mail:
                mail.send(msg)
                print(f"✅ Email sent successfully to {msg.recipients[0]}")
            else:
                print("❌ Mail extension not found in app")
        except Exception as e:
            print(f"❌ Failed to send email: {e}")


def send_email(subject, recipients, text_body, html_body):

    msg = Message(subject, recipients=recipients)
    msg.body = text_body
    msg.html = html_body


    Thread(target=send_async_email, 
           args=(current_app._get_current_object(), msg)).start()


def send_password_reset_email(user):

    from flask import current_app
    
    token = user.get_reset_password_token()
    
    reset_url = f"{current_app.config['PUBLIC_BASE_URL']}/auth/reset_password/{token}"
    
    send_email(
        subject='[DILWL Staff Internal System] Reset Your Password',
        recipients=[user.email],
        text_body=render_template('email/reset_password.txt.j2', 
                                  user=user, reset_url=reset_url),
        html_body=render_template('email/reset_password.html.j2', 
                                  user=user, reset_url=reset_url)
    )