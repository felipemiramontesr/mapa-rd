from jinja2 import Environment, FileSystemLoader
import os
from datetime import datetime

class HTMLRenderer:
    def __init__(self, template_dir="templates"):
        """
        Initialize the Jinja2 environment.
        """
        self.env = Environment(loader=FileSystemLoader(template_dir))
        
    def render(self, data, template_name="report_base.html", output_path=None):
        """
        Render the HTML from data.
        
        Args:
            data (dict): The report data directory.
            template_name (str): The name of the template file.
            output_path (str): Optional path to save the rendered HTML.
            
        Returns:
            str: The rendered HTML string.
        """
        try:
            template = self.env.get_template(template_name)
            rendered_html = template.render(**data)
            
            if output_path:
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(rendered_html)
                    
            return rendered_html
        except Exception as e:
            raise RuntimeError(f"Error rendering HTML: {e}")

if __name__ == "__main__":
    # Test Block
    pass
