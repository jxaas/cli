import logging
import sys

from cliff.app import App

import cliff.commandmanager

import logs
import properties

class CliApp(App):

    log = logging.getLogger(__name__)

    def __init__(self):
      command_manager = cliff.commandmanager.CommandManager('jxaas')
      command_manager.add_command('list-properties', properties.ListProperties)
      command_manager.add_command('list-log', logs.ListLog)
      # command_manager.add_command('complete', cliff.complete.CompleteCommand)
      super(CliApp, self).__init__(
            description='JXaaS CLI app',
            version='0.1',
            command_manager=command_manager
            )

    def initialize_app(self, argv):
        self.log.debug('initialize_app')

    def prepare_to_run_command(self, cmd):
        self.log.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.log.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.log.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    app = CliApp()
    return app.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
