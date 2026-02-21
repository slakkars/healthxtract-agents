from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class ExtractionResult(BaseModel):
    doc_type: str
    fields: Dict[str, Any] = Field(default_factory=dict)
    missing_required: List[str] = Field(default_factory=list)
    confidence: float = 0.0
    notes: Optional[str] = None

class AgentState(BaseModel):
    filename: str
    raw_text: str = ""
    doc_type: str = "unknown"
    extraction: Optional[ExtractionResult] = None