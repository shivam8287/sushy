# -*- coding: utf-8 -*-

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import json

import mock

from sushy.resources.chassis.thermal import thermal
from sushy.tests.unit import base


class ThermalTestCase(base.TestCase):

    def setUp(self):
        super(ThermalTestCase, self).setUp()
        self.conn = mock.Mock()
        with open('sushy/tests/unit/json_samples/thermal.json') as f:
            self.conn.get.return_value.json.return_value = json.load(f)

        self.thermal = thermal.Thermal(
            self.conn, '/redfish/v1/Chassis/Blade1/Thermal',
            redfish_version='1.5.0')

    def test__parse_attributes(self):
        self.thermal._parse_attributes()
        self.assertEqual('1.5.0', self.thermal.redfish_version)
        self.assertEqual('Thermal', self.thermal.identity)
        self.assertEqual('Blade Thermal', self.thermal.name)

        self.assertEqual('0', self.thermal.fans[0].identity)
        self.assertEqual('CPU Fan', self.thermal.fans[0].name)
        self.assertEqual('CPU', self.thermal.fans[0].physical_context)
        self.assertEqual('enabled', self.thermal.fans[0].status.state)
        self.assertEqual('ok', self.thermal.fans[0].status.health)
        self.assertEqual(6000, self.thermal.fans[0].reading)
        self.assertEqual('RPM', self.thermal.fans[0].reading_units)
        self.assertEqual(2000, self.thermal.fans[0].lower_threshold_fatal)
        self.assertEqual(0, self.thermal.fans[0].min_reading_range)
        self.assertEqual(10000, self.thermal.fans[0].max_reading_range)

        self.assertEqual('0', self.thermal.temperatures[0].identity)
        self.assertEqual('CPU Temp', self.thermal.temperatures[0].name)
        self.assertEqual('enabled', self.thermal.temperatures[0].status.state)
        self.assertEqual('ok', self.thermal.temperatures[0].status.health)
        self.assertEqual(62, self.thermal.temperatures[0].reading_celsius)
        self.assertEqual(
            75,
            self.thermal.temperatures[0].upper_threshold_non_critical
        )
        self.assertEqual(
            90,
            self.thermal.temperatures[0].upper_threshold_critical
        )
        self.assertEqual(
            95,
            self.thermal.temperatures[0].upper_threshold_fatal
        )
        self.assertEqual(0,
                         self.thermal.temperatures[0].min_reading_range_temp)
        self.assertEqual(120,
                         self.thermal.temperatures[0].max_reading_range_temp)
        self.assertEqual('CPU', self.thermal.temperatures[0].physical_context)