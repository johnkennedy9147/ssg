import os
import re

from markdown_blocks import markdown_to_html_node


def extract_title(markdown):
    main_heading_regex = r"^# (.*)"
    main_heading = re.search(main_heading_regex, markdown)
    if not main_heading:
        raise ValueError("Invalid source, pages are required to have at least one H1.")
    return main_heading.group(1)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating Page {from_path} to {dest_path} using {template_path}")
    if not os.path.exists(from_path):
        print(f"Page source {from_path} not found, exiting.")

    with open(from_path, "r", encoding="utf-8") as file:
        file_content = file.read()
        file.close()
        title = extract_title(file_content)
        content = markdown_to_html_node(file_content).to_html()
        with open(template_path, "r") as template_file:
            template = template_file.read()
            template_file.close()
            template = template.replace("{{ Title }}", title)
            template = template.replace("{{ Content }}", content)
            dest_dir = os.path.dirname(dest_path)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir, exist_ok=True)
            with open(dest_path, "w") as created_file:
                created_file.write(template)
                created_file.close()


def generate_pages_recursive(content_dir, template_path, dest_dir):
    print(f"Creating Pages from {content_dir}")
    if not os.path.exists(content_dir):
        print(f"{content_dir} directory not found, exiting.")
        return
    if not os.path.exists(template_path):
        print(f"Page template {template_path} not found, exiting.")
    paths_to_copy = os.listdir(content_dir)
    for path in paths_to_copy:
        fullpath = os.path.join(content_dir, path)
        if os.path.isdir(fullpath):
            print(f"{fullpath} is a directory, recursing")
            generate_pages_recursive(
                f"{content_dir}/{path}", template_path, f"{dest_dir}/{path}"
            )
        else:
            destination_fullpath = os.path.join(dest_dir, path).replace(".md", ".html")
            print(
                f"Creating HTML page from file {fullpath} and saving to {destination_fullpath}"
            )
            generate_page(fullpath, template_path, destination_fullpath)
