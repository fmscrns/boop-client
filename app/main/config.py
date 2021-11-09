import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    NAME_CLOUDINARY = "tjcmfrnc"
    KEY_API_CLOUDINARY = os.getenv('CLOUD_KEY')
    SECRET_API_CLOUDINARY = os.getenv("CLOUD_SECRET")
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    API_DOMAIN = "http://127.0.0.1:5000"
    MEDIA_STORAGE = "/static/images/"

class ProductionConfig(Config):
    DEBUG = False
    API_DOMAIN = "https://boop-proj-server.herokuapp.com"
    MEDIA_STORAGE = "https://res.cloudinary.com/tjcmfrnc/image/upload/v1635309887/BoopDev/"

config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
