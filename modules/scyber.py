import os
import json
import base64
from datetime import datetime
import ephem

from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

class Scyber:
    ALPS_LAT = 46.8
    ALPS_LON = 9.5

    @staticmethod
    def generate_master_key() -> bytes:
       
        return ChaCha20Poly1305.generate_key()

    @staticmethod
    def _get_moon_phase(lat: float, lon: float) -> str:
        
        obs = ephem.Observer()
        obs.lat, obs.lon = str(lat), str(lon)
        obs.date = datetime.utcnow()
        moon = ephem.Moon(obs)
        moon.compute(obs)
        return f"{moon.phase:.2f}"

    @staticmethod
    def _derive_key(master_key: bytes, moon_salt: str) -> bytes:
        salt = moon_salt.encode("utf-8")
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            info=b"scyber-key-derivation",
        )
        return hkdf.derive(master_key)

    def __init__(self, data: bytes):
        
        self.data = data

    def encode(
        self,
        master_key: bytes,
        associated_data: bytes = None,
        lat: float = ALPS_LAT,
        lon: float = ALPS_LON,
    ) -> str:
        
        phase = self._get_moon_phase(lat, lon)

        session_key = self._derive_key(master_key, phase)

        aead = ChaCha20Poly1305(session_key)
        nonce = os.urandom(12)
        ciphertext = aead.encrypt(nonce, self.data, associated_data)

        token = {
            "phase":  phase,
            "nonce":  base64.b64encode(nonce).decode("utf-8"),
            "cipher": base64.b64encode(ciphertext).decode("utf-8"),
        }
        return json.dumps(token)

    @staticmethod
    def decode(
        token_str: str,
        master_key: bytes,
        associated_data: bytes = None
    ) -> bytes:
       
        data = json.loads(token_str)
        phase = data["phase"]
        nonce = base64.b64decode(data["nonce"])
        cipher = base64.b64decode(data["cipher"])

        session_key = Scyber._derive_key(master_key, phase)

        aead = ChaCha20Poly1305(session_key)
        return aead.decrypt(nonce, cipher, associated_data)
