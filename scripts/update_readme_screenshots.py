#!/usr/bin/env python3
"""
Helper script to update README.md with screenshot references
Can be used standalone or called from capture-screenshots scripts
"""

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
README_PATH = PROJECT_ROOT / "README.md"
SCREENSHOT_DIR = PROJECT_ROOT / "docs" / "assets" / "screenshots"

def update_readme():
    """Update README.md with screenshot references."""
    if not README_PATH.exists():
        print("Error: README.md not found")
        return False
    
    # Read README
    with open(README_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find existing screenshots
    screenshot_files = []
    if SCREENSHOT_DIR.exists():
        for file in SCREENSHOT_DIR.glob("*.png"):
            screenshot_files.append(file)
    
    if not screenshot_files:
        print("No screenshots found. Run capture-screenshots script first.")
        return False
    
    # Create screenshots section
    screenshots_section = "## 📸 Screenshots\n\n"
    
    # Sort screenshots by name
    screenshot_files.sort()
    
    for i, filepath in enumerate(screenshot_files, 1):
        rel_path = filepath.relative_to(PROJECT_ROOT)
        if "main-window" in filepath.name.lower():
            screenshots_section += f"![md2office GUI Main Window]({rel_path})\n\n"
        elif "file-selected" in filepath.name.lower():
            screenshots_section += f"![md2office GUI with File Selected]({rel_path})\n\n"
        else:
            screenshots_section += f"![md2office GUI Screenshot {i}]({rel_path})\n\n"
    
    screenshots_section += "\n"
    
    # Remove existing screenshots section if present
    content = re.sub(
        r'## 📸 Screenshots.*?(?=\n## |$)',
        '',
        content,
        flags=re.DOTALL
    )
    
    # Insert before Quick Start section
    if "## 🚀 Quick Start" in content:
        content = content.replace(
            "## 🚀 Quick Start",
            screenshots_section + "## 🚀 Quick Start"
        )
    else:
        # If no Quick Start section, add after Features
        if "## ✨ Features" in content:
            # Find end of Features section
            features_end = content.find("## 🚀", content.find("## ✨ Features"))
            if features_end == -1:
                features_end = content.find("\n\n", content.find("## ✨ Features"))
            if features_end != -1:
                content = content[:features_end] + "\n\n" + screenshots_section + content[features_end:]
            else:
                # Fallback: append at end
                content += "\n\n" + screenshots_section
    
    # Write back
    with open(README_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ README.md updated with {len(screenshot_files)} screenshot(s)")
    return True

if __name__ == "__main__":
    update_readme()

