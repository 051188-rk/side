from typing import Dict, Any, Optional, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from app.agents import (
    FeedbackCleanerAgent,
    ClassificationAgent,
    SeverityAgent,
    SentimentAgent,
    DuplicateDetectionAgent,
    TicketGenerationAgent,
    PriorityAgent,
    MemoryAgent,
    ResponseDraftAgent,
    SearchAgent,
    FetchAgent,
    RoutingAgent,
)
from app.core.logging import log


class FeedbackState(TypedDict):
    content: str
    feedback_id: Optional[str]
    ticket_id: Optional[str]
    cleaned_content: Optional[str]
    is_spam: Optional[bool]
    language: Optional[str]
    category: Optional[str]
    severity: Optional[str]
    sentiment: Optional[str]
    is_duplicate: Optional[bool]
    cluster_id: Optional[str]
    priority_score: Optional[float]
    priority_level: Optional[str]
    memory_id: Optional[str]
    draft_response: Optional[str]
    search_results: Optional[list]
    fetched_content: Optional[list]
    context: Dict[str, Any]
    errors: list


class FeedbackProcessingGraph:
    def __init__(self):
        self.cleaner_agent = FeedbackCleanerAgent()
        self.classification_agent = ClassificationAgent()
        self.severity_agent = SeverityAgent()
        self.sentiment_agent = SentimentAgent()
        self.duplicate_agent = DuplicateDetectionAgent()
        self.ticket_agent = TicketGenerationAgent()
        self.priority_agent = PriorityAgent()
        self.memory_agent = MemoryAgent()
        self.response_agent = ResponseDraftAgent()
        self.search_agent = SearchAgent()
        self.fetch_agent = FetchAgent()
        self.routing_agent = RoutingAgent()
        
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        workflow = StateGraph(FeedbackState)
        
        workflow.add_node("routing", self._routing_node)
        workflow.add_node("cleaning", self._cleaning_node)
        workflow.add_node("classification", self._classification_node)
        workflow.add_node("sentiment", self._sentiment_node)
        workflow.add_node("severity", self._severity_node)
        workflow.add_node("search", self._search_node)
        workflow.add_node("fetch", self._fetch_node)
        workflow.add_node("duplicate_detection", self._duplicate_detection_node)
        workflow.add_node("memory_storage", self._memory_storage_node)
        workflow.add_node("ticket_generation", self._ticket_generation_node)
        workflow.add_node("priority_calculation", self._priority_calculation_node)
        workflow.add_node("response_draft", self._response_draft_node)
        
        workflow.set_entry_point("routing")
        
        workflow.add_conditional_edges(
            "routing",
            self._should_clean,
            {
                "clean": "cleaning",
                "skip_cleaning": "classification",
                "spam": END,
            }
        )
        
        workflow.add_edge("cleaning", "classification")
        
        workflow.add_conditional_edges(
            "classification",
            self._should_analyze_sentiment,
            {
                "analyze": "sentiment",
                "skip": "severity",
            }
        )
        
        workflow.add_edge("sentiment", "severity")
        
        workflow.add_conditional_edges(
            "severity",
            self._should_search,
            {
                "search": "search",
                "skip": "duplicate_detection",
            }
        )
        
        workflow.add_conditional_edges(
            "search",
            self._should_fetch,
            {
                "fetch": "fetch",
                "skip": "duplicate_detection",
            }
        )
        
        workflow.add_edge("fetch", "duplicate_detection")
        
        workflow.add_conditional_edges(
            "duplicate_detection",
            self._should_generate_ticket,
            {
                "generate": "ticket_generation",
                "skip": "memory_storage",
            }
        )
        
        workflow.add_edge("ticket_generation", "priority_calculation")
        workflow.add_edge("priority_calculation", "memory_storage")
        
        workflow.add_conditional_edges(
            "memory_storage",
            self._should_draft_response,
            {
                "draft": "response_draft",
                "skip": END,
            }
        )
        
        workflow.add_edge("response_draft", END)
        
        return workflow.compile()

    async def _routing_node(self, state: FeedbackState) -> FeedbackState:
        log.info("Executing routing node")
        
        routing_result = await self.routing_agent.execute({
            "task_type": "process_feedback",
            "content": state["content"],
            "context": state["context"],
        })
        
        state["context"]["workflow"] = routing_result.get("result", {}).get("workflow", {})
        
        return state

    async def _cleaning_node(self, state: FeedbackState) -> FeedbackState:
        log.info("Executing cleaning node")
        
        cleaning_result = await self.cleaner_agent.execute({
            "content": state["content"],
        })
        
        result_data = cleaning_result.get("result", {})
        state["cleaned_content"] = result_data.get("cleaned_content")
        state["is_spam"] = result_data.get("is_spam")
        state["language"] = result_data.get("language")
        
        if state["is_spam"]:
            state["errors"].append("Content marked as spam")
        
        return state

    async def _classification_node(self, state: FeedbackState) -> FeedbackState:
        log.info("Executing classification node")
        
        content = state.get("cleaned_content") or state["content"]
        
        classification_result = await self.classification_agent.execute({
            "content": content,
        })
        
        result_data = classification_result.get("result", {})
        state["category"] = result_data.get("category")
        state["context"]["category"] = result_data.get("category")
        
        return state

    async def _sentiment_node(self, state: FeedbackState) -> FeedbackState:
        log.info("Executing sentiment node")
        
        content = state.get("cleaned_content") or state["content"]
        
        sentiment_result = await self.sentiment_agent.execute({
            "content": content,
        })
        
        result_data = sentiment_result.get("result", {})
        state["sentiment"] = result_data.get("sentiment")
        state["context"]["sentiment"] = result_data.get("sentiment")
        
        return state

    async def _severity_node(self, state: FeedbackState) -> FeedbackState:
        log.info("Executing severity node")
        
        content = state.get("cleaned_content") or state["content"]
        
        severity_result = await self.severity_agent.execute({
            "content": content,
            "category": state.get("category", ""),
        })
        
        result_data = severity_result.get("result", {})
        state["severity"] = result_data.get("severity")
        state["context"]["severity"] = result_data.get("severity")
        
        return state

    async def _search_node(self, state: FeedbackState) -> FeedbackState:
        log.info("Executing search node")
        
        content = state.get("cleaned_content") or state["content"]
        
        search_result = await self.search_agent.execute({
            "query": content[:500],
            "search_type": "semantic",
            "limit": 5,
        })
        
        state["search_results"] = search_result.get("result", {}).get("results", [])
        
        return state

    async def _fetch_node(self, state: FeedbackState) -> FeedbackState:
        log.info("Executing fetch node")
        
        urls = []
        for result in state.get("search_results", []):
            if result.get("url"):
                urls.append(result["url"])
        
        if urls:
            fetch_result = await self.fetch_agent.execute({
                "url": urls[0],
            })
            state["fetched_content"] = [fetch_result.get("result", {})]
        
        return state

    async def _duplicate_detection_node(self, state: FeedbackState) -> FeedbackState:
        log.info("Executing duplicate detection node")
        
        content = state.get("cleaned_content") or state["content"]
        
        duplicate_result = await self.duplicate_agent.execute({
            "content": content,
            "category": state.get("category", ""),
        })
        
        result_data = duplicate_result.get("result", {})
        state["is_duplicate"] = result_data.get("is_duplicate")
        state["cluster_id"] = result_data.get("cluster_id")
        
        return state

    async def _ticket_generation_node(self, state: FeedbackState) -> FeedbackState:
        log.info("Executing ticket generation node")
        
        content = state.get("cleaned_content") or state["content"]
        
        ticket_result = await self.ticket_agent.execute({
            "content": content,
            "category": state.get("category", ""),
            "severity": state.get("severity", ""),
            "sentiment": state.get("sentiment", ""),
            "organization_id": state["context"].get("organization_id"),
        })
        
        result_data = ticket_result.get("result", {})
        state["ticket_id"] = result_data.get("ticket_id")
        
        return state

    async def _priority_calculation_node(self, state: FeedbackState) -> FeedbackState:
        log.info("Executing priority calculation node")
        
        priority_result = await self.priority_agent.execute({
            "severity": state.get("severity", "Medium"),
            "sentiment": state.get("sentiment", "Neutral"),
            "duplicate_count": 1 if state.get("is_duplicate") else 0,
            "affected_users": 1,
            "customer_tier": state["context"].get("customer_tier", "standard"),
            "category": state.get("category", ""),
        }, ticket_id=state.get("ticket_id"))
        
        result_data = priority_result.get("result", {})
        state["priority_score"] = result_data.get("priority_score")
        state["priority_level"] = result_data.get("priority_level")
        
        return state

    async def _memory_storage_node(self, state: FeedbackState) -> FeedbackState:
        log.info("Executing memory storage node")
        
        content = state.get("cleaned_content") or state["content"]
        
        memory_result = await self.memory_agent.execute({
            "content": content,
            "memory_type": f"feedback_{state.get('category', 'general')}",
            "related_entities": [state.get("feedback_id"), state.get("ticket_id")],
        }, feedback_id=state.get("feedback_id"), ticket_id=state.get("ticket_id"))
        
        result_data = memory_result.get("result", {})
        state["memory_id"] = result_data.get("memory_id")
        
        return state

    async def _response_draft_node(self, state: FeedbackState) -> FeedbackState:
        log.info("Executing response draft node")
        
        content = state.get("cleaned_content") or state["content"]
        
        response_result = await self.response_agent.execute({
            "content": content,
            "channel": state["context"].get("channel", "email"),
            "ticket_title": state["context"].get("ticket_title", ""),
            "resolution": state["context"].get("resolution", ""),
        })
        
        result_data = response_result.get("result", {})
        state["draft_response"] = result_data.get("draft_response")
        
        return state

    def _should_clean(self, state: FeedbackState) -> str:
        if state.get("is_spam"):
            return "spam"
        workflow = state.get("context", {}).get("workflow", {})
        if workflow.get("skip_cleaning", False):
            return "skip_cleaning"
        return "clean"

    def _should_analyze_sentiment(self, state: FeedbackState) -> str:
        category = state.get("category", "")
        if category in ["Question", "Praise"]:
            return "skip"
        return "analyze"

    def _should_search(self, state: FeedbackState) -> str:
        category = state.get("category", "")
        if category in ["Question", "Feature Request"]:
            return "search"
        return "skip"

    def _should_fetch(self, state: FeedbackState) -> str:
        if state.get("search_results"):
            return "fetch"
        return "skip"

    def _should_generate_ticket(self, state: FeedbackState) -> str:
        if state.get("is_duplicate"):
            return "skip"
        category = state.get("category", "")
        if category in ["Praise", "Question"]:
            return "skip"
        return "generate"

    def _should_draft_response(self, state: FeedbackState) -> str:
        sentiment = state.get("sentiment", "")
        if sentiment in ["Angry", "Frustrated", "Urgent"]:
            return "draft"
        return "skip"

    async def process(self, content: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        initial_state: FeedbackState = {
            "content": content,
            "feedback_id": context.get("feedback_id") if context else None,
            "ticket_id": None,
            "cleaned_content": None,
            "is_spam": False,
            "language": None,
            "category": None,
            "severity": None,
            "sentiment": None,
            "is_duplicate": False,
            "cluster_id": None,
            "priority_score": None,
            "priority_level": None,
            "memory_id": None,
            "draft_response": None,
            "search_results": None,
            "fetched_content": None,
            "context": context or {},
            "errors": [],
        }
        
        log.info("Starting feedback processing graph")
        
        final_state = await self.graph.ainvoke(initial_state)
        
        log.info("Feedback processing graph completed")
        
        return {
            "feedback_id": final_state.get("feedback_id"),
            "ticket_id": final_state.get("ticket_id"),
            "category": final_state.get("category"),
            "severity": final_state.get("severity"),
            "sentiment": final_state.get("sentiment"),
            "priority_level": final_state.get("priority_level"),
            "is_duplicate": final_state.get("is_duplicate"),
            "cluster_id": final_state.get("cluster_id"),
            "draft_response": final_state.get("draft_response"),
            "errors": final_state.get("errors", []),
        }


feedback_graph = FeedbackProcessingGraph()
