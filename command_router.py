COMMANDS = ['list', 'on', 'off', 'toggle', 'brightness', 'color']

class CommandRouter:
    def __init__(self, api):
        self.api = api

    def route_command(self, command, args):
        if command == 'list':
            self.api.list_lights()
        elif command in ['on', 'off', 'toggle']:
            self.handle_no_value_command(command, args)
        else:
            self.handle_command_with_value(command, args)

    def handle_no_value_command(self, command, args):
        if command == 'on':
            action = self.api.turn_on
        elif command == 'off':
            action = self.api.turn_off
        elif command == 'toggle':
            action = self.api.toggle
        light = None
        if len(args) == 1:
            light = args[0]
        action(index=light)

    def handle_command_with_value(self, command, args):
        if command == 'brightness':
            action = self.api.set_brightness
        elif command == 'color':
            action = self.api.set_color
        light = None
        value = args[0]
        if len(args) == 2:
            light = args[1]
        action(value, index=light)
