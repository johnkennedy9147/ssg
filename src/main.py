from copystatic import copy_static


def main():
    print(f"Running main...")
    copy_static("static", "public")
    print(f"Main completed successfully.")


main()
