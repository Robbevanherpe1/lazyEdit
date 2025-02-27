import keyboard
from textual.app import App, ComposeResult
from textual.containers import Horizontal, HorizontalScroll, Vertical
from textual.widgets import Static
from textual.events import Key
import sys

from .fileEditor import FileEditor
from .directory import Directory
from .terminal import Terminal

if sys.platform == "win32":
    import winpty
else:
    import pty

class CommandFooter(Static):
    def on_mount(self):
        self.update("Commands: (Ctrl+q) Quit     (Ctrl+s) Save File    (Ctrl+1) Directory Mode    (Ctrl+2) File Editing Mode    (Ctrl+3) Terminal")

class MyApp(App):
    CSS = """
    Screen {
        layout: vertical;
    }
    Horizontal {
        layout: horizontal;
        height: 1fr;
    }
    Directory {
        width: 25%;
        height: 100%;
    }
    FileEditor {
        height: 100%;
    }
    Terminal {
        height: 30%;
    }
    CommandFooter {
        dock: bottom;
        height: auto;
    }
    """

    def __init__(self):
        super().__init__()
        self.active_widget = None
        self.cursor_row = 0
        self.cursor_column = 0

    def compose(self) -> ComposeResult:
        self.directory = Directory()
        self.file_editor = FileEditor()
        self.terminal = Terminal()
        self.footer = CommandFooter()

        with Horizontal():
            yield self.directory
            with Vertical():
                with HorizontalScroll():
                    yield self.file_editor
                yield self.terminal
        yield self.footer

        self.active_widget = self.directory

    def on_key(self, event):
        if keyboard.is_pressed("ctrl") and keyboard.is_pressed("q"):
            self.exit()

        elif keyboard.is_pressed("ctrl") and keyboard.is_pressed("2"):
            
            self.file_editor.exit_editing()
            self.file_editor.editing = False
            self.active_widget = self.directory
            self.directory.browsing = True

        elif keyboard.is_pressed("ctrl") and keyboard.is_pressed("3"):
            self.directory.browsing = False
            self.active_widget = self.file_editor
            self.file_editor.editing = True
            self.file_editor.focus()
                 

        elif keyboard.is_pressed("ctrl") and keyboard.is_pressed("4"):
            self.file_editor.exit_editing()
            self.active_widget = self.terminal
            self.directory.browsing = False

        elif keyboard.is_pressed("ctrl") and keyboard.is_pressed("s") and self.active_widget == self.file_editor:
            self.file_editor.save_file()

        elif hasattr(self.active_widget, "on_key"):
            self.active_widget.on_key(event)

def run():
    MyApp().run()
