import getpass
import json
import os
from xdg import XDG_CONFIG_HOME

MATRIX_INSTANCE_INDEX = 'matrix_instance'
MATRIX_BOT_ADDRESS_INDEX = 'matrix_bot_address'
MATRIX_USER_INDEX = 'matrix_user'
MATRIX_PASSWORD_INDEX = 'matrix_password'
PLAZA_BRIDGE_ENDPOINT_INDEX = 'plaza_bridge_endpoint'
PLAZA_AUTH_TOKEN_INDEX = 'plaza_authentication_token'

MATRIX_INSTANCE_ENV = 'MATRIX_INSTANCE'
MATRIX_BOT_ADDRESS_ENV = 'MATRIX_BOT_ADDRESS'
MATRIX_USER_ENV = 'MATRIX_USER'
MATRIX_PASSWORD_ENV = 'MATRIX_PASSWORD'
PLAZA_BRIDGE_ENDPOINT_ENV = 'PLAZA_BRIDGE_ENDPOINT'
PLAZA_AUTH_TOKEN_ENV = 'PLAZA_BRIDGE_AUTH_TOKEN'

global directory, config_file
directory = os.path.join(XDG_CONFIG_HOME, 'plaza', 'bridges', 'matrix')
config_file = os.path.join(directory, 'config.json')


def _get_config():
    if not os.path.exists(config_file):
        return {}
    with open(config_file, 'rt') as f:
        return json.load(f)


def _save_config(config):
    os.makedirs(directory, exist_ok=True)
    with open(config_file, 'wt') as f:
        return json.dump(config, f)


def get_matrix_instance():
    env_val = os.getenv(MATRIX_INSTANCE_ENV, None)
    if env_val is not None:
        return env_val

    config = _get_config()
    if config.get(MATRIX_INSTANCE_INDEX, None) is None:
        config[MATRIX_INSTANCE_INDEX] = input(
            'Matrix instance: ').strip()
        if not config[MATRIX_INSTANCE_INDEX]:
            raise Exception('No matrix instance introduced')
        _save_config(config)
    return config[MATRIX_INSTANCE_INDEX]


def get_matrix_bot_address():
    env_val = os.getenv(MATRIX_BOT_ADDRESS_ENV, None)
    if env_val is not None:
        return env_val

    config = _get_config()
    if config.get(MATRIX_BOT_ADDRESS_INDEX, None) is None:
        config[MATRIX_BOT_ADDRESS_INDEX] = input('Matrix bot address: ').strip()
        if not config[MATRIX_BOT_ADDRESS_INDEX]:
            raise Exception('No matrix bot address introduced')
        _save_config(config)
    return config[MATRIX_BOT_ADDRESS_INDEX]


def get_user():
    env_val = os.getenv(MATRIX_USER_ENV, None)
    if env_val is not None:
        return env_val

    config = _get_config()
    if config.get(MATRIX_USER_INDEX, None) is None:
        config[MATRIX_USER_INDEX] = input('User: ').strip()
        if not config[MATRIX_USER_INDEX]:
            raise Exception('No user introduced')
        _save_config(config)
    return config[MATRIX_USER_INDEX]


def get_password():
    env_val = os.getenv(MATRIX_PASSWORD_ENV, None)
    if env_val is not None:
        return env_val

    config = _get_config()
    if config.get(MATRIX_PASSWORD_INDEX, None) is None:
        config[MATRIX_PASSWORD_INDEX] = getpass.getpass(prompt='Password: ')
        if not config[MATRIX_PASSWORD_INDEX]:
            raise Exception('No password introduced')
        _save_config(config)
    return config[MATRIX_PASSWORD_INDEX]


def get_bridge_endpoint():
    env_val = os.getenv(PLAZA_BRIDGE_ENDPOINT_ENV, None)
    if env_val is not None:
        return env_val

    config = _get_config()
    if config.get(PLAZA_BRIDGE_ENDPOINT_INDEX, None) is None:
        config[PLAZA_BRIDGE_ENDPOINT_INDEX] = input('Plaza bridge endpoint: ')
        if not config[PLAZA_BRIDGE_ENDPOINT_INDEX]:
            raise Exception('No bridge endpoint introduced')
        _save_config(config)
    return config[PLAZA_BRIDGE_ENDPOINT_INDEX]


def get_auth_token():
    env_val = os.getenv(PLAZA_AUTH_TOKEN_ENV, None)
    if env_val is not None:
        return env_val

    config = _get_config()
    if config.get(PLAZA_AUTH_TOKEN_INDEX, None) is None:
        config[PLAZA_AUTH_TOKEN_INDEX] = input('Plaza authentication TOKEN: ')
        if not config[PLAZA_AUTH_TOKEN_INDEX]:
            raise Exception('No authentication token introduced')
        _save_config(config)
    return config[PLAZA_AUTH_TOKEN_INDEX]
