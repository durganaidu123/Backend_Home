import requests
import xmltodict
import pandas as pd
import re
from typing import List, Dict, Optional


PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_SUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


def search_pubmed(query: str, max_results: int = 10) -> List[str]:
    """Fetch PubMed IDs based on a query."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json"
    }
    response = requests.get(PUBMED_API_URL, params=params)
    response.raise_for_status()
    data = response.json()
    print(data)
    print("------search_pubmed--------")
    print(data["esearchresult"]["idlist"])
    return data["esearchresult"]["idlist"]


def fetch_paper_details(pubmed_id: str) -> Optional[Dict]:
    """Retrieve paper details from PubMed."""
    params = {
        "db": "pubmed",
        "id": pubmed_id,
        "retmode": "xml"
    }
    response = requests.get(PUBMED_FETCH_URL, params=params)
    response.raise_for_status()
    
    data = xmltodict.parse(response.content)
    article = data.get("PubmedArticleSet", {}).get("PubmedArticle", {})
    
    if not article:
        return None

    medline = article.get("MedlineCitation", {})
    article_details = medline.get("Article", {})
    authors = article_details.get("AuthorList", {}).get("Author", [])

    title = article_details.get("ArticleTitle", "N/A")
    pub_date = article_details.get("Journal", {}).get("JournalIssue", {}).get("PubDate", {}).get("Year", "N/A")
    
    # Extract authors with non-academic affiliations
    non_academic_authors, company_affiliations = [], []
    for author in authors:
        if isinstance(author, dict) and "AffiliationInfo" in author:
            print(author["AffiliationInfo"])
            if isinstance(author["AffiliationInfo"], list) and len(author["AffiliationInfo"]) > 0:
                affiliation = author["AffiliationInfo"][0].get("Affiliation", "")
            else:
                affiliation = ""

            if affiliation and is_non_academic(affiliation):
                non_academic_authors.append(author.get("LastName", "Unknown"))
                company_affiliations.append(affiliation)


    # Extract corresponding author email
    corresponding_author_email = extract_email(article_details)
    print("------extracted the details--------")

    return {
        "PubmedID": pubmed_id,
        "Title": title,
        "Publication Date": pub_date,
        "Non-academic Author(s)": ", ".join(non_academic_authors),
        "Company Affiliation(s)": ", ".join(company_affiliations),
        "Corresponding Author Email": corresponding_author_email
    }


def is_non_academic(affiliation: str) -> bool:
    """Check if an affiliation is non-academic."""
    academic_keywords = ["university", "college", "institute", "lab", "department", "research center"]
    print("is noot academic")
    return not any(word in affiliation.lower() for word in academic_keywords)


def extract_email(article_details: Dict) -> str:
    """Extract email of the corresponding author if available."""
    abstract_texts = article_details.get("Abstract", {}).get("AbstractText", [])

    if isinstance(abstract_texts, list):
        for text in abstract_texts:
            if isinstance(text, dict):  # Convert dict to string if necessary
                text = str(text)
            emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
            if emails:
                print(emails)
                return emails[0]
    
    return "N/A"



def save_to_csv(papers: List[Dict], filename: str):
    """Save results to a CSV file."""
    df = pd.DataFrame(papers)
    df.to_csv(filename, index=False)
    print("File Created")
