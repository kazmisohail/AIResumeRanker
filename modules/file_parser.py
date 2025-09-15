import docx # for handling .docx files
import io

def extract_text_from_docx(file_stream):
    """
    Extracts text from a .docx file stream.
    Args:
        file_stream: A file-like object (bytes stream) from the uploaded file.
    Returns:
        A string containing the text from the document.
    """
    try:
        # The file_stream from Flask is a byte stream, so we use io.BytesIO
        document = docx.Document(io.BytesIO(file_stream.read()))
        return "\n".join([paragraph.text for paragraph in document.paragraphs])
    except Exception as e:
        print(f"Error processing docx file: {e}")
        return ""