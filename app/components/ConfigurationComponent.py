import configparser
import os


class ConfigurationComponent:
    def __init__(self):
        config = configparser.ConfigParser()
        directory = os.path.abspath(os.path.join(os.path.realpath(__file__), os.pardir, os.pardir, os.pardir))
        init_file = os.path.join(directory, 'app.ini')
        if os.path.exists(init_file):
            config.read(init_file)
            self.username = config["DEFAULT"]["username"]
            self.password = config["DEFAULT"]["password"]
        else:
            self.username = os.environ["username"]
            self.password = os.environ["password"]

