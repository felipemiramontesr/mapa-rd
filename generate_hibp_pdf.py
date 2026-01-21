import sys
import os
import requests
import json
from datetime import datetime

# Add path to pdf_renderer
sys.path.append(r'c:\Felipe\Projects\Mapa-rd\05_Build\report_engine')
from pdf_renderer import PDFRenderer

# Configuration
API_KEY = "344ba3142e664cf29effcebea34e9f3e"
TARGET_EMAILS = [
    "felipemiramontesr@gmail.com", 
    "felipe.maria.romero@gmail.com",
    "anafbaca@gmail.com"
]

def fetch_breaches(email):
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}?truncateResponse=false"
    headers = {
        "hibp-api-key": API_KEY,
        "user-agent": "OSINT-PDF-Generator"
    }
    
    print(f"Fetching data for {email}...")
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            breaches = response.json()
            print(f"Found {len(breaches)} breaches.")
            return breaches
        elif response.status_code == 404:
            print("No breaches found.")
            return []
        else:
            print(f"Error fetching data: {response.status_code}")
            return []
    except Exception as e:
        print(f"Connection error: {e}")
        return []

import time

def generate_hibp_pdf():
    all_breaches_dict = {} # Key: BreachName, Value: BreachData
    email_breaches_map = {email: set() for email in TARGET_EMAILS}
    
    # 1. Fetch Data & Build Maps
    all_html_sections = ""
    
    for i, email in enumerate(TARGET_EMAILS):
        # Add delay to avoid Rate Limit (429) - Increased to 10s to be safe
        if i > 0:
            print("Waiting 10s for rate limit...")
            time.sleep(10)
            
        breaches = fetch_breaches(email)
        
        # Populate maps for comparison table
        for b in breaches:
            all_breaches_dict[b['Name']] = b
            email_breaches_map[email].add(b['Name'])
            
        # Pagination Logic
        page_break_style = 'page-break-before: always;' if i > 0 else ''
        
        # Start Section Wrapper
        all_html_sections += f'<div style="{page_break_style}">'
        
        # Summary Header
        all_html_sections += f"""
        <div class="summary" style="margin-top: 40px; border-left: 5px solid #3498db;">
            <p><strong>Objetivo:</strong> {email}</p>
            <p><strong>Fecha de Reporte:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Total de Brechas Encontradas:</strong> <span style="font-size: 1.5em; font-weight: bold; color: #e74c3c;">{len(breaches)}</span></p>
        </div>
        """
        
        if not breaches:
            all_html_sections += "<p><em>No se encontraron brechas para este correo.</em></p><hr>"
        else:
            all_html_sections += ''.join([f'''
            <div class="breach-card">
                <div class="breach-header">
                    <span class="breach-title">{b['Name']}</span>
                    <span class="breach-date">{b['BreachDate']}</span>
                </div>
                <div class="data-classes">Datos Comprometidos: {', '.join(b['DataClasses'])}</div>
                <div class="description">{b['Description']}</div>
            </div>
            ''' for b in sorted(breaches, key=lambda x: x['BreachDate'], reverse=True)])
            
        # End Section Wrapper
        all_html_sections += '</div>'

    # 2. Build Comparison Table HTML
    if all_breaches_dict:
        sorted_breaches = sorted(all_breaches_dict.values(), key=lambda x: x['BreachDate'], reverse=True)
        
        table_rows = ""
        for b in sorted_breaches:
            row_cells = ""
            for email in TARGET_EMAILS:
                is_pwned = "🔴" if b['Name'] in email_breaches_map[email] else "<span style='color:#ccc'>-</span>"
                bg_color = "#fce4e4" if b['Name'] in email_breaches_map[email] else "#fff"
                row_cells += f"<td style='text-align: center; background-color: {bg_color};'>{is_pwned}</td>"
            
            table_rows += f"""
            <tr>
                <td style="font-weight: bold;">{b['Name']}</td>
                <td style="color: #666; font-size: 0.9em;">{b['BreachDate']}</td>
                {row_cells}
            </tr>
            """
            
        # Table Header with Emails
        header_cells = "".join([f"<th style='width: 25%; word-break: break-all;'>{email}</th>" for email in TARGET_EMAILS])

        comparison_html = f"""
        <div style="page-break-before: always;">
            <h1>Matriz de Exposición (Comparativo)</h1>
            <p>Resumen cruzado de afectaciones por cuenta de correo.</p>
            
            <table class="comparison-table">
                <thead>
                    <tr>
                        <th>Brecha</th>
                        <th>Fecha</th>
                        {header_cells}
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
        </div>
        """
    else:
        comparison_html = "<div style='page-break-before: always;'><h1>Matriz Comparativa</h1><p>No se encontraron datos para generar la matriz.</p></div>"

    # HTML Shell
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; color: #333; }}
            h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
            .summary {{ background-color: #ecf0f1; padding: 20px; border-radius: 5px; margin-bottom: 30px; }}
            .breach-card {{ border: 1px solid #ddd; padding: 15px; margin-bottom: 20px; border-radius: 5px; page-break-inside: avoid; }}
            .breach-header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #eee; padding-bottom: 10px; margin-bottom: 10px; }}
            .breach-title {{ font-size: 1.2em; font-weight: bold; color: #e74c3c; }}
            .breach-date {{ color: #7f8c8d; font-size: 0.9em; }}
            .data-classes {{ font-weight: bold; color: #2980b9; font-size: 0.9em; margin-top: 5px; }}
            .description {{ margin-top: 10px; font-size: 0.95em; line-height: 1.5; }}
            .footer {{ margin-top: 40px; text-align: center; font-size: 0.8em; color: #95a5a6; }}
            
            /* Table Styles */
            .comparison-table {{ width: 100%; border-collapse: collapse; margin-top: 20px; font-size: 0.85em; }}
            .comparison-table th, .comparison-table td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
            .comparison-table th {{ background-color: #2c3e50; color: white; text-align: center; }}
            .comparison-table tr:nth-child(even) {{ background-color: #f9f9f9; }}
        </style>
    </head>
    <body>
        <h1>Reporte de Brechas de Seguridad (HIBP) - Detallado</h1>
        {all_html_sections}
        {comparison_html}
        <div class="footer">
            Generado por MAPA-RD OSINT Module | Fuente: Have I Been Pwned API
        </div>
    </body>
    </html>
    """

    # 3. Render PDF
    output_pdf = r"c:\Felipe\Projects\Mapa-rd\HIBP_Compare_Report.pdf"
    
    try:
        print("Rendering PDF...")
        renderer = PDFRenderer()
        renderer.render_from_string(html_content, output_pdf)
        print(f"PDF Generated successfully: {output_pdf}")
    except Exception as e:
        print(f"Failed to generate PDF: {e}")

if __name__ == "__main__":
    generate_hibp_pdf()
