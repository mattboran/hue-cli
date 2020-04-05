#!/usr/bin/env python3
import argparse
from api import HueApi

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', type=str)
    parser.add_argument('additional_args', nargs='*')

    api = HueApi()
    simple_command_map = {
        'list': api.list_lights,
        'on': api.turn_on,
        'off': api.turn_off,
        'toggle': api.toggle_on,
    }

    argument_command_map = {
        'brightness': api.set_brightness,
        'color': api.set_color
    }

    args = parser.parse_args()
    command = args.command
    action = simple_command_map.get(command)
    if action:
        handle_simple_action(action, args.additional_args)
    action = argument_command_map.get(command)
    if action:
        handle_argument_action(action, args.additional_args)

def handle_simple_action(action, args):
    try:
        if len(args) > 0:
            light = args[0]
            action(light)
        else:
            action()
    except ValueError:
        print("Invalid argument passed to action")

def handle_argument_action(action, args):
    value = args[0]
    try:
        if len(args) > 1:
            light = args[1]
            action(value, light)
        else:
            action(value)
    except ValueError:
        print("Invalid argument passed to action")

if __name__ == "__main__":
    main()
