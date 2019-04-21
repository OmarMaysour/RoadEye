from DTOs.AccelerometerDTO import AccelerometerDTO
from DataManagment.CacheManager import CacheManager


def get_accelerometer_cache_manager_instance(db_connection):
    if not _AccelerometerCacheManager._AccelerometerCacheManagerInstance:
        _AccelerometerCacheManager._AccelerometerCacheManagerInstance = _AccelerometerCacheManager(db_connection)
    return _AccelerometerCacheManager._AccelerometerCacheManagerInstance

def get_new_accelerometer_cache_manager_instance(db_connection):
    return _AccelerometerCacheManager(db_connection)

class _AccelerometerCacheManager(CacheManager):
    _AccelerometerCacheManagerInstance = None

    def __init__(self, db_connection):
        self._db_connection = db_connection

    def cache(self, accelerometer_dto):
        cursor = self._db_connection.cursor()
        cursor.execute(
            """INSERT INTO accelerometer_cache (accelerometer_read_x, accelerometer_read_y, accelerometer_read_z, lat,
             lng, created_at) VALUES (?,?,?,?,?,?);"""
            , (accelerometer_dto.accelerometer_read_x, accelerometer_dto.accelerometer_read_y
               , accelerometer_dto.accelerometer_read_z, accelerometer_dto.lat
               , accelerometer_dto.lng, accelerometer_dto.created_at)
        )
        self._db_connection.commit()
        cursor.close()


    def get_oldest_cache(self):
        cursor = self._db_connection.cursor()
        cursor.execute("SELECT * FROM accelerometer_cache ORDER BY ID ASC")
        cached_accelerometer = self._get_accelerometer_dto_from_cursor(cursor.fetchone())
        cursor.close()
        return cached_accelerometer

    def _get_accelerometer_dto_from_cursor(self, cursor):
        return AccelerometerDTO(cursor[0], cursor[1], cursor[2], cursor[3], cursor[4], cursor[5], cursor[6])

    def delete_cache(self, accelerometer_dto):
        cursor = self._db_connection.cursor()
        cursor.execute('''DELETE FROM accelerometer_cache WHERE id = ? ''', (accelerometer_dto.id,))
        self._db_connection.commit()
        cursor.close()
