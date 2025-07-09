from app.configs.broker_config import mqtt_broker_configs
from .mqtt_connection.mqtt_client_connection import MqttClientConnection


def start():
    mqtt_client_connection = MqttClientConnection(
        mqtt_broker_configs['HOST'],
        mqtt_broker_configs['PORT'],
        mqtt_broker_configs['CLIENT_NAME'],
        mqtt_broker_configs['KEEPALIVE'],
        mqtt_broker_configs['TOPICS']
    )
    mqtt_client_connection.start_connection()
    return mqtt_client_connection
