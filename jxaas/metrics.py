import datetime

import logging
import os

import cliff.show
import cliff.lister
import utils


class ListMetrics(cliff.lister.Lister):
    "List the metrics that apply to an instance."

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ListMetrics, self).get_parser(prog_name)
        parser.add_argument('bundle_type')
        parser.add_argument('instance')
        return parser

    def take_action(self, parsed_args):
        client = utils.get_jxaas_client(self)

        metric_info = client.get_metrics(parsed_args.bundle_type, parsed_args.instance)
        columns = ('Metric',)
        data = [(v,) for v in metric_info['Metric']]
        return (columns, data)

class GetMetricValues(cliff.lister.Lister):
    "Show the values of a metric."

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(GetMetricValues, self).get_parser(prog_name)
        parser.add_argument('bundle_type')
        parser.add_argument('instance')
        parser.add_argument('metric')
        return parser

    def take_action(self, parsed_args):
        client = utils.get_jxaas_client(self)

        values = client.get_metric_values(parsed_args.bundle_type, parsed_args.instance, parsed_args.metric)
        columns = ('Timestamp','Value')
        data = [(datetime.datetime.fromtimestamp(v['T']), v['V']) for v in values['Points']]
        return (columns, data)
