import logging
import os
import arxiv
import requests
from tempfile import NamedTemporaryFile
from PyPDF2 import PdfReader
from mcp.server.fastmcp import FastMCP
from openai import OpenAI
from anthropic import Anthropic
from google.generativeai import GenerativeModel
from dotenv import load_dotenv

# Set up logging to a common file
logging.basicConfig(filename='mcp_log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

load_dotenv()

# Initialize the FastMCP app
mcp = FastMCP(name="ArxivSummarizerServer")

@mcp.tool()
def summarize_pdf(pdf_url: str) -> dict:
    """
    Downloads a PDF, extracts its text, and summarizes it using an LLM.

    Args:
        pdf_url: URL of the PDF

    Returns:
        Dictionary with a summary string
    """
    logging.info(f"Received PDF URL for summarization: {pdf_url} , Now using now using ArxivSummarizerServer")
    # Download the PDF
    if "arxiv.org/abs/" in pdf_url:
        pdf_url = pdf_url.replace("arxiv.org/abs/", "arxiv.org/pdf/") + ".pdf"

    response = requests.get(pdf_url)
    response.raise_for_status()

    if "application/pdf" not in response.headers.get("Content-Type", ""):
        raise ValueError("Provided URL did not return a valid PDF.")

    # Save to temp file
    with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(response.content)
        tmp_path = tmp_file.name

    # Extract text
    reader = PdfReader(tmp_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""

    # Clean up
    os.unlink(tmp_path)

    # Get LLM provider from environment variable
    provider = os.getenv("LLM_PROVIDER", "openai").lower()

    if provider == "openai":
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        completion = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            messages=[
                {"role": "system", "content": "Summarize this academic paper:"},
                {"role": "user", "content": text[:10000]}
            ]
        )
        summary = completion.choices[0].message.content.strip()

    elif provider == "anthropic":
        client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        summary = client.messages.create(
            model=os.getenv("ANTHROPIC_MODEL", "claude-3-haiku-20240307"),
            max_tokens=512,
            messages=[
                {"role": "user", "content": f"Summarize this paper:\n{text[:10000]}"}
            ]
        ).content[0].text.strip()

    elif provider == "google":
        model = GenerativeModel(model_name=os.getenv("GOOGLE_MODEL", "gemini-pro"))
        summary = model.generate_content(f"Summarize this academic paper:\n\n{text[:10000]}").text

    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")

    logging.info(f"Returning summary: {summary}")
    return {"summary": summary}

# Start the FastMCP server
if __name__ == "__main__":
    logging.info("Starting ArxivSummarizerServer.")
    mcp.serve()
