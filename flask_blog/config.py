import os


class Config:
    TEMPLATES_AUTO_RELOAD = True
    FLASK_DEBUG = 1
    SECRET_KEY = "63f4ce6948a9d40a72191bb94b9c23fb"
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv("FLASKBLOG_DB_URL")
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("EMAIL_USER")
    MAIL_PASSWORD = os.getenv("EMAIL_PASS")

    # OAUTH KEYS
    CLIENT_ID = (
        "88130896554-jgfjq4g536lerid3l3or0mpu306k30ou.apps.googleusercontent.com",
    )
    CLIENT_SECRET = "FU84RphdKR-A_IwpT5MPRoss"
