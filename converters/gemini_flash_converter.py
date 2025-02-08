import os
from google import genai

# Set up the Gemini 2.0 Flash client
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise EnvironmentError("Please set the GEMINI_API_KEY environment variable")

client = genai.Client(api_key=api_key)
model_id = "gemini-2.0-flash"


def auto_extract_structured_data(file_path: str) -> dict:
    """
    Automatically extract structured data from a given file (PDF or image) using Gemini 2.0 Flash.
    
    This function uploads the file using the Gemini File API and sends a prompt instructing the model to
    decide the most appropriate data structure based solely on the content. The response is expected to be
    in JSON format.

    Args:
        file_path (str): The local path to the file (PDF or image).

    Returns:
        dict: The structured data extracted from the document.
    """
    # Derive a display name from the file name
    display_name = os.path.basename(file_path).split('.')[0]

    # Upload the file using the File API
    uploaded_file = client.files.upload(file=file_path, config={'display_name': display_name})

    # Construct a generic prompt that instructs the model to determine the best structure
    prompt = (
        "Extract all relevant structured information from the attached document. "
        "Decide on the most suitable data structure based solely on the content. "
        "Return the output in JSON format."
    )

    # Call the Gemini API with the prompt and the uploaded file
    response = client.models.generate_content(
        model=model_id,
        contents=[prompt, uploaded_file],
        config={'response_mime_type': 'application/json'}
    )

    # Attempt to parse the response into a dictionary; if parsing fails, return the raw response
    try:
        result = response.parsed
    except Exception as e:
        result = {"raw_response": response.text, "error": str(e)}

    return result
