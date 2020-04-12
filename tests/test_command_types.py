from hue_cli.command_types import (IdentifiableCommand,
                                   ValueCommand,
                                   EnumeratedCommand,
                                   InitializingCommand)

import pytest


class MockApi:
    def __init__(self):
        self.method_a_called = False
        self.method_a_args = []
        self.method_a_kwargs = {}
        self.method_b_called = False
        self.method_b_args = []
        self.method_b_kwargs = {}

    def method_a(self, *args, **kwargs):
        self.method_a_called = True
        self.method_a_args = args
        self.method_a_kwargs = kwargs

    def method_b(self, *args, **kwargs):
        self.method_b_called = True
        self.method_b_args = args
        self.method_b_kwargs = kwargs

@pytest.fixture
def mock_light_indices(monkeypatch):
    """Return [] for light indices"""

    def mock_get_light_indices(*args, **kwargs):
        return args[1]
    monkeypatch.setattr(IdentifiableCommand, "get_light_indices", mock_get_light_indices)

def test_initializing_command():
    api = MockApi()
    command = InitializingCommand(api, actions=['method_a', 'method_b'], args=['test_arg'])
    command()
    assert api.method_a_called
    assert api.method_a_args == (['test_arg'],)
    assert api.method_a_kwargs == {}
    assert api.method_b_called
    assert api.method_b_args == (['test_arg'],)
    assert api.method_b_kwargs == {}

def test_value_command(mock_light_indices):
    api = MockApi()
    command = ValueCommand(api, actions=['method_a'], args=['test_value'])
    command()
    assert api.method_a_called
    assert api.method_a_args == ('test_value', [])

    command = ValueCommand(api, actions=['method_b'], args=['test_value', 'arg1', 'arg2'])
    command()
    assert api.method_b_called
    assert api.method_b_args == ('test_value', ['arg1', 'arg2'])
