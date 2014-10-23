import logging
import os

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
    url = os.getenv('JXAAS_URL', "http://127.0.0.1:5000")
    auth = jujuxaas.auth.openstack.AuthOpenstack(url=url, tenant=tenant, username=username, password=password)
  else:
    raise Exception("Unknown authentication method specified: %s" % auth)

  client = jujuxaas.client.Client(auth)
  return client
