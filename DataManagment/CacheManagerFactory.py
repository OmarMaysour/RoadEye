import sqlite3
from DataManagment.AccelerometerCacheManager import get_accelerometer_cache_manager_instance
from DataManagment.AnomalyCacheManager import get_anomaly_cache_manager_instance

def get_cache_manager_instance(instance_type):
    if not _CacheManagerFactory._CacheManagerFactoryInstance:
        _CacheManagerFactory._CacheManagerFactoryInstance = _CacheManagerFactory()

    if instance_type == 'Anomaly':
        return get_anomaly_cache_manager_instance(_CacheManagerFactory._CacheManagerFactoryInstance.get_db_connection())
    elif instance_type == 'Accelerometer':
        return get_accelerometer_cache_manager_instance(_CacheManagerFactory._CacheManagerFactoryInstance.get_db_connection())
    else:
        raise Exception('Invalid instance type for cache manager')

def initiate_cache_manager_factory_instance_creation():
    if not _CacheManagerFactory._CacheManagerFactoryInstance:
        _CacheManagerFactory._CacheManagerFactoryInstance = _CacheManagerFactory()

class _CacheManagerFactory:
    _CacheManagerFactoryInstance = None

    def __init__(self):
        self._db_connection = sqlite3.connect('roadeye_cache.db')
        self._create_tables_if_not_exist()

    def __del__(self):
        self._db_connection.close()

    def _create_tables_if_not_exist(self):
        cursor = self._db_connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS anomaly_cache
                     (ID                     INTEGER PRIMARY KEY    AUTOINCREMENT,
                     pothole_confidence      REAL                   NOT NULL,
                     bump_confidence         REAL                   NOT NULL,
                     manhole_confidence      REAL                   NOT NULL,
                     roadCrack_confidence    REAL                   NOT NULL,
                     lat                     REAL                   NOT NULL,
                     lng                     REAL                   NOT NULL,
                     image_uri               TEXT                   NOT NULL,
                     created_at              TEXT                   NOT NULL);''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS accelerometer_cache
                             (ID                   INTEGER PRIMARY KEY    AUTOINCREMENT,
                             accelerometer_read_x    REAL                   NOT NULL,
                             accelerometer_read_y    REAL                   NOT NULL,
                             accelerometer_read_z    REAL                   NOT NULL,
                             lat                   REAL                   NOT NULL,
                             lng                   REAL                   NOT NULL,
                             created_at            TEXT                   NOT NULL);''')
        cursor.close()

    def get_db_connection(self):
        return self._db_connection