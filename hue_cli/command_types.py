class IdentifiableCommand:
    def __init__(self, api, actions=[], args=[], init_command=None):
        self.args = args
        self.api = api
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
        int_args = set()
        non_int_args = []
        if isinstance(args, str):
            args = [args]
        for arg in args:
            try:
                int_args.add(int(arg))
            except ValueError:
                non_int_args.append(arg)
                pass
        for arg in non_int_args:
            for light in self.api.lights:
                if arg.lower() in light.name.lower():
                    int_args.add(light.id)
                    continue
            for group in self.api.groups:
                if arg.lower() in group.name.lower():
                    for light in group.lights:
                        int_args.add(light.id)
                        continue
        return list(int_args)


class ValueCommand(IdentifiableCommand):
    def __call__(self):
        value = self.args.pop(0)
        indices = self.get_light_indices(self.args)
        action = self.actions[0]
        action(value, indices)


class EnumeratedCommand(IdentifiableCommand):
    def __init__(self, api, actions={}, args=[], init_command=None):
        try:
            key = args.pop(0)
        except IndexError:
            key = '__default'
        try:
            actions = [actions[key]]
        except KeyError:
            actions = [actions[key + 's']]
        super().__init__(api, actions=actions, args=args, init_command=init_command)


class InitializingCommand(IdentifiableCommand):
    def __call__(self):
        for action in self.actions:
            action(self.args)
