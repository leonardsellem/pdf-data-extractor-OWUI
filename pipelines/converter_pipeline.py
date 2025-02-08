from typing import Any, Dict

def run(message: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """Test pipeline that just returns a simple message."""
    message['content'] = "Pipeline test successful!"
    return message

# This is required for Open-WebUI to detect the pipeline
PIPELINE = {
    'name': 'GeminiConverterPipeline',
    'description': 'Pipeline for converting files (PDFs, images) to structured data using Gemini 2.0 Flash.',
    'run': run
}
