#!/usr/bin/env python3
"""
Minimal static site generator for Esubalew's portfolio.
Converts markdown to HTML with minimal dependencies.
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.tables import TableExtension
from markdown.extensions.toc import TocExtension

# Paths
ROOT = Path(__file__).parent
SRC = ROOT / "src"
CONTENT = SRC / "content"
TEMPLATES = SRC / "templates"
CSS = SRC / "css"
BLOG = ROOT / "docs" / "blog"  # Keep existing blog posts
ASSETS = ROOT / "docs" / "assets"
OUTPUT = ROOT / "dist"

# Site config
SITE_URL = "https://esubalew.dev"


def humanize_date(date: datetime) -> str:
    """Return a human-readable relative date string."""
    now = datetime.now()
    diff = now - date
    
    days = diff.days
    
    if days == 0:
        return "today"
    elif days == 1:
        return "yesterday"
    elif days < 7:
        return f"{days} days ago"
    elif days < 14:
        return "1 week ago"
    elif days < 30:
        weeks = days // 7
        return f"{weeks} weeks ago"
    elif days < 60:
        return "1 month ago"
    elif days < 365:
        months = days // 30
        return f"{months} months ago"
    elif days < 730:
        return "1 year ago"
    else:
        years = days // 365
        return f"{years} years ago"


def read_template(name: str) -> str:
    """Read an HTML template."""
    return (TEMPLATES / name).read_text(encoding="utf-8")


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return {}, content
    
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    
    frontmatter = {}
    for line in parts[1].strip().split("\n"):
        # Split on ': ' to handle keys with colons like 'og:image'
        if ": " in line:
            idx = line.index(": ")
            key = line[:idx].strip()
            value = line[idx+2:].strip().strip('"').strip("'")
            frontmatter[key] = value
        elif ":" in line:
            # Fallback for simple key: value
            key, value = line.split(":", 1)
            value = value.strip().strip('"').strip("'")
            frontmatter[key.strip()] = value
    
    return frontmatter, parts[2].strip()


def render_markdown(content: str) -> str:
    """Convert markdown to HTML."""
    md = markdown.Markdown(
        extensions=[
            CodeHiliteExtension(css_class='highlight', linenums=False),
            FencedCodeExtension(),
            TableExtension(),
            TocExtension(permalink=False),
            'smarty',
        ]
    )
    return md.convert(content)


def render_template(template: str, **kwargs) -> str:
    """Simple template rendering with {{variable}} syntax."""
    result = template
    for key, value in kwargs.items():
        result = result.replace("{{" + key + "}}", str(value) if value else "")
    # Remove any remaining template variables
    result = re.sub(r'\{\{[^}]+\}\}', '', result)
    return result


def get_blog_posts() -> list[dict]:
    """Get all blog posts sorted by date."""
    posts = []
    
    for md_file in BLOG.glob("*.md"):
        if md_file.name == "index.md":
            continue
        
        content = md_file.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(content)
        
        # Extract date
        date_str = meta.get("date", "")
        if not date_str:
            # Try to get from og:image or use file mtime
            date_str = "2025-01-01"
        
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            date = datetime.now()
        
        slug = md_file.stem
        
        posts.append({
            "title": meta.get("title", slug.replace("-", " ").title()),
            "description": meta.get("description", ""),
            "date": date,
            "date_str": date.strftime("%Y-%m-%d"),
            "date_formatted": date.strftime("%B %d, %Y"),
            "year": date.strftime("%Y"),
            "slug": slug,
            "url": f"/blog/{slug}",
            "content": body,
            "meta": meta,
        })
    
    # Sort by date descending
    posts.sort(key=lambda x: x["date"], reverse=True)
    return posts


def build_home(posts: list[dict]):
    """Build the home page."""
    # Read index content
    index_content = (CONTENT / "index.md").read_text(encoding="utf-8")
    meta, body = parse_frontmatter(index_content)
    
    # Build post list HTML
    post_list_html = '<ul class="post-list">\n'
    current_year = None
    for post in posts[:10]:  # Show latest 10 posts
        year_html = ""
        if post["year"] != current_year:
            current_year = post["year"]
            year_html = f'<span class="year">{current_year}</span>'
        else:
            year_html = '<span class="year"></span>'
        
        post_list_html += f'''    <li>
        {year_html}
        <span class="title"><a href="{post["url"]}">{post["title"]}</a></span>
    </li>\n'''
    post_list_html += '</ul>'
    
    # Build content
    intro_html = render_markdown(body)
    
    content_html = f'''
        <section class="intro">
            <h1>Esubalew Chekol</h1>
            <p class="subtitle">Software Engineer & MSc AI Student</p>
            {intro_html}
        </section>
        
        <section>
            <h2 class="section-header">Latest Posts</h2>
            {post_list_html}
        </section>
    '''
    
    template = read_template("base.html")
    html = render_template(
        template,
        title=meta.get("title", "Home"),
        description=meta.get("description", ""),
        keywords=meta.get("keywords", ""),
        og_title=meta.get("og_title", meta.get("title", "")),
        og_description=meta.get("og_description", meta.get("description", "")),
        og_image=f"{SITE_URL}{meta.get('og_image', '/assets/og-image.png')}",
        og_type=meta.get("og_type", "website"),
        canonical_url=SITE_URL,
        content=content_html,
    )
    
    (OUTPUT / "index.html").write_text(html, encoding="utf-8")
    print("✓ Built index.html")


def build_blog_index(posts: list[dict]):
    """Build the blog index page."""
    post_list_html = '<ul class="post-list">\n'
    current_year = None
    for post in posts:
        year_html = ""
        if post["year"] != current_year:
            current_year = post["year"]
            year_html = f'<span class="year">{current_year}</span>'
        else:
            year_html = '<span class="year"></span>'
        
        post_list_html += f'''    <li>
        {year_html}
        <span class="title"><a href="{post["url"]}">{post["title"]}</a></span>
    </li>\n'''
    post_list_html += '</ul>'
    
    content_html = f'''
        <section>
            <h1 class="section-header">Blog</h1>
            {post_list_html}
        </section>
    '''
    
    template = read_template("base.html")
    html = render_template(
        template,
        title="Blog",
        description="Technical blog about Rust, Python, machine learning, and software engineering.",
        keywords="software engineering blog, Rust, Python, machine learning, AI, systems programming, technical blog",
        og_title="Blog - Esubalew Chekol",
        og_description="Thoughts on software engineering, machine learning, and computing.",
        og_image=f"{SITE_URL}/assets/og-blog.png",
        og_type="website",
        canonical_url=f"{SITE_URL}/blog",
        content=content_html,
    )
    
    blog_dir = OUTPUT / "blog"
    blog_dir.mkdir(exist_ok=True)
    (blog_dir / "index.html").write_text(html, encoding="utf-8")
    print("✓ Built blog/index.html")


def build_blog_posts(posts: list[dict]):
    """Build individual blog post pages."""
    template = read_template("blog-post.html")
    blog_dir = OUTPUT / "blog"
    blog_dir.mkdir(exist_ok=True)
    
    for post in posts:
        content_html = render_markdown(post["content"])
        
        html = render_template(
            template,
            title=post["title"],
            description=post["description"],
            keywords=post["meta"].get("keywords", ""),
            og_title=post["meta"].get("og:title", post["title"]),
            og_description=post["meta"].get("og:description", post["description"]),
            og_image=f"{SITE_URL}{post['meta'].get('og:image', '/assets/og-blog.png')}",
            og_type="article",
            canonical_url=f"{SITE_URL}{post['url']}",
            date=post["date_str"],
            date_formatted=post["date_formatted"],
            content=content_html,
        )
        
        post_dir = blog_dir / post["slug"]
        post_dir.mkdir(exist_ok=True)
        (post_dir / "index.html").write_text(html, encoding="utf-8")
    
    print(f"✓ Built {len(posts)} blog posts")


def build_projects():
    """Build the projects page."""
    content = (CONTENT / "projects.md").read_text(encoding="utf-8")
    meta, body = parse_frontmatter(content)
    
    # Convert markdown to HTML
    body_html = render_markdown(body)
    
    content_html = f'''
        <section>
            <h1 class="section-header">Projects</h1>
            <div class="projects-content">
                {body_html}
            </div>
        </section>
    '''
    
    template = read_template("base.html")
    html = render_template(
        template,
        title=meta.get("title", "Projects"),
        description=meta.get("description", ""),
        keywords=meta.get("keywords", ""),
        og_title=meta.get("og_title", "Projects"),
        og_description=meta.get("og_description", ""),
        og_image=f"{SITE_URL}{meta.get('og_image', '/assets/og-projects.png')}",
        og_type="website",
        canonical_url=f"{SITE_URL}/projects",
        content=content_html,
    )
    
    projects_dir = OUTPUT / "projects"
    projects_dir.mkdir(exist_ok=True)
    (projects_dir / "index.html").write_text(html, encoding="utf-8")
    print("✓ Built projects/index.html")


def build_resume():
    """Build the resume page."""
    content = (CONTENT / "resume.md").read_text(encoding="utf-8")
    meta, body = parse_frontmatter(content)
    
    body_html = render_markdown(body)
    
    content_html = f'''
        <section class="resume">
            <h1 class="section-header">Resume</h1>
            <div class="resume-content">
                {body_html}
            </div>
        </section>
    '''
    
    template = read_template("base.html")
    html = render_template(
        template,
        title=meta.get("title", "Resume"),
        description=meta.get("description", ""),
        keywords=meta.get("keywords", ""),
        og_title=meta.get("og_title", "Resume"),
        og_description=meta.get("og_description", ""),
        og_image=f"{SITE_URL}{meta.get('og_image', '/assets/og-resume.png')}",
        og_type="profile",
        canonical_url=f"{SITE_URL}/resume",
        content=content_html,
    )
    
    resume_dir = OUTPUT / "resume"
    resume_dir.mkdir(exist_ok=True)
    (resume_dir / "index.html").write_text(html, encoding="utf-8")
    print("✓ Built resume/index.html")


def build_links():
    """Build the links page."""
    content = (CONTENT / "links.md").read_text(encoding="utf-8")
    meta, body = parse_frontmatter(content)
    
    body_html = render_markdown(body)
    
    content_html = f'''
        <section>
            <h1 class="section-header">Links</h1>
            <div class="links-content">
                {body_html}
            </div>
        </section>
    '''
    
    template = read_template("base.html")
    html = render_template(
        template,
        title=meta.get("title", "Links"),
        description=meta.get("description", ""),
        keywords=meta.get("keywords", ""),
        og_title=meta.get("og_title", "Links"),
        og_description=meta.get("og_description", ""),
        og_image=f"{SITE_URL}{meta.get('og_image', '/assets/og-image.png')}",
        og_type="website",
        canonical_url=f"{SITE_URL}/links",
        content=content_html,
    )
    
    links_dir = OUTPUT / "links"
    links_dir.mkdir(exist_ok=True)
    (links_dir / "index.html").write_text(html, encoding="utf-8")
    print("✓ Built links/index.html")


def build_wegoch():
    """Build all weg pages."""
    wegoch_dir = CONTENT / "wegoch"
    if not wegoch_dir.exists():
        return []
    
    works = []
    template = read_template("work.html")
    output_base = OUTPUT / "wegoch"
    output_base.mkdir(exist_ok=True)
    
    for md_file in wegoch_dir.glob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(content)
        
        # Extract date
        date_str = meta.get("date", "")
        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d")
        
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            date = datetime.now()
        
        slug = md_file.stem
        url = f"/wegoch/{slug}"
        
        content_html = render_markdown(body)
        
        html = render_template(
            template,
            title=meta.get("title", slug.replace("-", " ").title()),
            description=meta.get("description", ""),
            keywords=meta.get("keywords", ""),
            og_title=meta.get("og_title", meta.get("title", "")),
            og_description=meta.get("og_description", meta.get("description", "")),
            og_image=f"{SITE_URL}{meta.get('og_image', '/assets/og-image.png')}",
            og_type="article",
            canonical_url=f"{SITE_URL}{url}",
            date=date_str,
            date_formatted=date.strftime("%B {0}, %Y").format(date.day),
            content=content_html,
            back_url="/wegoch",
            back_label="Back to Wegoch",
        )
        
        work_dir = output_base / slug
        work_dir.mkdir(exist_ok=True)
        (work_dir / "index.html").write_text(html, encoding="utf-8")
        
        works.append({
            "title": meta.get("title", slug.replace("-", " ").title()),
            "url": url,
            "slug": slug,
            "type": "weg",
            "date": date,
            "date_formatted": date.strftime("%B %d, %Y"),
            "date_humanized": humanize_date(date),
        })
    
    # Sort by date descending
    works.sort(key=lambda x: x["date"], reverse=True)
    
    if works:
        print(f"✓ Built {len(works)} weg pages")
    return works


def build_getem():
    """Build all poem pages."""
    getem_dir = CONTENT / "getem"
    if not getem_dir.exists():
        return []
    
    works = []
    template = read_template("work.html")
    output_base = OUTPUT / "getem"
    output_base.mkdir(exist_ok=True)
    
    for md_file in getem_dir.glob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(content)
        
        # Extract date
        date_str = meta.get("date", "")
        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d")
        
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            date = datetime.now()
        
        slug = md_file.stem
        url = f"/getem/{slug}"
        
        content_html = render_markdown(body)
        
        html = render_template(
            template,
            title=meta.get("title", slug.replace("-", " ").title()),
            description=meta.get("description", ""),
            keywords=meta.get("keywords", ""),
            og_title=meta.get("og_title", meta.get("title", "")),
            og_description=meta.get("og_description", meta.get("description", "")),
            og_image=f"{SITE_URL}{meta.get('og_image', '/assets/og-image.png')}",
            og_type="article",
            canonical_url=f"{SITE_URL}{url}",
            date=date_str,
            date_formatted=date.strftime("%B {0}, %Y").format(date.day),
            content=content_html,
            back_url="/getem",
            back_label="Back to Getem",
        )
        
        work_dir = output_base / slug
        work_dir.mkdir(exist_ok=True)
        (work_dir / "index.html").write_text(html, encoding="utf-8")
        
        works.append({
            "title": meta.get("title", slug.replace("-", " ").title()),
            "url": url,
            "slug": slug,
            "type": "poem",
            "date": date,
            "date_formatted": date.strftime("%B %d, %Y"),
            "date_humanized": humanize_date(date),
        })
    
    # Sort by date descending
    works.sort(key=lambda x: x["date"], reverse=True)
    
    if works:
        print(f"✓ Built {len(works)} poem pages")
    return works


def parse_geez_content(content: str) -> dict:
    """Parse Ge'ez content sections (geez:, meaning:, reference:, ማስታወሻ:)."""
    result = {"geez": "", "meaning": "", "reference": "", "memorial": ""}
    current_section = None
    
    for line in content.split("\n"):
        line_stripped = line.strip()
        if line_stripped.startswith("geez:"):
            current_section = "geez"
            # Get content after geez: if on same line
            after = line_stripped[5:].strip()
            if after:
                result["geez"] = after
        elif line_stripped.startswith("meaning:"):
            current_section = "meaning"
            after = line_stripped[8:].strip()
            if after:
                result["meaning"] = after
        elif line_stripped.startswith("reference:"):
            current_section = "reference"
            after = line_stripped[10:].strip()
            if after:
                result["reference"] = after
        elif line_stripped.startswith("ማስታወሻ:"):
            current_section = "memorial"
            after = line_stripped[7:].strip()
            if after:
                result["memorial"] = after
        elif current_section and line_stripped:
            if result[current_section]:
                result[current_section] += "\n" + line_stripped
            else:
                result[current_section] = line_stripped
    
    return result


