import database
from sqlalchemy import Column, Integer, String, Float, DateTime


class Action(database.Base):
    """
    Action 

    Attributes:
        action (str): `captcha`, `ip`, `device`
        expiration (datetime): # FIXME: change to timestamp
        keycloak_device_id (str): 
        fingerprint_device_id (str):
        ip_address (str):  
    """

    __tablename__ = 'actions'
    id = Column(Integer, primary_key=True)
    keycloak_device_id = Column(String, nullable=True)
    fingerprint_device_id = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)
    action = Column(String, nullable=False)
    expiration = Column(DateTime, nullable=False)

    def __init__(self, action, expiration, keycloak_device_id=None, fingerprint_device_id=None, ip_address=None):
        assert any([keycloak_device_id, fingerprint_device_id, ip_address])
        self.action = action
        self.expiration = expiration
        self.keycloak_device_id = keycloak_device_id
        self.fingerprint_device_id = fingerprint_device_id
        self.ip_address = ip_address

    def __repr__(self):
        return f"""Action(
            action: {self.action}
            expiration: {self.expiration}
            keycloak_device_id: {self.keycloak_device_id}
            fingerprint_device_id: {self.fingerprint_device_id}
            ip_address: {self.ip_address}
        )"""

    def __str__(self):
        return f"Action({self.keycloak_device_id}, {self.fingerprint_device_id}, {self.ip_address}, {self.action})"
