# API Documentation

## Base URL

```
http://localhost:5001
```

## Endpoints

### Health Check

Check if the API is running.

**Endpoint:** `GET /api/health`

**Response:**
```json
{
  "status": "healthy",
  "service": "Link Extractor API"
}
```

### Extract Links

Extract all links from a given URL.

**Endpoint:** `POST /api/extract`

**Request Body:**
```json
{
  "url": "https://example.com",
  "use_browser": false,
  "filter_domain": false,
  "include_external": true,
  "timeout": 30,
  "wait_time": 15
}
```

**Parameters:**
- `url` (required): The website URL to extract links from
- `use_browser` (optional, default: false): Use browser automation for JavaScript sites
- `filter_domain` (optional, default: false): Filter links by domain
- `include_external` (optional, default: true): Include external links
- `timeout` (optional, default: 30): Request timeout in seconds
- `wait_time` (optional, default: 15): Wait time for browser automation

**Success Response:**
```json
{
  "success": true,
  "links": [
    "https://example.com/page1",
    "https://example.com/page2"
  ],
  "count": 2,
  "diagnostics": {
    "status_code": 200,
    "content_length": 1234,
    "anchor_tags_found": 10,
    "unique_links_found": 2,
    "success": true
  }
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Error message here",
  "links": [],
  "count": 0,
  "diagnostics": {
    "error": "Detailed error information"
  }
}
```

## Example Usage

### Using cURL

```bash
curl -X POST http://localhost:5001/api/extract \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "use_browser": false,
    "include_external": true
  }'
```

### Using Python

```python
import requests

url = "http://localhost:5001/api/extract"
data = {
    "url": "https://example.com",
    "use_browser": False,
    "include_external": True
}

response = requests.post(url, json=data)
result = response.json()

if result["success"]:
    print(f"Found {result['count']} links")
    for link in result["links"]:
        print(link)
else:
    print(f"Error: {result['error']}")
```

### Using JavaScript

```javascript
fetch('http://localhost:5001/api/extract', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    url: 'https://example.com',
    use_browser: false,
    include_external: true
  })
})
.then(response => response.json())
.then(data => {
  if (data.success) {
    console.log(`Found ${data.count} links`);
    data.links.forEach(link => console.log(link));
  } else {
    console.error('Error:', data.error);
  }
});
```

## Error Codes

- `400`: Bad Request - Invalid URL or missing required parameters
- `500`: Internal Server Error - Server-side error during processing

## Rate Limiting

Currently, there is no rate limiting implemented. Please use responsibly.

## CORS

CORS is enabled for all origins. This allows the frontend to make requests from any domain.

