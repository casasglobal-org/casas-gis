from string import Template

DEFAULT_TEMPLATE = "template.html"
DEFAULT_RESULT_FILE = "result.html"


def generate_html_file(template=DEFAULT_TEMPLATE, output=DEFAULT_RESULT_FILE):
    with open(template) as f, open(output, "w") as g:
        template = Template(f.read())
        output = template.substitute(
            title="my title",
            subtitle="my subtitle",
            cmd="python ...",
            link="https",
            img="image.png",
        )
        g.write(output)


if __name__ == "__main__":
    generate_html_file()
