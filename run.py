from flask import Flask
from main.model import db

from main.controller import media_api
from main.exception import init_exc_handlers


class ConfigLoader:
    config_name_map = {"local": 'config.LocalConfig'}

    def load_config(self, app: Flask, config="local"):
        config_object = self.config_name_map[config]
        app.config.from_object(config_object)
        print(f'Run Config:  {config.upper()}')


class SocialMediaApp:
    def __init__(self):
        self.app = Flask(__name__)

    def set_app(self):
        self._load_config()
        media_api.init_app(self.app)
        init_exc_handlers(self.app)
        db.init_app(self.app)
        # db.create_all(app=self.app)

    def run_app(self):
        self.app.run()

    def _load_config(self):
        config = ConfigLoader()
        config.load_config(self.app)


if __name__ == '__main__':
    media_app = SocialMediaApp()
    media_app.set_app()
    media_app.run_app()
