import os
from configparser import ConfigParser
from argparse import ArgumentParser

CORE_STAGE_KEY = "CORE_STAGE"
DEFAULT_CORE_STAGE = "LOCAL"
SECRETS_CONFIG_FILE_NAME = ".conf"
DEFAULT_PORT = 8000
DEFAULT_HOST = "127.0.0.1"

def load_app_config():
    config = ConfigParser()
    
    # configparser by default converts keys to lowercase, I want to make sure keys are read as is.
    config.optionxform = str

    config.read(SECRETS_CONFIG_FILE_NAME)
    
    if not config.sections():
        raise ValueError(f'No valid configuration found. Please add {SECRETS_CONFIG_FILE_NAME} file to the root of project')
    
    PROFILE = os.getenv(CORE_STAGE_KEY, DEFAULT_CORE_STAGE)
    if PROFILE not in config:
        raise KeyError(f'Stage "{PROFILE}" does not exist in configuration.')
    
    for key, value in config[PROFILE].items():
        os.environ[key] = value

def parse_arguments():
    parser = ArgumentParser(description='Inherit Core APIs')
    parser.add_argument('--stage', help=f'STAGE for running the application. {DEFAULT_CORE_STAGE} by default', default=DEFAULT_CORE_STAGE)
    parser.add_argument('--host', help=f'HOST for running the application. {DEFAULT_HOST} by defailt', default=DEFAULT_HOST)
    parser.add_argument('--port', help=f'PORT for running the application. {DEFAULT_PORT} by defailt', type=int, default=DEFAULT_PORT)

    args = parser.parse_args()
    os.environ[CORE_STAGE_KEY] = DEFAULT_CORE_STAGE
    if args.stage:
        os.environ[CORE_STAGE_KEY] = args.stage
    return parser, args