# 🔗 Link Extractor

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
![Maintenance](https://img.shields.io/badge/maintained-yes-green.svg)

> **Effortlessly discover and explore all links on any webpage**

A powerful, beautiful, and versatile tool for extracting all hyperlinks from any website URL. Available in multiple formats: modern web interface, Streamlit app, REST API, and command-line tool. Perfect for web scraping, SEO analysis, site mapping, and link auditing.

## 📑 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Screenshots](#-screenshots)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#-usage)
  - [Web Interface](#web-interface)
  - [Streamlit App](#streamlit-app)
  - [REST API](#rest-api)
  - [Command Line](#command-line)
  - [Python Library](#python-library)
- [Project Structure](#-project-structure)
- [Features in Detail](#-features-in-detail)
- [Examples](#-examples)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

## ✨ Features

- 🎨 **Modern UI**: Beautiful, vibrant interface with gradient backgrounds and smooth animations
- 🔍 **Smart Link Extraction**: Extract all unique hyperlinks from any website
- 🌐 **Browser Automation**: Support for JavaScript-rendered content using Selenium
- 🎯 **Advanced Filtering**: Filter by domain, include/exclude external links
- 📊 **Rich Statistics**: View total links, internal/external counts, and unique domains
- 📥 **Export Options**: Download links as TXT or CSV files
- 🔎 **Search & Filter**: Real-time search through extracted links
- ⚙️ **Highly Configurable**: Adjustable timeouts, wait times, and extraction options
- 📱 **Fully Responsive**: Works seamlessly on desktop, tablet, and mobile devices
- 🚀 **Multiple Interfaces**: Web UI, Streamlit app, REST API, and CLI
- 🛡️ **Robust Error Handling**: Comprehensive error messages and diagnostics
- 🔒 **URL Validation**: Automatic filtering of malformed and invalid URLs

## 🛠️ Tech Stack

### Backend
- **Python 3.7+** - Core language
- **Flask** - REST API framework
- **Flask-CORS** - Cross-origin resource sharing
- **Requests** - HTTP library
- **BeautifulSoup4** - HTML parsing
- **Selenium** - Browser automation for JavaScript sites
- **Webdriver Manager** - Automatic ChromeDriver management

### Frontend
- **HTML5** - Modern markup
- **CSS3** - Gradient designs and animations
- **JavaScript (ES6+)** - Interactive functionality
- **Streamlit** - Python web app framework

### Tools & Libraries
- **lxml** - Fast HTML/XML parser
- **urllib** - URL handling and parsing

## 📷 Screenshots

### Web Interface
![Web Interface](docs/screenshots/web-interface.png)
*Modern, vibrant web interface with gradient design*

### Streamlit App
![Streamlit App](docs/screenshots/streamlit-app.png)
*Interactive Python-based interface with statistics*

### API Response
```json
{
  "success": true,
  "links": ["https://example.com/page1", "https://example.com/page2"],
  "count": 2,
  "diagnostics": {
    "status_code": 200,
    "anchor_tags_found": 15,
    "unique_links_found": 2
  }
}
```

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.7 or higher** - [Download Python](https://www.python.org/downloads/)
- **Google Chrome** (for browser automation) - [Download Chrome](https://www.google.com/chrome/)
- **pip** - Python package manager (usually comes with Python)
- **Git** - [Download Git](https://git-scm.com/downloads)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sridharankaliyamoorthy/website_link_eaxtractor.git
   cd website_link_eaxtractor
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python3 -m venv venv
   
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install ChromeDriver** (for browser automation - optional)
   ```bash
   # macOS (using Homebrew)
   brew install chromedriver
   
   # Or it will be automatically downloaded on first use
   ```

## 💻 Usage

### Web Interface

1. **Start the Flask API server**
   ```bash
   cd src
   python3 api.py
   ```
   The API will run on `http://localhost:5001`

2. **Start the frontend server** (in a new terminal)
   ```bash
   cd src
   python3 -m http.server 8000
   ```

3. **Open your browser**
   Navigate to `http://localhost:8000`

4. **Extract links**
   - Enter a website URL
   - Optionally enable "Use Browser Automation" for JavaScript sites
   - Click "Extract Links"
   - View results and download as TXT/CSV

### Streamlit App

```bash
cd src
streamlit run link_extractor_ui.py
```

The app will open automatically at `http://localhost:8501`

### REST API

**Start the API server:**
```bash
cd src
python3 api.py
```

**Extract links via API:**
```bash
curl -X POST http://localhost:5001/api/extract \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "use_browser": false,
    "include_external": true,
    "timeout": 30
  }'
```

**Health check:**
```bash
curl http://localhost:5001/api/health
```

### Command Line

```bash
cd src
python3 link_extractor.py
```

Edit the `base_url` variable in the script to change the target website.

### Python Library

```python
from src.link_extractor import LinkExtractor

# Basic usage
extractor = LinkExtractor("https://example.com")
links, diagnostics = extractor.get_all_links(include_external=True)

for link in links:
    print(link)

# With browser automation (for JavaScript sites)
links, diagnostics = extractor.extract_links_with_browser(
    include_external=True,
    wait_time=20
)
```

## 📁 Project Structure

```
website_link_eaxtractor/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── workflows/
│   │   └── ci.yml
│   └── PULL_REQUEST_TEMPLATE.md
├── docs/
│   ├── screenshots/
│   └── api-documentation.md
├── src/
│   ├── link_extractor.py      # Core extraction module
│   ├── link_extractor_ui.py   # Streamlit interface
│   ├── api.py                 # Flask REST API
│   ├── index.html             # Web frontend
│   ├── styles.css             # Frontend styling
│   ├── script.js              # Frontend JavaScript
│   └── start_website.sh       # Convenience script
├── test/
│   └── test_link_extractor.py
├── .gitignore
├── CONTRIBUTING.md
├── LICENSE
├── requirements.txt
└── README.md
```

## 🎯 Features in Detail

### Link Extraction
- Extracts all `<a>` tags with `href` attributes
- Handles relative and absolute URLs
- Filters out invalid, malformed, and duplicate links
- Supports links in data attributes and JavaScript code

### Browser Automation
- Uses Selenium for JavaScript-rendered content
- Automatic ChromeDriver management
- Smart timeout handling for slow sites
- Progressive content waiting for dynamic pages

### URL Validation
- Comprehensive URL validation and cleaning
- Filters HTML entities and malformed URLs
- Removes fragments and normalizes URLs
- Domain validation and filtering

### Error Handling
- Detailed diagnostics and error messages
- Graceful handling of timeouts
- Partial content extraction on failures
- User-friendly error messages

## 📝 Examples

### Extract links from a simple site
```python
from src.link_extractor import LinkExtractor

extractor = LinkExtractor("https://example.com")
links, diagnostics = extractor.get_all_links()

print(f"Found {len(links)} links")
for link in links:
    print(link)
```

### Extract with domain filtering
```python
extractor = LinkExtractor("https://example.com")
links, diagnostics = extractor.get_all_links(
    filter_domain=True,
    include_external=False
)
```

### Multi-page crawling example
```python
from src.link_extractor import LinkExtractor
from collections import deque

def crawl_website(start_url, max_pages=10):
    extractor = LinkExtractor(start_url)
    visited = set()
    to_visit = deque([start_url])
    all_links = set()
    
    while to_visit and len(visited) < max_pages:
        url = to_visit.popleft()
        if url in visited:
            continue
            
        visited.add(url)
        links, _ = extractor.extract_links(
            url, 
            filter_domain=True, 
            include_external=False
        )
        all_links.update(links)
        
        for link in links:
            if link not in visited:
                to_visit.append(link)
    
    return all_links
```

## 🔧 Troubleshooting

### "No links found" error
- **Solution**: Enable "Use Browser Automation" for JavaScript-rendered sites
- Check if the URL is accessible in a regular browser
- Some sites may block automated requests

### Browser automation fails
- **Solution**: Ensure Chrome/Chromium is installed
- Check internet connection (ChromeDriver download on first use)
- Try installing ChromeDriver manually: `brew install chromedriver` (macOS)

### API connection errors
- **Solution**: Ensure Flask API is running on port 5001
- Check firewall settings
- Verify CORS is enabled (already configured)

### Port already in use
- **Solution**: Change the port in `api.py` (default: 5001)
- Or kill the process using the port: `lsof -ti:5001 | xargs kill -9`

### Page load timeout
- **Solution**: Increase timeout in the request
- For very slow sites, use browser automation with longer wait times
- The tool will extract links from partially loaded content

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on:

- Code of conduct
- Development setup
- Pull request process
- Coding standards
- Issue reporting

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

**Project Maintainer**: Sridharan Kaliyamoorthy

- **GitHub**: [@sridharankaliyamoorthy](https://github.com/sridharankaliyamoorthy)
- **Repository**: [website_link_eaxtractor](https://github.com/sridharankaliyamoorthy/website_link_eaxtractor)

## 🙏 Acknowledgments

- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - HTML parsing
- [Selenium](https://www.selenium.dev/) - Browser automation
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Streamlit](https://streamlit.io/) - App framework
- [Best-README-Template](https://github.com/othneildrew/Best-README-Template) - README inspiration

## 📈 Roadmap

- [ ] Add support for more browsers (Firefox, Safari)
- [ ] Implement caching for faster repeated extractions
- [ ] Add support for authenticated pages
- [ ] Create Docker container for easy deployment
- [ ] Add unit tests and integration tests
- [ ] Implement rate limiting for API
- [ ] Add support for extracting links from PDFs
- [ ] Create browser extension

---

⭐ **Star this repo if you find it useful!**
