class IdentifiableCommand:
    def __init__(self, api, actions=[], args=[], init_command=None):
        self.args = args
        if isinstance(actions, str):
            actions = [actions]
        self.actions = [getattr(api, action) for action in actions]
        if init_command:
            init_command()

    def __call__(self):
        indices = self.get_light_indices(self.args)
        for action in self.actions:
            action(self.args)

    def get_light_indices(self, args):
        return args


class ValueCommand(IdentifiableCommand):
    def __call__(self):
        value = self.args.pop()
        indices = self.get_light_indices(self.args)
        self.action(value, self.args)


class EnumeratedCommand(IdentifiableCommand):
    def __init__(self, api, actions={}, args=[], init_command=None):
        key = args.pop()
        super().__init__(api, actions=[actions[key]], args=args, init_command=init_command)


class InitializingCommand(IdentifiableCommand):
    def __call__(self):
        for action in self.actions:
            action(self.args)
