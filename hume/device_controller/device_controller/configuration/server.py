from device_controller.configuration.model import DeviceConfiguration

from device_controller.utility.dispatch import Dispatch
from device_controller.utility.broker import Broker
from device_controller.utility.procedures import run_in_procedure, Procedure
from device_controller.lib.server_base import ServerBase


class ConfigServer(ServerBase, Dispatch, Procedure):
    """
    This server handles configuration scheduling, any conditions (such as
    storage-dependent scheduler actions), and limit-triggering.
    """

    dispatch_id = "ConfigServer"

    broker: Broker

    # TODO load configuration from storage into memory on start
    _device_config = None

    def __init__(self, broker=None):
        """
        :param broker: application wide broker instance
        """
        self.broker = broker

    def start(self):
        """
        Starts up the configuration server.
        """
        # TODO get configuration from storage and load it into memory
        # TODO create base configuration for the device_controller
        run_in_procedure(self, "yee haaaaa")

        config = DeviceConfiguration()
        print(config.id)
        print(type(config.id))

    def stop(self):
        """
        Not needed for now.
        """
        pass

    def on_dispatch(self, message):
        print("Config server got dispatch: {}".format(message))

    def start_procedure(self, *args):
        print("config server start_procedure called with args: {}".format(args))
