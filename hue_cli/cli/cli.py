#!/usr/bin/env python3
import argparse

from .command_router import CommandRouter, COMMANDS

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=COMMANDS)
    parser.add_argument('additional_args', nargs='*')

    args = parser.parse_args()
    router = CommandRouter()
    router.route_command(args.command, args.additional_args)
