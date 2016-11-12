from models.command import Command

from commands import all_commands

import asyncio


class BaseCommand(object):

    def __init__(self, name, config={}, parser, admin_required=False):
        self.name = name
        self.config = config
        self.parser = parser
        self.admin_required = admin_required

    @asyncio.coroutine
    def run(conversation, user, args):
        raise NotImplementedError("The `run` method must be implemented.")


def register_commands():
    # first we delete all the current registered commands
    Command.delete().execute()
    for command in all_commands:
        Command.create(name=command.name, admin_required=command.admin_required)
        if command.name in sys.modules:
            Command.delete().execute()
            raise NameError("Two modules of conflicting names found! Cleaning up and exiting...")
        importlib.import_module("commands.{}".format(command.name))
    return True
