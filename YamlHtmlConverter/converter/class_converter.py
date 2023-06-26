# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# -------------------------------------------------------------------------------
#   Class : Converter
#
#   Takes care of the conversion of a file,
#   handles communication between the elements
#
# -------------------------------------------------------------------------------
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

import os
import textwrap
from datetime import datetime

from bs4 import BeautifulSoup

from . import FileHandler
from . import Structure
from .lookup import lookup
import re


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class Converter():

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Static Method : Create
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    @staticmethod
    def create(file):

        # skip if file doesn't exist
        if not os.path.exists(file):
            return

        # get file name and extension
        file_name, file_extension = os.path.splitext(os.path.basename(file))

        # skip if extension isn't a yaml
        if file_extension not in [".yaml", ".yml"]:
            return

        # create a converter, return its instance
        return Converter(file)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Static Method : Apply Markdown
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    @staticmethod
    def apply_markdown(line: str) -> str:

        regex_type = r'\*{1}(.*?)\*{1}'
        regex_format = r'\*{2}(.*?)\*{2}'
        regex_appendix = r'\+\+(.*?)$'

        line = re.sub(regex_appendix, r'<span class="string-appendix">\1</span>', line)
        line = re.sub(regex_format, r'<span class="string-format">\1</span>', line)
        line = re.sub(regex_type, r'<span class="string-type">\1</span>', line)

        return line

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, file):

        # structural elements
        self.file_handler: FileHandler = FileHandler(self, file)
        self.structure: Structure = Structure(self)

        # unique ID make from timestamp
        self.id = self.generate_version_id()

        # make html file
        self.create_html()

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Generate Version ID
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def generate_version_id(self) -> str:
        return datetime.now().strftime("%Y%m%d%H%M%S") + str(datetime.now().microsecond)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Create HTML
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def create_html(self):

        # header start
        html_header = f"""
                        <!DOCTYPE html>
                        <html>
                        <head>
                        <title>{self.file_handler.file_name.capitalize()}</title>
                        <link rel="stylesheet" href="styles.css?v={self.id}">
                        </head>
                        <body>
                        """

        topbar = f"""
                    <div id="settings-bar">
                    <input type="text" id="input-filter" onkeyup="filterInput()" placeholder="Filter...">
                    <input type="checkbox" id="check-sidepanel" onchange="checkSidepanel(event)">
                    </div>
                    """

        sidebar = f"""
                <div id="table-of-contents">
                <ul id="table-of-contents-list"></ul>
                </div>
                """

        # get html data of structure
        html_structure = f"""
                        <div id={lookup.html_class_content}>
                        {self.structure.get_data().get_html_section()}
                        </div>
                        """

        # header end
        html_end = f"""
                        <script type="text/javascript" src="toc.js" ></script>
                        </body>
                        </html>
                        """

        # concatenate html output string
        html_print = ""
        html_print += textwrap.dedent(html_header).strip() + "\n"

        html_print += f'<div id="{lookup.html_class_grid_wrapper}">'

        html_print += textwrap.dedent(topbar).strip() + "\n"
        html_print += html_structure + "\n"
        html_print += textwrap.dedent(sidebar).strip() + "\n"


        html_print += f'</div>'

        html_print += textwrap.dedent(html_end).strip() + "\n"

        # auto-format html document
        soup = BeautifulSoup(html_print, 'html.parser')
        html_print_formatted = soup.prettify()

        # write text to file
        with open("test.html", "w") as f:
            f.write(html_print_formatted)
