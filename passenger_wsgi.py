import os
import sys
from MQTT_logger import ThreadedMQTTLogger

sys.path.insert(0, os.path.dirname(__file__))


def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    ThreadedMQTTLogger().start()
    message = 'started MQTT logger!\n'
    version = 'Python %s\n' % sys.version.split()[0]
    response = '\n'.join([message, version])
    return [response.encode()]
