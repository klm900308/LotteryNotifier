import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from datetime import datetime

from config import Config

def send_email(subject, content):
    """发送邮件通知"""
    cfg = Config()

    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] =formataddr(("彩票中奖通知", cfg.EMAIL_USER)) # Header(cfg.EMAIL_USER, 'utf-8')
    message['To'] = formataddr(("收件人", cfg.RECEIVER_EMAIL)) #Header(cfg.RECEIVER_EMAIL, 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')

    print(message)


    try:
        smtp_obj = smtplib.SMTP_SSL(cfg.SMTP_SERVER, int(cfg.SMTP_PORT))
        smtp_obj.login(cfg.EMAIL_USER, cfg.EMAIL_PASS)
        smtp_obj.sendmail(cfg.EMAIL_USER, cfg.RECEIVER_EMAIL, message.as_string())
        print("邮件发送成功",datetime.now().time())
        return True
    except smtplib.SMTPException as e:
        print(f"邮件发送失败: {e}")
        return False