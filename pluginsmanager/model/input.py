from abc import ABCMeta, abstractmethod

from unittest.mock import MagicMock


class Input(metaclass=ABCMeta):
    """
    Input is the medium in which the audio will go into effect to be processed.

    Effects usually have a one (mono) or two inputs (stereo L + stereo R). But this
    isn't a rule: Some have only class:`Output`, like audio frequency generators,
    others have more than two.

    For obtains the inputs::

        >>> my_awesome_effect
        <Lv2Effect object as 'Calf Reverb' active at 0x7fd58d874ba8>
        >>> my_awesome_effect.inputs
        (<Lv2Input object as In L at 0x7fd58c583208>, <Lv2Input object as In R at 0x7fd58c587320>)

        >>> effect_input = my_awesome_effect.inputs[0]
        >>> effect_input
        <Lv2Input object as In L at 0x7fd58c583208>

        >>> symbol = effect_input.symbol
        >>> symbol
        'in_l'

        >>> my_awesome_effect.inputs[symbol] == effect_input
        True

    For connections between effects, view :class:`Connections`.

    :param Effect effect: Effect of input
    """

    def __init__(self, effect):
        self._effect = effect

        self.observer = MagicMock()

    @property
    def effect(self):
        """
        :return: Effect of input
        """
        return self._effect

    @property
    @abstractmethod
    def symbol(self):
        """
        :return: Input identifier
        """
        pass

    @property
    def json(self):
        """
        Get a json decodable representation of this input

        :return dict: json representation
        """
        return self.__dict__

    @property
    def __dict__(self):
        return {
            'effect': self.effect.pedalboard.effects.index(self.effect),
            'symbol': self.symbol,
            'index': self.effect.inputs.index(self),
        }
