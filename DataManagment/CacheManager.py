import os
import sqlite3
import uuid

import cv2

from DTOs.AnomalyDTO import AnomalyDTO
from DTOs.ToClassifyAnomalyDTO import ToClassifyAnomalyDTO


def get_cache_manager_instance():
    if not _CacheManager._CacheManagerInstance:
        _CacheManager._CacheManagerInstance = _CacheManager()
    return _CacheManager._CacheManagerInstance

class _CacheManager:
    _CacheManagerInstance = None
    _db_connection = None

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
                     rumbleStrip_confidence    REAL                   NOT NULL,
                     lat                     REAL                   NOT NULL,
                     lng                     REAL                   NOT NULL,
                     image_uri               TEXT                   NOT NULL,
                     created_at              TEXT                   NOT NULL);''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS to_classify_anomaly_cache
                             (ID                     INTEGER PRIMARY KEY    AUTOINCREMENT,
                             lat                     REAL                   NOT NULL,
                             lng                     REAL                   NOT NULL,
                             image_uri               TEXT                   NOT NULL,
                             created_at              TEXT                   NOT NULL);''')
        cursor.close()

    def cache_anomaly(self, AnomalyDTO):
        cursor = self._db_connection.cursor()
        cursor.execute(
            """INSERT INTO anomaly_cache (pothole_confidence, bump_confidence, manhole_confidence, rumbleStrip_confidence,
             lat, lng, image_uri, created_at) VALUES (?,?,?,?,?,?,?,?);"""
            , (AnomalyDTO.pothole_confidence, AnomalyDTO.bump_confidence, AnomalyDTO.manhole_confidence, AnomalyDTO.rumbleStrip_confidence,
               AnomalyDTO.lat, AnomalyDTO.lng, AnomalyDTO.image_uri, AnomalyDTO.created_at)
        )
        self._db_connection.commit()
        cursor.close()

    def cache_to_classify_anomaly(self, ToClassifyAnomalyDTO, image):
        image_name = self._cache_image_and_return_name(image)

        cursor = self._db_connection.cursor()
        cursor.execute(
            """INSERT INTO to_classify_anomaly_cache (lat, lng, image_uri, created_at) VALUES (?,?,?,?);"""
            , (ToClassifyAnomalyDTO.lat, ToClassifyAnomalyDTO.lng, image_name, ToClassifyAnomalyDTO.created_at)
        )
        self._db_connection.commit()
        cursor.close()

    def _cache_image_and_return_name(self, image):
        generated_uuid = uuid.uuid4().hex
        image_name = generated_uuid + '.png'
        cv2.imwrite('Cache/' + image_name, image)
        return image_name

    def get_oldest_to_classify_anomaly_cache(self):
        cursor = self._db_connection.cursor()
        cursor.execute("SELECT * FROM to_classify_anomaly_cache ORDER BY ID ASC")
        cached_image = self._get_to_classify_anomaly_dto_from_cursor(cursor.fetchone())
        cursor.close()
        return cached_image

    def _get_to_classify_anomaly_dto_from_cursor(self, cursor):
        if cursor is None:
            return None
        return ToClassifyAnomalyDTO(cursor[0], cursor[1], cursor[2], cursor[3], cursor[4])

    def get_oldest_anomaly_cache(self):
        cursor = self._db_connection.cursor()
        cursor.execute("SELECT * FROM anomaly_cache ORDER BY ID ASC")
        cached_image = self._get_anomaly_dto_from_cursor(cursor.fetchone())
        cursor.close()
        return cached_image

    def _get_anomaly_dto_from_cursor(self, cursor):
        if cursor is None:
            return None
        return AnomalyDTO(cursor[0], cursor[1], cursor[2], cursor[3], cursor[4], cursor[5], cursor[6], cursor[7], cursor[8])


    def delete_to_classify_anomaly(self, id):
        cursor = self._db_connection.cursor()
        cursor.execute('''DELETE FROM to_classify_anomaly_cache WHERE id = ? ''', (id,))
        self._db_connection.commit()
        cursor.close()

    def delete_cache(self, anomaly_dto):
        os.remove('Cache/' + anomaly_dto.image_uri)
        cursor = self._db_connection.cursor()
        cursor.execute('''DELETE FROM anomaly_cache WHERE id = ? ''', (anomaly_dto.id,))
        self._db_connection.commit()
        cursor.close()

    def delete_image(self, image_uri):
        os.remove('Cache/' + image_uri)