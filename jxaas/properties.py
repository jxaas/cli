import logging
import os

import cliff.show
import cliff.lister
import utils


class ListProperties(cliff.lister.Lister):
    "Show properties for a JXaaS instance"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ListProperties, self).get_parser(prog_name)
        parser.add_argument('bundle_type')
        parser.add_argument('instance')
        parser.add_argument('relation')
        return parser

    def take_action(self, parsed_args):
        client = utils.get_jxaas_client(self)

        relation_properties = client.get_relation_properties(parsed_args.bundle_type, parsed_args.instance, parsed_args.relation)

        relation_properties = relation_properties['Properties']
        columns = ('Key',
                   'Value')
        data = [(k,v) for k, v in relation_properties.iteritems()]
        return (columns, data)
