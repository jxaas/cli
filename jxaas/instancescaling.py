import datetime

import logging
import os

import cliff.show
import cliff.lister
import utils

def _format(scaling):
    columns = ('Metric','MetricCurrent', 'MetricMin', 'MetricMax', 'ScaleCurrent', 'ScaleMin', 'ScaleMax', 'ScaleTarget')
    policy = scaling['Policy']
    data = [(policy.get('MetricName'),
        scaling.get('MetricCurrent'),
        policy.get('MetricMin'),
        policy.get('MetricMax'),
        scaling.get('ScaleCurrent'),
        policy.get('ScaleMin'),
        policy.get('ScaleMax'),
        scaling.get('ScaleTarget'))]
    return (columns, data)


class SetInstanceScaling(cliff.command.Command):
    "Set a configuration value on a JXaaS instance"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(SetInstanceScaling, self).get_parser(prog_name)
        parser.add_argument('bundle_type')
        parser.add_argument('instance')
        parser.add_argument('--scale-min')
        parser.add_argument('--scale-max')
        parser.add_argument('--metric-min')
        parser.add_argument('--metric-max')
        parser.add_argument('--metric-name')
        return parser

    def take_action(self, parsed_args):
        args = vars(parsed_args)
        print args
        policy = {}
        if args['scale_min'] is not None:
          policy['ScaleMin'] = int(args['scale_min'])
        if args['scale_max'] is not None:
          policy['ScaleMax'] = int(args['scale_max'])
        if args['metric_min'] is not None:
          policy['MetricMin'] = float(args['metric_min'])
        if args['metric_max'] is not None:
          policy['MetricMax'] = float(args['metric_max'])
        if args['metric_name'] is not None:
          policy['MetricName'] = args['metric_name']

        client = utils.get_jxaas_client(self)
        client.set_scaling(parsed_args.bundle_type, parsed_args.instance, policy=policy)


class GetInstanceScaling(cliff.lister.Lister):
    "Gets the scaling state of an instance."

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(GetInstanceScaling, self).get_parser(prog_name)
        parser.add_argument('bundle_type')
        parser.add_argument('instance')
        return parser

    def take_action(self, parsed_args):
        client = utils.get_jxaas_client(self)

        scaling = client.get_scaling(parsed_args.bundle_type, parsed_args.instance)
        #print scaling
        return _format(scaling)


