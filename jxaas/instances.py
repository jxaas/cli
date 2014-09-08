import logging
import os
import subprocess

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


class RepairInstance(cliff.command.Command):
    "Repair a JXaaS instance"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(RepairInstance, self).get_parser(prog_name)
        parser.add_argument('bundle_type')
        parser.add_argument('instance')
        return parser

    def take_action(self, parsed_args):
        client = utils.get_jxaas_client(self)
        client.repair_instance(parsed_args.bundle_type, parsed_args.instance)


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

class GetInstanceHealth(cliff.lister.Lister):
    "Gets the health of an instance."

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(GetInstanceHealth, self).get_parser(prog_name)
        parser.add_argument('bundle_type')
        parser.add_argument('instance')
        return parser

    def take_action(self, parsed_args):
        client = utils.get_jxaas_client(self)

        health_info = client.get_health(parsed_args.bundle_type, parsed_args.instance)

        columns = ('Unit','Healthy')
        data = [(k,v) for k, v in health_info['Units'].iteritems()]
        return (columns, data)

class ConnectInstance(cliff.command.Command):
    "Connect to a JXaaS instance, by launching the appropriate tool"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ConnectInstance, self).get_parser(prog_name)
        parser.add_argument('bundle_type')
        parser.add_argument('instance')
        return parser

    def take_action(self, parsed_args):
        client = utils.get_jxaas_client(self)

        relation = None
        bundle_type = parsed_args.bundle_type
        if bundle_type in ['mysql', 'multimysql']:
          relation = 'mysql'
        if bundle_type in ['mongodb']:
          relation = 'mongodb'
        if bundle_type in ['pg']:
          relation = 'pgsql'
        if bundle_type in ['cassandra']:
          relation = 'cassandra'
        if not relation:
          raise Exception("Unhandled bundle_type")

        relation_properties = client.get_relation_properties(bundle_type, parsed_args.instance, relation)
        properties = relation_properties.get('Properties', {})
        addresses = relation_properties.get('PublicAddresses', [])

        host = None
        if addresses:
          host = addresses[0]

        env = os.environ.copy()
        if relation == 'mysql':
          if not 'user' in properties:
            raise Exception("Service not ready")
          if not host:
            host = properties['host']
          command = ['mysql']
          command = command + [ '--user=' + properties['user'] ]
          command = command + [ '--host=' + host ]
          command = command + [ '--password=' + properties['password'] ]
          command = command + [ '--database=' + properties['database'] ]
          if 'port' in properties:
            command = command + [ '--port=' + properties['port'] ]

        if relation == 'cassandra':
          if not 'private-address' in properties:
            raise Exception("Service not ready")
          if not host:
            host = properties['private-address']
          port = properties['port'] or '9160'
          command = ['cqlsh']
          command = command + [ host ]
          command = command + [ port ]

        if relation == 'mongodb':
          if not 'port' in properties:
            raise Exception("Service not ready")
          if not host:
            host = properties['hostname']
          command = ['mongo']
          command = command + [ '%s:%s/%s' % (host, properties['port'], properties['replset']) ]

        if relation == 'pgsql':
          if not 'user' in properties:
            raise Exception("Service not ready")
          if not host:
            host = properties['host']
          command = ['psql']
          command = command + [ '--username=' + properties['user'] ]
          command = command + [ '--host=' + host ]
          command = command + [ '--dbname=' + properties['database'] ]
          # command = command + [ '--password']
          env['PGPASSWORD'] = properties['password']

        self.log.debug("Running command: %s", " ".join(command))
        p = subprocess.Popen(command, env=env)
        p.wait()
