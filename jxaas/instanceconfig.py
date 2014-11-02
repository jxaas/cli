import datetime

import logging
import os

import cliff.show
import cliff.lister
import utils


class SetOption(cliff.command.Command):
    "Set a configuration value on a JXaaS instance"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(SetOption, self).get_parser(prog_name)
        parser.add_argument('bundle_type')
        parser.add_argument('instance')
        parser.add_argument('option_key')
        parser.add_argument('option_value')
        return parser

    def take_action(self, parsed_args):
        options = {}
        options[parsed_args.option_key] = parsed_args.option_value

        client = utils.get_jxaas_client(self)
        units = None
        client.ensure_instance(parsed_args.bundle_type, parsed_args.instance, options=options, units=units)


class GetOptions(cliff.lister.Lister):
    "List the configuration values that apply to an instance."

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(GetOptions, self).get_parser(prog_name)
        parser.add_argument('bundle_type')
        parser.add_argument('instance')
        return parser

    def take_action(self, parsed_args):
        client = utils.get_jxaas_client(self)

        info = client.get_instance_state(parsed_args.bundle_type, parsed_args.instance)
        columns = ('Option Key','Option Value')
        self.log.debug("Instance state: %s", info)
        data = [(k, v,) for k, v in info['Options'].iteritems()]
        return (columns, data)

