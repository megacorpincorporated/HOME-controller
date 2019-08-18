from . import application


def start(args=None, utility_applications=None):
    """
    Start method of this application module. When invoked, this function shall
    start the underlying application and return its instance.

    :param args: arguments intended for the serial application.
    :param utility_applications: a list of all utility applications that
                                 the serial application is allowed to
                                 use.
    :return: SerialApplication
    """
    serial_application = application.SerialApplication()
    serial_application.start(
        args=args,
        utility_applications=utility_applications
    )

    return serial_application