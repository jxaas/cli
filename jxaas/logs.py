import logging
import os

import cliff.show
import cliff.lister
import utils


class ListLog(cliff.lister.Lister):
    "Show the log for a JXaaS instance"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ListLog, self).get_parser(prog_name)
        parser.add_argument('bundle_type')
        parser.add_argument('instance')
        return parser

    def take_action(self, parsed_args):
        client = utils.get_jxaas_client(self)

        log = client.get_log(parsed_args.bundle_type, parsed_args.instance)
        print log
        relation_properties = relation_properties['Properties']
        columns = ('Key',
                   'Value')
        data = [(k, v) for k, v in relation_properties.iteritems()]
        return (columns, data)
