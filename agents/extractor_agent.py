import re
from core.schemas import ExtractionResult

def extract_fields(doc_type: str, text: str) -> ExtractionResult:
    t = text or ""
    fields = {}
    missing = []

    if doc_type == "invoice":
        # examples only — tune to your data
        amt = re.search(r"(amount due|total)\s*[:$]?\s*\$?\s*([0-9,]+(\.[0-9]{2})?)", t, re.I)
        inv = re.search(r"(invoice\s*(no|#))\s*[:#]?\s*([A-Z0-9\-]+)", t, re.I)

        if inv: fields["invoice_number"] = inv.group(3)
        else: missing.append("invoice_number")

        if amt: fields["amount_due"] = amt.group(2)
        else: missing.append("amount_due")

        confidence = 0.8 if len(missing) == 0 else 0.5

    elif doc_type == "lab_report":
        # very simplified: extract patient name and a few results patterns
        name = re.search(r"patient\s*name\s*[:\-]\s*(.+)", t, re.I)
        if name: fields["patient_name"] = name.group(1).strip()

        # Example: "Glucose 95 mg/dL"
        results = re.findall(r"\n([A-Za-z][A-Za-z \-/]+)\s+([0-9.]+)\s+([a-zA-Z/%]+)\b", t)
        fields["results"] = [{"test": a.strip(), "value": b, "unit": c} for a,b,c in results[:25]]
        confidence = 0.6

    else:
        fields["raw_excerpt"] = t[:1000]
        confidence = 0.3
        missing = []

    return ExtractionResult(
        doc_type=doc_type,
        fields=fields,
        missing_required=missing,
        confidence=confidence,
        notes="Baseline regex extractor; replace with model-based extractor later."
    )