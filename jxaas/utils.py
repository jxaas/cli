import logging
import os

from cliff.command import Command

import jujuxaas.client
import jujuxaas.auth.direct
import jujuxaas.auth.openstack

def get_jxaas_client(command):
  tenant = 'admin'
  username = 'admin'
  password= 'secret'

  #url = os.getenv('JXAAS_URL', "http://127.0.0.1:8080/xaas")
  #auth = jujuxaas.auth.direct.AuthDirect(url=url, tenant=tenant, username=username, password=password)

  url = os.getenv('JXAAS_URL', "http://127.0.0.1:5000")
  auth = jujuxaas.auth.openstack.AuthOpenstack(url=url, username=username, password=password, tenant=tenant)

  client = jujuxaas.client.Client(auth)
  return client
