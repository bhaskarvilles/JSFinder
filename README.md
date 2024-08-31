## Description

**JSFinder** is a Python script designed to automate the process of discovering JavaScript files in a list of subdomains. By leveraging web scraping techniques, JSFinder fetches the HTML content of each subdomain, parses it, and identifies all linked JavaScript files. The script supports saving the discovered URLs into an output file for further analysis. It also includes a verbose mode that provides detailed output during the scanning process, making it easier to troubleshoot and understand the flow of operations.

---

## README

# JSFinder

JSFinder is a Python-based tool for finding JavaScript files across a list of subdomains. This tool is particularly useful for security researchers, penetration testers, and developers who need to analyze JavaScript files for vulnerabilities, dependencies, or any other purposes.

## Features

- **Subdomain Scanning:** Scans a list of subdomains to find linked JavaScript files.
- **Output to File:** Saves discovered JavaScript URLs to a specified output file.
- **Verbose Mode:** Provides detailed output during the scanning process.
- **Error Handling:** Gracefully handles errors when a subdomain cannot be accessed.

## Requirements

- Python 3.x
- `requests` library
- `beautifulsoup4` library

You can install the necessary Python libraries using pip:

```bash
pip install requests beautifulsoup4
```

## Usage

### Command-Line Arguments

- **`-f`, `--file`**: Input file containing subdomains (required).
- **`-o`, `--output`**: Output file to save JavaScript URLs (required).
- **`-v`, `--verbose`**: Enable verbose output (optional).

### Example

```bash
python jsfinder.py -f subdomains.txt -o js_output.txt -v
```

This command will scan the subdomains listed in `subdomains.txt`, find all JavaScript files, save the URLs in `js_output.txt`, and provide verbose output during the process.

### Input File

The input file should contain one subdomain per line, for example:

```
example.com
test.example.com
sub.example.com
```

### Output File

The output file will contain the full URLs of all JavaScript files discovered:

```
https://example.com/js/app.js
https://example.com/js/vendor.js
https://test.example.com/assets/main.js
```

## Contributing

Contributions are welcome! If you have suggestions for improving JSFinder or have found a bug, feel free to create an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [Mozilla Public License](https://www.mozilla.org/en-US/MPL/2.0/) file for details.

## Acknowledgments

- The `requests` library for making HTTP requests easy.
- The `beautifulsoup4` library for HTML parsing.
- Inspired by the need to automate the discovery of JavaScript files in web security assessments.

---

## Additional Notes

- Ensure that you have permission to scan the subdomains listed in your input file. Unauthorized scanning may be illegal and against the terms of service of the websites you scan.
- JSFinder assumes the subdomains use HTTPS. If some subdomains use HTTP, you might need to modify the script or manually adjust your input file accordingly.
