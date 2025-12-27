"""
Markdown Viewer Widget

Displays markdown content with Mermaid.js diagram support using QWebEngineView.
"""

import re
from pathlib import Path
from typing import Optional
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QFont

# Try to import QWebEngineView, handle gracefully if not available
try:
    from PySide6.QtWebEngineWidgets import QWebEngineView
    WEBENGINE_AVAILABLE = True
except ImportError:
    WEBENGINE_AVAILABLE = False
    # Create a dummy class for type hints
    class QWebEngineView:
        def __init__(self, *args, **kwargs):
            raise ImportError(
                "QWebEngineView is not available. "
                "Please install PySide6-QtWebEngine package:\n"
                "  pip install PySide6-QtWebEngine"
            )


class MarkdownViewer(QWidget):
    """
    Widget for displaying markdown content with Mermaid.js support.
    
    Uses QWebEngineView to render HTML generated from markdown,
    with Mermaid.js integration for diagram rendering.
    """
    
    def __init__(self, parent=None):
        """Initialize markdown viewer."""
        super().__init__(parent)
        
        # Check if QWebEngineView is available
        if not WEBENGINE_AVAILABLE:
            self._show_error("QWebEngineView is not available. Please install PySide6-QtWebEngine.")
            return
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Create web view for rendering HTML
        try:
            self.web_view = QWebEngineView(self)
            layout.addWidget(self.web_view)
        except Exception as e:
            self._show_error(f"Failed to initialize QWebEngineView: {str(e)}")
            return
        
        # Status label for errors/loading
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setVisible(False)
        self.status_label.setStyleSheet("background-color: #f0f0f0; padding: 8px;")
        layout.addWidget(self.status_label)
        
        # Initialize with empty content
        self.set_markdown("")
    
    def _show_error(self, message: str):
        """Show error message when QWebEngineView is not available."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        error_label = QLabel(message)
        error_label.setWordWrap(True)
        error_label.setStyleSheet("color: red; padding: 10px;")
        layout.addWidget(error_label)
    
    def set_markdown(self, markdown_content: str, base_path: Optional[Path] = None):
        """
        Set markdown content to display.
        
        Args:
            markdown_content: Raw markdown text
            base_path: Base path for resolving relative image URLs
        """
        if not WEBENGINE_AVAILABLE or not hasattr(self, 'web_view'):
            return
        
        try:
            html = self._markdown_to_html(markdown_content, base_path)
            self.web_view.setHtml(html)
            self.status_label.setVisible(False)
        except Exception as e:
            error_msg = f"Error rendering markdown: {str(e)}"
            self.status_label.setText(error_msg)
            self.status_label.setVisible(True)
            if hasattr(self, 'web_view'):
                self.web_view.setHtml(f"<html><body><p style='color: red;'>{error_msg}</p></body></html>")
    
    def set_markdown_file(self, file_path: Path):
        """
        Load and display markdown from file.
        
        Args:
            file_path: Path to markdown file
        """
        if not WEBENGINE_AVAILABLE or not hasattr(self, 'web_view'):
            return
        
        try:
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            content = file_path.read_text(encoding='utf-8')
            self.set_markdown(content, base_path=file_path.parent)
        except Exception as e:
            error_msg = f"Error loading file: {str(e)}"
            self.status_label.setText(error_msg)
            self.status_label.setVisible(True)
            if hasattr(self, 'web_view'):
                self.web_view.setHtml(f"<html><body><p style='color: red;'>{error_msg}</p></body></html>")
    
    def _markdown_to_html(self, markdown_content: str, base_path: Optional[Path] = None) -> str:
        """
        Convert markdown to HTML with Mermaid.js support.
        
        Args:
            markdown_content: Raw markdown text
            base_path: Base path for resolving relative image URLs
            
        Returns:
            Complete HTML document as string
        """
        # Pre-process: Extract Mermaid blocks and replace with HTML comments
        # HTML comments survive markdown processing and can be easily found
        mermaid_blocks = []
        mermaid_pattern = r'```\s*mermaid\s*\n(.*?)```'
        
        def extract_mermaid(match):
            diagram_code = match.group(1).strip()
            block_id = len(mermaid_blocks)
            mermaid_blocks.append(diagram_code)
            # Use HTML comment as placeholder - survives markdown processing
            return f"<!-- MERMAID_BLOCK_{block_id} -->"
        
        # Extract all Mermaid blocks first (case-insensitive)
        processed_content = re.sub(mermaid_pattern, extract_mermaid, markdown_content, flags=re.DOTALL | re.IGNORECASE)
        
        # Try to import markdown library
        try:
            import markdown
            # Use extensions for better markdown support
            extensions = ['fenced_code', 'tables', 'nl2br', 'toc']
            try:
                # Try to add codehilite if available
                extensions.append('codehilite')
            except:
                pass
            
            md = markdown.Markdown(extensions=extensions)
            html_body = md.convert(processed_content)
        except ImportError:
            # Fallback to basic markdown conversion if library not available
            html_body = self._basic_markdown_to_html(processed_content)
        
        # Restore Mermaid blocks as divs
        # Replace HTML comment placeholders with actual Mermaid divs
        import hashlib
        for i, diagram_code in enumerate(mermaid_blocks):
            placeholder_comment = f"<!-- MERMAID_BLOCK_{i} -->"
            diagram_id = f"mermaid-{hashlib.md5(diagram_code.encode()).hexdigest()[:8]}"
            mermaid_div = f'<div class="mermaid" id="{diagram_id}">{diagram_code}</div>'
            
            # Replace the HTML comment with the Mermaid div
            html_body = html_body.replace(placeholder_comment, mermaid_div)
        
        # Process any remaining Mermaid blocks that might have been missed
        html_body = self._process_mermaid_blocks(html_body)
        
        # Process image paths to resolve relative URLs
        if base_path:
            html_body = self._process_image_paths(html_body, base_path)
        
        # Build complete HTML document
        html = self._build_html_document(html_body, base_path)
        
        return html
    
    def _process_image_paths(self, html_content: str, base_path: Path) -> str:
        """
        Process image paths in HTML to resolve relative URLs.
        
        Args:
            html_content: HTML content with image tags
            base_path: Base path for resolving relative image URLs
            
        Returns:
            HTML with resolved image paths
        """
        # Pattern to match img tags with src attribute
        pattern = r'<img\s+([^>]*src=["\']([^"\']+)["\'][^>]*)>'
        
        def resolve_image_path(match):
            full_tag = match.group(1)
            src_path = match.group(2)
            
            # Skip if already absolute URL (http/https)
            if src_path.startswith(('http://', 'https://', 'data:')):
                return f'<img {full_tag}>'
            
            # Resolve relative path
            image_path = Path(src_path)
            if not image_path.is_absolute():
                resolved_path = (base_path / image_path).resolve()
            else:
                resolved_path = image_path.resolve()
            
            # Convert to file:// URL for QWebEngineView
            if resolved_path.exists():
                file_url = QUrl.fromLocalFile(str(resolved_path)).toString()
                # Replace src in the tag
                new_tag = re.sub(r'src=["\'][^"\']+["\']', f'src="{file_url}"', full_tag)
                return f'<img {new_tag}>'
            else:
                # Image not found - add error styling
                new_tag = re.sub(
                    r'src=["\'][^"\']+["\']',
                    f'src="data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'400\' height=\'100\'%3E%3Ctext x=\'10\' y=\'50\' fill=\'red\'%3EImage not found: {src_path}%3C/text%3E%3C/svg%3E"',
                    full_tag
                )
                return f'<img {new_tag} style="border: 1px dashed #ccc;">'
        
        html_content = re.sub(pattern, resolve_image_path, html_content)
        return html_content
    
    
    def _basic_markdown_to_html(self, markdown_content: str) -> str:
        """
        Basic markdown to HTML conversion without external libraries.
        
        This is a fallback implementation for basic markdown syntax.
        """
        html = markdown_content
        
        # Headings
        html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        
        # Bold
        html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
        
        # Italic
        html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
        
        # Code blocks (preserve for Mermaid processing)
        html = re.sub(
            r'```(\w+)?\n(.*?)```',
            r'<pre><code class="language-\1">\2</code></pre>',
            html,
            flags=re.DOTALL
        )
        
        # Inline code
        html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
        
        # Paragraphs (wrap consecutive lines)
        paragraphs = html.split('\n\n')
        html = '\n'.join([f'<p>{p.strip()}</p>' if p.strip() and not p.strip().startswith('<') else p for p in paragraphs])
        
        # Line breaks
        html = html.replace('\n', '<br>\n')
        
        return html
    
    def _process_mermaid_blocks(self, html_content: str) -> str:
        """
        Process Mermaid code blocks and convert them for Mermaid.js rendering.
        
        Args:
            html_content: HTML content with code blocks
            
        Returns:
            HTML with Mermaid blocks converted to div elements
        """
        import hashlib
        
        # Pattern to match code blocks - handle multiple formats:
        # 1. <pre><code class="language-mermaid">...</code></pre>
        # 2. <pre><code class="language-mermaid" data-language="mermaid">...</code></pre>
        # 3. <pre><code>...</code></pre> (for heuristic detection)
        # Use a more flexible pattern that handles whitespace variations
        pattern = r'<pre><code(?:\s+[^>]*class="[^"]*language-([Mm]ermaid)[^"]*"[^>]*)?\s*>(.*?)</code></pre>'
        
        def replace_mermaid(match):
            lang = match.group(1)
            diagram_code = match.group(2)
            
            # Clean up HTML entities
            diagram_code = diagram_code.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
            # Remove leading/trailing whitespace and newlines
            diagram_code = diagram_code.strip()
            
            # If language is explicitly mermaid, use it
            if lang and lang.lower() == 'mermaid':
                if not diagram_code:
                    return match.group(0)  # Return original if empty
                
                # Generate unique ID for this diagram
                diagram_id = f"mermaid-{hashlib.md5(diagram_code.encode()).hexdigest()[:8]}"
                
                # Replace with Mermaid div (preserve whitespace)
                return f'<div class="mermaid" id="{diagram_id}">{diagram_code}</div>'
            
            # Check if it's a mermaid diagram by content (heuristic)
            # Only apply heuristic if no language was specified
            if not lang and diagram_code:
                mermaid_keywords = ['graph', 'flowchart', 'sequenceDiagram', 'classDiagram', 
                                   'stateDiagram', 'stateDiagram-v2', 'erDiagram', 'gantt', 
                                   'pie', 'gitgraph', 'journey', 'mindmap', 'C4Context', 
                                   'quadrantChart', 'requirement', 'timeline']
                
                first_line = diagram_code.split('\n')[0].strip()
                # Check if first line starts with a mermaid keyword
                if any(first_line.startswith(keyword) for keyword in mermaid_keywords):
                    diagram_id = f"mermaid-{hashlib.md5(diagram_code.encode()).hexdigest()[:8]}"
                    return f'<div class="mermaid" id="{diagram_id}">{diagram_code}</div>'
            
            return match.group(0)  # Return original if not mermaid
        
        # Replace mermaid code blocks (non-greedy match, case-insensitive)
        html_content = re.sub(pattern, replace_mermaid, html_content, flags=re.DOTALL | re.IGNORECASE)
        
        return html_content
    
    def _build_html_document(self, body_content: str, base_path: Optional[Path] = None) -> str:
        """
        Build complete HTML document with Mermaid.js integration.
        
        Args:
            body_content: HTML body content
            base_path: Base path for resolving resources
            
        Returns:
            Complete HTML document
        """
        # Mermaid.js CDN (using latest stable version)
        mermaid_js = "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"
        # Highlight.js CDN for syntax highlighting
        highlight_js = "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"
        highlight_css = "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/default.min.css"
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Markdown Preview</title>
    <link rel="stylesheet" href="{highlight_css}">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
            background-color: #fff;
        }}
        h1 {{ font-size: 2em; margin-top: 0.67em; margin-bottom: 0.67em; }}
        h2 {{ font-size: 1.5em; margin-top: 0.83em; margin-bottom: 0.83em; }}
        h3 {{ font-size: 1.17em; margin-top: 1em; margin-bottom: 1em; }}
        h4 {{ font-size: 1em; margin-top: 1.33em; margin-bottom: 1.33em; }}
        h5 {{ font-size: 0.83em; margin-top: 1.67em; margin-bottom: 1.67em; }}
        h6 {{ font-size: 0.67em; margin-top: 2.33em; margin-bottom: 2.33em; }}
        p {{ margin: 1em 0; }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: "Courier New", monospace;
            font-size: 0.9em;
        }}
        pre {{
            background-color: #f4f4f4;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
            border: 1px solid #ddd;
        }}
        pre code {{
            background-color: transparent;
            padding: 0;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 1em 0;
        }}
        table th, table td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        table th {{
            background-color: #f2f2f2;
            font-weight: bold;
        }}
        blockquote {{
            border-left: 4px solid #ddd;
            margin: 1em 0;
            padding-left: 1em;
            color: #666;
        }}
        img {{
            max-width: 100%;
            height: auto;
        }}
        .mermaid {{
            text-align: center;
            margin: 20px 0;
            background-color: #fff;
            min-height: 100px;
        }}
        .mermaid-error {{
            border: 1px solid #ff6b6b;
            background-color: #ffe0e0;
            padding: 10px;
            margin: 20px 0;
            border-radius: 5px;
            color: #c92a2a;
        }}
        .mermaid-error code {{
            background-color: #fff;
            padding: 5px;
            display: block;
            margin-top: 10px;
            font-size: 0.9em;
        }}
        a {{
            color: #0066cc;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        ul, ol {{
            margin: 1em 0;
            padding-left: 2em;
        }}
        li {{
            margin: 0.5em 0;
        }}
        hr {{
            border: none;
            border-top: 1px solid #ddd;
            margin: 2em 0;
        }}
    </style>
    <script src="{highlight_js}"></script>
    <script src="{mermaid_js}"></script>
</head>
<body>
    {body_content}
    <script>
        // Wait for both DOM and scripts to be ready
        (function() {{
            function initMermaid() {{
                // Check if Mermaid is loaded
                if (typeof mermaid === 'undefined') {{
                    console.warn('Mermaid.js not loaded, retrying...');
                    setTimeout(initMermaid, 100);
                    return;
                }}
                
                // Initialize Mermaid.js
                mermaid.initialize({{
                    startOnLoad: false,
                    theme: 'default',
                    securityLevel: 'loose',
                    flowchart: {{
                        useMaxWidth: true,
                        htmlLabels: true
                    }},
                    errorCallback: function(err, hash) {{
                        console.error('Mermaid rendering error:', err);
                        // Find the element and show error
                        const element = document.getElementById(hash);
                        if (element) {{
                            element.innerHTML = '<div class="mermaid-error">' +
                                '<strong>Mermaid Diagram Error:</strong><br>' +
                                (err.message || String(err)).replace(/\\n/g, '<br>') +
                                '<code>' + element.textContent + '</code>' +
                                '</div>';
                        }}
                    }}
                }});
                
                // Render all Mermaid diagrams
                const mermaidElements = document.querySelectorAll('.mermaid');
                console.log('Found', mermaidElements.length, 'Mermaid diagrams');
                if (mermaidElements.length > 0) {{
                    mermaid.run({{
                        nodes: mermaidElements
                    }}).then(function() {{
                        console.log('Mermaid diagrams rendered successfully');
                    }}).catch(function(err) {{
                        console.error('Mermaid run error:', err);
                        // Show error in each diagram element
                        mermaidElements.forEach(function(el) {{
                            if (!el.querySelector('svg')) {{
                                el.innerHTML = '<div class="mermaid-error">' +
                                    '<strong>Mermaid Rendering Failed:</strong><br>' +
                                    (err.message || String(err)) +
                                    '<code>' + el.textContent + '</code>' +
                                    '</div>';
                            }}
                        }});
                    }});
                }}
            }}
            
            function initHighlight() {{
                // Initialize syntax highlighting
                if (typeof hljs !== 'undefined') {{
                    document.querySelectorAll('pre code:not(.mermaid *)').forEach(function(block) {{
                        try {{
                            hljs.highlightElement(block);
                        }} catch (e) {{
                            console.warn('Syntax highlighting failed:', e);
                        }}
                    }});
                }}
            }}
            
            // Initialize when DOM is ready
            if (document.readyState === 'loading') {{
                document.addEventListener('DOMContentLoaded', function() {{
                    initHighlight();
                    initMermaid();
                }});
            }} else {{
                // DOM already loaded
                initHighlight();
                initMermaid();
            }}
        }})();
    </script>
</body>
</html>"""
        
        return html
    
    def clear(self):
        """Clear the viewer content."""
        if hasattr(self, 'web_view'):
            self.web_view.setHtml("")
        self.status_label.setVisible(False)

