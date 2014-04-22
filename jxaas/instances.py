import logging
import os

import cliff.show
import cliff.lister
import utils


class ListInstances(cliff.lister.Lister):
    "List JXaaS instances"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ListInstances, self).get_parser(prog_name)
        parser.add_argument('bundle_type')
        return parser

    def take_action(self, parsed_args):
        client = utils.get_jxaas_client(self)

        instances = client.list_instances(parsed_args.bundle_type)
        columns = ('Id', 'Status', 'NumberUnits')
        data = [(i.get('Id'), i.get('Status'), i.get('NumberUnits')) for i in instances]
        return (columns, data)

class DestroyInstance(cliff.command.Command):
    "Delete a JXaaS instance"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(DestroyInstance, self).get_parser(prog_name)
        parser.add_argument('bundle_type')
        parser.add_argument('instance')
        return parser

    def take_action(self, parsed_args):
        client = utils.get_jxaas_client(self)
        client.destroy_instance(parsed_args.bundle_type, parsed_args.instance)


class CreateInstance(cliff.command.Command):
    "Create a JXaaS instance"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(CreateInstance, self).get_parser(prog_name)
        parser.add_argument('bundle_type')
        parser.add_argument('instance')
        return parser

    def take_action(self, parsed_args):
        client = utils.get_jxaas_client(self)
        config = None
        units = None
        client.ensure_instance(parsed_args.bundle_type, parsed_args.instance, config=config, units=units)
