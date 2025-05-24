import os
import json 
from datetime import datetime, timedelta
from astral import LocationInfo
from astral.sun import sun
import hashlib
import ephem
from modules.palette import Palette as p
import os
from dotenv import load_dotenv
from modules.exceptions import RatException

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

import ast 

class GCoder:
    def __init__(self):
        self.security_folder = 'app/configs/security'
        self.config_name = 'coded.json'
        
        self.total_size = 512
        self.iv_size = 16
        self.data_size = self.total_size - self.iv_size
        self.block_size = 256
        
    def __call__(self):
        if not os.path.exists(self.security_folder):
            os.makedirs(self.security_folder)
        self._create_coded_hash()
        
    def generate_random_seed(self):
        city = LocationInfo("Innsbruck", "Austria", "Europe/Vienna", 47.2682, 11.3923)
        s = sun(city.observer, date=datetime.now())
        zenith_angle = s['noon'].timestamp()
        
        moon = ephem.Moon()
        moon.compute(datetime.now())
        moon_phase = moon.phase
        
        seed = moon_phase / zenith_angle if moon_phase > zenith_angle else zenith_angle / moon_phase  
        
        return str(seed)
        
        
    def _json_code_operator(self,date_folder,hash_folder,period_in_days,json_archiv,archiv,lenght_hash: int = 64):
        current_date = datetime.now()
        
        if date_folder in json_archiv:
            stored_date = datetime.strptime(json_archiv[date_folder], '%Y-%m-%d')
            if current_date <= stored_date:
                p.cyanTag("GCoder",f"Continue with not changes ;) - {date_folder} is not Expired")
                return
        
        new_date = current_date + timedelta(days=period_in_days)
        json_archiv[date_folder] = new_date.strftime('%Y-%m-%d')
        
        
        seed = self.generate_random_seed()        
        seed_hash = hashlib.sha512(seed.encode('utf-8')).digest()
        bunny_hash = os.urandom(lenght_hash)
        combined_bytes = bytes(a ^ b for a, b in zip(bunny_hash, seed_hash))
        combined_hex = combined_bytes.hex()
        
        json_archiv[hash_folder] = combined_hex
        with open(archiv, 'w') as archV:
            json.dump(json_archiv, archV, indent=4)
        
        p.redTag("GCoder",f"{date_folder} had been expired")
        p.cyanFatTag("GCoder",f"{hash_folder} had been generated")    
        
    def _create_coded_hash(self,lenght_hash: int = 64)->None:
        if not os.path.exists(self.security_folder):
            os.makedirs(self.security_folder)
        
        archiv = os.path.join(self.security_folder,self.config_name)
        
        
        if not os.path.exists(archiv):
            with open(archiv,"w") as archV:
                json.dump({}, archV)
                
            p.yellowTag("GCoder","File wasn't exist. Creating...")

        with open(archiv, 'r') as archV:
            json_archiv = json.load(archV)
        
        self._json_code_operator("date", "hash",7,json_archiv,archiv,lenght_hash)
        self._json_code_operator("refrash_date", "refrash_hash",7*12,json_archiv,archiv,lenght_hash)
            
        
    def _get_key_material(self,column_hash):
        with open('app/configs/security/coded.json', 'r') as codes:
            codes_content = json.load(codes)
        cds_hash = bytes.fromhex(codes_content.get(column_hash)) 
        if len(cds_hash) != 64:
            p.redFatTag("GCoder",f"Key size might be 64 bytes not {len(cds_hash)}")
            raise Exception("Key size might be 64 bytes")
        return cds_hash
    
    def _derive_key_iv(self, cds_hash: bytes):
        key = hashlib.sha512(cds_hash).digest()
        iv = hashlib.sha512(cds_hash[32:]).digest()[:16]
        return key, iv
    
    def encode_data(self,data,column_hash)->str:
        cds_hash = self._get_key_material(column_hash)
        key, iv = self._derive_key_iv(cds_hash)
        data_bytes = data.encode('utf-8')
        
        
        padder = padding.PKCS7(self.block_size).padder()
        padded_data = padder.update(data_bytes) + padder.finalize()

        if len(padded_data) > self.data_size:
            raise ValueError("Data is too long to encode")

        if len(padded_data) < self.data_size:
            padded_data += b'\x00' * (self.data_size - len(padded_data))
        
        key1 = key[:32]
        key2 = key[32:]

        cipher1 = Cipher(algorithms.AES(key1), modes.CTR(iv))
        encryptor1 = cipher1.encryptor()
        intermediate = encryptor1.update(padded_data) + encryptor1.finalize()
        
        cipher2 = Cipher(algorithms.AES(key2), modes.CTR(iv))
        encryptor2 = cipher2.encryptor()
        ciphertext = encryptor2.update(intermediate) + encryptor2.finalize()

        ciphertext_hex = ciphertext.hex()
        
        return ciphertext_hex
    
    
    def decoder(self,token):
        cds_hash = self._get_key_material('hash')
        key, iv = self._derive_key_iv(cds_hash)

        key1 = key[:32]
        key2 = key[32:]
        
        token = token['auth_token']
        token_bytes = bytes.fromhex(token)

        try:
            cipher2 = Cipher(algorithms.AES(key2), modes.CTR(iv))
            decryptor2 = cipher2.decryptor()
            intermediate = decryptor2.update(token_bytes) + decryptor2.finalize()
        
            cipher1 = Cipher(algorithms.AES(key1), modes.CTR(iv))
            decryptor1 = cipher1.decryptor()
            padded_data = decryptor1.update(intermediate) + decryptor1.finalize()

            padded_data = padded_data.rstrip(b'\x00')

            unpadder = padding.PKCS7(self.block_size).unpadder()
            unpadded_data = unpadder.update(padded_data) + unpadder.finalize()
            data = unpadded_data.decode('utf-8', errors='ignore')
        except Exception as e:
            RatException.fastLiquid("Failed to decode: Exp or Wrong")
        try:
            data_dict = ast.literal_eval(data)
        except Exception as e:
            RatException.fastLiquid("Invalid was maked this token")

                
        load_dotenv()
        _creds = os.getenv("ACCESS_CREDS")
        
        try:
            _creds_dict = ast.literal_eval(_creds)
        except Exception as e:
            RatException.fastLiquid("Internal Error ,but WTF")
        if data_dict['login'] and data_dict['password'] and data_dict['login'] == _creds_dict['login'] and data_dict['password'] == _creds_dict['password']:
            login = data_dict['login']
            password = data_dict['password']
            return login, password
        else:
            return False,False
        
        
        
    def decoder_verify(self,token):
        cds_hash = self._get_key_material('refrash_hash')
        key, iv = self._derive_key_iv(cds_hash)

        key1 = key[:32]
        key2 = key[32:]
        
        type = None
        if token.get('type'):
            type = token['type']
        if type != "refresh":
            RatException.fastLiquid("Invalid using this token now.")
        
        token = token['token_raw_code']
        token_bytes = bytes.fromhex(token)

        cipher2 = Cipher(algorithms.AES(key2), modes.CTR(iv))
        decryptor2 = cipher2.decryptor()
        intermediate = decryptor2.update(token_bytes) + decryptor2.finalize()
        
        cipher1 = Cipher(algorithms.AES(key1), modes.CTR(iv))
        decryptor1 = cipher1.decryptor()
        padded_data = decryptor1.update(intermediate) + decryptor1.finalize()

        padded_data = padded_data.rstrip(b'\x00')

        unpadder = padding.PKCS7(self.block_size).unpadder()
        unpadded_data = unpadder.update(padded_data) + unpadder.finalize()

        data = unpadded_data.decode('utf-8', errors='ignore')
        
        try:
            data_dict = ast.literal_eval(data)
        except Exception as e:
            RatException.fastLiquid("Invalid was maked this token")

                
        load_dotenv()
        _creds = os.getenv("ACCESS_CREDS")
        
        try:
            _creds_dict = ast.literal_eval(_creds)
        except Exception as e:
            RatException.fastLiquid("Internal Error ,but WTF")
        if data_dict['login'] and data_dict['password'] and data_dict['login'] == _creds_dict['login'] and data_dict['password'] == _creds_dict['password']:
            login = data_dict['login']
            password = data_dict['password']
            return login, password
        else:
            return False,False
        
        