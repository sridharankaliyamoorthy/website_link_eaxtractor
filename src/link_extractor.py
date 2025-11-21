"""
Link Extractor Module
Fetches and extracts all hyperlinks from a given website URL.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import Set, List, Optional, Dict, Tuple
import re
import time
import json
import platform


class LinkExtractor:
    """Extracts hyperlinks from web pages."""
    
    def __init__(self, base_url: str, timeout: int = 10):
        """
        Initialize the LinkExtractor.
        
        Args:
            base_url: The base URL to extract links from
            timeout: Request timeout in seconds (default: 10)
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        # Complete User-Agent string to avoid blocking
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        self.last_error = None
        self.diagnostics = {}
    
    def fetch_page(self, url: str) -> Tuple[Optional[requests.Response], Optional[str]]:
        """
        Fetch a web page with better error handling.
        
        Args:
            url: URL to fetch
            
        Returns:
            Tuple of (Response object or None, error message or None)
        """
        try:
            # Allow redirects
            response = self.session.get(
                url, 
                timeout=self.timeout,
                allow_redirects=True,
                verify=True
            )
            
            # Store diagnostics
            self.diagnostics = {
                'status_code': response.status_code,
                'content_length': len(response.content),
                'content_type': response.headers.get('Content-Type', 'unknown'),
                'final_url': response.url,
                'redirected': response.url != url
            }
            
            # Check for common blocking indicators
            if response.status_code == 403:
                self.last_error = "Access forbidden (403). The website may be blocking automated requests."
                return None, self.last_error
            elif response.status_code == 401:
                self.last_error = "Unauthorized (401). The website may require authentication."
                return None, self.last_error
            elif response.status_code == 404:
                self.last_error = "Page not found (404)."
                return None, self.last_error
            
            response.raise_for_status()
            return response, None
            
        except requests.exceptions.Timeout:
            self.last_error = f"Request timed out after {self.timeout} seconds."
            return None, self.last_error
        except requests.exceptions.ConnectionError:
            self.last_error = "Connection error. Check your internet connection or the URL."
            return None, self.last_error
        except requests.exceptions.TooManyRedirects:
            self.last_error = "Too many redirects. The URL may be redirecting in a loop."
            return None, self.last_error
        except requests.RequestException as e:
            self.last_error = f"Request failed: {str(e)}"
            return None, self.last_error
        except Exception as e:
            self.last_error = f"Unexpected error: {str(e)}"
            return None, self.last_error
    
    def extract_links(self, url: Optional[str] = None, 
                     filter_domain: bool = True,
                     include_external: bool = True) -> Tuple[Set[str], Dict]:
        """
        Extract all unique links from the page.
        
        Args:
            url: URL to extract links from (defaults to base_url)
            filter_domain: If True, only include links from the same domain
            include_external: If True, include external links
            
        Returns:
            Tuple of (Set of unique URLs, diagnostics dictionary)
        """
        target_url = url or self.base_url
        response, error = self.fetch_page(target_url)
        
        if not response:
            return set(), {'error': error, **self.diagnostics}
        
        # Try different parsers for better compatibility
        parsers = ['html.parser', 'lxml', 'html5lib']
        soup = None
        
        for parser in parsers:
            try:
                soup = BeautifulSoup(response.content, parser)
                break
            except Exception:
                continue
        
        if not soup:
            return set(), {'error': 'Failed to parse HTML with any parser', **self.diagnostics}
        
        links = set()
        
        # Extract all anchor tags with href attributes
        anchors = soup.find_all('a', href=True)
        self.diagnostics['anchor_tags_found'] = len(anchors)
        
        for anchor in anchors:
            href = anchor.get('href', '').strip()
            
            # Skip empty, javascript:, mailto:, tel:, and fragment-only links
            if not href or href.startswith('javascript:') or href.startswith('mailto:') or \
               href.startswith('tel:') or href.startswith('#') or href.startswith('data:'):
                continue
            
            # Convert relative URLs to absolute URLs
            try:
                absolute_url = urljoin(response.url, href)
                # Clean and validate the URL
                cleaned_url = self._clean_url(absolute_url)
                
                if not cleaned_url:
                    continue
                
                # Filter based on domain if requested
                if filter_domain and not include_external:
                    if self._is_same_domain(cleaned_url):
                        links.add(cleaned_url)
                else:
                    links.add(cleaned_url)
            except Exception:
                # Skip invalid URLs
                continue
        
        # Also try to extract links from other sources
        # Look for links in data attributes, onclick handlers, etc.
        additional_links = self._extract_links_from_scripts(soup, response.url)
        links.update(additional_links)
        
        # Look for links in other HTML elements
        for element in soup.find_all(['link', 'area'], href=True):
            href = element.get('href', '').strip()
            if href and not href.startswith('javascript:'):
                try:
                    absolute_url = urljoin(response.url, href)
                    cleaned_url = self._clean_url(absolute_url)
                    if cleaned_url:
                        links.add(cleaned_url)
                except Exception:
                    continue
        
        # Look for router links (common in SPAs)
        for element in soup.find_all(attrs={'routerlink': True}):
            href = element.get('routerlink', '').strip()
            if href:
                try:
                    absolute_url = urljoin(response.url, href)
                    cleaned_url = self._clean_url(absolute_url)
                    if cleaned_url:
                        links.add(cleaned_url)
                except Exception:
                    continue
        
        # Look for links in JSON-LD structured data
        for script in soup.find_all('script', type='application/ld+json'):
            if script.string:
                try:
                    data = json.loads(script.string)
                    if isinstance(data, dict):
                        for key, value in data.items():
                            if isinstance(value, str) and value.startswith('http'):
                                links.add(value.split('#')[0])
                            elif isinstance(value, list):
                                for item in value:
                                    if isinstance(item, str) and item.startswith('http'):
                                        links.add(item.split('#')[0])
                except:
                    pass
        
        self.diagnostics['unique_links_found'] = len(links)
        self.diagnostics['success'] = True
        
        return links, self.diagnostics
    
    def _extract_links_from_scripts(self, soup: BeautifulSoup, base_url: str) -> Set[str]:
        """Extract URLs from JavaScript code and data attributes."""
        links = set()
        
        # Look for URLs in script tags
        for script in soup.find_all('script'):
            if script.string:
                # Find URLs in JavaScript code
                url_pattern = r'https?://[^\s"\'<>]+'
                found_urls = re.findall(url_pattern, script.string)
                for url in found_urls:
                    try:
                        cleaned_url = self._clean_url(url)
                        if cleaned_url:
                            links.add(cleaned_url)
                    except Exception:
                        continue
        
        # Look for links in data attributes
        for element in soup.find_all(attrs={'data-href': True}):
            href = element.get('data-href', '').strip()
            if href and not href.startswith('javascript:'):
                try:
                    absolute_url = urljoin(base_url, href)
                    cleaned_url = self._clean_url(absolute_url)
                    if cleaned_url:
                        links.add(cleaned_url)
                except Exception:
                    continue
        
        return links
    
    def extract_links_with_browser(self, url: Optional[str] = None, 
                                   filter_domain: bool = True,
                                   include_external: bool = True,
                                   wait_time: int = 10) -> Tuple[Set[str], Dict]:
        """
        Extract links using Selenium for JavaScript-rendered content.
        
        Args:
            url: URL to extract links from (defaults to base_url)
            filter_domain: If True, only include links from the same domain
            include_external: If True, include external links
            wait_time: Seconds to wait for page to load (default: 5)
            
        Returns:
            Tuple of (Set of unique URLs, diagnostics dictionary)
        """
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.service import Service
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from webdriver_manager.chrome import ChromeDriverManager
        except ImportError:
            return set(), {
                'error': 'Selenium not installed. Install with: pip install selenium webdriver-manager',
                'suggestion': 'Use extract_links() for non-JavaScript sites'
            }
        
        target_url = url or self.base_url
        links = set()
        
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in background
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument(f'user-agent={self.session.headers["User-Agent"]}')
        
        driver = None
        try:
            # Initialize Chrome driver with better error handling
            # Set Chrome binary location for macOS
            if platform.system().lower() == 'darwin':
                chrome_binary = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
                import os
                if os.path.exists(chrome_binary):
                    chrome_options.binary_location = chrome_binary
            
            # Try to use system ChromeDriver first (faster and more reliable)
            import os
            import shutil
            driver_found = False
            
            # Check common ChromeDriver locations
            common_paths = [
                '/opt/homebrew/bin/chromedriver',  # Homebrew on Apple Silicon
                '/usr/local/bin/chromedriver',      # Homebrew on Intel Mac
                shutil.which('chromedriver'),       # System PATH
            ]
            
            # Remove None values
            common_paths = [p for p in common_paths if p and os.path.exists(p)]
            
            # Try system ChromeDriver first
            for path in common_paths:
                try:
                    service = Service(path)
                    driver = webdriver.Chrome(service=service, options=chrome_options)
                    driver_found = True
                    self.diagnostics['chromedriver_source'] = 'system'
                    break
                except Exception:
                    continue
            
            # If system ChromeDriver doesn't work, try ChromeDriverManager
            if not driver_found:
                try:
                    driver_path = ChromeDriverManager().install()
                    service = Service(driver_path)
                    driver = webdriver.Chrome(service=service, options=chrome_options)
                    driver_found = True
                    self.diagnostics['chromedriver_source'] = 'webdriver-manager'
                except Exception as e1:
                    # Last resort: try without specifying service
                    try:
                        driver = webdriver.Chrome(options=chrome_options)
                        driver_found = True
                        self.diagnostics['chromedriver_source'] = 'auto-detect'
                    except Exception as e2:
                        error_msg = f"ChromeDriver setup failed. Tried system paths and webdriver-manager. "
                        error_msg += f"Errors: {str(e1)} / {str(e2)}. "
                        error_msg += "If ChromeDriver is installed, ensure it's in PATH or try: brew install chromedriver"
                        raise Exception(error_msg)
            
            # Navigate to page with aggressive timeout handling
            # Use a very long timeout for browser automation (60 seconds)
            browser_timeout = max(timeout * 3, 60)
            driver.set_page_load_timeout(browser_timeout)
            
            page_loaded = False
            try:
                driver.get(target_url)
                page_loaded = True
            except Exception as page_load_error:
                # If page load times out, stop loading and work with what we have
                error_str = str(page_load_error).lower()
                if 'timeout' in error_str:
                    self.diagnostics['page_load_warning'] = 'Page load timeout - extracting from partially loaded content'
                    try:
                        # Stop the page load and work with what's there
                        driver.execute_script("window.stop();")
                        page_loaded = True  # We have partial content
                    except Exception:
                        pass
                else:
                    raise
            
            # If page loaded or partially loaded, wait for content
            if page_loaded:
                # Wait for body to exist with longer timeout
                try:
                    WebDriverWait(driver, wait_time).until(
                        EC.presence_of_element_located((By.TAG_NAME, "body"))
                    )
                except Exception:
                    # If body wait fails, continue anyway - some content might be there
                    self.diagnostics['body_wait_warning'] = 'Body element wait timeout, but continuing'
                
                # Additional wait for dynamic content
                # Use progressive waiting - check every second if content has stabilized
                initial_links = 0
                stable_count = 0
                for i in range(wait_time):
                    time.sleep(1)
                    try:
                        current_links = len(driver.find_elements(By.TAG_NAME, "a"))
                        if current_links == initial_links:
                            stable_count += 1
                            if stable_count >= 3:  # Content stable for 3 seconds
                                break
                        else:
                            initial_links = current_links
                            stable_count = 0
                    except Exception:
                        pass
            
            # Get page source after JavaScript execution
            try:
                html = driver.page_source
            except Exception as e:
                # If getting page source fails, we can't continue
                raise Exception(f"Failed to get page source: {str(e)}")
            
            if not html or len(html) < 100:
                raise Exception("Page source is empty or too small - page may not have loaded")
            
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract links
            anchors = soup.find_all('a', href=True)
            self.diagnostics['anchor_tags_found'] = len(anchors)
            self.diagnostics['page_title'] = driver.title
            
            for anchor in anchors:
                href = anchor.get('href', '').strip()
                
                if not href or href.startswith('javascript:') or href.startswith('mailto:') or \
                   href.startswith('tel:') or href.startswith('#') or href.startswith('data:'):
                    continue
                
                try:
                    absolute_url = urljoin(target_url, href)
                    cleaned_url = self._clean_url(absolute_url)
                    
                    if not cleaned_url:
                        continue
                    
                    if filter_domain and not include_external:
                        if self._is_same_domain(cleaned_url):
                            links.add(cleaned_url)
                    else:
                        links.add(cleaned_url)
                except Exception:
                    continue
            
            # Also extract from JavaScript and other sources
            additional_links = self._extract_links_from_scripts(soup, target_url)
            links.update(additional_links)
            
            self.diagnostics['unique_links_found'] = len(links)
            self.diagnostics['success'] = True
            self.diagnostics['method'] = 'browser_automation'
            
            return links, self.diagnostics
            
        except Exception as e:
            error_msg = str(e)
            # Provide more helpful error messages
            if 'ChromeDriver' in error_msg or 'chromedriver' in error_msg.lower() or 'driver' in error_msg.lower():
                error_msg = f"ChromeDriver setup issue: {error_msg}. "
                error_msg += "Try: 1) Install manually: brew install chromedriver (macOS) or download from chromedriver.chromium.org, "
                error_msg += "2) Check internet connection (first run downloads ChromeDriver), "
                error_msg += "3) Try without browser automation for simpler sites."
            elif 'timeout' in error_msg.lower():
                error_msg = f"Page load timeout. The website took too long to load. Try increasing the timeout or check your internet connection."
            elif 'chrome' in error_msg.lower() and ('not found' in error_msg.lower() or 'cannot find' in error_msg.lower()):
                error_msg = "Chrome browser not found. Please install Google Chrome from https://www.google.com/chrome/"
            else:
                error_msg = f"Browser automation failed: {error_msg}"
            
            self.diagnostics['error'] = error_msg
            self.diagnostics['success'] = False
            return set(), self.diagnostics
        finally:
            if driver:
                try:
                    driver.quit()
                except Exception:
                    pass  # Ignore errors when closing driver
    
    def _is_valid_url(self, url: str) -> bool:
        """
        Validate if a URL is properly formatted and not malformed.
        
        Args:
            url: URL to validate
            
        Returns:
            True if URL is valid, False otherwise
        """
        try:
            parsed = urlparse(url)
            
            # Must have scheme and netloc
            if not parsed.scheme or not parsed.netloc:
                return False
            
            # Scheme must be http or https
            if parsed.scheme not in ['http', 'https']:
                return False
            
            # Check for malformed patterns
            # URLs with HTML entities encoded (like %22%3E, %3C/a%3E)
            if '%22%3E' in url or '%3C' in url or '%3E' in url:
                # But allow normal URL encoding like %20 for spaces
                # Only reject if it looks like HTML entities
                if '%22%3E' in url or '%3C/a' in url or 'href%3D' in url.lower():
                    return False
            
            # Check for multiple URLs concatenated (contains http:// or https:// more than once)
            if url.count('http://') > 1 or url.count('https://') > 1:
                return False
            
            # Check for URLs that are too long (likely malformed)
            if len(url) > 2000:
                return False
            
            # Check for invalid characters in domain
            if any(char in parsed.netloc for char in ['<', '>', '"', "'"]):
                return False
            
            # Check if URL can be parsed properly
            # Try to reconstruct it - if it's malformed, this will fail
            reconstructed = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            if parsed.query:
                reconstructed += f"?{parsed.query}"
            if parsed.fragment:
                reconstructed += f"#{parsed.fragment}"
            
            # Basic sanity check - URL should be reasonable
            return True
            
        except Exception:
            return False
    
    def _clean_url(self, url: str) -> Optional[str]:
        """
        Clean and normalize a URL.
        
        Args:
            url: URL to clean
            
        Returns:
            Cleaned URL or None if invalid
        """
        try:
            # Remove fragments
            url = url.split('#')[0]
            
            # Remove trailing slashes (except for root)
            if url.endswith('/') and urlparse(url).path != '/':
                url = url.rstrip('/')
            
            # Validate the URL
            if not self._is_valid_url(url):
                return None
            
            return url
        except Exception:
            return None
    
    def _is_same_domain(self, url: str) -> bool:
        """Check if URL belongs to the same domain as base_url."""
        try:
            base_domain = urlparse(self.base_url).netloc
            url_domain = urlparse(url).netloc
            return base_domain == url_domain
        except Exception:
            return False
    
    def get_all_links(self, filter_domain: bool = False, 
                     include_external: bool = True) -> Tuple[List[str], Dict]:
        """
        Get all links as a sorted list with diagnostics.
        
        Args:
            filter_domain: If True, only include links from the same domain
            include_external: If True, include external links
            
        Returns:
            Tuple of (Sorted list of unique URLs, diagnostics dictionary)
        """
        links, diagnostics = self.extract_links(
            filter_domain=filter_domain,
            include_external=include_external
        )
        return sorted(list(links)), diagnostics


def main():
    """Example usage of LinkExtractor."""
    # Example URL - can be easily changed
    base_url = "https://example.com"
    
    extractor = LinkExtractor(base_url)
    links, diagnostics = extractor.get_all_links(include_external=True)
    
    print(f"\nFound {len(links)} unique links from {base_url}:\n")
    print(f"Diagnostics: {diagnostics}\n")
    for i, link in enumerate(links, 1):
        print(f"{i}. {link}")


if __name__ == "__main__":
    main()

