import datetime

import logging
import os

import cliff.show
import cliff.lister
import utils


class SetConfig(cliff.command.Command):
    "Set a configuration value on a JXaaS instance"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(SetConfig, self).get_parser(prog_name)
        parser.add_argument('bundle_type')
        parser.add_argument('instance')
        parser.add_argument('config_key')
        parser.add_argument('config_value')
        return parser

    def take_action(self, parsed_args):
        config = {}
        config[parsed_args.config_key] = parsed_args.config_value

        client = utils.get_jxaas_client(self)
        units = None
        client.ensure_instance(parsed_args.bundle_type, parsed_args.instance, config=config, units=units)


class GetConfig(cliff.lister.Lister):
    "List the configuration values that apply to an instance."

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(GetConfig, self).get_parser(prog_name)
        parser.add_argument('bundle_type')
        parser.add_argument('instance')
        return parser

    def take_action(self, parsed_args):
        client = utils.get_jxaas_client(self)

        info = client.get_instance_state(parsed_args.bundle_type, parsed_args.instance)
        columns = ('Config Key','Config Value')
        self.log.debug("Instance state: %s", info)
        data = [(k, v,) for k, v in info['Options'].iteritems()]
        return (columns, data)

