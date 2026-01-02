def build_prompt(structure):
    return f"""
Generate a modern website layout using:
- Flask
- Jinja Templates
- Tailwind CSS
- Bootstrap if needed
- Minimal JS

Website structure:
Header: {structure['header']}
Navigation: {structure['nav']}
Number of Sections: {structure['sections']}
Main Content: {structure['main']}
Footer: {structure['footer']}

Return:
1. base.html
2. index.html
3. Tailwind classes
4. Optional JS
"""
