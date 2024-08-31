import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import argparse

def find_js_urls(base_url, verbose=False):
    """
    Finds JavaScript URLs within a given base URL.

    Args:
        base_url (str): The base URL to scan.
        verbose (bool): If True, print additional details.

    Returns:
        list: A list of JavaScript URLs found.
    """

    js_urls = []

    try:
        if verbose:
            print(f"Fetching {base_url}...")

        response = requests.get(base_url)
        response.raise_for_status()  # Check for HTTP errors

        if verbose:
            print(f"Successfully fetched {base_url}. Parsing content...")

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all JavaScript URLs
        js_urls = [urljoin(base_url, script['src']) for script in soup.find_all('script', src=True)]

        if verbose:
            print(f"Found {len(js_urls)} JavaScript file(s) in {base_url}.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {base_url}: {e}")

    return js_urls

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find JavaScript files in given subdomains.")
    parser.add_argument("-f", "--file", required=True, help="Input file containing subdomains")
    parser.add_argument("-o", "--output", required=True, help="Output file to save JavaScript URLs")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    js_urls_found = []

    with open(args.file, 'r') as f:
        subdomains = [line.strip() for line in f]

    for subdomain in subdomains:
        base_url = f"https://{subdomain}"  # Assuming HTTPS
        if args.verbose:
            print(f"Scanning {base_url}...")

        js_urls = find_js_urls(base_url, verbose=args.verbose)
        if js_urls:
            print("JavaScript files found:")
            for js_url in js_urls:
                print(js_url)
                js_urls_found.append(js_url)  # Add to the list of found URLs
        else:
            print("No JavaScript files found.")

    # Save the found JavaScript URLs to the output file
    with open(args.output, 'w') as output_file:
        for js_url in js_urls_found:
            output_file.write(js_url + "\n")

    print(f"JavaScript URLs have been saved to {args.output}")
