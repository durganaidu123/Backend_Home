import click
import logging
from pubmed_fetcher.fetcher import search_pubmed, fetch_paper_details, save_to_csv
from typing import Optional


@click.command()
@click.argument("query")
@click.option("-d", "--debug", is_flag=True, help="Enable debug mode")
@click.option("-f", "--file", type=str, help="Specify output CSV filename")
def main(query: str, debug: bool, file: Optional[str]):
    """Fetch research papers from PubMed based on a user query."""
    
    if debug:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Debug mode enabled")
    
    logging.info(f"Fetching papers for query: {query}")
    
    pubmed_ids = search_pubmed(query)
    if not pubmed_ids:
        click.echo("No papers found.")
        return
    
    papers = []
    for pubmed_id in pubmed_ids:
        paper_details = fetch_paper_details(pubmed_id)
        if paper_details:
            papers.append(paper_details)

    if file:
        save_to_csv(papers, file)
        click.echo(f"Results saved to {file}")
    else:
        for paper in papers:
            click.echo(paper)


if __name__ == "__main__":
    main()
