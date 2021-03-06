import signal
import sys
import threading
import argparse

from device_controller import root

from device_controller.util.log import set_up_logging


def parse_args():
    """
    Parse arguments provided at running the python program.
    """
    parser = argparse.ArgumentParser(
        description="HUME device controller"
    )

    #
    # Positional arguments
    #

    # HUME identification
    parser.add_argument('hume_uuid',
                        metavar="HUME_UUID",
                        help="HUME UUID")

    #
    # Optional arguments
    #

    # Testing arguments are prepended with "--test", or "-t" for short.
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-t-dma',
                       '--test-device-mock-address',
                       help="Set up a device mock address where all device "
                            "requests will be routed")
    group.add_argument('-t-rds',
                       '--test-run-device-simulator',
                       help="Run a device simulator, where a single device "
                            "will attach to the HUME on start and can reply "
                            "to all standard requests such as: capability, "
                            "heartbeat, and action",
                       action='store_true')

    print("Starting DC with the following arguments:")
    print(parser.parse_args())

    return parser.parse_args()


def set_up_interrupt():
    """
    Ensures that the program can exist gracefully.
    :return:
    """

    def interrupt(_signum, _frame):
        """
        :param _signum:
        :param _frame:
        """
        root.stop()
        sys.exit(0)

    def terminate(_signum, _frame):
        """
        :param _signum:
        :param _frame:
        """
        root.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, interrupt)
    signal.signal(signal.SIGTERM, terminate)


if __name__ == "__main__":
    cli_args = parse_args()

    set_up_interrupt()

    # Only set up logging if DC is run standalone and not from HTT. Rely on HTT
    # to set up logging otherwise.
    set_up_logging()

    print(f"DC sys.path: {sys.path}")

    root.start(cli_args)

    threading.Event().wait()  # Blocks indefinitely
