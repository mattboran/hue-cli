import colorsys
import json
import os
import requests as re
import webcolors

from api.lights import HueLight

BRIDGE_IP_ADDRESS = os.getenv('HUE_BRIDGE_IP_ADDRESS')
USER_NAME = os.getenv('HUE_USER_NAME')


class HueApi:

    # TODO: - Add register user
    def __init__(self, bridge_ip_address=BRIDGE_IP_ADDRESS, user_name=USER_NAME):
        self.bridge_ip_address = bridge_ip_address
        self.user_name = user_name
        self.lights = self.get_all_lights()

    @property
    def base_url(self):
        return f"http://{self.bridge_ip_address}/api/{self.user_name}/lights"

    def get_all_lights(self):
        url = self.base_url
        response = re.get(url).json()
        lights = []
        for id in response:
            state = response[id].get('state')
            name = response[id].get('name')
            hue_light = HueLight(id, name, state, self.base_url)
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
        if isinstance(brightness, float):
            brightness = int(brightness * 254)
        elif isinstance(brightness, str):
            if brightness == 'max':
                brightness = 254
            elif brightness == 'min':
                brightness = 1
            elif brightness == 'med':
                brightness = 127
            else:
                brightness = 255
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
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        hue = int((2**16 - 1) * h)
        saturation = int((2**8 - 1) * s)
        for light in self.filter_lights(index):
            light.set_color(hue, saturation)
