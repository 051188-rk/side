from typing import Dict, Any, Optional
import re
from app.agents.base_agent import BaseAgent
from app.utils.helpers import sanitize_input, normalize_whitespace, extract_urls, extract_emails
from app.core.logging import log


class FeedbackCleanerAgent(BaseAgent):
    def __init__(self):
        super().__init__("feedback_cleaner")

    async def _execute(
        self,
        input_data: Dict[str, Any],
        feedback_id: Optional[str] = None,
        ticket_id: Optional[str] = None
    ) -> Dict[str, Any]:
        content = input_data.get("content", "")
        
        if not content:
            raise ValueError("Content is required")
        
        cleaned_content = await self._clean_content(content)
        
        is_spam = await self._detect_spam(cleaned_content)
        
        language = await self._detect_language(cleaned_content)
        
        urls = extract_urls(cleaned_content)
        emails = extract_emails(cleaned_content)
        
        log.info(f"Cleaned feedback: {feedback_id}, spam: {is_spam}, language: {language}")
        
        return {
            "cleaned_content": cleaned_content,
            "is_spam": is_spam,
            "language": language,
            "urls": urls,
            "emails": emails,
            "original_length": len(content),
            "cleaned_length": len(cleaned_content),
        }

    async def _clean_content(self, content: str) -> str:
        content = sanitize_input(content)
        content = normalize_whitespace(content)
        
        content = re.sub(r'\s+', ' ', content)
        
        content = re.sub(r'(\r\n|\n|\r)', ' ', content)
        
        content = content.strip()
        
        return content

    async def _detect_spam(self, content: str) -> bool:
        spam_keywords = [
            "buy now", "click here", "free money", "winner", "congratulations",
            "you have won", "act now", "limited time", "exclusive offer",
            "viagra", "casino", "lottery", "prize", "award"
        ]
        
        content_lower = content.lower()
        
        for keyword in spam_keywords:
            if keyword in content_lower:
                return True
        
        if len(content) < 10:
            return True
        
        url_count = len(re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content))
        if url_count > 5:
            return True
        
        return False

    async def _detect_language(self, content: str) -> str:
        if not content:
            return "unknown"
        
        common_words = {
            "english": ["the", "be", "to", "of", "and", "a", "in", "that", "have", "i"],
            "spanish": ["el", "de", "que", "y", "a", "en", "un", "ser", "se", "no"],
            "french": ["le", "de", "et", "à", "un", "il", "être", "et", "en", "avoir"],
            "german": ["der", "die", "und", "in", "den", "von", "das", "mit", "sich", "auf"],
        }
        
        content_lower = content.lower()
        words = content_lower.split()
        
        language_scores = {}
        for lang, keywords in common_words.items():
            score = sum(1 for word in words if word in keywords)
            language_scores[lang] = score
        
        detected_language = max(language_scores, key=language_scores.get) if language_scores else "unknown"
        
        if language_scores.get(detected_language, 0) == 0:
            detected_language = "unknown"
        
        return detected_language

    async def extract_attachments(self, content: str) -> list:
        attachment_patterns = [
            r'\[.*?attachment.*?\]',
            r'attached:.*',
            r'attachment:.*',
        ]
        
        attachments = []
        for pattern in attachment_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            attachments.extend(matches)
        
        return attachments
