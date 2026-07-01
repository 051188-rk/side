from typing import Optional, List
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import aiosmtplib
from app.config import settings
from app.core.logging import log
from app.core.exceptions import ExternalServiceException


class SMTPIntegration:
    def __init__(self):
        self._host = settings.smtp_host
        self._port = settings.smtp_port
        self._username = settings.smtp_username
        self._password = settings.smtp_password
        self._from_email = settings.smtp_from_email
        self._from_name = settings.smtp_from_name
        self._use_tls = settings.smtp_use_tls

    async def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        html: bool = False,
        from_name: Optional[str] = None,
        reply_to: Optional[str] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None
    ) -> bool:
        try:
            message = MIMEMultipart("alternative")
            
            from_display_name = from_name or self._from_name
            message["From"] = formataddr((from_display_name, self._from_email))
            message["To"] = to_email
            message["Subject"] = subject
            
            if reply_to:
                message["Reply-To"] = reply_to
            
            if cc:
                message["Cc"] = ", ".join(cc)
            
            if html:
                html_part = MIMEText(body, "html")
                message.attach(html_part)
            else:
                text_part = MIMEText(body, "plain")
                message.attach(text_part)
            
            recipients = [to_email]
            if cc:
                recipients.extend(cc)
            if bcc:
                recipients.extend(bcc)
            
            await aiosmtplib.send(
                message,
                hostname=self._host,
                port=self._port,
                username=self._username,
                password=self._password,
                use_tls=self._use_tls,
                sender=self._from_email,
                recipients=recipients,
            )
            
            log.info(f"Sent SMTP email to {to_email}")
            return True
            
        except Exception as e:
            log.error(f"Failed to send SMTP email: {e}")
            raise ExternalServiceException("SMTP", f"Failed to send email: {str(e)}")

    async def send_bulk_email(
        self,
        to_emails: List[str],
        subject: str,
        body: str,
        html: bool = False
    ) -> int:
        success_count = 0
        for email in to_emails:
            try:
                await self.send_email(email, subject, body, html)
                success_count += 1
            except Exception as e:
                log.error(f"Failed to send bulk email to {email}: {e}")
        
        log.info(f"Sent bulk email to {success_count}/{len(to_emails)} recipients")
        return success_count

    async def send_template_email(
        self,
        to_email: str,
        template_name: str,
        context: Dict[str, Any]
    ) -> bool:
        try:
            from jinja2 import Template
            
            template_content = self._load_template(template_name)
            template = Template(template_content)
            body = template.render(**context)
            
            await self.send_email(to_email, context.get("subject", ""), body, html=True)
            return True
            
        except Exception as e:
            log.error(f"Failed to send template email: {e}")
            raise ExternalServiceException("SMTP", f"Failed to send template email: {str(e)}")

    def _load_template(self, template_name: str) -> str:
        templates = {
            "welcome": """
            <h1>Welcome to SIDE!</h1>
            <p>Hello {{ name }},</p>
            <p>Welcome to the SIDE platform. We're excited to have you on board!</p>
            """,
            "ticket_created": """
            <h1>New Ticket Created</h1>
            <p>Hello {{ name }},</p>
            <p>A new ticket has been created:</p>
            <p><strong>Title:</strong> {{ ticket_title }}</p>
            <p><strong>Description:</strong> {{ ticket_description }}</p>
            """,
            "ticket_assigned": """
            <h1>Ticket Assigned to You</h1>
            <p>Hello {{ name }},</p>
            <p>Ticket #{{ ticket_id }} has been assigned to you.</p>
            <p><strong>Title:</strong> {{ ticket_title }}</p>
            """,
        }
        
        return templates.get(template_name, "")


smtp_integration = SMTPIntegration()
