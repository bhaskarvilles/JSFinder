import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import argparse
import concurrent.futures
import logging
from tqdm import tqdm
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import certifi

# Setup logging to file for error handling
logging.basicConfig(filename='errors.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Function to create a session with retry logic
def create_session():
    session = requests.Session()
    retry = Retry(connect=5, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)
    session.mount('http://', adapter)
    return session

# Function to find JavaScript URLs
def find_js_urls(base_url, timeout, verify_ssl):
    """
    Finds JavaScript URLs within a given base URL.

    Args:
        base_url (str): The base URL to scan.
        timeout (int): Timeout duration for requests.
        verify_ssl (bool): Whether to verify SSL certificates.

    Returns:
        list: A list of JavaScript URLs found.
    """
    js_urls = []
    session = create_session()

    # Try both HTTPS and HTTP
    for scheme in ['https://', 'http://']:
        try:
            url = scheme + base_url
            response = session.get(url, timeout=timeout, verify=verify_ssl)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            js_urls.extend([urljoin(url, script['src']) for script in soup.find_all('script', src=True)])
            break  # If successful, break the loop
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching {url}: {e}")

    return js_urls

# Function to scan subdomains concurrently
def scan_subdomains(subdomains, timeout, verify_ssl):
    js_urls_found = []

    # Using ThreadPoolExecutor for concurrent execution
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(tqdm(executor.map(lambda subdomain: find_js_urls(subdomain, timeout, verify_ssl), subdomains), total=len(subdomains), desc="Scanning subdomains", unit="subdomain"))

    # Combine results from each subdomain
    for result in results:
        js_urls_found.extend(result)

    return js_urls_found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan subdomains for JavaScript files.")
    parser.add_argument("-f", "--file", required=True, help="Input file containing subdomains, one per line")
    parser.add_argument("-o", "--output", required=True, help="Output file to save JavaScript URLs found")
    parser.add_argument("--timeout", type=int, default=10, help="Request timeout duration in seconds (default: 10s)")
    parser.add_argument("--no-verify", action='store_true', help="Disable SSL certificate verification")

    args = parser.parse_args()

    # Read subdomains from input file
    with open(args.file, 'r') as f:
        subdomains = [line.strip() for line in f]

    # Scan subdomains and find JavaScript URLs
    js_urls_found = scan_subdomains(subdomains, args.timeout, not args.no_verify)

    # Save JavaScript URLs to output file
    with open(args.output, 'w') as output_file:
        for js_url in js_urls_found:
            output_file.write(js_url + "\n")

    print(f"\nJavaScript URLs have been saved to {args.output}\n")
    print("Completed. Check 'errors.log' for any errors encountered during the scan.")
