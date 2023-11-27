import os
import google.generativeai as palm
from langchain import LLMChain
from langchain.llms import GooglePalm
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredPDFLoader

# Setup the env for the Model
def setup_env(api_key):
    os.environ['GOOGLE_API_KEY'] = api_key
    llm = GooglePalm(temperature=0)

    return llm

# Defile the output format and template for Prompt
def define_format_template():
    # One-Shot Prompting
    output_format = """The output should be a markdown code snippet formatted in the following schema, including the leading and trailing "```json" and "```":
    Do not add trailing "\" anywhere to the output

    ```json
    {{ \"Question\": string // A question.
       \"Options\": string // Possible 4 multiple choices for the question in a list.
       \"Answer\": string // Correct answer for the question.
    }}
    ```
    Use the below example delimited by &&&& as a reference
    Example:
    &&&&
    ```json {{
    {{\"Question\": \"What is the capital of India?\",
      \"Options": ["New Delhi", "Mumbai", "Kolkata", "Chennai"),
      \"Answer\": \"New Delhi\"
    }},
    {{\"Question\": \"What is the capital of USA?\",
      \"Options": ["New York", "Washington DC", "Chicago", "Los Angeles"],
      \"Answer\": \"Washington DC\"
    }} }} ````
    &&&&
    """

    template = """Generate exactly {mcq_no} Multiple Choices Single Correct Questions from the given document
    {output_format}

    Use the following document information to work upon
    {docs}
    """

    return output_format, template

# Create Chunks of the data extracted from the PDF file
def create_docs(file):
    # Load the PDF File first
    """
    The `UnstructuredPDFLoader` can load in one of two modes: “single” and “elements”.
    If we use “single” mode, the document will be returned as a single langchain Document object.
    If we use “elements” mode, the unstructured library will split the document into elements such as Title and NarrativeText

    It also allow users to pass in a strategy parameter that lets unstructured know how to partition the document.
    Currently supported strategies are "hi_res" (the default) and "fast"
    Hi res partitioning strategies are more accurate, but take longer to process.
    Fast strategies partition the document more quickly, but trade-off accuracy
    """
    loader = UnstructuredPDFLoader(file)
    pages = loader.load()

    # TextSplitter instance to use for splitting documents
    """
    The `RecursiveCharacterTextSplitter` divides the input text into smaller chunks in a hierarchical and iterative
    manner using a set of separators

    If the initial attempt at splitting the text doesnt produce chunks of the desired size or structure, the method
    recursively calls itself on the resulting chunks with a different separator or criterion until the desired chunk
    size or structure is achieved
    This means that while the chunks arent going to be exactly the same size, theyll still “aspire” to be of a similar size.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2048,
        chunk_overlap=20,
        is_separator_regex=False
    )

    docs = text_splitter.split_documents(pages)

    return docs

# Initialize the Prompt that will be passed in the LLMChain
def initialize_prompt(template):
    prompt = PromptTemplate(
        template = template,
        input_variables = ["output_format", "mcq_no", "docs"]
    )

    return prompt

# Initialize the LLMChain to which will generate the final response
def initialize_llm_chain(llm, prompt):
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    return llm_chain

# Define all the model parameters and modules
def model(api_key, file, num_questions):
    llm = setup_env(api_key)
    docs = create_docs(file)
    output_format, template = define_format_template()
    prompt = initialize_prompt(template)
    llm_chain = initialize_llm_chain(llm, prompt)
    response = llm_chain.run(output_format=output_format, mcq_no=num_questions, docs=docs)
    return response