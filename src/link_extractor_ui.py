"""
Streamlit UI for Link Extractor
A vibrant and modern interface for extracting links from websites.
"""

import streamlit as st
import sys
import os

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from link_extractor import LinkExtractor
import time
from urllib.parse import urlparse


# Page configuration
st.set_page_config(
    page_title="🔗 Link Extractor",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for vibrant styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    .main {
        font-family: 'Poppins', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        text-align: center;
    }
    
    .main-header h1 {
        color: white;
        font-size: 3rem;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        margin-top: 0.5rem;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    .link-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border-left: 4px solid #667eea;
    }
    
    .link-card:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stats-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .stats-number {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .stats-label {
        color: #666;
        font-size: 1rem;
        margin-top: 0.5rem;
    }
    
    .success-message {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        font-weight: 600;
        margin: 1rem 0;
    }
    
    .error-message {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        font-weight: 600;
        margin: 1rem 0;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    input[type="text"] {
        border-radius: 10px !important;
        border: 2px solid #667eea !important;
    }
    </style>
""", unsafe_allow_html=True)


def validate_url(url: str) -> bool:
    """Validate if the URL is properly formatted."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def main():
    # Header
    st.markdown("""
        <div class="main-header">
            <h1>🔗 Link Extractor</h1>
            <p>Extract all hyperlinks from any website with style!</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        
        filter_domain = st.checkbox(
            "🔒 Filter by Domain",
            value=False,
            help="Only show links from the same domain as the base URL"
        )
        
        include_external = st.checkbox(
            "🌐 Include External Links",
            value=True,
            help="Include links to external websites"
        )
        
        use_browser = st.checkbox(
            "🌐 Use Browser Automation (for JavaScript sites)",
            value=False,
            help="Enable this for websites that load content with JavaScript (slower but more accurate)"
        )
        
        timeout = st.slider(
            "⏱️ Request Timeout (seconds)",
            min_value=5,
            max_value=30,
            value=10,
            step=5
        )
        
        st.markdown("---")
        st.markdown("### 📝 About")
        st.info("""
        This tool extracts all hyperlinks from a given website URL.
        
        **Features:**
        - Extract unique links
        - Filter by domain
        - Export results
        - Beautiful UI
        """)
    
    # Main content area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        url_input = st.text_input(
            "🌐 Enter Website URL",
            placeholder="https://example.com",
            help="Enter the full URL including http:// or https://"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        extract_button = st.button("🚀 Extract Links", use_container_width=True)
    
    # Processing
    if extract_button:
        if not url_input:
            st.markdown("""
                <div class="error-message">
                    ⚠️ Please enter a valid URL!
                </div>
            """, unsafe_allow_html=True)
        elif not validate_url(url_input):
            st.markdown("""
                <div class="error-message">
                    ⚠️ Invalid URL format! Please include http:// or https://
                </div>
            """, unsafe_allow_html=True)
        else:
            with st.spinner("🔄 Extracting links... This may take a moment"):
                try:
                    extractor = LinkExtractor(url_input, timeout=timeout)
                    
                    if use_browser:
                        links, diagnostics = extractor.extract_links_with_browser(
                            filter_domain=filter_domain,
                            include_external=include_external,
                            wait_time=5
                        )
                    else:
                        links, diagnostics = extractor.get_all_links(
                            filter_domain=filter_domain,
                            include_external=include_external
                        )
                    
                    # Store diagnostics
                    st.session_state['diagnostics'] = diagnostics
                    
                    if links:
                        st.session_state['extracted_links'] = links
                        st.session_state['source_url'] = url_input
                        
                        st.markdown(f"""
                            <div class="success-message">
                                ✅ Successfully extracted {len(links)} unique links!
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Show diagnostics in expander
                        with st.expander("📊 Request Diagnostics"):
                            st.json(diagnostics)
                    else:
                        # Show detailed error information
                        error_msg = diagnostics.get('error', 'Unknown error')
                        anchor_count = diagnostics.get('anchor_tags_found', 0)
                        content_length = diagnostics.get('content_length', 0)
                        status_code = diagnostics.get('status_code', 'N/A')
                        
                        error_html = f"""
                            <div class="error-message">
                                ⚠️ No links found on this page.
                                <br><br>
                                <strong>Details:</strong><br>
                                • Status Code: {status_code}<br>
                                • Content Length: {content_length:,} bytes<br>
                                • Anchor Tags Found: {anchor_count}<br>
                                • Error: {error_msg if error_msg else 'None'}
                            </div>
                        """
                        
                        st.markdown(error_html, unsafe_allow_html=True)
                        
                        # Provide helpful suggestions
                        st.info("""
                        **Possible reasons why no links were found:**
                        - The page content is loaded dynamically with JavaScript (requires browser automation)
                        - The website is blocking automated requests
                        - The page requires authentication
                        - The page structure doesn't use standard `<a>` tags
                        - The page returned an error or empty content
                        
                        **Try:**
                        - Increasing the timeout in settings
                        - Checking if the URL is accessible in a browser
                        - Trying a different page from the same website
                        """)
                        
                        # Show diagnostics
                        with st.expander("📊 Request Diagnostics"):
                            st.json(diagnostics)
                            
                except Exception as e:
                    st.markdown(f"""
                        <div class="error-message">
                            ❌ Error: {str(e)}
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.error(f"Full error details: {type(e).__name__}: {str(e)}")
    
    # Display results
    if 'extracted_links' in st.session_state and st.session_state['extracted_links']:
        links = st.session_state['extracted_links']
        source_url = st.session_state.get('source_url', 'Unknown')
        
        # Statistics
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
                <div class="stats-card">
                    <div class="stats-number">{len(links)}</div>
                    <div class="stats-label">Total Links</div>
                </div>
            """, unsafe_allow_html=True)
        
        # Count internal vs external links
        internal_count = sum(1 for link in links if urlparse(link).netloc == urlparse(source_url).netloc)
        external_count = len(links) - internal_count
        
        with col2:
            st.markdown(f"""
                <div class="stats-card">
                    <div class="stats-number">{internal_count}</div>
                    <div class="stats-label">Internal Links</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="stats-card">
                    <div class="stats-number">{external_count}</div>
                    <div class="stats-label">External Links</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
                <div class="stats-card">
                    <div class="stats-number">{len(set(urlparse(link).netloc for link in links))}</div>
                    <div class="stats-label">Unique Domains</div>
                </div>
            """, unsafe_allow_html=True)
        
        # Export options
        st.markdown("---")
        export_col1, export_col2 = st.columns([1, 1])
        
        with export_col1:
            # Create text file content
            links_text = "\n".join(links)
            st.download_button(
                label="📥 Download as TXT",
                data=links_text,
                file_name=f"links_{urlparse(source_url).netloc.replace('.', '_')}.txt",
                mime="text/plain"
            )
        
        with export_col2:
            # Create CSV content
            import csv
            import io
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(['#', 'URL'])
            for i, link in enumerate(links, 1):
                writer.writerow([i, link])
            csv_content = output.getvalue()
            
            st.download_button(
                label="📊 Download as CSV",
                data=csv_content,
                file_name=f"links_{urlparse(source_url).netloc.replace('.', '_')}.csv",
                mime="text/csv"
            )
        
        # Display links
        st.markdown("---")
        st.markdown("### 📋 Extracted Links")
        
        # Search/filter functionality
        search_term = st.text_input("🔍 Filter links", placeholder="Search in URLs...")
        
        filtered_links = links
        if search_term:
            filtered_links = [link for link in links if search_term.lower() in link.lower()]
            st.info(f"Showing {len(filtered_links)} of {len(links)} links")
        
        # Display links in a scrollable container
        links_container = st.container()
        with links_container:
            for i, link in enumerate(filtered_links, 1):
                domain = urlparse(link).netloc
                is_internal = domain == urlparse(source_url).netloc
                
                badge = "🏠 Internal" if is_internal else "🌐 External"
                badge_color = "#667eea" if is_internal else "#f5576c"
                
                st.markdown(f"""
                    <div class="link-card">
                        <strong>#{i}</strong> {badge}
                        <br>
                        <a href="{link}" target="_blank" style="color: #667eea; text-decoration: none;">
                            {link}
                        </a>
                    </div>
                """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

