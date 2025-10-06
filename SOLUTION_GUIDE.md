# South Carolina Courts Scraper - Complete Solution Guide

## 🎯 Current Situation
- **Your Location**: Hyderabad, Telangana, India
- **Target Website**: Blocks non-US IP addresses
- **Solution Needed**: US-based connection required

## 🚀 Solutions (Ranked by Effectiveness)

### 1. **US VPN (Most Recommended)**
**Best Option**: Use a US-based VPN service

**Popular VPN Services:**
- **ExpressVPN** - Fast, reliable, many US servers
- **NordVPN** - Good performance, US servers available
- **Surfshark** - Budget-friendly, US servers
- **CyberGhost** - User-friendly, US servers

**Steps:**
1. Install VPN software
2. Connect to a US server (preferably East Coast)
3. Verify connection: `python check_us_connection.py`
4. Run scraper: `python sc_courts_scraper.py`

### 2. **Cloud Server in US**
**Alternative**: Use a US-based cloud server

**Providers:**
- **AWS EC2** (US East/West regions)
- **Google Cloud** (US regions)
- **DigitalOcean** (US datacenters)
- **Linode** (US locations)

**Steps:**
1. Create US-based cloud server
2. Install Python and dependencies
3. Upload scraper code
4. Run from US server

### 3. **Paid Proxy Services**
**For Advanced Users**: Use professional proxy services

**Services:**
- **Bright Data** (formerly Luminati)
- **Smartproxy**
- **ProxyMesh**
- **Oxylabs**

## 📁 Files Created

### Core Scraper Files
- `sc_courts_scraper.py` - Main scraper with proxy support
- `requirements.txt` - Python dependencies
- `README.md` - Basic documentation

### Utility Scripts
- `check_us_connection.py` - Check if you're US-based
- `test_proxy.py` - Test individual proxies
- `add_proxy.py` - Add proxies manually
- `fetch_geonode_proxies.py` - Fetch from GeoNode API
- `comprehensive_proxy_finder.py` - Multi-source proxy finder

### Helper Files
- `run_scraper.bat` - Windows batch file
- `example_usage.py` - Usage examples

## 🔧 Quick Start (With VPN)

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Connect to US VPN:**
   - Choose a US server (East Coast recommended)
   - Verify connection: `python check_us_connection.py`

3. **Run the Scraper:**
   ```bash
   python sc_courts_scraper.py
   ```

## 🛠️ Advanced Usage

### With Manual Proxies
If you have US proxies:
```bash
# Test a proxy
python test_proxy.py 192.168.1.1:8080

# Add working proxy
python add_proxy.py 192.168.1.1:8080

# Run with proxies
python sc_courts_scraper.py --proxy
```

### With Cloud Server
1. Create US-based server
2. Install Python and dependencies
3. Upload all files
4. Run: `python sc_courts_scraper.py`

## 📊 Expected Results

When successful, you'll see:
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

## ⚠️ Troubleshooting

### Still Getting 403 Errors?
1. **Check VPN**: Ensure you're connected to US
2. **Try Different US Server**: Some servers might be blocked
3. **Clear Browser Data**: Sometimes helps with session issues
4. **Use Different User Agent**: The scraper tries multiple automatically

### No Working Proxies Found?
- Free proxies have high failure rates
- Consider paid proxy services
- VPN is more reliable for this use case

## 🔒 Legal and Ethical Considerations

- **Respect Rate Limits**: Don't overload the server
- **Follow Terms of Service**: Check website's ToS
- **Use Responsibly**: Don't abuse the system
- **Data Privacy**: Handle any scraped data appropriately

## 📞 Support

If you need help:
1. Check the troubleshooting section
2. Verify your US connection
3. Try different VPN servers
4. Consider paid proxy services

## 🎉 Success Indicators

You'll know it's working when:
- No 403 Forbidden errors
- HTML content is returned
- Forms and inputs are detected
- Response files are created

Good luck with your scraping project! 🚀
