import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    NAME_CLOUDINARY = "fmscrns"
    KEY_API_CLOUDINARY = os.getenv('CLOUD_KEY')
    SECRET_API_CLOUDINARY = os.getenv("CLOUD_SECRET")
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    API_DOMAIN = "http://127.0.0.1:5000"

class ProductionConfig(Config):
    DEBUG = False


config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY