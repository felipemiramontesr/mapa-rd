import os

file_path = r"c:\Felipe\Projects\Mapa-rd\report_engine\out\MAPA-RD-MASTER-TEMPLATE.html"

try:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
except FileNotFoundError:
    print(f"File not found: {file_path}")
    exit(1)

# 1. Fix IRD Score (if not already done)
old_ird = """                <div class="ird-hero-score">
                    <span class="score-val">94</span>
                    <span class="score-label">Riesgo Máximo</span>
                </div>"""
new_ird = """                <div class="ird-hero-score">
                    <span class="score-val" style="color: {{ ird_color|default('#fff') }}">{{ ird_score }}</span>
                    <span class="score-label" style="color: {{ ird_color|default('#fff') }}">{{ ird_label }}</span>
                </div>"""

if old_ird in content:
    content = content.replace(old_ird, new_ird)
    print("Replaced IRD Score.")
else:
    print("IRD Score check: Strings did not exact match or already replaced.")

# 2. Remove Hardcoded Vectors
start_marker = "<!-- PAGE 3: VECTOR SLIDE (VEC-001) -->"
end_marker = "<!-- TIMELINE SLIDE 1 -->"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
    # Replace vectors
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Replaced hardcoded vector pages with placeholder.")

    # Reload content for next steps
    content = new_content

# 3. Remove Hardcoded Timeline (All Slides)
# Strategy: Find the start of the first timeline page and the end of the last timeline page.
# Finding distinct markers is key.
tl_start = '<div class="pdf-page timeline-page">'
tl_end_marker = '<!-- PAGE: EXPOSURE VALUE -->'

start_tl = content.find(tl_start)
end_tl = content.find(tl_end_marker)

if start_tl != -1 and end_tl != -1:
    content = content[:start_tl] + "{{ timeline_pages_html }}\n\n    " + content[end_tl:]
    print("Replaced Timeline sections.")
else:
    print("Timeline markers not found (or already replaced).")

# 4. Templatize Exposure Values (Invoice)
# We will replace the specific rows with a variable
invoice_start = '<tbody>'
invoice_end = '</tbody>'
# We have to be careful as there might be other tbodys, but likely only one in this snippet or we use context.
# Actually, let's find the specific block for the Invoice Table.
inv_marker = '<table class="invoice-table">'
inv_idx = content.find(inv_marker)
if inv_idx != -1:
    # Find tbody after table start
    tbody_start = content.find('<tbody>', inv_idx)
    tbody_end = content.find('</tbody>', tbody_start)
    if tbody_start != -1 and tbody_end != -1:
        # Construct dynamic tbody
        new_tbody = """<tbody>
                        {{ exposure_invoice_rows }}
                        <tr class="invoice-total-row">
                            <td colspan="3">TOTAL ESTIMADO</td>
                            <td class="amount">{{ exposure_grand_total }}</td>
                        </tr>
                    </tbody>"""
        content = content[:tbody_start] + new_tbody + content[tbody_end+7:]
        print("Replaced Invoice Data.")

# 5. Templatize Exposure Big Number
# <div class="total-value-huge">$385.00 USD</div>
# We use regex or simple replace for the inner text if it's unique enough or use the class.
import re
content = re.sub(r'<div class="total-value-huge">.*?</div>', '<div class="total-value-huge">{{ exposure_grand_total }}</div>', content)
print("Replaced Big Total Number.")

# 6. Dossier Evidence (Specific names)
content = content.replace('Banorte Leak + SAT', '{{ dossier_source_1 }}')
content = content.replace('Synthient Stealer', '{{ dossier_source_2 }}')
print("Replaced Dossier Evidence.")

# Final Save
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

