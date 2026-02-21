from core.schemas import ExtractionResult

def validate(result: ExtractionResult) -> ExtractionResult:
    # Example policy: require certain fields & min confidence
    if result.doc_type == "invoice":
        required = ["invoice_number", "amount_due"]
        missing = [k for k in required if k not in result.fields or not result.fields.get(k)]
        result.missing_required = missing
        if missing:
            result.confidence = min(result.confidence, 0.5)

    # Add format checks
    # Add routing decisions elsewhere (or add result.fields["needs_review"]=True)
    return result