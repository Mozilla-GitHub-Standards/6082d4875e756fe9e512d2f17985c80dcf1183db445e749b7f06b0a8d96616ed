# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is Sync Server
#
# The Initial Developer of the Original Code is the Mozilla Foundation.
# Portions created by the Initial Developer are Copyright (C) 2010
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#   Tarek Ziade (tarek@mozilla.com)
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****
import unittest

from syncreg.storage.multi import WeaveMultiStorage
from syncreg.storage import WeaveStorage

WeaveStorage.register(WeaveMultiStorage)


class Storage(object):

    def __init__(self, param1, param2):
        self.param1 = param1
        self.param2 = param2
        self.items = {}

    @classmethod
    def get_name(self):
        """Returns the name of the storage"""
        return 'storage'

    def user_exists(self, user_name):
        ''
        return True

    def set_user(self, user_email, **values):
        ''

    def get_user(self, user_name, fields=None):
        ''

    def delete_user(self, user_name):
        ''

    def delete_collection(self, user_name, collection_name):
        ''

    def collection_exists(self, user_name, collection_name):
        ''

    def set_collection(self, user_name, collection_name, **values):
        ''

    def get_collection(self, user_name, collection_name, fields=None):
        ''

    def get_collections(self, user_name, fields=None):
        ''

    def get_collection_names(self, user_name):
        ''

    def get_collection_timestamps(self, user_name):
        ''

    def get_collection_counts(self, user_name):
        ''

    def item_exists(self, user_name, collection_name, item_id):
        ''

    def get_items(self, user_name, collection_name, fields=None):
        ''

    def get_item(self, user_name, collection_name, item_id, fields=None):
        ''

    def set_item(self, user_name, collection_name, item_id, **values):
        ''
        self.items[item_id] = values

    def set_items(self, user_name, collection_name, items):
        ''

    def delete_item(self, user_name, collection_name, item_id):
        ''

    def delete_items(self, user_name, collection_name, item_ids=None):
        ''

    def get_total_size(self, user_id):
        ''

    def get_collection_sizes(self, user_id):
        ''

    def get_size_left(self, user_id):
        ''


class TestMultiStorage(unittest.TestCase):

    def test_multiple_storages(self):
        WeaveStorage.register(Storage)

        # Defining a master with two slaves, with the same backend
        config = {'storage': 'syncserver.storage.multi.WeaveMultiStorage',
                  'storage.master': 'storage',
                  'storage.master.param1': 'one',
                  'storage.master.param2': 'two',
                  'storage.slaves': 'storage1:storage,storage2:storage',
                  'storage.storage1.param1': 'one',
                  'storage.storage1.param2': 'two',
                  'storage.storage2.param1': 'three',
                  'storage.storage2.param2': 'four',
                  }
        multi = WeaveStorage.get_from_config(config)

        # trying a read
        self.assertTrue(multi.user_exists('tarek'))

        # trying a write
        multi.set_item('xx', 'xx', '1', ok=1)
        for storage in [multi.master] + multi.slaves:
            self.assertEquals(storage.items, {'1': {'ok': 1}})


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestMultiStorage))
    return suite

if __name__ == "__main__":
    unittest.main(defaultTest="test_suite")
