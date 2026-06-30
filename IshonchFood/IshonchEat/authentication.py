import jwt 
from django.conf import settings
import base64
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed

class JWTSharedSecretAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        print(f"=== JWT DEBUG START ===")
        print(f"Raw Authorization Header: {auth_header}") # 🔍 Check if Swagger is actually sending it

        if not auth_header:
            print("❌ Dropped out: No Authorization header found!")
            print(f"=== JWT DEBUG END ===")
            return None # Pass to other authentication layers or let permissions fail it

        try:
            # Expecting "Bearer <token>"
            parts = auth_header.split(' ')
            print(f"Split Header Parts: {parts}") # 🔍 Check if it split into exactly 2 parts

            if len(parts) != 2:
                print("❌ Dropped out: Header does not contain exactly 2 parts (Bearer <token>)")
                print(f"=== JWT DEBUG END ===")
                return None

            #token_type, token = auth_header.split(' ')

            token_type, token = parts[0], parts[1]
            if token_type.lower() != 'bearer':
                print(f"❌ Dropped out: Token prefix is '{token_type}', expected 'Bearer'")
                print(f"=== JWT DEBUG END ===")
                return None
        except Exception as e:
            print(f"❌ Dropped out during splitting: {e}")
            print(f"=== JWT DEBUG END ===")
            raise AuthenticationFailed('Invalid Authorization header format. Use "Bearer <token>"')

        # 3. If it passes everything above, it finally reaches the decoder!
        print(f"Attempting to decode token: {token[:15]}...")

        try:
            # Decode using the shared symmetric secret key (HS256)
            # Make sure settings.JWT_ACCESS_SECRET_KEY is configured in settings.py
            # 🔍 CRITICAL DEBUG PRINTS
            print(f"➔ RAW KEY IN SETTINGS: {settings.JWT_ACCESS_SECRET_KEY}")
            print(f"➔ KEY LENGTH: {len(settings.JWT_ACCESS_SECRET_KEY)}")

            secret_bytes = settings.JWT_ACCESS_SECRET_KEY.encode('utf-8')
            print(f"➔ ENCODED BYTES: {secret_bytes}")

            payload = jwt.decode(token,secret_bytes, algorithms=['HS256'],issuer='foodexpress-auth')
            print(f"✅ Success! Decoded Payload: {payload}")
            print(f"=== JWT DEBUG END ===")
            
            # 🌟 WE ADD A TRY/EXCEPT HERE TO CATCH THE 500 CRASH LINE INSTANTLY
            try:
                user = EphemeralJWTUser(payload)
                print(f"👤 EphemeralUser created successfully! ID: {user.id}, Permissions: {user.permissions}")
                print(f"=== JWT DEBUG END ===")
                return (user, token)
            except Exception as user_error:
                import traceback
                print("\n❌ CRASH HAPPENED INSIDE EphemeralJWTUser INITIALIZATION:")
                print(traceback.format_exc()) # 🔍 This will print the EXACT traceback
                print(f"=== JWT DEBUG END ===")
                raise Exception(f"Failed to build user: {user_error}")
            
        except jwt.ExpiredSignatureError:
            print("❌ JWT Error: The token has expired!")
            print(f"=== JWT DEBUG END ===")
            raise AuthenticationFailed('Access token has expired')
        except jwt.InvalidTokenError as e:
            print(f"❌ JWT Error: Decode failed because -> {e}")
            print(f"=== JWT DEBUG END ===")
            raise AuthenticationFailed('Invalid access token signature')

class EphemeralJWTUser:
    """
    Safely maps the parsed Node.js payload data to properties 
    Django views expect.
    """
    def __init__(self,payload):
        #FIXED: Read 'user_id' instead of standard 'sub'
        self.id = payload.get('user_id')          
        self.role = payload.get('role')     # CUSTOMER, RESTAURSNT_OWNER, COURIER, ADMIN
       
        # Safe extraction of permission code strings
        raw_permissions = payload.get('permissions', [])
        self.permissions = []

        for perm in raw_permissions:
            if isinstance(perm, dict) and 'code' in perm:
                self.permissions.append(perm['code'])
            elif isinstance(perm, str):
                self.permissions.append(perm)
            
        self.is_authenticated = True

    def has_perm(self,  permission_name):
        if self.role == 'ADMIN':
            return True
        return permission_name in self.permissions