from typing import Optional, Dict, Any, List
from github import Github, GithubException
from app.config import settings
from app.core.logging import log
from app.core.exceptions import ExternalServiceException


class GitHubIntegration:
    def __init__(self):
        self._client: Optional[Github] = None
        self._initialized = False

    async def _ensure_initialized(self):
        if not self._initialized:
            try:
                self._client = Github(settings.github_access_token)
                self._initialized = True
                log.info("GitHub integration initialized")
            except Exception as e:
                log.error(f"Failed to initialize GitHub: {e}")
                raise ExternalServiceException("GitHub", str(e))

    async def get_repository(self, repo_name: str) -> Dict[str, Any]:
        await self._ensure_initialized()
        try:
            repo = self._client.get_repo(repo_name)
            return {
                "name": repo.name,
                "full_name": repo.full_name,
                "description": repo.description,
                "url": repo.html_url,
                "stars": repo.stargazers_count,
                "forks": repo.forks_count,
                "open_issues": repo.open_issues_count,
                "owner": repo.owner.login,
            }
        except GithubException as e:
            log.error(f"Failed to get GitHub repository: {e}")
            raise ExternalServiceException("GitHub", f"Failed to get repository: {str(e)}")

    async def create_issue(
        self,
        repo_name: str,
        title: str,
        body: str,
        labels: Optional[List[str]] = None,
        assignees: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        await self._ensure_initialized()
        try:
            repo = self._client.get_repo(repo_name)
            issue = repo.create_issue(
                title=title,
                body=body,
                labels=labels or [],
                assignees=assignees or [],
            )
            
            log.info(f"Created GitHub issue #{issue.number} in {repo_name}")
            return {
                "number": issue.number,
                "id": issue.id,
                "title": issue.title,
                "url": issue.html_url,
                "state": issue.state,
            }
        except GithubException as e:
            log.error(f"Failed to create GitHub issue: {e}")
            raise ExternalServiceException("GitHub", f"Failed to create issue: {str(e)}")

    async def update_issue(
        self,
        repo_name: str,
        issue_number: int,
        title: Optional[str] = None,
        body: Optional[str] = None,
        state: Optional[str] = None,
        labels: Optional[List[str]] = None
    ) -> bool:
        await self._ensure_initialized()
        try:
            repo = self._client.get_repo(repo_name)
            issue = repo.get_issue(issue_number)
            
            if title:
                issue.edit(title=title)
            if body:
                issue.edit(body=body)
            if state:
                issue.edit(state=state)
            if labels:
                issue.edit(labels=labels)
            
            log.info(f"Updated GitHub issue #{issue_number} in {repo_name}")
            return True
        except GithubException as e:
            log.error(f"Failed to update GitHub issue: {e}")
            raise ExternalServiceException("GitHub", f"Failed to update issue: {str(e)}")

    async def get_issues(self, repo_name: str, state: str = "open", limit: int = 100) -> List[Dict[str, Any]]:
        await self._ensure_initialized()
        try:
            repo = self._client.get_repo(repo_name)
            issues = repo.get_issues(state=state)[:limit]
            
            results = []
            for issue in issues:
                results.append({
                    "number": issue.number,
                    "id": issue.id,
                    "title": issue.title,
                    "body": issue.body,
                    "state": issue.state,
                    "url": issue.html_url,
                    "user": issue.user.login,
                    "labels": [label.name for label in issue.labels],
                    "created_at": issue.created_at.isoformat() if issue.created_at else None,
                })
            
            log.info(f"Retrieved {len(results)} GitHub issues from {repo_name}")
            return results
        except GithubException as e:
            log.error(f"Failed to get GitHub issues: {e}")
            raise ExternalServiceException("GitHub", f"Failed to get issues: {str(e)}")

    async def add_comment(self, repo_name: str, issue_number: int, body: str) -> bool:
        await self._ensure_initialized()
        try:
            repo = self._client.get_repo(repo_name)
            issue = repo.get_issue(issue_number)
            issue.create_comment(body)
            
            log.info(f"Added comment to GitHub issue #{issue_number} in {repo_name}")
            return True
        except GithubException as e:
            log.error(f"Failed to add GitHub comment: {e}")
            raise ExternalServiceException("GitHub", f"Failed to add comment: {str(e)}")

    async def close_issue(self, repo_name: str, issue_number: int) -> bool:
        await self._ensure_initialized()
        try:
            repo = self._client.get_repo(repo_name)
            issue = repo.get_issue(issue_number)
            issue.edit(state="closed")
            
            log.info(f"Closed GitHub issue #{issue_number} in {repo_name}")
            return True
        except GithubException as e:
            log.error(f"Failed to close GitHub issue: {e}")
            raise ExternalServiceException("GitHub", f"Failed to close issue: {str(e)}")

    async def verify_webhook(self, payload: bytes, signature: str) -> bool:
        import hmac
        import hashlib
        
        expected_signature = hmac.new(
            settings.github_webhook_secret.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_signature)

    async def get_user_info(self, username: str) -> Dict[str, Any]:
        await self._ensure_initialized()
        try:
            user = self._client.get_user(username)
            return {
                "login": user.login,
                "name": user.name,
                "email": user.email,
                "bio": user.bio,
                "public_repos": user.public_repos,
                "followers": user.followers,
                "following": user.following,
            }
        except GithubException as e:
            log.error(f"Failed to get GitHub user info: {e}")
            raise ExternalServiceException("GitHub", f"Failed to get user info: {str(e)}")


github_integration = GitHubIntegration()
