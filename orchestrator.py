from langgraph.graph import StateGraph, END
from core.schemas import AgentState
from agents.ocr_agent import run_ocr
from agents.classifier_agent import classify_doc
from agents.extractor_agent import extract_fields
from agents.validator_agent import validate

def build_graph():
    g = StateGraph(AgentState)

    def ocr_node(state: AgentState):
        return {"raw_text": state.raw_text}

    def classify_node(state: AgentState):
        return {"doc_type": classify_doc(state.raw_text)}

    def extract_node(state: AgentState):
        return {"extraction": extract_fields(state.doc_type, state.raw_text)}

    def validate_node(state: AgentState):
        return {"extraction": validate(state.extraction)}

    g.add_node("classify", classify_node)
    g.add_node("extract", extract_node)
    g.add_node("validate", validate_node)

    g.set_entry_point("classify")
    g.add_edge("classify", "extract")
    g.add_edge("extract", "validate")
    g.add_edge("validate", END)
    return g.compile()

GRAPH = build_graph()

def run_pipeline(filename: str, raw_text: str) -> AgentState:
    state = AgentState(filename=filename, raw_text=raw_text)
    out = GRAPH.invoke(state)
    return out