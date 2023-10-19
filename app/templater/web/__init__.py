def check_requirements():
    try:
        import imgkit
        import jinja2
    except ImportError:
        print("Import error")
