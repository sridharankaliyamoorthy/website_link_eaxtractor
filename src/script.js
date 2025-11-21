// API Configuration
const API_URL = 'http://localhost:5001/api/extract';

// DOM Elements
const urlInput = document.getElementById('urlInput');
const extractBtn = document.getElementById('extractBtn');
const useBrowserCheckbox = document.getElementById('useBrowser');
const errorMessage = document.getElementById('errorMessage');
const resultsSection = document.getElementById('resultsSection');
const linksContainer = document.getElementById('linksContainer');
const countBadge = document.getElementById('countBadge');
const exampleButtons = document.querySelectorAll('.example-btn');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Focus on input
    urlInput.focus();
    
    // Enter key to submit
    urlInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            extractLinks();
        }
    });
    
    // Extract button click
    extractBtn.addEventListener('click', extractLinks);
    
    // Example buttons
    exampleButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const url = btn.getAttribute('data-url');
            urlInput.value = url;
            extractLinks();
        });
    });
});

// Extract Links Function
async function extractLinks() {
    const url = urlInput.value.trim();
    
    // Validate URL
    if (!url) {
        showError('Please enter a website URL');
        return;
    }
    
    if (!isValidUrl(url)) {
        showError('Invalid URL format. Please include http:// or https://');
        return;
    }
    
    // Hide previous results and errors
    hideError();
    hideResults();
    
    // Show loading state
    setLoading(true);
    
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                url: url,
                use_browser: useBrowserCheckbox.checked,
                filter_domain: false,
                include_external: true,
                timeout: 60,  // Very long timeout for slow sites
                wait_time: useBrowserCheckbox.checked ? 30 : 5  // Very long wait for browser automation
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to extract links');
        }
        
        if (data.success) {
            if (data.links && data.links.length > 0) {
                displayResults(data.links, data.count);
            } else {
                showError('No links found on this page. Try enabling "Use Browser Automation" for JavaScript-rendered sites like IBM documentation.');
            }
        } else {
            // Show the error from the API
            const errorMsg = data.error || 'Unknown error occurred';
            showError(errorMsg);
            
            // If browser automation failed, suggest alternatives
            if (errorMsg.includes('ChromeDriver') || errorMsg.includes('Chrome')) {
                showError(errorMsg + ' You can try without browser automation for simpler sites.');
            }
        }
        
    } catch (error) {
        console.error('Error:', error);
        
        if (error.message.includes('fetch')) {
            showError('Unable to connect to the server. Make sure the API is running on http://localhost:5001');
        } else {
            showError(error.message || 'An error occurred while extracting links');
        }
    } finally {
        setLoading(false);
    }
}

// Display Results
function displayResults(links, count) {
    // Update count badge
    countBadge.textContent = `${count} link${count !== 1 ? 's' : ''} found`;
    
    // Clear previous links
    linksContainer.innerHTML = '';
    
    // Create link cards
    links.forEach((link, index) => {
        const linkCard = createLinkCard(link, index + 1);
        linksContainer.appendChild(linkCard);
    });
    
    // Show results section
    resultsSection.style.display = 'block';
    
    // Smooth scroll to results
    setTimeout(() => {
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 100);
}

// Create Link Card
function createLinkCard(link, number) {
    const card = document.createElement('div');
    card.className = 'link-card';
    
    const numberSpan = document.createElement('span');
    numberSpan.className = 'link-number';
    numberSpan.textContent = number;
    
    const linkElement = document.createElement('a');
    linkElement.href = link;
    linkElement.textContent = link;
    linkElement.target = '_blank';
    linkElement.rel = 'noopener noreferrer';
    
    card.appendChild(numberSpan);
    card.appendChild(linkElement);
    
    return card;
}

// Show Error
function showError(message) {
    errorMessage.textContent = `⚠️ ${message}`;
    errorMessage.style.display = 'block';
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        hideError();
    }, 5000);
}

// Hide Error
function hideError() {
    errorMessage.style.display = 'none';
}

// Hide Results
function hideResults() {
    resultsSection.style.display = 'none';
}

// Set Loading State
function setLoading(loading) {
    extractBtn.disabled = loading;
    const btnText = extractBtn.querySelector('.btn-text');
    const btnLoader = extractBtn.querySelector('.btn-loader');
    
    if (loading) {
        btnText.style.display = 'none';
        btnLoader.style.display = 'inline-block';
    } else {
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    }
}

// Validate URL
function isValidUrl(url) {
    try {
        const urlObj = new URL(url);
        return urlObj.protocol === 'http:' || urlObj.protocol === 'https:';
    } catch {
        return false;
    }
}

