# pip install scholarly


from scholarly import scholarly

# Search for a keyword or author
query = scholarly.search_pubs("Deep Learning in Medical Imaging")


def generate_url_google_scholar(query: str, number_of_results: int = 5):
    """
    Generate some Google Scholar URL for the given query.
    """
    url_lists = []

    # Fetch and display results
    for i in range(number_of_results):  # Retrieve top 5 results
        try:
            paper = next(query)
            print(f"Title: {paper['bib']['title']}")
            print(f"Authors: {paper['bib']['author']}")
            print(f"Year: {paper['bib'].get('year', 'Unknown')}")
            print(f"Abstract: {paper['bib'].get('abstract', 'No abstract available')}")
            print(f"Link: {paper.get('pub_url', 'No link available')}\n")
            url_lists.append(paper.get('pub_url', 'No link available'))
        except StopIteration:
            break
    return url_lists

def download_pdfs(urls: list):
    """
    Download the PDFs from the given URLs.
    """
    for url in urls:
        # Here you would implement the logic to download the PDF
        # For example, using requests or any other library
        print(f"Downloading PDF from {url}...")
        response = requests.get(url)
        with open(f"{url.split('/')[-1]}.pdf", 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {url.split('/')[-1]}.pdf")
    
