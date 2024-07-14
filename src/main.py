from copystatic import copy_static
from generate_page import generate_pages_recursive


def main():
    print(f"Running main...")
    copy_static("static", "public")
    generate_pages_recursive("./content", "./template.html", "./public")
    print(f"Main completed successfully.")


main()
