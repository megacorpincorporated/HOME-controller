from device_controller.utility.broker import Broker
from device_controller.utility.storage.data_store.storage_service import \
    StorageService
from device_controller.utility.storage.definitions import DataModel


def initialize(broker, service_name):
    global _store
    _store = DataStore(broker, service_name)


def register(model):
    assert issubclass(model, DataModel)

    _store.register(model)


class DataStore:

    _broker: Broker
    _service_name: str
    _store: dict

    _storage_service: StorageService

    def __init__(self, broker, service_name):
        self._broker = broker
        self._service_name = service_name
        self._store = dict()
        self._storage_service = StorageService(self._broker, self._service_name)

    def register(self, model):
        # Registration process:
        # 1. Instantiate model class
        # 2. Define storage space in _store, named same as model class
        # 3. TODO Call storage service to define table(s)
        # 4. TODO Get data from storage if tables were already defined and at
        #    TODO least one field is marked persistent

        model_instance = model()
        print("model key field: {}".format(model_instance.key()))
        print("model _store key: {}".format(model.__name__))
        self.define_storage(model_instance)

    def define_storage(self, model_instance: DataModel):
        # Allocate local storage
        self._store[str(model_instance.__class__.__name__)] = dict()
        print("_store state: {}".format(self._store))

        if model_instance.persistent:
            self._storage_service.define_table(model_instance)


_store = None