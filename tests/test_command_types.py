from hue_cli.command_types import (IdentifiableCommand,
                                   ValueCommand,
                                   EnumeratedCommand,
                                   InitializingCommand)
from hue_api.groups import HueGroup
from hue_api.lights import HueLight

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

def test_enumerating_command(mock_light_indices):
    api = MockApi()
    actions = {'a': 'method_a', '__default': 'method_b'}
    command_a = EnumeratedCommand(api, actions=actions, args=['a'])
    command_a()
    assert api.method_a_called
    assert not api.method_b_called

    api.method_a_called = False
    command_b = EnumeratedCommand(api, actions=actions, args=[])
    command_b()
    assert not api.method_a_called
    assert api.method_b_called

def test_get_light_indices():
    api = MockApi()
    lights = [
        HueLight(1, 'Desk Light', {}, None),
        HueLight(2, 'Bedroom Light', {}, None),
        HueLight(3, 'Kitchen Light', {}, None),
        HueLight(4, 'Dining Room Light', {}, None),
        HueLight(5, 'Bathroom Light', {}, None)
    ]
    bedroom_lights = [lights[0], lights[1]]
    eating_lights = [lights[2], lights[3]]
    bathroom_lights = [lights[4]]
    groups = [
        HueGroup(1, 'Bedroom', bedroom_lights),
        HueGroup(2, 'Eating', eating_lights),
        HueGroup(3, 'Bathroom', bathroom_lights)
    ]
    api.lights = lights
    api.groups = groups
    command = IdentifiableCommand(api)
    # Test int indices
    ids = command.get_light_indices(['1', '3', '4'])
    assert ids == [1, 3, 4]
    # Test ID groups
    bedroom_ids = command.get_light_indices(['bedroom'])
    assert bedroom_ids == [1, 2]
    eating_ids = command.get_light_indices(['eating'])
    assert eating_ids == [3, 4]
    bathroom_ids = command.get_light_indices(['bath'])
    assert bathroom_ids == [5]
    # Test ID individual lights
    kitchen_ids = command.get_light_indices(['kitchen'])
    assert kitchen_ids == [3]
    dining_room_ids = command.get_light_indices(['dining'])
    assert dining_room_ids == [4]
