class TestConfig:
    SECRET_KEY = 'c28e87882654f5d1e84b6e1a0c12a77f'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'  # Test
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Removes some notification in cmd


# class Config:
    # SECRET_KEY = os.environ.get('ARTUR_FLASKBLOG_SECRET_KEY')
    # SECRET_KEY = 'c28e87882654f5d1e84b6e1a0c12a77f'

    # SQLite
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # That should be also in env vars
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'  # Test
    # SQLALCHEMY_TRACK_MODIFICATIONS = False  # Removes some notification in cmd

    # Sending emails from g-mail account
    # MAIL_SERVER = 'smtp.googlemail.com'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # MAIL_USERNAME = os.environ.get('ARTUR_GOOGLE_USER')
    # MAIL_PASSWORD = os.environ.get('ARTUR_GOOGLE_PASSWORD')

