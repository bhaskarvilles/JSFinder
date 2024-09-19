import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import argparse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def find_js_urls(base_url, session):
    """
    Finds JavaScript URLs within a given base URL.

    Args:
        base_url (str): The base URL to scan.
        session (requests.Session): The session to use for requests.

    Returns:
        list: A list of JavaScript URLs found.
    """
    js_urls = []

    try:
        response = session.get(base_url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        js_urls = [urljoin(base_url, script['src']) for script in soup.find_all('script', src=True)]

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {base_url}: {e}")

    return js_urls

def configure_session():
    """
    Configures a requests session with retries and backoff strategy.

    Returns:
        requests.Session: Configured session object.
    """
    session = requests.Session()
    
    # Retry with exponential backoff
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('https://', adapter)
    session.mount('http://', adapter)

    # Custom headers (e.g., User-Agent)
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })

    return session

def scan_subdomain(subdomain, session, verbose):
    base_url = f"https://{subdomain}"  # Assuming HTTPS
    if verbose:
        print(f"Scanning {base_url}...")
    js_urls = find_js_urls(base_url, session)
    return base_url, js_urls

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find JavaScript files in given subdomains.")
    parser.add_argument("-f", "--file", required=True, help="Input file containing subdomains")
    parser.add_argument("-o", "--output", required=True, help="Output file to save JavaScript URLs")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--no-verify", action='store_true', help="Disable SSL certificate verification")

    args = parser.parse_args()

    with open(args.file, 'r') as f:
        subdomains = [line.strip() for line in f]

    session = configure_session()

    # Disable SSL verification if specified
    if args.no_verify:
        session.verify = False

    js_urls_found = []

    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_subdomain = {executor.submit(scan_subdomain, subdomain, session, args.verbose): subdomain for subdomain in subdomains}
        
        for future in as_completed(future_to_subdomain):
            subdomain = future_to_subdomain[future]
            try:
                base_url, js_urls = future.result()
                if js_urls:
                    js_urls_found.extend(js_urls)
                    if args.verbose:
                        print(f"JavaScript files found at {base_url}:")
                        for js_url in js_urls:
                            print(f" - {js_url}")
            except Exception as e:
                print(f"Error processing {subdomain}: {e}")

    with open(args.output, 'w') as output_file:
        for js_url in js_urls_found:
            output_file.write(js_url + "\n")

    if args.verbose:
        print(f"JavaScript URLs have been saved to {args.output}")
