from temperusb import TemperHandler
from urllib.request import urlopen
import urllib.request
import json

def server_update(server, device, temperature):
    url = "http://%s/log/update/%d/%f/" % (
            server["host"],
            device["id"],
            temperature
        )

    try:
        response = urlopen(url)
        data = response.read().decode("utf-8")
        feedback = json.loads(data)
    except urllib.error.HTTPError:
        feedback = {"error": "Bad URL: %s" % url}
    return feedback
    

if __name__ == "__main__":
    settings = json.load(open('settings.json'))
    devices = json.load(open('devices.json'))

    temp_handler = TemperHandler()
    temp_devices = temp_handler.get_devices()

    for index, device in enumerate(devices):
        temperature = temp_devices[index].get_temperature()
        feedback = server_update(settings["server"], device, temperature)

        if feedback["error"]:
            print(feedback["error"])
        else:
            print("%fC written to server" % temperature)

