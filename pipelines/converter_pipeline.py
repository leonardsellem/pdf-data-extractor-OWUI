from typing import Any, Dict

def run(message, config):
    """Simple test pipeline."""
    return {
        "content": "Pipeline test successful!",
        "files": message.get("files", []),
        "images": message.get("images", []),
        "error": None
    }

# Pipeline configuration
pipeline = {
    "name": "GeminiConverterPipeline",
    "description": "Pipeline for converting files to structured data using Gemini 2.0 Flash",
    "pipeline_id": "gemini_converter",
    "show_in_list": True,
    "run": run
}
