import os
import re

import streamlit as st

from src.model import model

from dotenv import load_dotenv

def iterate_data(data_str):
    """
    Using regex to find the question, options, and answer
    Iterating over each question block, using a list of option labels
    Print the question in bold, Print the options in normal text, and Print the answer in bold green using HTML
    """
    question_blocks = re.findall(r"\{[^}]*\}", data_str)

    option_labels = ["A", "B", "C", "D"]

    for i, block in enumerate(question_blocks, start=1):
        question = re.search(r'"Question": "([^"]*)"', block).group(1)
        options = re.findall(
            r'"([^"]*)"',
            re.search(r'"Options": (\[[^\]]*\])', block).group(1)
        )
        answer = re.search(r'"Answer": "([^"]*)"', block).group(1)

        st.markdown(f"**Question {i}: {question}**")

        st.write("Options:")
        for j, option in enumerate(options):
            st.write(f"Option {option_labels[j]}: {option}")

        answer_index = options.index(answer)
        st.markdown(
            f'<p style="color:green;font-weight:bold">Answer: Option {option_labels[answer_index]} ({answer})</p>',
            unsafe_allow_html=True,
        )
        st.write("---")

def main():
    st.header('PDF2MCQ Generator')

    # Load the default API key from .env
    load_dotenv()
    api_key = os.getenv('GOOGLE_API_KEY')

    # Ask for API key if not found
    if api_key is None:
        api_key = st.text_input('Enter your google API Key', type="password")

    file = st.file_uploader('Upload your PDF', type='pdf')

    if file is not None:
        # Save the uploaded file temporarily
        # Reason: UnstructuredPDFLoader initializes with file path only
        temp_file = "temp_file.pdf"
        with open(temp_file, "wb") as out_file:
            out_file.write(file.getbuffer())

        num_questions = st.number_input('Enter the number of questions you would like to generate', min_value=1, value=10, step=1)

        if st.button('Submit'):
            # Call the model
            response = model(api_key, temp_file, num_questions)
            iterate_data(response)

        # Remove the temporary file
        os.remove(temp_file)

if __name__ == "__main__":
    main()

def test_regex():
    data_str = """
    {
        "Question": "What is the capital of France?",
        "Options": ["Paris", "London", "Rome", "Berlin"],
        "Answer": "Paris"
    }
    """

    question_blocks = re.findall(r"\{[^}]*\}", data_str)

    assert len(question_blocks) == 1

    question = re.search(r'"Question": "([^"]*)"', question_blocks[0]).group(1)
    assert question == "What is the capital of France?"

    options = re.findall(
        r'"([^"]*)"',
        re.search(r'"Options": (\[[^\]]*\])', question_blocks[0]).group(1)
    )
    assert options == ["Paris", "London", "Rome", "Berlin"]

    answer = re.search(r'"Answer": "([^"]*)"', question_blocks[0]).group(1)
    assert answer == "Paris"