import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # 邮箱配置
    EMAIL_USER = os.getenv('EMAIL_USER')
    EMAIL_PASS = os.getenv('EMAIL_PASS')
    SMTP_SERVER = os.getenv('SMTP_SERVER')
    SMTP_PORT = os.getenv('SMTP_PORT')
    RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL')

    # 彩票配置
    api_key = "381ff1bc8b54482bbc714d59e14a4712"
    LOTTERY_TYPE = '14'  # 14大乐透  11双色球
    USER_NUMBERS = [
       # {"issue": None, "numbers": ["03", "16", "20", "21", "27", "09", "10"]},
        {"issue": None, "numbers": ["06", "15", "20", "23", "33", "03", "08"]}
    ]