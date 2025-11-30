#!/usr/bin/env python3
"""
Auto-generate OG images for blog posts based on their titles.
Scans docs/blog/ for markdown files and creates OG images for any that don't have one.
"""

import os
import re
import subprocess
import hashlib
from pathlib import Path

# Configuration
BLOG_DIR = Path("docs/blog")
OUTPUT_WIDTH = 1200
OUTPUT_HEIGHT = 630

# Color themes for variety (cycles based on title hash)
THEMES = [
    {
        "gradient": [("#1a1a2e", 0), ("#16213e", 50), ("#0f3460", 100)],
        "accent": "#e94560",
        "text": "#ffffff",
        "subtitle": "#a5b4fc",
        "footer": "#94a3b8",
    },
    {
        "gradient": [("#0d1b2a", 0), ("#1b263b", 50), ("#415a77", 100)],
        "accent": "#00b4d8",
        "text": "#ffffff",
        "subtitle": "#90e0ef",
        "footer": "#caf0f8",
    },
    {
        "gradient": [("#2d1b69", 0), ("#11998e", 50), ("#38ef7d", 100)],
        "accent": "#f7dc6f",
        "text": "#ffffff",
        "subtitle": "#d5f5e3",
        "footer": "#abebc6",
    },
    {
        "gradient": [("#1f1c2c", 0), ("#928dab", 50), ("#1f1c2c", 100)],
        "accent": "#ff6b6b",
        "text": "#ffffff",
        "subtitle": "#ffeaa7",
        "footer": "#dfe6e9",
    },
    {
        "gradient": [("#0f0c29", 0), ("#302b63", 50), ("#24243e", 100)],
        "accent": "#f093fb",
        "text": "#ffffff",
        "subtitle": "#c471ed",
        "footer": "#a29bfe",
    },
]


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


def get_theme_for_title(title: str) -> dict:
    """Get a consistent theme based on title hash."""
    hash_val = int(hashlib.md5(title.encode()).hexdigest(), 16)
    return THEMES[hash_val % len(THEMES)]


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


def generate_svg(title: str, theme: dict) -> str:
    """Generate SVG content for the OG image."""
    lines = wrap_text(title, 30)
    
    # Build gradient stops
    gradient_stops = "\n".join(
        f'      <stop offset="{pct}%" style="stop-color:{color};stop-opacity:1" />'
        for color, pct in theme["gradient"]
    )
    
    # Calculate title positioning
    line_height = 60
    total_height = len(lines) * line_height
    start_y = (OUTPUT_HEIGHT // 2) - (total_height // 2) + 20
    
    title_lines = "\n".join(
        f'  <text x="{OUTPUT_WIDTH // 2}" y="{start_y + i * line_height}" '
        f'fill="{theme["text"]}" font-family="Arial, sans-serif" font-size="48" '
        f'font-weight="bold" text-anchor="middle">{escape_xml(line)}</text>'
        for i, line in enumerate(lines)
    )
    
    svg = f'''<svg width="{OUTPUT_WIDTH}" height="{OUTPUT_HEIGHT}" viewBox="0 0 {OUTPUT_WIDTH} {OUTPUT_HEIGHT}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
{gradient_stops}
    </linearGradient>
  </defs>
  
  <rect width="{OUTPUT_WIDTH}" height="{OUTPUT_HEIGHT}" fill="url(#bgGrad)"/>
  
  <!-- Decorative elements -->
  <circle cx="100" cy="100" r="150" fill="{theme["accent"]}" fill-opacity="0.1"/>
  <circle cx="1100" cy="530" r="200" fill="{theme["accent"]}" fill-opacity="0.08"/>
  
  <!-- Accent bar -->
  <rect x="100" y="80" width="80" height="6" rx="3" fill="{theme["accent"]}"/>
  
  <!-- Blog label -->
  <text x="100" y="130" fill="{theme["subtitle"]}" font-family="Arial, sans-serif" font-size="22" font-weight="500">BLOG POST</text>
  
  <!-- Title -->
{title_lines}
  
  <!-- Footer -->
  <line x1="100" y1="540" x2="1100" y2="540" stroke="{theme["footer"]}" stroke-opacity="0.3" stroke-width="1"/>
  <text x="{OUTPUT_WIDTH // 2}" y="580" fill="{theme["footer"]}" font-family="Arial, sans-serif" font-size="20" text-anchor="middle">Esubalew Chekol • esubalew.dev</text>
</svg>'''
    
    return svg


def get_og_filename(md_file: Path) -> str:
    """Generate OG image filename from markdown filename."""
    stem = md_file.stem
    # Create a shorter, cleaner name
    words = stem.split("-")[:4]
    return "og-" + "-".join(words)


def main():
    """Main function to generate missing OG images."""
    if not BLOG_DIR.exists():
        print(f"Blog directory not found: {BLOG_DIR}")
        return
    
    generated = 0
    skipped = 0
    
    for md_file in BLOG_DIR.glob("*.md"):
        # Skip index
        if md_file.name == "index.md":
            continue
        
        # Check if OG image already exists
        og_base = get_og_filename(md_file)
        og_png = BLOG_DIR / f"{og_base}.png"
        og_svg = BLOG_DIR / f"{og_base}.svg"
        
        # Also check for existing custom OG images with different naming
        existing_ogs = list(BLOG_DIR.glob(f"og-*{md_file.stem[:10]}*"))
        
        if og_png.exists() or og_svg.exists() or existing_ogs:
            print(f"⏭️  Skipping {md_file.name} - OG image exists")
            skipped += 1
            continue
        
        # Extract title
        title = extract_title_from_md(md_file)
        if not title:
            print(f"⚠️  Skipping {md_file.name} - No title found")
            continue
        
        # Generate SVG
        theme = get_theme_for_title(title)
        svg_content = generate_svg(title, theme)
        
        # Write SVG
        og_svg.write_text(svg_content, encoding="utf-8")
        print(f"✅ Generated {og_svg.name}")
        
        # Convert to PNG using rsvg-convert if available
        try:
            subprocess.run(
                ["rsvg-convert", "-w", str(OUTPUT_WIDTH), "-h", str(OUTPUT_HEIGHT), 
                 str(og_svg), "-o", str(og_png)],
                check=True,
                capture_output=True
            )
            print(f"✅ Generated {og_png.name}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Try cairosvg as fallback
            try:
                import cairosvg
                cairosvg.svg2png(url=str(og_svg), write_to=str(og_png), 
                               output_width=OUTPUT_WIDTH, output_height=OUTPUT_HEIGHT)
                print(f"✅ Generated {og_png.name} (via cairosvg)")
            except ImportError:
                print(f"⚠️  PNG conversion skipped - install cairosvg or rsvg-convert")
        
        generated += 1
    
    print(f"\n📊 Summary: {generated} generated, {skipped} skipped")


if __name__ == "__main__":
    main()

