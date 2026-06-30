import jwt 
from django.conf import settings
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed

class JWTSharedSecretAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        print(f"=== JWT DEBUG START ===")
        print(f"Raw Authorization Header: {auth_header}")

        if not auth_header:
            print(" Dropped out: No Authorization header found!")
            print(f"=== JWT DEBUG END ===")
            return None 

        try:
            parts = auth_header.split(' ')
            if len(parts) != 2:
                print(" Dropped out: Header does not contain exactly 2 parts (Bearer <token>)")
                print(f"=== JWT DEBUG END ===")
                return None

            token_type, token = parts[0], parts[1]
            if token_type.lower() != 'bearer':
                print(f" Dropped out: Token prefix is '{token_type}', expected 'Bearer'")
                print(f"=== JWT DEBUG END ===")
                return None
        except Exception as e:
            print(f"❌ Dropped out during splitting: {e}")
            print(f"=== JWT DEBUG END ===")
            raise AuthenticationFailed('Invalid Authorization header format. Use "Bearer <token>"')

        print(f"Attempting to decode token: {token[:15]}...")

        try:

            
            secret_key = str(settings.JWT_ACCESS_SECRET_KEY)

            print(f"\nJWT ACCESS TOKEN: {settings.JWT_ACCESS_SECRET_KEY}\n")

            #  MATCH DRF CLAIMS EXACTLY: Pass the explicit issuer check
            payload = jwt.decode(
                token, 
                secret_key, 
                algorithms=['HS256'],
                issuer='foodexpress-auth' #  Crucial configuration line
            )
            print(f" Success! Decoded Payload: {payload}")
            
            try:
                user = EphemeralJWTUser(payload)
                print(f"👤 EphemeralUser created successfully! ID: {user.id}, Permissions: {user.permissions}")
                print(f"=== JWT DEBUG END ===")
                return (user, token)
            except Exception as user_error:
                import traceback
                print("\n CRASH HAPPENED INSIDE EphemeralJWTUser INITIALIZATION:")
                print(traceback.format_exc()) 
                print(f"=== JWT DEBUG END ===")
                raise Exception(f"Failed to build user: {user_error}")
            
        except jwt.ExpiredSignatureError:
            print(" JWT Error: The token has expired!")
            print(f"=== JWT DEBUG END ===")
            raise AuthenticationFailed('Access token has expired')
        except jwt.InvalidSignatureError:
            print(" JWT Error: Signature verification failed!")
            print(f"=== JWT DEBUG END ===")
            raise AuthenticationFailed('Invalid access token signature')
        except jwt.InvalidTokenError as e:
            print(f" JWT Error: Decode failed because -> {e}")
            print(f"=== JWT DEBUG END ===")
            raise AuthenticationFailed('Invalid access token structure')

class EphemeralJWTUser:
    """
    Maps parsed Node.js payload data to standard Django properties.
    """
    def __init__(self, payload):
        self.id = payload.get('user_id')          
        self.role = payload.get('role')     
       
        raw_permissions = payload.get('permissions', [])
        self.permissions = []

        for perm in raw_permissions:
            if isinstance(perm, dict) and 'code' in perm:
                self.permissions.append(perm['code'])
            elif isinstance(perm, str):
                self.permissions.append(perm)
            
        self.is_authenticated = True

    def has_perm(self, permission_name):
        if self.role == 'ADMIN':
            return True
        return permission_name in self.permissions