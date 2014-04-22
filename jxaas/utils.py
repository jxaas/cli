import logging

from cliff.command import Command

import jujuxaas.client

def get_jxaas_client(command):
  tenant = 'abcdef'
  username = '123'
  password= '123'

  client = jujuxaas.client.Client(url="http://127.0.0.1:8080/xaas", tenant=tenant, username=username, password=password)
  return client
