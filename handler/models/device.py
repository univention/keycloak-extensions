import database
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, UniqueConstraint
import datetime


class Device(database.Base):
    """
    Device

    Description:
        This table will hold devices with an user attatched, making it easy to track
        new devices login. With this, if a user logs in to a device that it has never
        logged in before, it will be stored here. Also stores if the user was notified
        of the login.

    Attributes:
        keycloak_device_id (str):
        fingerprint_device_id (str):
        user_id (str):
        is_notified (bool):
        created_at (datetime):
    """

    __tablename__ = 'devices'
    __table_args__ = (UniqueConstraint("fingerprint_device_id", "user_id"), )
    id = Column(Integer, primary_key=True)
    keycloak_device_id = Column(String, nullable=False)
    fingerprint_device_id = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    is_notified = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, keycloak_device_id, fingerprint_device_id, user_id, is_notified=False):
        assert any([keycloak_device_id, fingerprint_device_id])
        self.keycloak_device_id = keycloak_device_id
        self.fingerprint_device_id = fingerprint_device_id
        self.user_id = user_id
        self.is_notified = is_notified

    def __repr__(self):
        return f"""Device(
            keycloak_device_id: {self.keycloak_device_id}
            fingerprint_device_id: {self.fingerprint_device_id}
            user_id: {self.user_id}
            is_notified: {self.is_notified}
        )"""

    def __str__(self):
        return f"Device({self.keycloak_device_id}, {self.fingerprint_device_id}, {self.user_id}, {self.is_notified})"
