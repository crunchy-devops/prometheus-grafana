import configparser


config = configparser.ConfigParser()
config.read('../../../db_config.ini')

DATABASE = {
    'host':    config['postgresql']['host'],
    'name': config['postgresql']['database'],
    'user': config['postgresql']['user'],
    'pass': config['postgresql']['password'],
    'port': config['postgresql']['port']
}