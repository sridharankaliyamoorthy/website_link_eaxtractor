"""
Unit tests for Link Extractor
"""

import unittest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from link_extractor import LinkExtractor


class TestLinkExtractor(unittest.TestCase):
    """Test cases for LinkExtractor class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_url = "https://example.com"
        self.extractor = LinkExtractor(self.test_url, timeout=10)
    
    def test_initialization(self):
        """Test LinkExtractor initialization"""
        self.assertEqual(self.extractor.base_url, self.test_url)
        self.assertEqual(self.extractor.timeout, 10)
        self.assertIsNotNone(self.extractor.session)
    
    def test_url_validation(self):
        """Test URL validation"""
        # Valid URLs
        self.assertTrue(self.extractor._is_valid_url("https://example.com"))
        self.assertTrue(self.extractor._is_valid_url("http://example.com/page"))
        
        # Invalid URLs
        self.assertFalse(self.extractor._is_valid_url("not-a-url"))
        self.assertFalse(self.extractor._is_valid_url("javascript:alert(1)"))
        self.assertFalse(self.extractor._is_valid_url("mailto:test@example.com"))
    
    def test_same_domain_check(self):
        """Test domain comparison"""
        self.assertTrue(self.extractor._is_same_domain("https://example.com/page"))
        self.assertFalse(self.extractor._is_same_domain("https://google.com"))
    
    def test_url_cleaning(self):
        """Test URL cleaning"""
        # Test fragment removal
        cleaned = self.extractor._clean_url("https://example.com/page#section")
        self.assertEqual(cleaned, "https://example.com/page")
        
        # Test invalid URL
        cleaned = self.extractor._clean_url("javascript:alert(1)")
        self.assertIsNone(cleaned)
    
    def test_extract_links_basic(self):
        """Test basic link extraction"""
        links, diagnostics = self.extractor.get_all_links(include_external=True)
        
        # Should extract at least some links
        self.assertIsInstance(links, list)
        self.assertIsInstance(diagnostics, dict)
        self.assertIn('success', diagnostics)
    
    def test_extract_links_filter_domain(self):
        """Test domain filtering"""
        links, diagnostics = self.extractor.get_all_links(
            filter_domain=True,
            include_external=False
        )
        
        # All links should be from the same domain
        for link in links:
            self.assertTrue(self.extractor._is_same_domain(link))


if __name__ == '__main__':
    unittest.main()

