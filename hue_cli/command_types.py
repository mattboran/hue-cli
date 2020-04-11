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
            action(indices)

    def get_light_indices(self, args):
        int_args = []
        for arg in args:
            try:
                int_args.append(int(arg))
            except ValueError:
                pass
        return int_args


class ValueCommand(IdentifiableCommand):
    def __call__(self):
        value = self.args.pop(0)
        indices = self.get_light_indices(self.args)
        action = self.actions[0]
        indices = self.get_light_indices(self.args)
        action(value, indices)


class EnumeratedCommand(IdentifiableCommand):
    def __init__(self, api, actions={}, args=[], init_command=None):
        try:
            key = args.pop(0)
        except IndexError:
            key = '__default'
        super().__init__(api, actions=[actions[key]], args=args, init_command=init_command)


class InitializingCommand(IdentifiableCommand):
    def __call__(self):
        for action in self.actions:
            action(self.args)
