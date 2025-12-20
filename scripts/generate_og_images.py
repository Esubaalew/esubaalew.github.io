#!/usr/bin/env python3
"""
Auto-generate OG images for blog posts, wegs, and poems based on their titles.
Supports Amharic/Ethiopic text using embedded Ethiopian fonts.
"""

import base64
import re
import subprocess
from pathlib import Path

# Configuration
BLOG_DIR = Path("docs/blog")
WEGOCH_DIR = Path("src/content/wegoch")
GETEM_DIR = Path("src/content/getem")
GEEZ_DIR = Path("src/content/geez")
CS_DIR = Path("src/content/cs")
ASSETS_DIR = Path("docs/assets")
FONT_DIR = Path("docs/assets")
OUTPUT_WIDTH = 1200
OUTPUT_HEIGHT = 630

# Ethiopian font for Amharic text
ETHIOPIC_FONT_PATH = FONT_DIR / "AddisAbebaUnicode.ttf"
ETHIOPIC_FONT_BOLD_PATH = FONT_DIR / "EthiopicLeTewahedo-Bold.ttf"

# Cache for embedded font
_font_cache = {}


def has_ethiopic(text: str) -> bool:
    """Check if text contains Ethiopic characters."""
    for char in text:
        # Ethiopic Unicode range: U+1200 to U+137F
        if '\u1200' <= char <= '\u137F':
            return True
    return False


def get_embedded_font(font_path: Path) -> str:
    """Get base64-encoded font for embedding in SVG."""
    if str(font_path) in _font_cache:
        return _font_cache[str(font_path)]
    
    if not font_path.exists():
        return ""
    
    font_data = font_path.read_bytes()
    encoded = base64.b64encode(font_data).decode('ascii')
    _font_cache[str(font_path)] = encoded
    return encoded