def build_geez():
    """Build all Ge'ez qine pages (hidden SEO pages)."""
    geez_dir = CONTENT / "geez"
    if not geez_dir.exists():
        return []
    
    works = []
    template = read_template("geez.html")
    output_base = OUTPUT / "geez"
    output_base.mkdir(exist_ok=True)
    
    for md_file in geez_dir.glob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(content)
        
        # Parse the special Ge'ez content format
        geez_content = parse_geez_content(body)
        
        slug = md_file.stem
        url = f"/geez/{slug}"
        
        # Format Ge'ez text with line breaks
        geez_text_html = ""
        for line in geez_content["geez"].split("\n"):
            if line.strip():
                geez_text_html += f'<span class="line">{line.strip()}</span>\n'
        
        # Format meaning section with line breaks
        meaning_section = ""
        if geez_content["meaning"]:
            meaning_lines = ""
            for line in geez_content["meaning"].split("\n"):
                if line.strip():
                    meaning_lines += f'<span class="line">{line.strip()}</span>\n'
            meaning_section = f'''
            <div class="geez-separator"></div>
            <div class="geez-meaning">
              {meaning_lines}
            </div>'''
        
        # Format reference section
        reference_section = ""
        if geez_content["reference"]:
            reference_section = f'''
            <div class="geez-reference">
              {geez_content["reference"]}
            </div>'''
        
        # Format memorial section (ማስታወሻ)
        memorial_section = ""
        if geez_content["memorial"]:
            memorial_section = f'''
            <div class="geez-memorial">
              <span class="memorial-label">ማስታወሻ:</span> {geez_content["memorial"]}
            </div>'''
        
        html = render_template(
            template,
            title=meta.get("title", slug.replace("-", " ").title()),
            title_transliterated=meta.get("title_transliterated", ""),
            description=meta.get("description", ""),
            keywords=meta.get("keywords", ""),
            og_title=meta.get("og:title", meta.get("title", "")),
            og_description=meta.get("og:description", meta.get("description", "")),
            og_image=f"{SITE_URL}{meta.get('og:image', '/assets/og-image.png')}",
            canonical_url=f"{SITE_URL}{url}",
            geez_text=geez_text_html,
            meaning_section=meaning_section,
            reference_section=reference_section,
            memorial_section=memorial_section,
        )
        
        work_dir = output_base / slug
        work_dir.mkdir(exist_ok=True)
        (work_dir / "index.html").write_text(html, encoding="utf-8")
        
        works.append({
            "title": meta.get("title", slug.replace("-", " ").title()),
            "title_transliterated": meta.get("title_transliterated", ""),
            "url": url,
            "slug": slug,
            "type": "geez",
        })
    
    if works:
        print(f"✓ Built {len(works)} Ge'ez pages")
    return works


