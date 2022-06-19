class LocalConfig:
    HOST_NAME = 'http://127.0.0.1:3100'
    ENV = 'local'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///social_media.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "RJyoeTBQSzi78kMGDYIhb1EfxBCxuxve"
    JWT_EXPIRATION_LIMIT = 7200
