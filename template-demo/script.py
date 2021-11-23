from pathlib import Path
from string import Template

DEFAULT_TEMPLATE = Path("template-demo") / "template.html"
DEFAULT_RESULT_FILE = "result.html"


def generate_html_file(template_input_file=DEFAULT_TEMPLATE, template_output_file=DEFAULT_RESULT_FILE, **kwargs):
    with open(template_input_file) as f, open(template_output_file, "w") as g:
        template = Template(f.read())
        output = template.substitute(
            **kwargs,
        )
        g.write(output)


if __name__ == "__main__":
    template_variables = {
        "title": "my title",
        "subtitle": "my subtitle",
        "cmd": "python ...",
        "link": "https",
        "img": "image.png",
    }
    generate_html_file(template_output_file="output-template.html", **template_variables)
