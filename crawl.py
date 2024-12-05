import requests
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch

def extract(url: str, filename: str):
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to fetch page")
        return

    print("Parsing..")
    soup = BeautifulSoup(response.content, "html.parser")
    content = soup.get_text(separator="\n").strip()


    print("Saving..")
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)

    print("Content extracted!")

def indexing(es: Elasticsearch, filename: str):
    with open(filename, "r", encoding="utf-8") as file:
        content = file.readlines()
        
    for i, line in enumerate(content):
        doc = {
            "line": i+1,
            "content": line.strip()
        }
        es.index(index="wiki-scratch", id=i+1, document=doc)
        
    print("Indexing completed!")
    
def main():
    url = "https://en.wikipedia.org/wiki/Killing_of_JonBen%C3%A9t_Ramsey"
    filename = "wiki.txt"
    es = Elasticsearch("http://localhost:9200")
    
    extract(url, filename)
    indexing(es, filename)
    
if __name__ == "__main__":
    main()
