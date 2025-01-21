c = get_config()
c.InteractiveShellApp.exec_lines = [
    "import sys",
    "print('Executing exec_lines...')",
    "import utils.utils as utils",
]
