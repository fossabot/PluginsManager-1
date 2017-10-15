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

from abc import ABCMeta

from pluginsmanager.model.connection import Connection, ConnectionError
from pluginsmanager.model.port import Port


class MidiOutput(Port, metaclass=ABCMeta):
    """
    MidiOutput is the medium in which the midi output processed
    by the effect is returned.

    For obtains the outputs::

        >>> cctonode
        <Lv2Effect object as 'CC2Note'  active at 0x7efe5480af28>
        >>> cctonode.outputs
        (<Lv2MidiOutput object as MIDI Out at 0x7efe5420eeb8>,)

        >>> midi_output = cctonode.midi_outputs[0]
        >>> midi_output
        <Lv2Output object as Out L at 0x7fd58c58a438>

        >>> symbol = midi_output.symbol
        >>> symbol
        'midiout'

        >>> cctonode.midi_outputs[symbol] == midi_output
        True

    For connections between effects, view :class:`.pluginsmanager.model.connection.Connection`.

    :param Effect effect: Effect that contains the output
    """

    def connect(self, effect_input):
        """
        Connect it with effect_input::

            >>> driver_output = driver.outputs[0]
            >>> reverb_input = reverb.inputs[0]
            >>> Connection(driver_output, reverb_input) in driver.effect.connections
            False
            >>> driver_output.connect(reverb_input)
            >>> Connection(driver_output, reverb_input) in driver.effect.connections
            True

        .. note::

            This method does not work for all cases.
            class:`SystemOutput` can not be connected with class:`SystemInput` this way.
            For this case, use ::

                >>> pedalboard.connections.append(Connection(system_output, system_input))

        :param Input effect_input: Input that will be connected with it
        """
        if self.effect.is_unique_for_all_pedalboards and effect_input.effect.is_unique_for_all_pedalboards:
            error = "Isn't possible connect ports that both are from effects uniques for all pedalboards. "
            error += "Please use pedalboard.connect(Connection(output, input))"
            raise ConnectionError(error)

        pedalboard = self.effect.pedalboard if not self.effect.is_unique_for_all_pedalboards else effect_input.effect.pedalboard
        pedalboard.connections.append(Connection(self, effect_input))

    def disconnect(self, effect_input):
        """
        Disconnect it with effect_input

            >>> driver_output = driver.outputs[0]
            >>> reverb_input = reverb.inputs[0]
            >>> Connection(driver_output, reverb_input) in driver.effect.connections
            True
            >>> driver_output.disconnect(reverb_input)
            >>> Connection(driver_output, reverb_input) in driver.effect.connections
            False

        .. note::

            This method does not work for all cases.
            class:`SystemOutput` can not be disconnected with class:`SystemInput` this way.
            For this case, use ::

                >>> pedalboard.connections.remove(Connection(system_output, system_input))

        :param Input effect_input: Input that will be disconnected with it
        """
        if self.effect.is_unique_for_all_pedalboards and effect_input.effect.is_unique_for_all_pedalboards:
            error = "Isn't possible connect ports that both are from effects uniques for all pedalboards. "
            error += "Please use pedalboard.connect(Connection(output, input))"
            raise ConnectionError(error)

        self.effect.pedalboard.connections.remove(Connection(self, effect_input))

    @property
    def index(self):
        """
        :return: Output index in the your effect
        """
        return self.effect.midi_outputs.index(self)