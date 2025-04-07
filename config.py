class Config:
    SECRET_KEY = 'maucurhat-secret-key'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/maucurhat_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False