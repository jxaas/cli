import logging
import os

from cliff.command import Command

import jujuxaas.client

def get_jxaas_client(command):
  tenant = 'tenant1'
  username = 'tenant1'
  password= 'tenant1'

  url = os.getenv('JXAAS_URL', "http://127.0.0.1:8080/xaas")
  client = jujuxaas.client.Client(url=url, tenant=tenant, username=username, password=password)
  return client
