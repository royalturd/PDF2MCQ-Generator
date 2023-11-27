# PDF2MCQ Generator

PDF2MCQ Generator is an app written in Python that generates  multiple-choice questions (MCQs) based on PDF document knowledge.
It uses Google PaLM language model

## Prerequisites

- Python latest version installed.
- An active internet connection for accessing the Google Palm language model.
- PDF documents that you want to convert to MCQs.
- Google API key to use the Google Palm language model. If you don't have one, you can obtain it [here](https://makersuite.google.com).

## Getting Started

1. Clone the repository and enter into project folder
2. Create a virtual environment
```
python -m venv .venv
```

3. Activate the virtual environment (varies by platform)
- On Windows:
```
.venv\Scripts\activate
```
- On macOS and Linux:
```
source .venv/bin/activate
```

4. Install project dependencies
```
pip install -r requirements.txt
```

5. Run the application:
```
streamlit run app.py
```

## Note

If you plan to deploy the application, add your API key to the `.env` file. If the key is not found, the application will prompt you to enter it.

**Note for Linux users:**
If you face the following errors:
```
FileNotFoundError: [Errno 2] No such file or directory: 'pdfinfo'
FileNotFoundError: [Errno 2] No such file or directory: 'tesseract'
```

you need to install the following dependencies:
```
sudo apt-get install poppler-utils tesseract-ocr
```

## Usage

1. The application will launch in your web browser.
2. Upload a PDF document that you want to convert to MCQs.
3. Specify the number of questions you would like to generate.
4. Click the "Submit" button to start the generation process.
5. The generated MCQs will be displayed in the web interface.

## Acknowledgments
Thanks to the creators of Streamlit, Google Palm, and the various Python libraries used in this project for their contributions to open-source software.