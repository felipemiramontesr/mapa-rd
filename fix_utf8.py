
import re
import os

file_path = r'c:\Felipe\Projects\Mapa-rd\report_engine\out\MAPA-RD-V2-PRINT.html'

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    print("Opened as UTF-8")
except:
    with open(file_path, 'r', encoding='latin-1') as f:
        content = f.read()
    print("Opened as Latin-1")

# 1. Regex Replace the logic
# Replace inner content of h4 highlight-text with '14 A&ntilde;os'
# This handles any messed up $114 artifacts
content = re.sub(r'<h4 class="highlight-text">.*?</h4>', '<h4 class="highlight-text">14 A&ntilde;os</h4>', content)

# 2. Fix encoding artifacts (Latin-1 interpreted as UTF-8)
replacements = {
    '$114': '14',
    '114 A': '14 A',
    # Specific Title Fixes (Decoding + Title Case)
    'DEUDA HISTÃ“RICA': 'Deuda Histórica',
    'DEUDA HISTÓRICA': 'Deuda Histórica', # In case it was already valid utf8
    'NUEVA VISIBILIDAD': 'Nueva Visibilidad',
    'COLAPSO INEVITABLE': 'Colapso Inevitable',
    # General repairs
    'Ã±': 'ñ',
    'Ã³': 'ó',
    'Ã¡': 'á',
    'Ã©': 'é',
    'Ãí': 'í',
    'Ãº': 'ú',
    'InacciÃ³n': 'Inacción',
    'reconstrucciÃ³n': 'reconstrucción',
    'automÃ¡tico': 'automático'
}

for bad, good in replacements.items():
    content = content.replace(bad, good)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("File repaired and saved as UTF-8.")
