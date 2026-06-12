import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # ==================== Cloud SQL for MySQL ====================
    INSTANCE_CONNECTION_NAME = os.environ.get('INSTANCE_CONNECTION_NAME')
    DB_USER = os.environ.get('DB_USER', 'root')           
    DB_PASS = os.environ.get('DB_PASS')
    DB_NAME = os.environ.get('DB_NAME', 'eadb')           


    if INSTANCE_CONNECTION_NAME:
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASS}@127.0.0.1:3306/{DB_NAME}"
    else:

        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    

    GCS_BUCKET_NAME = "itp4122-upload-1780634365"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

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

    PUBLIC_BASE_URL = os.environ.get('PUBLIC_BASE_URL') or 'http://localhost:5000'
    PREFERRED_URL_SCHEME = 'https' if PUBLIC_BASE_URL.startswith('https') else 'http'