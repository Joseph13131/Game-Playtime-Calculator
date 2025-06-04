import os, sys
def pure_path(path):
    if getattr(sys, 'frozen', False):
        # If bundled by PyInstaller
        base_path = os.path.dirname(sys.executable)
    else:
        # If running as a script
        base_path = os.path.dirname(os.path.abspath(__file__))
    final_path = base_path
    for p in path.split("/"):
        final_path = os.path.join(final_path, p)
    return final_path