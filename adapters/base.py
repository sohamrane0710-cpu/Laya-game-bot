
from abc import ABC, abstractmethod


class GameClient(ABC):
    @abstractmethod
    def reset(self):
        """Start a new episode and return its initial state."""
        raise NotImplementedError

    @abstractmethod
    def observe(self):
        """Return the current raw game observation."""
        raise NotImplementedError

    @abstractmethod
    def execute(self, action):
        """Execute a supported action and return its outcome."""
        raise NotImplementedError

    @abstractmethod
    def is_terminal(self):
        """Return whether the episode has ended."""
        raise NotImplementedError

    @abstractmethod
    def close(self):
        """Release resources."""
        raise NotImplementedError
