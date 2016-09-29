from utils.page_objects import PageObject


class TerminalPage(PageObject):
    """Execute shell command in the terminal"""

    # Elements

    def __init__(self, *args, **kwargs):
        super(TerminalPage, self).__init__(*args, **kwargs)
        self.get("/system/terminal")

    # function_1: execute command
    def execute_command(self):
        pass
