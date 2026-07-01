import firebase_admin
from firebase_admin import credentials, firestore, auth, storage
from app.config import settings
from app.core.logging import log
from typing import Optional


class FirebaseClient:
    _instance: Optional["FirebaseClient"] = None
    _db: Optional[firestore.Client] = None
    _auth: Optional[auth.Client] = None
    _storage: Optional[storage.Client] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def initialize(self):
        if not firebase_admin._apps:
            try:
                cred = credentials.Certificate(settings.firebase_credentials_dict)
                firebase_admin.initialize_app(cred)
                log.info("Firebase initialized successfully")
            except Exception as e:
                log.error(f"Failed to initialize Firebase: {e}")
                raise

    @property
    def db(self) -> firestore.Client:
        if self._db is None:
            self.initialize()
            self._db = firestore.client()
        return self._db

    @property
    def auth_client(self) -> auth.Client:
        if self._auth is None:
            self.initialize()
            self._auth = auth
        return self._auth

    @property
    def storage_client(self) -> storage.Client:
        if self._storage is None:
            self.initialize()
            self._storage = storage.bucket(settings.firebase_storage_bucket)
        return self._storage


firebase_client = FirebaseClient()
