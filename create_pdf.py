#!/usr/bin/env python3
"""
Script pour convertir l'eBook astroEthique2025 en format PDF
"""

import os
import subprocess
import tempfile
from pathlib import Path

def create_combined_html():
    """Combine tous les fichiers HTML en un seul fichier"""
    
    # Ordre des chapitres
    chapters = [
        "index.html",
        "preface.html", 
        "chapitre1.html",
        "chapitre2.html",
        "chapitre3.html", 
        "chapitre4.html",
        "chapitre5.html",
        "chapitre6.html",
        "chapitre7.html",
        "chapitre8.html",
        "chapitre9.html",
        "chapitre10.html",
        "chapitre11.html",
        "chapitre12.html",
        "about.html"
    ]
    
    # Créer le HTML combiné
    combined_html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Les Mystères des Trous Noirs - astroEthique2025</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
            color: #e2e8f0;
            line-height: 1.7;
        }
        
        .chapter-title {
            font-family: 'Playfair Display', serif;
            font-weight: 700;
            font-size: clamp(2.5rem, 5vw, 4rem);
            line-height: 1.1;
            color: white;
        }
        
        .content-section {
            max-width: 900px;
            margin: 0 auto;
            padding: 4rem 2rem;
        }
        
        .highlight-box {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 2rem;
            margin: 2rem 0;
        }
        
        .page-break {
            page-break-before: always;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
        }
        
        .drop-cap {
            float: left;
            font-size: 4rem;
            line-height: 3rem;
            padding-right: 0.5rem;
            padding-top: 0.25rem;
            font-family: 'Playfair Display', serif;
            font-weight: 700;
            color: #ff6b35;
        }
        
        .image-container {
            text-align: center;
            margin: 2rem 0;
        }
        
        .image-container img {
            max-width: 100%;
            height: auto;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }
        
        .navigation {
            display: none;
        }
        
        @media print {
            .page-break {
                page-break-before: always;
            }
        }
    </style>
</head>
<body>
"""
    
    # Lire et combiner tous les fichiers
    for chapter in chapters:
        file_path = Path(chapter)
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Extraire le contenu principal (entre les balises body)
                start = content.find('<body>') + 6
                end = content.find('</body>')
                main_content = content[start:end].strip()
                
                # Ajouter un saut de page entre les chapitres (sauf pour le premier)
                if chapter != "index.html":
                    combined_html += '<div class="page-break">'
                
                combined_html += main_content
                
                if chapter != "index.html":
                    combined_html += '</div>'
    
    combined_html += """
</body>
</html>
"""
    
    # Sauvegarder le fichier combiné
    with open('ebook_combined.html', 'w', encoding='utf-8') as f:
        f.write(combined_html)
    
    print("✅ Fichier HTML combiné créé avec succès!")
    return 'ebook_combined.html'

def create_pdf_with_wkhtmltopdf(html_file):
    """Convertir le HTML en PDF en utilisant wkhtmltopdf"""
    
    # Options pour wkhtmltopdf pour une meilleure qualité
    options = [
        'wkhtmltopdf',
        '--page-size', 'A4',
        '--orientation', 'Portrait',
        '--margin-top', '20mm',
        '--margin-bottom', '20mm',
        '--margin-left', '15mm', 
        '--margin-right', '15mm',
        '--encoding', 'UTF-8',
        '--print-media-type',
        '--disable-smart-shrinking',
        '--enable-local-file-access',
        '--javascript-delay', '2000',
        '--no-stop-slow-scripts',
        '--images',
        '--enable-plugins',
        html_file,
        'Les_Mysteres_des_Trous_Noirs_astroEthique2025.pdf'
    ]
    
    try:
        subprocess.run(options, check=True)
        print("✅ PDF créé avec succès!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de la création du PDF: {e}")
        return False
    except FileNotFoundError:
        print("❌ wkhtmltopdf n'est pas installé. Installation en cours...")
        return False

def create_pdf_with_weasyprint(html_file):
    """Alternative: utiliser WeasyPrint pour créer le PDF"""
    try:
        from weasyprint import HTML, CSS
        from weasyprint.text.fonts import FontConfiguration
        
        font_config = FontConfiguration()
        
        # CSS personnalisé pour l'impression
        css_string = """
        @page {
            size: A4;
            margin: 2cm;
        }
        
        .page-break {
            page-break-before: always;
        }
        
        body {
            font-size: 12pt;
            line-height: 1.6;
        }
        
        .chapter-title {
            font-size: 24pt;
            margin-bottom: 1cm;
        }
        
        .highlight-box {
            page-break-inside: avoid;
            margin: 1cm 0;
        }
        
        .image-container img {
            max-width: 100%;
            height: auto;
        }
        """
        
        html_doc = HTML(filename=html_file)
        css_doc = CSS(string=css_string, font_config=font_config)
        
        html_doc.write_pdf(
            'Les_Mysteres_des_Trous_Noirs_astroEthique2025.pdf',
            stylesheets=[css_doc],
            font_config=font_config
        )
        
        print("✅ PDF créé avec succès via WeasyPrint!")
        return True
        
    except ImportError:
        print("❌ WeasyPrint n'est pas installé.")
        return False
    except Exception as e:
        print(f"❌ Erreur avec WeasyPrint: {e}")
        return False

def install_requirements():
    """Installer les dépendances nécessaires"""
    print("📦 Installation des dépendances...")
    
    try:
        subprocess.run(['pip', 'install', 'weasyprint'], check=True)
        print("✅ WeasyPrint installé avec succès!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erreur lors de l'installation de WeasyPrint")
        return False

def main():
    """Fonction principale"""
    print("🚀 Conversion de l'eBook astroEthique2025 en PDF...")
    print("=" * 50)
    
    # Créer le HTML combiné
    html_file = create_combined_html()
    
    # Essayer de créer le PDF avec wkhtmltopdf d'abord
    print("\n📄 Tentative de création du PDF avec wkhtmltopdf...")
    if create_pdf_with_wkhtmltopdf(html_file):
        print("\n🎉 eBook PDF créé avec succès!")
        print("📁 Fichier: Les_Mysteres_des_Trous_Noirs_astroEthique2025.pdf")
        return
    
    # Si wkhtmltopdf échoue, essayer avec WeasyPrint
    print("\n📄 Tentative avec WeasyPrint...")
    if create_pdf_with_weasyprint(html_file):
        print("\n🎉 eBook PDF créé avec succès!")
        print("📁 Fichier: Les_Mysteres_des_Trous_Noirs_astroEthique2025.pdf")
        return
    
    # Si les deux échouent, installer les dépendances
    print("\n📦 Installation des dépendances nécessaires...")
    if install_requirements():
        print("\n📄 Nouvelle tentative avec WeasyPrint...")
        if create_pdf_with_weasyprint(html_file):
            print("\n🎉 eBook PDF créé avec succès!")
            print("📁 Fichier: Les_Mysteres_des_Trous_Noirs_astroEthique2025.pdf")
            return
    
    print("\n❌ Impossible de créer le PDF automatiquement.")
    print("💡 Solutions alternatives:")
    print("   1. Utiliser un navigateur web pour imprimer le fichier HTML combiné")
    print("   2. Utiliser des outils en ligne comme HTML2PDF")
    print("   3. Copier-coller le contenu dans un éditeur de texte et exporter en PDF")

if __name__ == "__main__":
    main()