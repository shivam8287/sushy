# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


import json
import mock

from sushy.resources.registry import message_registry_file
from sushy.tests.unit import base


class MessageRegistryFileTestCase(base.TestCase):

    def setUp(self):
        super(MessageRegistryFileTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('sushy/tests/unit/json_samples/'
                  'message_registry_file.json') as f:
            self.conn.get.return_value.json.return_value = json.load(f)

        self.reg_file = message_registry_file.MessageRegistryFile(
            self.conn, '/redfish/v1/Registries/Test',
            redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.reg_file._parse_attributes()
        self.assertEqual('Test', self.reg_file.identity)
        self.assertEqual('Test Message Registry File', self.reg_file.name)
        self.assertEqual('Message Registry file for testing',
                         self.reg_file.description)
        self.assertEqual('en', self.reg_file.languages[0])
        self.assertEqual('Test.1.0', self.reg_file.registry)
        self.assertEqual('default', self.reg_file.location[0].language)
        self.assertEqual('/redfish/v1/Registries/Test/Test.1.0.json',
                         self.reg_file.location[0].uri)
        self.assertEqual('https://example.com/Registries/Test.1.0.json',
                         self.reg_file.location[0].publication_uri)
        self.assertEqual('/redfish/v1/Registries/Archive.zip',
                         self.reg_file.location[0].archive_uri)
        self.assertEqual('Test.1.0.json',
                         self.reg_file.location[0].archive_file)

    @mock.patch('sushy.resources.registry.message_registry.MessageRegistry',
                autospec=True)
    def test_get_message_registry_uri(self, mock_msg_reg):
        mock_msg_reg_rv = mock.Mock()
        mock_msg_reg.return_value = mock_msg_reg_rv

        registry = self.reg_file.get_message_registry('en', None)
        mock_msg_reg.assert_called_once_with(
            self.conn, path='/redfish/v1/Registries/Test/Test.1.0.json',
            redfish_version=self.reg_file.redfish_version)
        self.assertEqual(mock_msg_reg_rv, registry)

    @mock.patch('sushy.resources.registry.message_registry.MessageRegistry',
                autospec=True)
    @mock.patch('sushy.resources.base.JsonArchiveReader', autospec=True)
    def test_get_message_registry_archive(self, mock_reader, mock_msg_reg):
        mock_reader_rv = mock.Mock()
        mock_reader.return_value = mock_reader_rv
        mock_msg_reg_rv = mock.Mock()
        mock_msg_reg.return_value = mock_msg_reg_rv
        self.reg_file.location[0].uri = None

        registry = self.reg_file.get_message_registry('fr', None)
        mock_msg_reg.assert_called_once_with(
            self.conn, path='/redfish/v1/Registries/Archive.zip',
            redfish_version=self.reg_file.redfish_version,
            reader=mock_reader_rv)
        mock_reader.assert_called_once_with('Test.1.0.json')
        self.assertEqual(mock_msg_reg_rv, registry)

    @mock.patch('sushy.resources.registry.message_registry.MessageRegistry',
                autospec=True)
    @mock.patch('sushy.resources.base.JsonPublicFileReader', autospec=True)
    def test_get_message_registry_public(self, mock_reader, mock_msg_reg):
        public_connector = mock.Mock()
        mock_reader_rv = mock.Mock()
        mock_reader.return_value = mock_reader_rv
        mock_msg_reg_rv = mock.Mock()
        mock_msg_reg.return_value = mock_msg_reg_rv
        self.reg_file.location[0].uri = None
        self.reg_file.location[0].archive_uri = None

        registry = self.reg_file.get_message_registry('en', public_connector)
        mock_msg_reg.assert_called_once_with(
            public_connector,
            path='https://example.com/Registries/Test.1.0.json',
            redfish_version=self.reg_file.redfish_version,
            reader=mock_reader_rv)
        self.assertEqual(mock_msg_reg_rv, registry)

    @mock.patch('sushy.resources.registry.message_registry.MessageRegistry',
                autospec=True)
    @mock.patch('sushy.resources.registry.message_registry_file.LOG',
                autospec=True)
    def test_get_message_registry_invalid(self, mock_log, mock_msg_reg):
        mock_msg_reg_rv = mock.Mock()
        mock_msg_reg.return_value = mock_msg_reg_rv
        self.reg_file.location[0].uri = None
        self.reg_file.location[0].archive_uri = None
        self.reg_file.location[0].publication_uri = None

        registry = self.reg_file.get_message_registry('en', None)
        mock_msg_reg.assert_not_called()
        self.assertIsNone(registry)
        mock_log.warning.assert_called_with(
            'No location defined for language %(language)s',
            {'language': 'en'})


class MessageRegistryFileCollectionTestCase(base.TestCase):

    def setUp(self):
        super(MessageRegistryFileCollectionTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('sushy/tests/unit/json_samples/'
                  'message_registry_file_collection.json') as f:
            self.conn.get.return_value.json.return_value = json.load(f)
        self.reg_file_col =\
            message_registry_file.MessageRegistryFileCollection(
                self.conn, '/redfish/v1/Registries',
                redfish_version='1.0.2')

    def test__parse_attributes(self):
        self.reg_file_col._parse_attributes()
        self.assertEqual('1.0.2', self.reg_file_col.redfish_version)
        self.assertEqual('Message Registry Test Collection',
                         self.reg_file_col.name)
        self.assertEqual(('/redfish/v1/Registries/Test',),
                         self.reg_file_col.members_identities)