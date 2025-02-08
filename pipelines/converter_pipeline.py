from typing import Any, Dict

class Pipeline:
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def run(self, message: Any) -> Any:
        raise NotImplementedError

class GeminiConverterPipeline(Pipeline):
    """Pipeline for converting files (PDFs, images) to structured data using Gemini 2.0 Flash."""

    def __init__(self, config: Dict[str, Any]) -> None:
        super().__init__(config)

    def run(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Test pipeline that just returns a simple message."""
        message['content'] = "Pipeline test successful!"
        return message

# This is required for Open-WebUI to detect the pipeline
PIPELINE_CLASSES = {
    'GeminiConverterPipeline': GeminiConverterPipeline
}
