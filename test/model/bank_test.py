# Copyright 2017 SrMouraSilva
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import unittest
from unittest.mock import MagicMock

from pluginsmanager.model.bank import Bank
from pluginsmanager.model.lv2.lv2_effect_builder import Lv2EffectBuilder
from pluginsmanager.model.pedalboard import Pedalboard
from pluginsmanager.model.system.system_effect import SystemEffect
from pluginsmanager.observer.update_type import UpdateType


class BankTest(unittest.TestCase):

    def test_add_pedalboard_by_pedalboards(self):
        bank = Bank('Bank 1')

        pedalboard1 = MagicMock()
        pedalboard2 = MagicMock()

        bank.observer = MagicMock()

        bank.pedalboards.append(pedalboard1)
        self.assertEqual(pedalboard1.bank, bank)
        self.assertEqual(bank.pedalboards[0], pedalboard1)
        bank.observer.on_pedalboard_updated.assert_called_with(pedalboard1, UpdateType.CREATED, index=0, origin=bank)

        bank.pedalboards.append(pedalboard2)
        self.assertEqual(pedalboard2.bank, bank)
        self.assertEqual(bank.pedalboards[1], pedalboard2)
        bank.observer.on_pedalboard_updated.assert_called_with(pedalboard2, UpdateType.CREATED, index=1, origin=bank)

    def test_add_pedalboard(self):
        bank = Bank('Bank 1')

        pedalboard1 = MagicMock()
        pedalboard2 = MagicMock()

        bank.observer = MagicMock()

        bank.append(pedalboard1)
        self.assertEqual(pedalboard1.bank, bank)
        self.assertEqual(bank.pedalboards[0], pedalboard1)
        bank.observer.on_pedalboard_updated.assert_called_with(pedalboard1, UpdateType.CREATED, index=0, origin=bank)

        bank.append(pedalboard2)
        self.assertEqual(pedalboard2.bank, bank)
        self.assertEqual(bank.pedalboards[1], pedalboard2)
        bank.observer.on_pedalboard_updated.assert_called_with(pedalboard2, UpdateType.CREATED, index=1, origin=bank)

    def test_update_pedalboard(self):
        bank = Bank('Bank 1')

        pedalboard1 = MagicMock()
        pedalboard2 = MagicMock()

        bank.append(pedalboard1)

        bank.observer = MagicMock()
        bank.pedalboards[0] = pedalboard2

        self.assertEqual(pedalboard2.bank, bank)
        self.assertEqual(bank.pedalboards[0], pedalboard2)
        bank.observer.on_pedalboard_updated.assert_called_with(pedalboard2, UpdateType.UPDATED, index=0, origin=bank, old=pedalboard1)

    def test_delete_pedalboard(self):
        bank = Bank('Bank 1')

        pedalboard = MagicMock()

        bank.append(pedalboard)

        bank.observer = MagicMock()
        del bank.pedalboards[0]

        self.assertEqual(pedalboard.bank, None)
        self.assertEqual(len(bank.pedalboards), 0)
        bank.observer.on_pedalboard_updated.assert_called_with(pedalboard, UpdateType.DELETED, index=0, origin=bank)

    def test_json(self):
        bank = Bank('Bank 1')
        pedalboard = Pedalboard('Rocksmith')

        builder = Lv2EffectBuilder()
        system_effect = SystemEffect('system', ('capture_1', 'capture_2'), ('playback_1', 'playback_2'))

        reverb = builder.build('http://calf.sourceforge.net/plugins/Reverb')
        filter = builder.build('http://calf.sourceforge.net/plugins/Filter')
        reverb2 = builder.build('http://calf.sourceforge.net/plugins/Reverb')

        pedalboard.append(reverb)
        pedalboard.append(filter)
        pedalboard.append(reverb2)

        pedalboard.connect(system_effect.outputs[0], reverb.inputs[0])
        pedalboard.connect(reverb.outputs[0], filter.inputs[0])
        pedalboard.connect(reverb.outputs[1], filter.inputs[0])
        pedalboard.connect(filter.outputs[0], reverb2.inputs[0])
        pedalboard.connect(reverb.outputs[0], reverb2.inputs[0])
        pedalboard.connect(reverb.outputs[0], system_effect.inputs[0])

        bank.append(pedalboard)

        print(json.dumps(bank.json, sort_keys=True, indent=2))
