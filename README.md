# DocumentLoader

`DocumentLoader` is a Python class designed to load and process `.docx` documents. It extracts text from paragraphs, tables, and other elements, handling MathML content and converting it to plain text. This class is particularly useful for preparing documents for further processing, such as text splitting and retrieval-augmented generation (RAG) chatbots.

## Features

- Extracts text from paragraphs, tables, and other elements in `.docx` documents.
- Handles MathML content and converts it to plain text.
- Generates a list of text elements with optional tagging.
- Integrates with `langchain_core.documents` for further processing.

## Installation

To use `DocumentLoader`, you need to have the following dependencies installed:

```bash
pip install python-docx lxml docxlatex langchain-core
pip install python-docx lxml docxlatex langchain-core
```
## Usage

### Example

Here’s an example of how to use `DocumentLoader` to load a document and split its content:

```python
from doc_loader import DocumentLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Initialize the DocumentLoader with the path to your .docx file
doc_path = 'path_to_your_document.docx'
loader = DocumentLoader(doc_path)

# Load the document and extract the text
docs = loader.load()

# Initialize the text splitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=400)

# Split the document into chunks
splits = text_splitter.split_documents(docs)

# Print the splits
for split in splits:
    print(split.page_content)
```