def build_cs():
    """Build all CS (Computer Science) articles."""
    cs_dir = CONTENT / "cs"
    if not cs_dir.exists():
        return []
    
    articles = []
    template = read_template("cs.html")
    output_base = OUTPUT / "cs"
    output_base.mkdir(exist_ok=True)
    
    for md_file in cs_dir.glob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(content)
        
        # Extract date
        date_str = meta.get("date", "")
        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d")
        
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            date = datetime.now()
        
        slug = md_file.stem
        url = f"/cs/{slug}"
        
        # For CS articles, render markdown (which preserves HTML blocks)
        content_html = render_markdown(body)
        
        html = render_template(
            template,
            title=meta.get("title", slug.replace("-", " ").title()),
            description=meta.get("description", ""),
            keywords=meta.get("keywords", ""),
            og_title=meta.get("og_title", meta.get("title", "")),
            og_description=meta.get("og_description", meta.get("description", "")),
            og_image=f"{SITE_URL}{meta.get('og_image', '/assets/og-image.png')}",
            canonical_url=f"{SITE_URL}{url}",
            date=date_str,
            date_formatted=date.strftime("%B {0}, %Y").format(date.day),
            content=content_html,
        )
        
        article_dir = output_base / slug
        article_dir.mkdir(exist_ok=True)
        (article_dir / "index.html").write_text(html, encoding="utf-8")
        
        articles.append({
            "title": meta.get("title", slug.replace("-", " ").title()),
            "url": url,
            "slug": slug,
            "date": date,
            "date_formatted": date.strftime("%B %d, %Y"),
            "date_humanized": humanize_date(date),
            "description": meta.get("description", ""),
            "type": "cs",
        })
    
    # Sort by date descending
    articles.sort(key=lambda x: x["date"], reverse=True)
    
    if articles:
        print(f"✓ Built {len(articles)} CS articles")
    return articles


def build_works_index(works: list[dict], section: str, config: dict):
    """Build index page for a works section (geez, getem, wegoch)."""
    if not works:
        return
    
    template = read_template("works-index.html")
    output_dir = OUTPUT / section
    output_dir.mkdir(exist_ok=True)
    
    # Check if this section should show dates
    show_dates = config.get("show_dates", False)
    
    # Build the list HTML
    list_html = '<ul class="works-list">\n'
    for work in works:
        title = work.get("title", work["slug"])
        transliterated = work.get("title_transliterated", "")
        trans_html = f'<span class="work-transliterated">{transliterated}</span>' if transliterated else ""
        
        # Date display for sections that support it
        date_html = ""
        if show_dates and work.get("date"):
            date_formatted = work.get("date_formatted", "")
            date_humanized = work.get("date_humanized", "")
            date_html = f'''
      <span class="work-date">
        <time datetime="{work["date"].strftime("%Y-%m-%d")}" title="{date_formatted}">{date_humanized}</time>
      </span>'''
        
        list_html += f'''  <li>
    <a href="{work["url"]}">
      <span class="work-title">{title}</span>
      {trans_html}{date_html}
    </a>
  </li>\n'''
    list_html += '</ul>\n'
    list_html += f'<p class="works-count">{len(works)} {config["count_label"]}</p>'
    
    html = render_template(
        template,
        lang=config.get("lang", "am"),
        title=config["title"],
        title_ethiopic=config["title_ethiopic"],
        subtitle=config["subtitle"],
        description=config["description"],
        keywords=config["keywords"],
        og_title=config["og_title"],
        og_description=config["og_description"],
        og_image=f"{SITE_URL}/assets/og-{section}.png",
        canonical_url=f"{SITE_URL}/{section}",
        content=list_html,
    )
    
    (output_dir / "index.html").write_text(html, encoding="utf-8")
    print(f"✓ Built {section}/index.html")


def build_404():
    """Build the 404 page."""
    content_html = '''
        <section class="error-page">
            <h1>404</h1>
            <p>Page not found</p>
            <a href="/">← Back to home</a>
        </section>
    '''
    
    template = read_template("base.html")
    html = render_template(
        template,
        title="404 - Page Not Found",
        description="Page not found",
        keywords="",
        og_title="404 - Page Not Found",
        og_description="The page you're looking for doesn't exist.",
        og_image=f"{SITE_URL}/assets/og-404.png",
        og_type="website",
        canonical_url=SITE_URL,
        content=content_html,
    )
    
    (OUTPUT / "404.html").write_text(html, encoding="utf-8")
    print("✓ Built 404.html")


def copy_static():
    """Copy static assets."""
    # Copy CSS
    css_out = OUTPUT / "css"
    css_out.mkdir(exist_ok=True)
    for css_file in CSS.glob("*.css"):
        shutil.copy(css_file, css_out / css_file.name)
    print("✓ Copied CSS files")
    
    # Copy assets (fonts, images, etc.)
    assets_out = OUTPUT / "assets"
    if ASSETS.exists():
        shutil.copytree(ASSETS, assets_out, dirs_exist_ok=True)
        print("✓ Copied assets")
    
    # Copy CNAME
    cname = ROOT / "CNAME"
    if cname.exists():
        shutil.copy(cname, OUTPUT / "CNAME")
        print("✓ Copied CNAME")
    
    # Copy robots.txt
    robots = ROOT / "docs" / "robots.txt"
    if robots.exists():
        shutil.copy(robots, OUTPUT / "robots.txt")
        print("✓ Copied robots.txt")
    
    # Copy OG images from blog
    blog_out = OUTPUT / "blog"
    blog_out.mkdir(exist_ok=True)
    for og_file in BLOG.glob("og-*.png"):
        shutil.copy(og_file, blog_out / og_file.name)
    for og_file in BLOG.glob("og-*.svg"):
        shutil.copy(og_file, blog_out / og_file.name)
    print("✓ Copied blog OG images")
    
    # Copy wegoch images (misloch)
    wegoch_misloch = CONTENT / "wegoch" / "misloch"
    if wegoch_misloch.exists():
        wegoch_out = OUTPUT / "wegoch" / "misloch"
        wegoch_out.mkdir(parents=True, exist_ok=True)
        for img_file in wegoch_misloch.glob("*"):
            if img_file.is_file():
                shutil.copy(img_file, wegoch_out / img_file.name)
        print("✓ Copied wegoch images")
    
    # Copy getem images (misloch)
    getem_misloch = CONTENT / "getem" / "misloch"
    if getem_misloch.exists():
        getem_out = OUTPUT / "getem" / "misloch"
        getem_out.mkdir(parents=True, exist_ok=True)
        for img_file in getem_misloch.glob("*"):
            if img_file.is_file():
                shutil.copy(img_file, getem_out / img_file.name)
        print("✓ Copied getem images")


def generate_sitemap(posts: list[dict], wegs: list[dict], poems: list[dict], geez_pages: list[dict], cs_articles: list[dict]):
    """Generate sitemap.xml."""
    urls = [
        (SITE_URL, "1.0"),
        (f"{SITE_URL}/projects", "0.8"),
        (f"{SITE_URL}/blog", "0.9"),
        (f"{SITE_URL}/resume", "0.7"),
        (f"{SITE_URL}/links", "0.6"),
    ]
    
    # Add index pages for works sections
    if wegs:
        urls.append((f"{SITE_URL}/wegoch", "0.7"))
    if poems:
        urls.append((f"{SITE_URL}/getem", "0.7"))
    if geez_pages:
        urls.append((f"{SITE_URL}/geez", "0.8"))
    if cs_articles:
        urls.append((f"{SITE_URL}/cs", "0.8"))
    
    for post in posts:
        urls.append((f"{SITE_URL}{post['url']}", "0.6"))
    
    for weg in wegs:
        urls.append((f"{SITE_URL}{weg['url']}", "0.6"))
    
    for poem in poems:
        urls.append((f"{SITE_URL}{poem['url']}", "0.6"))
    
    # Ge'ez pages are SEO-focused so give them higher priority
    for geez in geez_pages:
        urls.append((f"{SITE_URL}{geez['url']}", "0.8"))
    
    # CS articles
    for article in cs_articles:
        urls.append((f"{SITE_URL}{article['url']}", "0.7"))
    
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for url, priority in urls:
        sitemap += f'''  <url>
    <loc>{url}</loc>
    <priority>{priority}</priority>
  </url>\n'''
    
    sitemap += '</urlset>'
    
    (OUTPUT / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    print("✓ Generated sitemap.xml")


def generate_og_images():
    """Try to generate OG images for blog posts without them."""
    try:
        import sys
        sys.path.insert(0, str(ROOT / "scripts"))
        from generate_og_images import main as og_main
        print("🖼️  Generating OG images...")
        og_main()
    except ImportError as e:
        print(f"⚠️  OG generation skipped (missing dependency: {e})")
    except Exception as e:
        print(f"⚠️  OG generation failed: {e}")


def main():
    """Build the site."""
    print("\n🔨 Building site...\n")
    
    # Try to generate OG images first
    generate_og_images()
    print()
    
    # Clean output directory
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir()
    
    # Get blog posts
    posts = get_blog_posts()
    print(f"📝 Found {len(posts)} blog posts\n")
    
    # Build pages
    build_home(posts)
    build_blog_index(posts)
    build_blog_posts(posts)
    build_projects()
    build_resume()
    build_links()
    wegs = build_wegoch()
    poems = build_getem()
    geez_pages = build_geez()
    cs_articles = build_cs()
    
    # Build index pages for works sections
    build_works_index(wegs, "wegoch", {
        "lang": "am",
        "title": "ወጎች - Wegs",
        "title_ethiopic": "ወጎች",
        "subtitle": "Short stories and reflections in Amharic",
        "description": "Collection of Ethiopian short stories (ወግ) and reflections written in Amharic by Esubalew Chekol.",
        "keywords": "ወግ, ወጎች, Amharic stories, Ethiopian literature, short stories, Esubalew Chekol",
        "og_title": "ወጎች - Ethiopian Short Stories",
        "og_description": "Amharic short stories and reflections",
        "count_label": "ወጎች",
        "show_dates": True,
    })
    
    build_works_index(poems, "getem", {
        "lang": "am",
        "title": "ግጥሞች - Poems",
        "title_ethiopic": "ግጥሞች",
        "subtitle": "Poetry in Amharic",
        "description": "Collection of Ethiopian poems (ግጥም) written in Amharic by Esubalew Chekol.",
        "keywords": "ግጥም, ግጥሞች, Amharic poetry, Ethiopian poetry, poems, Esubalew Chekol",
        "og_title": "ግጥሞች - Ethiopian Poetry",
        "og_description": "Amharic poems and verses",
        "count_label": "ግጥሞች",
        "show_dates": True,
    })
    
    build_works_index(geez_pages, "geez", {
        "lang": "gez",
        "title": "ግእዝ - Ge'ez",
        "title_ethiopic": "ግእዝ",
        "subtitle": "Sacred texts and qine in Ge'ez",
        "description": "Collection of Ethiopian Orthodox Ge'ez sacred texts, qine (poetry), and liturgical verses with Amharic translations.",
        "keywords": "ግእዝ, Ge'ez, ቅኔ, qine, Ethiopian Orthodox, sacred texts, liturgy, Ethiopic",
        "og_title": "ግእዝ - Ethiopian Sacred Texts",
        "og_description": "Ge'ez qine and sacred verses with translations",
        "count_label": "ቅኔዎች",
    })
    
    build_works_index(cs_articles, "cs", {
        "lang": "en",
        "title": "CS - Computer Science",
        "title_ethiopic": "CS",
        "subtitle": "Technical articles, reviews, and explorations",
        "description": "Computer Science articles, software reviews, and technical explorations by Esubalew Chekol.",
        "keywords": "Computer Science, programming, software engineering, technical articles, code review, Esubalew Chekol",
        "og_title": "CS - Computer Science Articles",
        "og_description": "Technical articles and software explorations",
        "count_label": "articles",
        "show_dates": True,
    })
    
    build_404()
    
    # Copy static files
    print()
    copy_static()
    
    # Generate sitemap
    generate_sitemap(posts, wegs, poems, geez_pages, cs_articles)
    
    print("\n✨ Site built successfully!")
    print(f"   Output: {OUTPUT}\n")


if __name__ == "__main__":
    main()

