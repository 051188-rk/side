from typing import Optional, Dict, Any, List
import base64
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from app.config import settings
from app.core.logging import log
from app.core.exceptions import ExternalServiceException
import os
import pickle


class GmailIntegration:
    def __init__(self):
        self._service = None
        self._credentials = None
        self._initialized = False

    async def _ensure_initialized(self):
        if not self._initialized:
            try:
                creds = None
                if os.path.exists(settings.gmail_token_file):
                    with open(settings.gmail_token_file, 'rb') as token:
                        creds = pickle.load(token)

                if not creds or not creds.valid:
                    if creds and creds.expired and creds.refresh_token:
                        creds.refresh(Request())
                    else:
                        flow = InstalledAppFlow.from_client_secrets_file(
                            settings.gmail_credentials_file,
                            settings.gmail_scopes_list
                        )
                        creds = flow.run_local_server(port=0)

                    with open(settings.gmail_token_file, 'wb') as token:
                        pickle.dump(creds, token)

                self._service = build('gmail', 'v1', credentials=creds)
                self._credentials = creds
                self._initialized = True
                log.info("Gmail integration initialized")
            except Exception as e:
                log.error(f"Failed to initialize Gmail: {e}")
                raise ExternalServiceException("Gmail", str(e))

    async def list_messages(self, query: str = "", max_results: int = 100) -> List[Dict[str, Any]]:
        await self._ensure_initialized()
        try:
            results = self._service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()
            messages = results.get('messages', [])
            
            log.info(f"Retrieved {len(messages)} Gmail messages")
            return messages
        except Exception as e:
            log.error(f"Failed to list Gmail messages: {e}")
            raise ExternalServiceException("Gmail", f"Failed to list messages: {str(e)}")

    async def get_message(self, message_id: str) -> Dict[str, Any]:
        await self._ensure_initialized()
        try:
            message = self._service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()
            
            payload = message.get('payload', {})
            headers = {h['name']: h['value'] for h in payload.get('headers', [])}
            
            body = ""
            if 'parts' in payload:
                for part in payload['parts']:
                    if 'data' in part.get('body', {}):
                        body += base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
            elif 'data' in payload.get('body', {}):
                body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
            
            return {
                "id": message['id'],
                "thread_id": message['threadId'],
                "subject": headers.get('Subject', ''),
                "from": headers.get('From', ''),
                "to": headers.get('To', ''),
                "date": headers.get('Date', ''),
                "body": body,
                "snippet": message.get('snippet', ''),
            }
        except Exception as e:
            log.error(f"Failed to get Gmail message: {e}")
            raise ExternalServiceException("Gmail", f"Failed to get message: {str(e)}")

    async def send_email(self, to: str, subject: str, body: str, html: bool = False) -> bool:
        await self._ensure_initialized()
        try:
            message = MIMEMultipart()
            message['to'] = to
            message['subject'] = subject
            
            if html:
                message.attach(MIMEText(body, 'html'))
            else:
                message.attach(MIMEText(body, 'plain'))
            
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            
            self._service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()
            
            log.info(f"Sent Gmail email to {to}")
            return True
        except Exception as e:
            log.error(f"Failed to send Gmail email: {e}")
            raise ExternalServiceException("Gmail", f"Failed to send email: {str(e)}")

    async def search_emails(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        await self._ensure_initialized()
        try:
            messages = await self.list_messages(query=query, max_results=max_results)
            results = []
            for msg in messages:
                full_message = await self.get_message(msg['id'])
                results.append(full_message)
            
            log.info(f"Found {len(results)} Gmail emails matching query: {query}")
            return results
        except Exception as e:
            log.error(f"Failed to search Gmail emails: {e}")
            raise ExternalServiceException("Gmail", f"Failed to search emails: {str(e)}")

    async def mark_as_read(self, message_id: str) -> bool:
        await self._ensure_initialized()
        try:
            self._service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            
            log.info(f"Marked Gmail message {message_id} as read")
            return True
        except Exception as e:
            log.error(f"Failed to mark Gmail message as read: {e}")
            raise ExternalServiceException("Gmail", f"Failed to mark as read: {str(e)}")

    async def add_label(self, message_id: str, label: str) -> bool:
        await self._ensure_initialized()
        try:
            self._service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'addLabelIds': [label]}
            ).execute()
            
            log.info(f"Added label {label} to Gmail message {message_id}")
            return True
        except Exception as e:
            log.error(f"Failed to add label to Gmail message: {e}")
            raise ExternalServiceException("Gmail", f"Failed to add label: {str(e)}")


gmail_integration = GmailIntegration()
