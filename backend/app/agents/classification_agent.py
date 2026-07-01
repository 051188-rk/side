from typing import Dict, Any, Optional
from app.agents.base_agent import BaseAgent
from app.integrations.llm_provider import llm_provider
from app.core.logging import log


class ClassificationAgent(BaseAgent):
    def __init__(self):
        super().__init__("classification_agent")
        self.categories = [
            "Bug",
            "Feature Request",
            "Question",
            "Complaint",
            "Praise",
            "Security",
            "Payment",
            "Account",
            "Other"
        ]

    async def _execute(
        self,
        input_data: Dict[str, Any],
        feedback_id: Optional[str] = None,
        ticket_id: Optional[str] = None
    ) -> Dict[str, Any]:
        content = input_data.get("content", "")
        
        if not content:
            raise ValueError("Content is required")
        
        system_prompt = f"""You are a feedback classification expert. Classify the given feedback into one of these categories:
{', '.join(self.categories)}.

Respond with a JSON object containing:
- category: the selected category
- confidence: a float between 0 and 1 indicating confidence
- reasoning: a brief explanation for the classification"""

        prompt = f"Classify this feedback:\n\n{content}"
        
        schema = {
            "type": "object",
            "properties": {
                "category": {"type": "string", "enum": self.categories},
                "confidence": {"type": "number"},
                "reasoning": {"type": "string"}
            },
            "required": ["category", "confidence", "reasoning"]
        }
        
        result = await llm_provider.generate_structured(prompt, schema, system_prompt)
        
        log.info(f"Classified feedback: {feedback_id} as {result['category']} with confidence {result['confidence']}")
        
        return {
            "category": result["category"],
            "confidence": result["confidence"],
            "reasoning": result["reasoning"],
        }

    async def classify_batch(self, feedback_items: list) -> Dict[str, Any]:
        results = []
        
        for item in feedback_items:
            result = await self.execute({
                "content": item.get("content", ""),
            })
            results.append({
                "feedback_id": item.get("id"),
                **result,
            })
        
        category_counts = {}
        for result in results:
            category = result.get("result", {}).get("category", "Other")
            category_counts[category] = category_counts.get(category, 0) + 1
        
        return {
            "results": results,
            "category_counts": category_counts,
            "total_classified": len(results),
        }
