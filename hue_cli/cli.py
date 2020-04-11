#!/usr/bin/env python3
import argparse

from hue_api import HueApi
from .command_router import CommandRouter, COMMANDS

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=COMMANDS)
    parser.add_argument('additional_args', nargs='*')

    args = parser.parse_args()
    router = CommandRouter(HueApi())
    router.route_command(args.command, args.additional_args)
