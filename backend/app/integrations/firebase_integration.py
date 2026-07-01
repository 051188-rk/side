from typing import Optional, Dict, Any
from firebase_admin import auth
from app.config import settings
from app.core.logging import log
from app.core.exceptions import ExternalServiceException


class FirebaseIntegration:
    def __init__(self):
        self._initialized = False

    def _ensure_initialized(self):
        if not self._initialized:
            try:
                from firebase_admin import credentials
                import firebase_admin
                if not firebase_admin._apps:
                    cred = credentials.Certificate(settings.firebase_credentials_dict)
                    firebase_admin.initialize_app(cred)
                self._initialized = True
                log.info("Firebase integration initialized")
            except Exception as e:
                log.error(f"Failed to initialize Firebase: {e}")
                raise ExternalServiceException("Firebase", str(e))

    async def create_user(self, email: str, password: str, display_name: Optional[str] = None) -> Dict[str, Any]:
        self._ensure_initialized()
        try:
            user = auth.create_user(
                email=email,
                password=password,
                display_name=display_name,
            )
            log.info(f"Created Firebase user: {user.uid}")
            return {
                "uid": user.uid,
                "email": user.email,
                "display_name": user.display_name,
            }
        except Exception as e:
            log.error(f"Failed to create Firebase user: {e}")
            raise ExternalServiceException("Firebase", f"Failed to create user: {str(e)}")

    async def verify_token(self, token: str) -> Dict[str, Any]:
        self._ensure_initialized()
        try:
            decoded_token = auth.verify_id_token(token)
            log.info(f"Verified Firebase token for user: {decoded_token.get('uid')}")
            return decoded_token
        except Exception as e:
            log.error(f"Failed to verify Firebase token: {e}")
            raise ExternalServiceException("Firebase", f"Failed to verify token: {str(e)}")

    async def get_user(self, uid: str) -> Optional[Dict[str, Any]]:
        self._ensure_initialized()
        try:
            user = auth.get_user(uid)
            return {
                "uid": user.uid,
                "email": user.email,
                "display_name": user.display_name,
                "email_verified": user.email_verified,
                "disabled": user.disabled,
            }
        except auth.UserNotFoundError:
            return None
        except Exception as e:
            log.error(f"Failed to get Firebase user: {e}")
            raise ExternalServiceException("Firebase", f"Failed to get user: {str(e)}")

    async def update_user(self, uid: str, updates: Dict[str, Any]) -> bool:
        self._ensure_initialized()
        try:
            auth.update_user(uid, **updates)
            log.info(f"Updated Firebase user: {uid}")
            return True
        except Exception as e:
            log.error(f"Failed to update Firebase user: {e}")
            raise ExternalServiceException("Firebase", f"Failed to update user: {str(e)}")

    async def delete_user(self, uid: str) -> bool:
        self._ensure_initialized()
        try:
            auth.delete_user(uid)
            log.info(f"Deleted Firebase user: {uid}")
            return True
        except Exception as e:
            log.error(f"Failed to delete Firebase user: {e}")
            raise ExternalServiceException("Firebase", f"Failed to delete user: {str(e)}")

    async def send_password_reset_email(self, email: str) -> bool:
        self._ensure_initialized()
        try:
            auth.generate_password_reset_link(email)
            log.info(f"Sent password reset email to: {email}")
            return True
        except Exception as e:
            log.error(f"Failed to send password reset email: {e}")
            raise ExternalServiceException("Firebase", f"Failed to send password reset: {str(e)}")

    async def send_email_verification(self, email: str) -> bool:
        self._ensure_initialized()
        try:
            auth.generate_email_verification_link(email)
            log.info(f"Sent email verification to: {email}")
            return True
        except Exception as e:
            log.error(f"Failed to send email verification: {e}")
            raise ExternalServiceException("Firebase", f"Failed to send email verification: {str(e)}")


firebase_integration = FirebaseIntegration()
