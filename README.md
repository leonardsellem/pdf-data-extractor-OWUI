# PDF Data Extractor for Open-WebUI

This project implements a pipeline for Open-WebUI that handles PDF and image file uploads and extracts structured data using Gemini 2.0 Flash. The pipeline leverages the Google GenAI Python SDK and integrates directly with Open-WebUI pipelines.

## Project Structure

```
pdf-data-extractor-OWUI/
├── converters/
│   └── gemini_flash_converter.py    # Contains function 'auto_extract_structured_data' that uses Gemini 2.0 Flash.
├── pipelines/
│   └── converter_pipeline.py        # Open-WebUI pipeline integration.
├── requirements.txt                 # Project dependencies.
└── README.md                        # Project instructions and documentation.
```

## Setup

1. **Gemini API Key**

   Set the environment variable `GEMINI_API_KEY` with your Gemini API key:
   ```bash
   export GEMINI_API_KEY=your_api_key_here
   ```

2. **Install Dependencies**

   Run the following command to install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Pipeline Integration with Open-WebUI

Follow the [Open-WebUI Pipelines documentation](https://docs.openwebui.com/pipelines/) for details on integrating a pipeline into your instance.

1. Place the pipeline file `pipelines/converter_pipeline.py` in your project according to your Open-WebUI instance directory structure.

2. Configure Open-WebUI to load the pipeline. An example configuration snippet might look like:
   ```json
   {
       "pipelines": [
           {
               "name": "Gemini Converter Pipeline",
               "module": "pipelines.converter_pipeline",
               "class": "GeminiConverterPipeline",
               "config": {}
           }
       ]
   }
   ```

3. After integration, when a file is uploaded through Open-WebUI, the pipeline will:
   - Verify file type (supports PDFs, JPEG, PNG, GIF).
   - Upload the file via Gemini’s File API.
   - Use Gemini 2.0 Flash to extract structured data automatically.
   - Return the structured output as JSON in the message content and metadata.

## Usage

- Upload a PDF or supported image through your Open-WebUI interface.
- The pipeline will process the file and output the structured data.
- Check the message content or metadata for the extracted JSON output.

## Customization

This project is designed to let Gemini 2.0 Flash decide on the structure automatically, eliminating the need to predefine templates for each file type.

If you need more control over the structure, consider modifying the pipeline or converter to utilize custom schemas.

## License

MIT License

## Acknowledgements

Based on the methodology from [From PDFs to Insights: Structured Outputs from PDFs with Gemini 2.0](https://www.philschmid.de/gemini-pdf-to-data).
