import logging
import os
import subprocess

import cliff.show
import cliff.lister
import utils

class ListBundleTypes(cliff.lister.Lister):
    "List JXaaS bundle types"

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        client = utils.get_jxaas_client(self)

        bundletypes = client.list_bundle_types()
        columns = ('Id', 'Name')
        data = [(b.get('Id'),b.get('Name')) for b in bundletypes.get('Bundles', [])]
        return (columns, data)
