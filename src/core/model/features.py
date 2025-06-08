from abc import ABC, abstractmethod
from typing import List


class IFeature(ABC):
    """Feature interface

    Methods:
        get_timestamp (int): test
    """
    _registry = {}

    def __init_subclass__(cls, **kwargs):
        """
        Subclass registry, for automatic serialization and deserialization
        """
        super().__init_subclass__(**kwargs)
        IFeature._registry[cls.__name__] = cls

    @abstractmethod
    def get_timestamp(self) -> int:
        """Returns this feature's start time in milliseconds.

        Returns:
            int: Start instant in milliseconds.
        """
        ...

    @abstractmethod
    def get_duration(self) -> int:
        """Returns this feature's duration in milliseconds.

        Returns:
            int: Duration in milliseconds.
        """
        ...

    @abstractmethod
    def mode(self) -> str:
        """Returns this feature's mode of operation.

        Returns:
            str: Operation mode name.
        """
        ...

    @abstractmethod
    def serialize(self) -> dict:
        """
        Serializes this feature's data into a dict.
        Should include type, timestamp, duration, mode and all other feature-specific attributes.
        """
        ...

    @classmethod
    @abstractmethod
    def get_feature_name(cls) -> str:
        """Returns the feature's class name

        Returns:
            str: Name of the feature
        """
        ...


class FeatureSerializer():
    """Serializes and deserializes features.
    """

    @staticmethod
    def serialize(feature: IFeature) -> dict:
        """Serializes a feature into a dict

        Args:
            feature (IFeature): _description_

        Returns:
            dict: _description_
        """
        return feature.serialize()

    @staticmethod
    def deserialize(data: dict) -> IFeature:
        """Deserializes a dict instance into a feature with its data.

        Args:
            data (dict): Dict with the feature data.

        Raises:
            ValueError: If the feature type cannot be found.
        """
        cls_name = data['type']
        cls = IFeature._registry.get(cls_name)
        if cls is None:
            raise ValueError(f"Unknown feature type: {cls_name}")
        return cls(**{k: v for k, v in data.items() if k != 'type'})


class IFeatureExporter(ABC):
    """
    Feature exporter interface. 
    """
    @abstractmethod
    def generate_scenes(self, feature: type[IFeature], data=None) -> List[object]:
        """Generates the scene data for a specific feature type. 
        This does not generate the feature instance in a timeline, it generates 
        the scene(s) that defines the feature.

        Args:
            feature (IFeature): Feature class for which to generate the scene(s).
            data (_type_, optional): Optional data for the generation.

        Returns:
            List[object]: A list of objects, representing the scene(s)
        """
        pass

    @abstractmethod
    def generate_instance(self, feature: IFeature, data=None) -> object:
        """Generates the data for this specific feature instance, to be arranged in a timeline.

        Args:
            feature (IFeature): Feature instance to arrange.
            data (_type_, optional): Optional data for the generation.

        Returns:
            object: _description_
        """
        pass


# ----- FEATURES -----

class SimpleFlash(IFeature):
    """
    Simple ParCan flash.

    Modes:  
        'all'
        'even'
        'odd'
    """

    _MODES = ['all', 'even', 'odd']

    def __init__(self, timestamp: int, duration: int, mode: str | None = None) -> None:
        self._timestamp = timestamp
        self._duration = duration

        if not mode or mode not in self._MODES:
            mode = self._MODES[0]
        self._mode = mode

    def __str__(self) -> str:
        return f"SimpleFlash (ts (ms): {self._timestamp}, duration (ms): {self._duration}, mode: {self._mode})"

    def get_timestamp(self) -> int:
        return self._timestamp

    def get_duration(self) -> int:
        return self._duration

    def mode(self) -> str:
        return self._mode

    @classmethod
    def get_feature_name(cls) -> str:
        return "Simple Flash"

    def serialize(self) -> dict:
        return {'type': 'SimpleFlash', 'timestamp': self._timestamp, 'duration': self._duration, 'mode': self._mode}

# --------------------------------------------------------------


class RGBWFlash(IFeature):
    """
    Simple RGBW flash. Color configurable.

    Modes:
        'white'
        'red'
        'green'
        'blue'
    """

    _MODES = ['white', 'red', 'green', 'blue']

    def __init__(self, timestamp: int, duration: int, mode: str | None = None) -> None:
        self._timestamp = timestamp
        self._duration = duration

        if not mode or mode not in self._MODES:
            mode = self._MODES[0]
        self._mode = mode
        """
        # Some day, this will work...
        def clamp(x): 
            return max(0, min(x, 255))
        self._color = "#{0:02x}{1:02x}{2:02x}".format(clamp(red), clamp(green), clamp(blue))
        """

    def __str__(self) -> str:
        return f"RGBWFlash (ts (ms): {self._timestamp}, duration (ms): {self._duration}, mode: {self._mode})"

    def get_timestamp(self) -> int:
        return self._timestamp

    def get_duration(self) -> int:
        return self._duration

    def mode(self) -> str:
        return self._mode

    @classmethod
    def get_feature_name(cls) -> str:
        return "RGBW Flash"

    def serialize(self) -> dict:
        return {'type': 'RGBWFlash', 'timestamp': self._timestamp, 'duration': self._duration, 'mode': self._mode}

# --------------------------------------------------------------


class RotFlash(IFeature):
    """
    Rotating, static color wash from moving heads.

    Modes:
        'yellow'
        'magenta'
        'cyan'
    """

    _MODES = ['yellow', 'magenta', 'cyan']

    def __init__(self, timestamp: int, duration: int, mode: str | None = None) -> None:
        self._timestamp = timestamp
        self._duration = duration

        if not mode or mode not in self._MODES:
            mode = self._MODES[0]
        self._mode = mode

    def __str__(self) -> str:
        return f"RotFlash (ts (ms): {self._timestamp}, duration (ms): {self._duration}, mode: {self._mode})"

    def get_timestamp(self) -> int:
        return self._timestamp

    def get_duration(self) -> int:
        return self._duration

    def mode(self) -> str:
        return self._mode

    @classmethod
    def get_feature_name(cls) -> str:
        return "Rotating Flash"

    def serialize(self) -> dict:
        return {'type': 'RotFlash', 'timestamp': self._timestamp, 'duration': self._duration, 'mode': self._mode}
