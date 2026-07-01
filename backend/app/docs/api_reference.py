"""
API Reference Documentation Generator

This module generates API reference documentation from FastAPI routes.
"""

from fastapi import FastAPI
from typing import Dict, List, Any
import json


class APIReferenceGenerator:
    def __init__(self, app: FastAPI):
        self.app = app

    def generate_openapi_spec(self) -> Dict[str, Any]:
        """Generate OpenAPI specification from the FastAPI app."""
        return self.app.openapi()

    def generate_markdown_docs(self) -> str:
        """Generate Markdown documentation from OpenAPI spec."""
        spec = self.generate_openapi_spec()
        markdown = []
        
        markdown.append(f"# {spec['info']['title']}\n")
        markdown.append(f"{spec['info']['description']}\n")
        markdown.append(f"Version: {spec['info']['version']}\n\n")
        
        # Group by tags
        paths_by_tag: Dict[str, List[Dict[str, Any]]] = {}
        for path, methods in spec['paths'].items():
            for method, details in methods.items():
                tags = details.get('tags', ['default'])
                for tag in tags:
                    if tag not in paths_by_tag:
                        paths_by_tag[tag] = []
                    paths_by_tag[tag].append({
                        'path': path,
                        'method': method.upper(),
                        'details': details
                    })
        
        # Generate documentation for each tag
        for tag, endpoints in paths_by_tag.items():
            markdown.append(f"## {tag}\n\n")
            for endpoint in endpoints:
                markdown.append(f"### {endpoint['method']} {endpoint['path']}\n\n")
                markdown.append(f"{endpoint['details'].get('summary', 'No description')}\n\n")
                
                # Parameters
                params = endpoint['details'].get('parameters', [])
                if params:
                    markdown.append("#### Parameters\n\n")
                    for param in params:
                        markdown.append(f"- **{param['name']}** ({param.get('in', 'query')}): {param.get('description', 'No description')}\n")
                    markdown.append("\n")
                
                # Request body
                if 'requestBody' in endpoint['details']:
                    markdown.append("#### Request Body\n\n")
                    content = endpoint['details']['requestBody'].get('content', {})
                    for content_type, schema in content.items():
                        markdown.append(f"Content-Type: {content_type}\n\n")
                        if 'schema' in schema:
                            markdown.append(f"Schema: {json.dumps(schema['schema'], indent=2)}\n\n")
                
                # Responses
                responses = endpoint['details'].get('responses', {})
                if responses:
                    markdown.append("#### Responses\n\n")
                    for status_code, response in responses.items():
                        markdown.append(f"**{status_code}**: {response.get('description', 'No description')}\n\n")
        
        return "\n".join(markdown)

    def save_openapi_json(self, filepath: str):
        """Save OpenAPI spec to JSON file."""
        spec = self.generate_openapi_spec()
        with open(filepath, 'w') as f:
            json.dump(spec, f, indent=2)

    def save_markdown_docs(self, filepath: str):
        """Save Markdown documentation to file."""
        markdown = self.generate_markdown_docs()
        with open(filepath, 'w') as f:
            f.write(markdown)
