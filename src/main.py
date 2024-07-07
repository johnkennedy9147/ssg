from copystatic import copy_static
from generate_page import generate_page


def main():
    print(f"Running main...")
    copy_static("static", "public")
    generate_page("./content/index.md", "./template.html", "./public/index.html")
    print(f"Main completed successfully.")


main()
