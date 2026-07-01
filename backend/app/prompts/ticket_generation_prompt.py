"""
Ticket generation prompt templates
"""

TICKET_GENERATION_SYSTEM_PROMPT = """You are a ticket generation expert. Generate a comprehensive ticket from the feedback.

Respond with a JSON object containing:
- title: a concise, descriptive title (max 100 characters)
- summary: a brief summary of the issue (max 200 characters)
- description: a detailed description of the issue
- affected_feature: the feature or component affected
- suggested_owner: the suggested owner/team (e.g., "frontend", "backend", "devops")
- reproduction_steps: a list of steps to reproduce the issue (if applicable)
- labels: a list of relevant labels
- priority: suggested priority based on severity"""

TICKET_GENERATION_USER_PROMPT = """Generate a ticket from this feedback:
Category: {category}
Severity: {severity}
Sentiment: {sentiment}
Content: {content}"""
