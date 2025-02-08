import os
import mimetypes
from typing import Any, Dict

from openwebui.core.pipeline import Pipeline
from openwebui.core.message import Message

from converters.gemini_flash_converter import auto_extract_structured_data


class GeminiConverterPipeline(Pipeline):
    """Pipeline for converting files (PDFs, images) to structured data using Gemini 2.0 Flash."""

    def __init__(self, config: Dict[str, Any]) -> None:
        super().__init__(config)

    def run(self, message: Message) -> Message:
        """Runs the pipeline to convert the file to structured data.

        Args:
            message (Message): The message object containing the file path.

        Returns:
            Message: The message object with the structured data added to the content.
        """
        file_path = message.files[0] if message.files else None

        if not file_path:
            message.content = "Error: No file attached."
            return message

        # Determine the file type
        mime_type, _ = mimetypes.guess_type(file_path)

        if mime_type not in ["application/pdf", "image/jpeg", "image/png", "image/gif"]:
            message.content = f"Error: Unsupported file type: {mime_type}"
            return message

        try:
            structured_data = auto_extract_structured_data(file_path)
            message.content = str(structured_data)  # Convert dict to string for message content
            message.metadata["structured_data"] = structured_data  # Store structured data in metadata
        except Exception as e:
            message.content = f"Error processing file: {str(e)}"

        return message


# Example usage (for testing purposes)
if __name__ == "__main__":
    # Create a dummy message object
    class DummyMessage:
        def __init__(self, files):
            self.files = files
            self.content = ""
            self.metadata = {}

    # Replace with the actual path to your test file
    test_file_path = "./test_invoice.pdf"  # Example: a local PDF file

    # Create a dummy config
    dummy_config = {}

    # Instantiate the pipeline
    pipeline = GeminiConverterPipeline(dummy_config)

    # Create a dummy message with the file path
    message = DummyMessage([test_file_path])

    # Run the pipeline
    message = pipeline.run(message)

    # Print the result
    print(f"Pipeline Result: {message.content}")
    print(f"Metadata: {message.metadata}")
