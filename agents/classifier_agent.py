from core.doc_types import DOC_TYPES

def classify_doc(text: str) -> str:
    t = (text or "").lower()

    if "invoice" in t or "amount due" in t or "bill to" in t:
        return "invoice"
    if "lab" in t and ("reference range" in t or "result" in t):
        return "lab_report"
    if "explanation of benefits" in t or "eob" in t:
        return "insurance_eob"
    if "patient" in t and ("mrn" in t or "medical record" in t):
        return "medical_record"
    return "unknown"