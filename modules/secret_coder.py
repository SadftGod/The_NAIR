import os
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64
import ast
from modules.palette import Palette as p
import json
from datetime import datetime, timedelta

class SecretCoder:
    def __init__(self) -> None:
        self.security_folder = 'app/configs/security'
        
    def generate_random_hash(self,length_hash: int = 32)->str:
        hash_code = os.path.join(self.security_folder,'codes.json')
        
        current_date = datetime.now()
        
        if not os.path.exists(self.security_folder):
            os.makedirs(self.security_folder)
        if not os.path.exists(hash_code):
            with open(hash_code,"w") as hash_folder:
                json.dump({}, hash_folder) 
                p.yellowTag("Secure Coder","File wasn't exist. Creating...")
            
        with open(hash_code, 'r') as hash_codes:
            json_codes = json.load(hash_codes)
        if 'date' in json_codes:
            stored_date = datetime.strptime(json_codes['date'], '%Y-%m-%d')
            if current_date <= stored_date:
                p.cyanTag("Secure Coder","Continue with not changes ;) - Date is not Expired")
                return
            new_date = current_date + timedelta(days=9*30)  # approximately 9 month 
            json_codes['date'] = new_date.strftime('%Y-%m-%d')
        else:
            json_codes['date'] = current_date.strftime('%Y-%m-%d')        
        
        bunny = os.urandom(length_hash).hex()
        json_codes['hash'] = bunny
    
        with open(hash_code, 'w') as file:
            json.dump(json_codes, file, indent=4)
        p.redTag("Secure Coder","Date had been expired")
        p.cyanTag("Secure Coder","Special hash generated")
        
    @staticmethod  
    def _unpad(data):
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        unpadded_data = unpadder.update(data) + unpadder.finalize()
        return unpadded_data  
    
    @staticmethod  
    def jwt_decoder(coded_data:str):
        """
        Method to decode payload from token 
        As argument request ['data'] from token 
        Returns normal dict with parametrs
        """
        
        with open('app/configs/security/codes.json','r') as codes:
            codes_content = json.load(codes)
        cds_hash = bytes.fromhex(codes_content.get('hash'))
        hash_key = cds_hash[:32]
        encrypted_payload_bytes = base64.b64decode(coded_data)
        iv = hash_key[:16] 
        encrypted_data = encrypted_payload_bytes[16:]
        cipher = Cipher(algorithms.AES(hash_key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_padded = decryptor.update(encrypted_data) + decryptor.finalize()
        decrypted = SecretCoder._unpad(decrypted_padded)
        
        decrypted_payload_str = decrypted.decode("utf-8")
        decrypted_payload = ast.literal_eval(decrypted_payload_str)
        return decrypted_payload
    
sc = SecretCoder()
