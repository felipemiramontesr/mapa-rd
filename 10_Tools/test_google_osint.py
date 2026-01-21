import json
import requests
import sys
import os
import re

# Add renderer path directly to sys.path
renderer_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '05_Build', 'report_engine'))
sys.path.append(renderer_dir)
from pdf_renderer import PDFRenderer

# Load Configuration
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), '..', '03_Config', 'config.json')
    with open(config_path, 'r') as f:
        return json.load(f)

def get_best_image(item):
    """
    Smart image selection:
    1. Try CSE Image (High Res).
    2. If it is internal (x-raw-image), fall back to public Thumbnail.
    3. Return None if neither exists.
    """
    img_src = None
    
    # Try getting high-res image
    if 'pagemap' in item and 'cse_image' in item['pagemap'] and len(item['pagemap']['cse_image']) > 0:
        img_src = item['pagemap']['cse_image'][0]['src']
    
    # Check if broken internal image or missing
    if not img_src or img_src.startswith('x-raw-image'):
        # Fallback to thumbnail
        if 'pagemap' in item and 'cse_thumbnail' in item['pagemap'] and len(item['pagemap']['cse_thumbnail']) > 0:
             img_src = item['pagemap']['cse_thumbnail'][0]['src']
    
    return img_src

def detect_file_type(item):
    """Detects if result is PDF, DOC, or Generic Web."""
    link = item.get('link', '').lower()
    file_format = item.get('fileFormat', '').lower()
    
    if 'pdf' in file_format or link.endswith('.pdf'):
        return 'PDF Document', '#ef4444' # Red
    if 'word' in file_format or link.endswith('.doc') or link.endswith('.docx'):
        return 'Word Document', '#3b82f6' # Blue
    if 'ppt' in file_format or link.endswith('.ppt') or link.endswith('.pptx'):
        return 'Presentation', '#f97316' # Orange
    
    return 'Sitio Web', '#10b981' # Green

def clean_snippet(text):
    """Clean newlines and excessive whitespace from snippets."""
    return text.replace('\n', ' ').strip()

def generate_html_content(results, query):
    style = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
        
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%) !important;
            color: #e2e8f0;
            margin: 0;
            padding: 40px;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            padding-bottom: 20px;
        }
        
        h1 {
            font-weight: 300;
            letter-spacing: 2px;
            color: #fff;
            margin: 0;
        }
        
        .meta {
            color: #94a3b8;
            font-size: 0.9rem;
            margin-top: 10px;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 25px;
        }

        .card {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            overflow: hidden;
            backdrop-filter: blur(10px);
            display: flex;
            flex-direction: column;
            transition: transform 0.2s;
            height: 100%;
        }

        .card-img-container {
            width: 100%;
            height: 160px;
            background: #020617;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }

        .card-img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        
        .no-img {
            color: #475569;
            font-size: 0.8rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 8px;
        }

        .card-content {
            padding: 20px;
            display: flex;
            flex-direction: column;
            flex-grow: 1;
        }
        
        .badges {
            display: flex;
            gap: 8px;
            margin-bottom: 12px;
        }
        
        .badge {
            font-size: 0.65rem;
            text-transform: uppercase;
            padding: 2px 8px;
            border-radius: 4px;
            font-weight: 600;
            letter-spacing: 0.5px;
        }

        .card-title {
            font-size: 1rem;
            font-weight: 600;
            margin-bottom: 10px;
            color: #f8fafc;
            line-height: 1.4;
        }
        
        .snippet {
            font-size: 0.85rem;
            color: #94a3b8;
            margin-bottom: 15px;
            line-height: 1.5;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
            flex-grow: 1;
        }

        .source-box {
            margin-top: auto;
            border-top: 1px solid rgba(255,255,255,0.1);
            padding-top: 12px;
            font-size: 0.75rem;
        }
        
        .domain {
            color: #38bdf8;
            font-weight: 600;
            display: block;
            margin-bottom: 4px;
        }
        
        .full-link {
            color: #64748b;
            text-decoration: none;
            overflow-wrap: break-word;
            display: block;
        }
    </style>
    """

    cards_html = ""
    for item in results:
        img_src = get_best_image(item)
        file_type, badge_color = detect_file_type(item)
        snippet = clean_snippet(item.get('snippet', 'No description available.'))
        domain = item.get('displayLink', 'Unknown Source')
        link = item.get('link', '#')
        
        # Image Element
        if img_src:
            image_html = f'<img src="{img_src}" class="card-img" onerror="this.onerror=null;this.src=\'\';this.parentElement.innerHTML=\'<div class=\"no-img\">Image Load Error</div>\'">'
        else:
            image_html = '<div class="no-img"><span>📄</span><span>No Preview</span></div>'
        
        cards_html += f"""
        <div class="card">
            <div class="card-img-container">
                {image_html}
            </div>
            <div class="card-content">
                <div class="badges">
                    <span class="badge" style="background: {badge_color}20; color: {badge_color}; border: 1px solid {badge_color}40">{file_type}</span>
                </div>
                <div class="card-title">{item.get('title', 'Sin Título')}</div>
                <div class="snippet">{snippet}</div>
                <div class="source-box">
                    <span class="domain">{domain}</span>
                    <a href="{link}" class="full-link" target="_blank">{link}</a>
                </div>
            </div>
        </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        {style}
    </head>
    <body>
        <div class="header">
            <h1>REPORTE DE INTELIGENCIA (OSINT)</h1>
            <div class="meta">Target: {query} | Hallazgos: {len(results)}</div>
        </div>
        <div class="grid">
            {cards_html}
        </div>
    </body>
    </html>
    """
    return html

def test_google_search(query):
    config = load_config()
    api_key = config['google_cse']['api_key']
    cx = config['google_cse']['cx']
    
    print(f"🔎 Buscando: {query}")
    
    url = "https://customsearch.googleapis.com/customsearch/v1"
    params = {
        'key': api_key,
        'cx': cx,
        'q': query,
        'searchType': 'image', 
        'num': 10
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        items = data.get('items', [])
        print(f"✅ Encontrados {len(items)} resultados.")
        
        # DEBUG: Print first item keys to understand structure
        if len(items) > 0:
            print("🔍 RAW ITEM STRUCTURE:")
            print(json.dumps(items[0], indent=2))
            
        # 1. Generate HTML
        html_content = generate_html_content(items, query)
        
        # 2. Render PDF
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'report_engine', 'out')
        os.makedirs(output_dir, exist_ok=True)
        pdf_path = os.path.join(output_dir, 'google_results_tests.pdf')
        
        renderer = PDFRenderer()
        renderer.render_from_string(html_content, pdf_path)
        
        print(f"📄 PDF Generado: {pdf_path}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        if 'response' in locals() and hasattr(response, 'text'):
            print(f"🔍 Detalle Google: {response.text}")

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    target_email = "felipemiramontesr@gmail.com"
    test_google_search(target_email)
