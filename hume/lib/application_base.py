from abc import ABCMeta, abstractmethod


class ApplicationABC(metaclass=ABCMeta):
    """
    Abstract Base Class for all applications of the HUME system. These abstract
    methods are intended to ease the way in which applications are started,
    stopped, and checked for status; in order to prevent applications all having
    different lifecycle management.

    Dependencies can be injected through extending the start() function with
    additional keyword arguments.
    """
    application_name: str
    sub_applications: dict

    @abstractmethod
    def start(self, *args, **kwargs):
        """
        Start lifecycle hook for all applications following the simple
        lifecycle management pattern.
        """
        pass

    @abstractmethod
    def stop(self, *args, **kwargs):
        """
        Stop lifecycle hook for all applications following the simple
        lifecycle management pattern. This hook should ensure that all resources
        related to this application are released.
        """
        pass

    @abstractmethod
    def status(self, *args, **kwargs):
        """
        Status information for the application. This function should
        return information about the application's current state.

        :return: status
        """
        pass
