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

import webbrowser

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class Converter():

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Static Method : Create
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    @staticmethod
    def create(file: str | list[str], html: str):

        # convert to list
        if not isinstance(file, list):
            file = [file]

        # check for valid files
        for f in file:

            # remove not exiting files
            if not os.path.exists(f):
                file.remove(f)
                break

            file_name, file_extension = os.path.splitext(os.path.basename(f))

            # remove non-yaml files
            if file_extension not in [".yaml", ".yml"]:
                file.remove(f)
                break

        # skip if there are no files
        if not file:
            return None

        # create a converter, return its instance
        return Converter(file, html)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Static Method : Apply Markdown
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    @staticmethod
    def apply_markdown(line: str) -> str:

        # ------------------------------
        #   Sub-Method : Apply RegEx
        # ------------------------------
        def apply_regex(input_str: str, class_name: str, tag_open: str, tag_close: str | None = None) -> str:

            if not tag_open:
                return input_str

            new_str = f'<span class="{class_name}">\\1</span>'

            if tag_close:
                regex = f'{re.escape(tag_open)}(.*?){re.escape(tag_close)}'
            else:
                regex = f'{re.escape(tag_open)}(.*?)$'

            return re.sub(regex, new_str, input_str)

        # ------------------------------

        # go through markdown entries
        for markdown in lookup.markdown:
            md = lookup.markdown[markdown]

            if len(md) > 1:
                line = apply_regex(line, markdown, md[0], md[1])
            else:
                line = apply_regex(line, markdown, md[0])


        return line

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, file: list[FileHandler], html: str):

        # html file about to be created
        self.html_file = html

        # flag to inform you that the building process went ok
        self.build_success = False

        # declare file handler list
        self.file_handler: list[FileHandler] = []

        # add file handlers
        for f in file:
            self.file_handler.append(FileHandler(self, f))

        # create structure
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
    #   Method : Open HTML
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def open_html(self):

        # get absolute path
        abs_path = os.path.abspath(self.html_file)

        # skip if file doesn't exist
        if not os.path.exists(abs_path):
            return

        # open file in web browser
        webbrowser.open(abs_path)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Create HTML
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def create_html(self):

        # header start
        html_header = f"""
                        <!DOCTYPE html>
                        <html>
                        <head>
                        <title>{self.file_handler[0].file_name.capitalize()}</title>
                        <link rel="stylesheet" href="styles.css?v={self.id}">
                        </head>
                        <body>
                        """

        topbar = f"""
                    <div id="settings-bar">
                    <input type="text" id="{lookup.html_id_filter}" 
                    onkeyup="{lookup.js_method_filter_input}" 
                    placeholder="Filter...">
                    </div>
                    """

        sidebar = f"""
                <div id="{lookup.html_id_sidebar}">
                <div id="{lookup.html_id_sidebar_wrapper}">
                <div id="{lookup.html_id_sidebar_collapse}">
                <input type="button" id="{lookup.html_id_sidebar_collapse_button}" 
                onclick="{lookup.js_method_toggle_side_panel}">
                </div>
                <div id="{lookup.html_id_table_of_contents}">
                
                <ul id="{lookup.html_id_table_of_contents_list}"></ul>
                </div>
                </div>
                </div>
                """

        # get html data of structure
        html_structure = f"""
                        <div id={lookup.html_id_content}>
                        {self.structure.get_data().get_html_section()}
                        </div>
                        """

        # header end
        html_end = f"""
                        <script type="text/javascript" src="{lookup.js_file}" ></script>
                        </body>
                        </html>
                        """

        # concatenate html output string
        html_print = ""
        html_print += textwrap.dedent(html_header).strip() + "\n"

        html_print += f'<div id="{lookup.html_id_grid_wrapper}">'

        html_print += textwrap.dedent(topbar).strip() + "\n"
        html_print += html_structure + "\n"
        html_print += textwrap.dedent(sidebar).strip() + "\n"

        html_print += f'</div>'

        html_print += textwrap.dedent(html_end).strip() + "\n"

        # auto-format html document
        soup = BeautifulSoup(html_print, 'html.parser')
        html_print_formatted = soup.prettify()


        # write text to file
        with open(self.html_file, "w") as f:
            f.write(html_print_formatted)

        self.build_success = True