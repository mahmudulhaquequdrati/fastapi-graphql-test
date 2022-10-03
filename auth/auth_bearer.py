
from .auth_handler import decodeJWT


def verify_jwt( jwtoken: str) -> bool:
        isTokenValid: bool = False
        
        
        try:

            
            if jwtoken.startswith("Bearer"):

               token = jwtoken.split(" ")[1]
               print(token)
               decoded_token = decodeJWT(token)
            if decoded_token:
                isTokenValid = True
            else:
                isTokenValid = False    
        except:
            decoded_token = None
       
        return isTokenValid
