import logging
import os
import time

from cliff.command import Command

import jujuxaas.client
import jujuxaas.auth.direct
import jujuxaas.auth.openstack

def get_jxaas_client(command):
  tenant = os.getenv('JXAAS_TENANT', 'admin')
  username = os.getenv('JXAAS_USER', 'admin')
  password= os.getenv('JXAAS_SECRET', 'secret')

  auth = os.getenv('JXAAS_AUTH', 'direct')
  if auth == 'direct':
    url = os.getenv('JXAAS_URL', "http://127.0.0.1:8080/xaas")
    auth = jujuxaas.auth.direct.AuthDirect(url=url, tenant=tenant, username=username, password=password)
  elif auth == 'openstack':
    if not jujuxaas.auth.openstack.AuthOpenstack.available():
      raise Exception("Openstack keystone API not available")
    url = os.getenv('JXAAS_URL', "http://127.0.0.1:5000")
    auth = jujuxaas.auth.openstack.AuthOpenstack(url=url, tenant=tenant, username=username, password=password)
  else:
    raise Exception("Unknown authentication method specified: %s" % auth)

  client = jujuxaas.client.Client(auth)
  return client


def wait_for(fn):
  # TODO: Timeout
  while True:
    done = fn()
    if done:
      return done
    time.sleep(1)


def wait_jxaas_started(client, bundle_type, service_name):
  def jxaas_started():
    service_state = client.get_instance_state(bundle_type, service_name)
    if service_state:
      #log.debug("Service state for %s => %s", service_name, service_state)
      status = service_state.get('Status')
      if status == 'started':
        return status
    return None

  return wait_for(jxaas_started)

