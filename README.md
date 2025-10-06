# South Carolina Courts Scraper

A Python scraper for accessing court roster information from `publicindex.sccourts.org`.

## ⚠️ Important Notice

This website has strong anti-bot protection and **blocks non-US IP addresses**. You will need to use a US-based proxy or VPN to access the site successfully.

## Features

- Automatic proxy detection and rotation
- Multiple user agent support
- Session management with cookies
- Response parsing and analysis
- Error handling and retry logic
- Detailed logging

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage
```bash
python sc_courts_scraper.py
```

### With Proxy Support
```bash
python sc_courts_scraper.py --proxy
```

### Manual Proxy Configuration

If you have US-based proxies, create a `us_proxies.txt` file with one proxy per line:
```
proxy1.example.com:8080
proxy2.example.com:3128
proxy3.example.com:8080
```

## Files Created

- `sc_courts_scraper.py` - Main scraper script
- `proxy_finder.py` - Utility to find working US proxies
- `requirements.txt` - Python dependencies
- `response.html` - Saved response content
- `us_proxies.txt` - Working US proxies (if found)

## Troubleshooting

### Getting 403 Forbidden Errors

The website uses Imperva/Incapsula protection that blocks:
- Non-US IP addresses
- Automated requests
- Certain user agents

**Solutions:**
1. Use a US-based VPN
2. Use US-based proxies
3. Try different user agents
4. Add delays between requests

### Proxy Issues

If proxies aren't working:
1. Check if proxies are actually US-based
2. Verify proxy connectivity
3. Try different proxy sources
4. Consider paid proxy services

## Code Structure

### SCCourtsScraper Class

Main scraper class with methods:
- `make_initial_request()` - Main request logic
- `parse_response()` - HTML parsing and analysis
- `try_alternative_approach()` - Fallback methods
- `make_request_with_proxy()` - Proxy-enabled requests

### Proxy Support

The scraper supports:
- Automatic proxy discovery
- Proxy rotation
- US IP verification
- Proxy testing

## Example Output

```
SCRAPING SUMMARY
==================================================
Page Title: Court Roster Selection
Forms Found: 2
Input Fields: 15
Select Dropdowns: 3
Links: 25
Scripts: 8
Has ViewState: True
Has EventValidation: True
```

## Legal Notice

Please ensure you comply with:
- Website terms of service
- Local laws and regulations
- Rate limiting and respectful scraping
- Data privacy requirements

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is for educational purposes. Use responsibly and in compliance with applicable laws.
