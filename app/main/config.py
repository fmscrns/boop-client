import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    API_DOMAIN = "http://127.0.0.1:5000"
    MEDIA_STORAGE = "/static/images/"

class ProductionConfig(Config):
    DEBUG = False
    API_DOMAIN = "https://boop-proj-server.herokuapp.com"
    NAME_CLOUDINARY = "fmscrns"
    KEY_API_CLOUDINARY = os.getenv('CLOUD_KEY')
    SECRET_API_CLOUDINARY = os.getenv("CLOUD_SECRET")
    MEDIA_STORAGE = "https://res.cloudinary.com/fmscrns/image/upload/v1598443648/Boop/"

config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY