"""HTML helper functions for rich content formatting."""


def styled_header(text: str, level: int = 1) -> str:
    """Create a styled header.
    
    Args:
        text: Header text
        level: Header level (1-6)
        
    Returns:
        HTML string
    """
    return f"<h{level}>{text}</h{level}>"


def styled_paragraph(text: str, bold: bool = False, italic: bool = False) -> str:
    """Create a styled paragraph.
    
    Args:
        text: Paragraph text
        bold: Make text bold
        italic: Make text italic
        
    Returns:
        HTML string
    """
    if bold:
        text = f"<strong>{text}</strong>"
    if italic:
        text = f"<em>{text}</em>"
    return f"<p>{text}</p>"


def styled_list(items: list, ordered: bool = False) -> str:
    """Create a styled list.
    
    Args:
        items: List of items
        ordered: Use ordered list (numbered) instead of unordered (bullets)
        
    Returns:
        HTML string
    """
    tag = "ol" if ordered else "ul"
    list_items = "".join([f"<li>{item}</li>" for item in items])
    return f"<{tag}>{list_items}</{tag}>"


def alert_box(message: str, alert_type: str = "info") -> str:
    """Create a styled alert box.
    
    Args:
        message: Alert message
        alert_type: Type of alert (info, warning, error, success)
        
    Returns:
        HTML string
    """
    colors = {
        "info": "#d1ecf1",
        "warning": "#fff3cd",
        "error": "#f8d7da",
        "success": "#d4edda"
    }
    
    bg_color = colors.get(alert_type, colors["info"])
    
    return f"""
    <div style="padding: 15px; margin: 10px 0; border-radius: 5px; background-color: {bg_color}; border-left: 5px solid #0c5460;">
        {message}
    </div>
    """


def create_link(text: str, url: str) -> str:
    """Create an HTML link.
    
    Args:
        text: Link text
        url: Link URL
        
    Returns:
        HTML string
    """
    return f'<a href="{url}" target="_blank">{text}</a>'


def format_code(code: str, language: str = "python") -> str:
    """Format code block.
    
    Args:
        code: Code content
        language: Programming language
        
    Returns:
        HTML string
    """
    return f'<pre><code class="language-{language}">{code}</code></pre>'


def create_table(headers: list, rows: list) -> str:
    """Create an HTML table.
    
    Args:
        headers: List of header strings
        rows: List of rows, where each row is a list of cell values
        
    Returns:
        HTML string
    """
    header_html = "<tr>" + "".join([f"<th>{h}</th>" for h in headers]) + "</tr>"
    
    rows_html = ""
    for row in rows:
        rows_html += "<tr>" + "".join([f"<td>{cell}</td>" for cell in row]) + "</tr>"
    
    return f"""
    <table style="border-collapse: collapse; width: 100%;">
        <thead style="background-color: #f0f0f0;">
            {header_html}
        </thead>
        <tbody>
            {rows_html}
        </tbody>
    </table>
    """