def extract_title_from_md(filepath: Path) -> str | None:
    """Extract title from markdown frontmatter."""
    content = filepath.read_text(encoding="utf-8")
    
    # Try YAML frontmatter
    match = re.search(r'^---\s*\n.*?title:\s*["\']?([^"\'\n]+)["\']?.*?\n---', content, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    # Try first H1
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    
    return None


def wrap_text(text: str, max_chars: int = 35) -> list[str]:
    """Wrap text into multiple lines."""
    words = text.split()
    lines = []
    current_line = []
    current_len = 0
    
    for word in words:
        if current_len + len(word) + 1 <= max_chars:
            current_line.append(word)
            current_len += len(word) + 1
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
            current_len = len(word)
    
    if current_line:
        lines.append(" ".join(current_line))
    
    return lines[:3]  # Max 3 lines


def escape_xml(text: str) -> str:
    """Escape special XML characters."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def generate_svg(title: str) -> str:
    """Generate minimal SVG content for the OG image with font support."""
    lines = wrap_text(title, 40)
    uses_ethiopic = has_ethiopic(title)
    
    # Font settings
    if uses_ethiopic:
        # Use Ethiopian font for Amharic titles
        font_path = ETHIOPIC_FONT_BOLD_PATH if ETHIOPIC_FONT_BOLD_PATH.exists() else ETHIOPIC_FONT_PATH
        font_base64 = get_embedded_font(font_path)
        font_family = "EthiopicFont, Arial, sans-serif"
        font_size = 48  # Slightly smaller for Ethiopic
        max_chars = 25  # Fewer chars per line for Ethiopic
        lines = wrap_text(title, max_chars)
    else:
        font_base64 = ""
        font_family = "Arial, sans-serif"
        font_size = 52
    
    # Calculate title positioning
    line_height = 70
    total_height = len(lines) * line_height
    start_y = (OUTPUT_HEIGHT // 2) - (total_height // 2) + 30
    
    title_lines = "\n".join(
        f'  <text x="{OUTPUT_WIDTH // 2}" y="{start_y + i * line_height}" '
        f'fill="#ededed" font-family="{font_family}" font-size="{font_size}" '
        f'font-weight="bold" text-anchor="middle" letter-spacing="0.01em">{escape_xml(line)}</text>'
        for i, line in enumerate(lines)
    )
    
    # Calculate underline position
    underline_y = start_y + len(lines) * line_height + 20
    
    # Font embedding style
    font_style = ""
    if font_base64:
        font_style = f'''
  <defs>
    <style type="text/css">
      @font-face {{
        font-family: 'EthiopicFont';
        src: url('data:font/truetype;charset=utf-8;base64,{font_base64}') format('truetype');
        font-weight: bold;
        font-style: normal;
      }}
    </style>
  </defs>'''
    
    svg = f'''<svg width="{OUTPUT_WIDTH}" height="{OUTPUT_HEIGHT}" viewBox="0 0 {OUTPUT_WIDTH} {OUTPUT_HEIGHT}" xmlns="http://www.w3.org/2000/svg">
{font_style}
  <rect width="{OUTPUT_WIDTH}" height="{OUTPUT_HEIGHT}" fill="#0a0a0a"/>
  
  <!-- Title -->
{title_lines}
  
  <!-- Subtle underline -->
  <line x1="300" y1="{underline_y}" x2="900" y2="{underline_y}" stroke="#666" stroke-width="1" stroke-opacity="0.3"/>
  
  <!-- Footer -->
  <text x="{OUTPUT_WIDTH // 2}" y="580" fill="#666" font-family="Arial, sans-serif" font-size="18" text-anchor="middle">esubalew.dev</text>
</svg>'''
    
    return svg


def get_og_filename(md_file: Path) -> str:
    """Generate OG image filename from markdown filename."""
    stem = md_file.stem
    # Create a shorter, cleaner name
    words = stem.split("-")[:4]
    return "og-" + "-".join(words)


def convert_svg_to_png(svg_path: Path, png_path: Path):
    """Convert SVG to PNG using available tools."""
    try:
        subprocess.run(
            ["rsvg-convert", "-w", str(OUTPUT_WIDTH), "-h", str(OUTPUT_HEIGHT), 
             str(svg_path), "-o", str(png_path)],
            check=True,
            capture_output=True
        )
        print(f"Generated {png_path.name}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            import cairosvg
            cairosvg.svg2png(url=str(svg_path), write_to=str(png_path), 
                           output_width=OUTPUT_WIDTH, output_height=OUTPUT_HEIGHT)
            print(f"Generated {png_path.name} (via cairosvg)")
            return True
        except ImportError:
            print("PNG conversion skipped - install cairosvg or rsvg-convert")
            return False


def process_blog_posts():
    """Process blog posts directory."""
    if not BLOG_DIR.exists():
        return 0, 0
    
    generated = 0
    skipped = 0
    
    for md_file in BLOG_DIR.glob("*.md"):
        if md_file.name == "index.md":
            continue
        
        og_base = get_og_filename(md_file)
        og_png = BLOG_DIR / f"{og_base}.png"
        og_svg = BLOG_DIR / f"{og_base}.svg"
        
        existing_ogs = list(BLOG_DIR.glob(f"og-*{md_file.stem[:10]}*"))
        
        if og_png.exists() or og_svg.exists() or existing_ogs:
            print(f"⏭️  Skipping {md_file.name} - OG image exists")
            skipped += 1
            continue
        
        title = extract_title_from_md(md_file)
        if not title:
            print(f"Skipping {md_file.name} - No title found")
            continue
        
        svg_content = generate_svg(title)
        og_svg.write_text(svg_content, encoding="utf-8")
        print(f"Generated {og_svg.name}")
        
        convert_svg_to_png(og_svg, og_png)
        generated += 1
    
    return generated, skipped


def process_works(content_dir: Path, work_type: str, force_regenerate: bool = False):
    """Process wegs or poems directory."""
    if not content_dir.exists():
        return 0, 0
    
    generated = 0
    skipped = 0
    
    # Ensure assets directory exists
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    
    for md_file in content_dir.glob("*.md"):
        if md_file.name == "index.md":
            continue
        
        # OG images go to assets with work type prefix
        og_base = f"og-{work_type}-{md_file.stem}"
        og_png = ASSETS_DIR / f"{og_base}.png"
        og_svg = ASSETS_DIR / f"{og_base}.svg"
        
        if not force_regenerate and (og_png.exists() or og_svg.exists()):
            print(f"⏭️  Skipping {md_file.name} - OG image exists")
            skipped += 1
            continue
        
        title = extract_title_from_md(md_file)
        if not title:
            print(f"Skipping {md_file.name} - No title found")
            continue
        
        svg_content = generate_svg(title)
        og_svg.write_text(svg_content, encoding="utf-8")
        print(f"Generated {og_svg.name}")
        
        convert_svg_to_png(og_svg, og_png)
        
        # Update the markdown file to use the new OG image
        update_og_image_in_md(md_file, f"/assets/{og_base}.png")
        
        generated += 1
    
    return generated, skipped


def update_og_image_in_md(md_file: Path, og_image_path: str):
    """Update the og_image field in markdown frontmatter."""
    content = md_file.read_text(encoding="utf-8")
    
    
    new_content = re.sub(
        r'og_image:\s*"[^"]*"',
        f'og_image: "{og_image_path}"',
        content
    )
    
    if new_content != content:
        md_file.write_text(new_content, encoding="utf-8")
        print(f"Updated {md_file.name} with new OG image")


def main():
    """Main function to generate missing OG images."""
    import sys
    
    # Check for --force flag to regenerate all
    force = "--force" in sys.argv
    
    if force:
        print("Force regenerating all OG images...\n")
    
    print("Processing blog posts...")
    blog_gen, blog_skip = process_blog_posts()
    
    print("\n📖 Processing wegs...")
    weg_gen, weg_skip = process_works(WEGOCH_DIR, "weg", force_regenerate=force)
    
    print("\n📜 Processing poems...")
    poem_gen, poem_skip = process_works(GETEM_DIR, "getem", force_regenerate=force)
    
    print("\n📿 Processing Ge'ez...")
    geez_gen, geez_skip = process_works(GEEZ_DIR, "geez", force_regenerate=force)
    
    print("\n💻 Processing CS articles...")
    cs_gen, cs_skip = process_works(CS_DIR, "cs", force_regenerate=force)
    
    total_gen = blog_gen + weg_gen + poem_gen + geez_gen + cs_gen
    total_skip = blog_skip + weg_skip + poem_skip + geez_skip + cs_skip
    
    print(f"\n📊 Summary: {total_gen} generated, {total_skip} skipped")


if __name__ == "__main__":
    main()
