import os
import mimetypes
from typing import Any, Dict
import os
from google import genai

from openwebui.core.pipeline import Pipeline
from openwebui.core.message import Message

class GeminiConverterPipeline(Pipeline):
    """Pipeline for converting files (PDFs, images) to structured data using Gemini 2.0 Flash."""

    def __init__(self, config: Dict[str, Any]) -> None:
        super().__init__(config)
        # Set up the Gemini 2.0 Flash client
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise EnvironmentError("Please set the GEMINI_API_KEY environment variable")
        
        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-2.0-flash"

    def auto_extract_structured_data(self, file_path: str) -> dict:
        """
        Automatically extract structured data from a given file (PDF or image) using Gemini 2.0 Flash.
        
        Args:
            file_path (str): The local path to the file (PDF or image).

        Returns:
            dict: The structured data extracted from the document.
        """
        # Derive a display name from the file name
        display_name = os.path.basename(file_path).split('.')[0]

        # Upload the file using the File API
        uploaded_file = self.client.files.upload(file=file_path, config={'display_name': display_name})

        # Construct a generic prompt that instructs the model to determine the best structure
        prompt = (
            "Extract all relevant structured information from the attached document. "
            "Decide on the most suitable data structure based solely on the content. "
            "Return the output in JSON format."
        )

        # Call the Gemini API with the prompt and the uploaded file
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=[prompt, uploaded_file],
            config={'response_mime_type': 'application/json'}
        )

        # Attempt to parse the response into a dictionary
        try:
            result = response.parsed
        except Exception as e:
            result = {"raw_response": response.text, "error": str(e)}

        return result

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
            structured_data = self.auto_extract_structured_data(file_path)
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
