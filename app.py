import gradio as gr
from agents.ocr_agent import run_ocr
from orchestrator import run_pipeline

def process(file_obj):
    filename = file_obj.name.split("/")[-1]
    file_bytes = open(file_obj.name, "rb").read()

    text = run_ocr(file_bytes, filename)
    final_state = run_pipeline(filename, text)

    extraction = final_state.extraction.model_dump() if final_state.extraction else {}
    return text[:8000], final_state.doc_type, extraction  # limit preview

with gr.Blocks() as demo:
    gr.Markdown("# Multi-Agent Document Processing Demo (OCR → Classify → Extract → Validate)")

    inp = gr.File(label="Upload PDF/Image")
    ocr_text = gr.Textbox(label="OCR Text (preview)", lines=16)
    doc_type = gr.Textbox(label="Predicted Doc Type")
    extracted = gr.JSON(label="Extracted JSON")

    btn = gr.Button("Run Agents")
    btn.click(process, inputs=[inp], outputs=[ocr_text, doc_type, extracted])

demo.launch()