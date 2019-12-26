import pika
import signal

from operations.log.application import Logger, LOG_LEVEL_DEBUG, \
    LOG_LEVEL_WARNING


class AsyncConsumer:
    """
    Class: AsyncConsumer

    Based on the asynchronous pattern provided by the pika module. This
    consumer will consume on each queue as provided in the classes' constructor.
    Messages produced on a consumed queue will result in a call to the
    function handle_message.

    Terminology:

    Connection  -
    Channel     -
    IO loop     -
    """

    consumer_name = "AsyncConsumer"

    _connection: pika.SelectConnection
    _channel = None

    logger: Logger = None

    def __init__(self, logger=None, queues=None):
        """
        Constructor for the AsyncConsumer.

        :param logger: logging application
        :param queues: a list of queues which the consumer should consume
                       from
        """
        self.logger = logger

        self._queues = queues
        self._queues_declared = 0
        self._closing = False

        signal.signal(signal.SIGTERM, self.terminate)

    def run(self):
        """
        Runs the AsyncConsumer:
         1. connects to the configured RabbitMQ server
         2. creates a channel
         3. declares queue(s)
         4. starts consuming on the created queues
        """
        self.connect()
        self._connection.ioloop.start()

    def connect(self):
        """
        Sets up the connection to the RabbitMQ server.
        """
        self._connection = pika.SelectConnection(
            pika.ConnectionParameters(),
            on_open_callback=self.on_connected,
            on_close_callback=self.on_closed
        )

    def on_connected(self, _unused_connection):
        """
        Callback for completed connection.

        :param _unused_connection: pika connection object, already registered
                                   with the class instance, hence ignored.
        """
        self.logger.write_to_log(
            LOG_LEVEL_DEBUG,
            self.consumer_name,
            "Opened connection to RabbitMQ server."
        )
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_closed(self, _unused_connection, reason):
        """
        Callback for closed connection.

        :param _unused_connection: pika connection object
        :param reason: reason for closed connection.
        """
        self.logger.write_to_log(
            LOG_LEVEL_DEBUG,
            self.consumer_name,
            "Connection closed unexpectedly, reason: {}".format(reason)
        )

    def on_channel_open(self, new_channel):
        """
        Callback for opened channel.

        :param new_channel: created pika channel
        """
        self.logger.write_to_log(
            LOG_LEVEL_DEBUG,
            self.consumer_name,
            "Opened channel to RabbitMQ server."
        )
        self._channel = new_channel
        self._channel.add_on_close_callback(self.on_channel_closed)

        for queue_name in self._queues:
            self._channel.queue_declare(queue=queue_name, callback=self.on_queue_declared)

    def on_channel_closed(self, _unused_channel, reason):
        """
        Callback for closed channel.

        :param _unused_channel: pika channel object
        :param reason: reason for closed channel
        """
        self.logger.write_to_log(
            LOG_LEVEL_DEBUG,
            self.consumer_name,
            "Channel closed unexpectedly, reason: {}".format(reason)
        )

    def on_queue_declared(self, _frame):
        """
        Callback for declared queue.

        :param _frame: response frame from RabbitMQ
        """
        self._queues_declared += 1

        self.logger.write_to_log(
            LOG_LEVEL_DEBUG,
            self.consumer_name,
            "Queue declared."
        )

        if self._queues_declared == len(self._queues):
            self.start_consuming()

    def start_consuming(self):
        """
        Starts consuming on the configured topics.
        """
        for queue_name in self._queues:
            self._channel.basic_consume(queue_name, self.handle_message)

        self.logger.write_to_log(
            LOG_LEVEL_DEBUG, self.consumer_name, "Started."
        )

    def handle_message(self, channel, method, header, body):
        """
        Callback for incoming message on a consumed queue.

        :param channel:
        :param method:
        :param header:
        :param body: message body
        """
        pass

    def terminate(self, signum, frame):
        """
        Used to handle the SIGTERM signal, so that the consumer system can be
        shut down gracefully, even after an interrupt.

        :param signum: <see python docs>
        :param frame:  <see python docs>
        :return:       N/A
        """
        self.logger.write_to_log(
            LOG_LEVEL_WARNING, self.consumer_name, "SIGTERM was received, stopping."
        )

        self.stop()

    def stop(self):
        """
        Stops the consumer by closing the connection and stopping the running
        IO loop.
        """
        self._connection.close()
        self._connection.ioloop.stop()
        self.logger.write_to_log(
            LOG_LEVEL_DEBUG, self.consumer_name, "Stopped."
        )
