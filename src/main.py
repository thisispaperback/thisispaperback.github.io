import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from markdown import markdown

from datetime import datetime


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
    posts_dir = content_dir.joinpath("posts")

    env = Environment(loader=FileSystemLoader(templates_dir))

    # copy over css files
    shutil.copytree(css_dir, static_dir, dirs_exist_ok=True)
    # copy over images
    shutil.copytree(images_dir, static_dir.joinpath("images"), dirs_exist_ok=True)

    # make about.html
    about_template = env.get_template("about.html")
    with open(pages_dir.joinpath("about.md"), "r") as f:
        content = markdown(f.read())
        about_html = about_template.render(
            site_title=SITE_TITLE,
            site_desc=SITE_DESCRIPTION,
            content=content,
        )
        with open(output_dir.joinpath("about.html"), "w") as f_out:
            f_out.write(about_html)

    # make mailing_list.html
    mailing_list_template = env.get_template("mailing_list.html")
    with open(pages_dir.joinpath("mailing_list.md"), "r") as f:
        content = markdown(f.read())
        mailing_list_html = mailing_list_template.render(
            site_title=SITE_TITLE,
            site_desc=SITE_DESCRIPTION,
            content=content,
        )
        with open(output_dir.joinpath("mailing_list.html"), "w") as f_out:
            f_out.write(mailing_list_html)

    # make index.html
    index_template = env.get_template("index.html")
    index_html = index_template.render(
        site_title=SITE_TITLE, site_desc=SITE_DESCRIPTION
    )

    with open(output_dir.joinpath("index.html"), "w") as f:
        f.write(index_html)

    # make blog.html
    post_template = env.get_template("post.html")
    posts = []
    for post in posts_dir.iterdir():
        if not post.is_file():
            continue

        parts = post.stem.split("-")
        month, day, year = parts[0], parts[1], parts[2]
        title_slug = parts[3:]
        date = datetime(int(year), int(month), int(day))
        date_str = date.strftime("%B %d, %Y")
        title = " ".join(word.capitalize() for word in title_slug)
        url = post.stem + ".html"

        with open(post, "r") as f:
            content = markdown(f.read())
            post_html = post_template.render(
                site_title=SITE_TITLE,
                site_desc=SITE_DESCRIPTION,
                content=content,
                title=title,
                date=date_str,
            )
            with open(output_dir.joinpath(url), "w") as f_out:
                f_out.write(post_html)

        posts.append(
            {
                "url": url,
                "title": title,
                "date_str": date_str,
                "date_obj": date,
                "content": content,
            }
        )
    posts.sort(key=lambda p: p["date_str"], reverse=True)
    blog_template = env.get_template("blog.html")
    blog_html = blog_template.render(
        site_title=SITE_TITLE, site_desc=SITE_DESCRIPTION, posts=posts
    )
    with open(output_dir.joinpath("blog.html"), "w") as f:
        f.write(blog_html)

    print("Done.")


if __name__ == "__main__":
    main()
