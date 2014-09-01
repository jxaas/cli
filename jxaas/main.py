import logging
import sys

from cliff.app import App

import cliff.commandmanager

import bundletypes
import instanceconfig
import instances
import logs
import metrics
import properties

class CliApp(App):

    log = logging.getLogger(__name__)

    def __init__(self):
      command_manager = cliff.commandmanager.CommandManager('jxaas')
      command_manager.add_command('list-bundles', bundletypes.ListBundleTypes)
      command_manager.add_command('list-properties', properties.ListProperties)
      command_manager.add_command('list-log', logs.ListLog)
      command_manager.add_command('list-instances', instances.ListInstances)
      command_manager.add_command('destroy-instance', instances.DestroyInstance)
      command_manager.add_command('create-instance', instances.CreateInstance)
      command_manager.add_command('repair-instance', instances.RepairInstance)
      command_manager.add_command('get-health', instances.GetInstanceHealth)
      command_manager.add_command('get-scaling', instances.GetInstanceScaling)
      command_manager.add_command('connect-instance', instances.ConnectInstance)
      command_manager.add_command('list-instances', instances.ListInstances)
      command_manager.add_command('list-metrics', metrics.ListMetrics)
      command_manager.add_command('get-metric', metrics.GetMetricValues)
      command_manager.add_command('get-config', instanceconfig.GetConfig)
      command_manager.add_command('set-config', instanceconfig.SetConfig)

      # Alias
      command_manager.add_command('connect', instances.ConnectInstance)

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

    def configure_logging(self):
        super(CliApp, self).configure_logging()

        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)

def main(argv=sys.argv[1:]):
    app = CliApp()
    return app.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
