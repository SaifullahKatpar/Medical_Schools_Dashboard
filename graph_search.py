import requests
from bs4 import BeautifulSoup
import networkx as nx

def parse_html(url):
    # Make a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Create an empty directed graph
    G = nx.DiGraph()

    # Iterate through all the HTML tags in the parsed content
    for tag in soup.find_all():

        # Get the name of the tag
        tag_name = tag.name

        # Add a node for the tag if it doesn't already exist
        if not G.has_node(tag_name):
            G.add_node(tag_name)

        # Iterate through all the attributes of the tag
        for attr in tag.attrs:

            # Add an edge between the tag and its attribute
            G.add_edge(tag_name, f"{attr}={tag.attrs[attr]}")

        # If the tag has any text, add an edge between the tag and its text
        if tag.string:
            G.add_edge(tag_name, tag.string.strip())

    return G

def search_data(G, query):
    # Search for the query in the graph
    result = []
    for node in G.nodes:
        if query in str(node):            
            result.append(node)
    return result

# Example usage
# url = 'https://en.wikipedia.org/wiki/Python_(programming_language)'
url = "https://www.hofstra.edu/admission/apply.html"
G = parse_html(url)
result = search_data(G, 'Submission')
print(result)
