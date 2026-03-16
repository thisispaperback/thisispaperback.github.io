import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from markdown import markdown

SITE_TITLE = "paperback"
SITE_DESCRIPTION = ""
SITE_URL = "https://thisispaperback.github.io"
FEED_URL = SITE_URL + "/feed.xml"


def main():
    print(f"Generating {SITE_URL}!")

    output_dir = Path("./out")

    if output_dir.is_dir():
        shutil.rmtree(output_dir)

    output_dir.mkdir()

    static_dir = output_dir.joinpath("static")
    content_dir = Path("./content")
    pages_dir = content_dir.joinpath("pages")
    templates_dir = content_dir.joinpath("templates")
    css_dir = content_dir.joinpath("css")
    images_dir = content_dir.joinpath("images")

    env = Environment(loader=FileSystemLoader(templates_dir))
    page_template = env.get_template("page.html")
    index_template = env.get_template("index.html")

    # copy over css files
    shutil.copytree(css_dir, static_dir, dirs_exist_ok=True)
    # copy over images
    shutil.copytree(images_dir, static_dir.joinpath("images"), dirs_exist_ok=True)

    # convert markdown pages into html
    for page in pages_dir.iterdir():
        if not page.is_file():
            continue

        with open(page, "r") as f:
            content = markdown(f.read())
            page_html = page_template.render(
                site_title="paperback",
                site_desc=SITE_DESCRIPTION,
                content=content,
            )
            with open(output_dir.joinpath(page.stem + ".html"), "w") as f_out:
                f_out.write(page_html)

    index_html = index_template.render(
        site_title=SITE_TITLE, site_desc=SITE_DESCRIPTION
    )

    with open(output_dir.joinpath("index.html"), "w") as f:
        f.write(index_html)

    print("Done.")


if __name__ == "__main__":
    main()
