import logging
import arxiv
from mcp.server.fastmcp import FastMCP

# Set up logging to a common file
logging.basicConfig(filename='mcp_log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Initialize the FastMCP app
mcp = FastMCP(name="ArxivSearchServer")

# Tool function
@mcp.tool()
def arxiv_search(search_query: str, max_result: int) -> list[dict]:
    """
    Search arXiv for recent papers.

    Args:
        search_query: query string for arXiv search
        max_result: maximum number of results

    Returns:
        List of dictionaries with title, URL and Published Date of each paper.
    """
    logging.info(f"Received search query : {search_query}  , Now using now using ArxivSearchServer ")
    client = arxiv.Client()
    search = arxiv.Search(
        query=search_query,
        max_results=max_result,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    results = client.results(search)
    papers = []
    for r in results:
        dt_aware = r.published
        dt_naive = dt_aware.replace(tzinfo=None)
        papers.append({
            "title": r.title,
            "url": r.entry_id,
            "Published": dt_naive
        })
    logging.info(f"Returning search results: {papers}")
    return papers

# Start the FastMCP server
if __name__ == "__main__":
    logging.info("Starting ArxivSearchServer.")
    mcp.serve()
