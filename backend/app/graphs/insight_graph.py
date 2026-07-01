from typing import Dict, Any, Optional, TypedDict
from langgraph.graph import StateGraph, END
from app.agents import InsightAgent, MemoryAgent, SearchAgent
from app.core.logging import log


class InsightState(TypedDict):
    insight_type: str
    time_range: str
    summary: Optional[str]
    trending_issues: Optional[list]
    top_bugs: Optional[list]
    feature_requests: Optional[list]
    context: Dict[str, Any]
    memory_context: Optional[dict]


class InsightGenerationGraph:
    def __init__(self):
        self.insight_agent = InsightAgent()
        self.memory_agent = MemoryAgent()
        self.search_agent = SearchAgent()
        
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        workflow = StateGraph(InsightState)
        
        workflow.add_node("memory_retrieval", self._memory_retrieval_node)
        workflow.add_node("insight_generation", self._insight_generation_node)
        
        workflow.set_entry_point("memory_retrieval")
        workflow.add_edge("memory_retrieval", "insight_generation")
        workflow.add_edge("insight_generation", END)
        
        return workflow.compile()

    async def _memory_retrieval_node(self, state: InsightState) -> InsightState:
        log.info("Executing memory retrieval node")
        
        query = f"{state['insight_type']} {state['time_range']}"
        
        memory_context = await self.memory_agent.retrieve_historical_context(query)
        
        state["memory_context"] = memory_context
        
        return state

    async def _insight_generation_node(self, state: InsightState) -> InsightState:
        log.info("Executing insight generation node")
        
        insight_result = await self.insight_agent.execute({
            "insight_type": state["insight_type"],
            "time_range": state["time_range"],
        })
        
        result_data = insight_result.get("result", {})
        
        if state["insight_type"] == "daily_summary":
            state["summary"] = result_data.get("summary")
        elif state["insight_type"] == "weekly_summary":
            state["summary"] = result_data.get("summary")
        elif state["insight_type"] == "trending_issues":
            state["trending_issues"] = result_data.get("trending_issues")
        elif state["insight_type"] == "top_bugs":
            state["top_bugs"] = result_data.get("top_bugs")
        elif state["insight_type"] == "feature_requests":
            state["feature_requests"] = result_data.get("top_features")
        
        return state

    async def generate_insights(
        self,
        insight_type: str = "daily_summary",
        time_range: str = "week"
    ) -> Dict[str, Any]:
        initial_state: InsightState = {
            "insight_type": insight_type,
            "time_range": time_range,
            "summary": None,
            "trending_issues": None,
            "top_bugs": None,
            "feature_requests": None,
            "context": {},
            "memory_context": None,
        }
        
        log.info(f"Starting insight generation graph: {insight_type}")
        
        final_state = await self.graph.ainvoke(initial_state)
        
        log.info("Insight generation graph completed")
        
        return {
            "insight_type": insight_type,
            "time_range": time_range,
            "summary": final_state.get("summary"),
            "trending_issues": final_state.get("trending_issues"),
            "top_bugs": final_state.get("top_bugs"),
            "feature_requests": final_state.get("feature_requests"),
            "memory_context": final_state.get("memory_context"),
        }


insight_graph = InsightGenerationGraph()
