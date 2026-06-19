import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # ==================== Force MySQL (Cloud SQL) ====================
    DB_USER = os.environ.get('DB_USER', 'esther')
    DB_PASS = os.environ.get('DB_PASS')
    DB_HOST = os.environ.get('DB_HOST')
    DB_NAME = os.environ.get('DB_NAME', 'eadb')

    # 強制使用 MySQL（Public IP）
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:3306/{DB_NAME}?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Google Cloud Storage (Serverless Feature)
    GCS_BUCKET_NAME = "itp4122-upload-1780634365"

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME')
    ADMINS = [os.environ.get('MAIL_USERNAME')] if os.environ.get('MAIL_USERNAME') else ['itp4115ead@gmail.com']

    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_DURATION = 3600
    POSTS_PER_PAGE = 10

    PUBLIC_BASE_URL = os.environ.get('PUBLIC_BASE_URL') or 'http://35.234.15.92'
    PREFERRED_URL_SCHEME = 'https' if PUBLIC_BASE_URL.startswith('https') else 'http'