#pip install arxiv
import os
import arxiv

# Directory to save PDFs
SAVE_DIR = "arxiv_papers"
os.makedirs(SAVE_DIR, exist_ok=True)

def download_arxiv(query: str, number_of_results: int = 5):
    """
    Generate some ArXiv URLs for the given query.
    """

    # Function to download and save PDF
    def download_pdf(url, title):
        pdf_path = os.path.join(SAVE_DIR, f"{title}.pdf")
        try:
            response = requests.get(url, stream=True, timeout=10)
            if response.status_code == 200:
                with open(pdf_path, "wb") as pdf_file:
                    for chunk in response.iter_content(1024):
                        pdf_file.write(chunk)
                print(f"Downloaded: {pdf_path}")
            else:
                print(f"Failed to download: {url}")
        except Exception as e:
            print(f"Error downloading {url}: {e}")

    # Search ArXiv for papers
    search_query = "deep learning medical imaging"  # Change this to any topic
    search = arxiv.Search(
        query=search_query,
        max_results=5,  # Number of papers to fetch
        sort_by=arxiv.SortCriterion.SubmittedDate  # Get latest papers
    )

    # Fetch results and download PDFs
    for result in search.results():
        print(f"Title: {result.title}")
        print(f"Authors: {', '.join([author.name for author in result.authors])}")
        print(f"Published: {result.published}")
        print(f"PDF URL: {result.pdf_url}\n")

        # Download the PDF
        title_cleaned = result.title.replace("/", "-")  # Clean title for filename
        download_pdf(result.pdf_url, title_cleaned)
    
