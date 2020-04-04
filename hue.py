import colorsys
import json
import os
import requests as re
import webcolors

BRIDGE_IP_ADDRESS = os.getenv('HUE_BRIDGE_IP_ADDRESS')
USER_NAME = os.getenv('HUE_USER_NAME')


class HueApi:

    # TODO: - Add register user
    def __init__(self, bridge_ip_address=BRIDGE_IP_ADDRESS, user_name=USER_NAME):
        self.bridge_ip_address = bridge_ip_address
        self.user_name = user_name
        self.lights = self.get_all_lights()

    def get_all_lights(self):
        url = self.base_url
        response = re.get(url).json()
        lights = []
        for id in response:
            state = response[id].get('state')
            name = response[id].get('name')
            hue_light = HueLight(id, name, state, self)
            lights.append(hue_light)
        return lights

    def list_lights(self):
        for light in self.lights:
            print(light)

    def filter_lights(self, index):
        if not index:
            return self.lights
        return [light for light in self.lights if light.id == str(index)]

    # When no index is supplied, all the lights are turned on
    def turn_on(self, index=None):
        for light in self.filter_lights(index):
            light.set_on()

    def turn_off(self, index=None):
        for light in self.filter_lights(index):
            light.set_off()

    def toggle_on(self, index=None):
        for light in self.filter_lights(index):
            light.toggle_on()

    def set_brightness(self, brightness, index=None):
        for light in self.filter_lights(index):
            light.set_brightness(brightness)

    def set_color(self, color, index=None):
        if isinstance(color, str):
            color = webcolors.name_to_rgb(color)
            r = color[0] / 255
            g = color[1] / 255
            b = color[2] / 255
        else:
            r, g, b = color
        for light in self.filter_lights(index):
            light.set_color(r, g, b)

    @property
    def base_url(self):
        return f"http://{self.bridge_ip_address}/api/{self.user_name}/lights"


class HueLight:
    def __init__(self, id, name, state, api):
        self.id = id
        self.name = name
        self.state = state
        self.api = api

    def __str__(self):
        string = f"{self.id} - {self.name}"
        if not self.is_reachable:
            return string + "(unreachable)"
        return string

    @property
    def is_reachable(self):
        return self.state['reachable']

    @property
    def light_url(self):
        return f"{self.api.base_url}/{self.id}/"

    # Fetches the most recent state from API
    @property
    def current_state(self):
        response = re.get(self.light_url)
        if response.status_code >= 300:
            print("There was an error updating state")
        return response.json().get('state', {})

    def handle_response(self, response):
        status_code = response.status_code
        if status_code >= 300:
            print(f"There was an {status_code} handling response")
            return {}
        response = response.json()[0]
        return response

    # Returns the response after putting state
    def put_state(self, payload):
        state_url = self.light_url + "state/"
        response = re.put(state_url, json=payload)
        return self.handle_response(response)

    def toggle_on(self):
        is_on = self.current_state['on']
        return self.put_state({"on": not is_on})

    def set_on(self):
        return self.put_state({"on": True})

    def set_off(self):
        return self.put_state({"on": False})

    # Provide values between 0 and 1
    def set_color(self, r, g, b):
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        hue = int((2**16 - 1) * h)
        saturation = int((2**8 - 1) * s)
        return self.put_state({"hue": hue, "sat": saturation})

    # Brightness should be between 0 and 254, but also accept between 0 and 1
    def set_brightness(self, brightness):
        if isinstance(brightness, float):
            brightness = int(brightness * 254)
        return self.put_state({"bri": brightness})

    def update_state(self):
        self.state = self.current_state
