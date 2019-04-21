import uuid
import cv2
from DTOs.AnomalyDTO import AnomalyDTO
import os

from DataManagment.CacheManager import CacheManager


def get_anomaly_cache_manager_instance(db_connection):
    if not _AnomalyCacheManager._AnomalyCacheManagerInstance:
        _AnomalyCacheManager._AnomalyCacheManagerInstance = _AnomalyCacheManager(db_connection)
    return _AnomalyCacheManager._AnomalyCacheManagerInstance

def get_new_anomaly_cache_manager_instance(db_connection):
    return _AnomalyCacheManager(db_connection)

class _AnomalyCacheManager(CacheManager):
    _AnomalyCacheManagerInstance = None

    def __init__(self, db_connection):
        self._db_connection = db_connection

    def cache(self, anomaly_create_dto, image):
        image_name = self._cache_image_and_return_name(image)

        cursor = self._db_connection.cursor()
        cursor.execute(
            """INSERT INTO anomaly_cache (pothole_confidence, bump_confidence, manhole_confidence, roadCrack_confidence
            , lat, lng, image_uri, created_at) VALUES (?,?,?,?,?,?,?,?);"""
            , (anomaly_create_dto.pothole_confidence, anomaly_create_dto.bump_confidence
               , anomaly_create_dto.manhole_confidence, anomaly_create_dto.roadCrack_confidence, anomaly_create_dto.lat
               , anomaly_create_dto.lng, image_name, anomaly_create_dto.created_at)
        )
        self._db_connection.commit()
        cursor.close()

    def _cache_image_and_return_name(self, image):
        generated_uuid = uuid.uuid4().hex
        image_name = generated_uuid + '.png'
        cv2.imwrite('Cache/' + image_name, image)
        return image_name


    def get_oldest_cache(self):
        cursor = self._db_connection.cursor()
        cursor.execute("SELECT * FROM anomaly_cache ORDER BY ID ASC")
        cached_image = self._get_anomaly_dto_from_cursor(cursor.fetchone())
        cursor.close()
        return cached_image

    def _get_anomaly_dto_from_cursor(self, cursor):
        return AnomalyDTO(cursor[0], cursor[1], cursor[2], cursor[3], cursor[4], cursor[5], cursor[6], cursor[7], cursor[8])

    def delete_cache(self, anomaly_dto):
        os.remove('Cache/' + anomaly_dto.image_uri)
        cursor = self._db_connection.cursor()
        cursor.execute('''DELETE FROM anomaly_cache WHERE id = ? ''', (anomaly_dto.id,))
        self._db_connection.commit()
        cursor.close()
