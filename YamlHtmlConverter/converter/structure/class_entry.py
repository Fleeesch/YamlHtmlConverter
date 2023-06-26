# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# -------------------------------------------------------------------------------
#   Class : Structure : Entry
#
#   Base class of entries from a file.
#
# -------------------------------------------------------------------------------
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from ..lookup import lookup


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class Entry:

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, structure):
        from YamlHtmlConverter.converter.structure.class_entry_section import Section

        # structure reference
        self.structure = structure

        # indent level
        self.level: int = 0

        # raw file string
        self.line: str = ""

        # unique identifier
        self.id: str = ""

        # section indicator
        self.is_section = False

        self.line_no_comment: str = ""
        self.comment_inline: str = ""

        self.line_value: str = ""
        self.line_no_value: str = ""

        # yaml comment flags
        self.is_empty: bool = False
        self.is_full_line_comment: bool = False
        self.has_comment: bool = False
        self.has_inline_comment: bool = False
        self.has_value: bool = False

        # reference to potential parent section
        self.parent_section: Section | None = None

        # 1st level entry flag
        self.is_root_entry: bool = False

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Detect Empty Line
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def detect_empty_line(self):
        if self.line.strip() == "":
            self.is_empty = True

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Detect Comment
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def detect_comment(self):

        # Full-Line Comment
        if self.line.strip().startswith("#"):
            self.is_full_line_comment = True

        # Comment Appearance
        if self.line.lstrip().find(" # ") > 0:
            self.has_comment = True

        # Inline Comment
        if self.has_comment and not self.is_full_line_comment:
            self.has_inline_comment = True

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Set Level
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def set_level(self, level: int):
        self.level = level

        # raise flag in case entry is on root level
        self.is_root_entry = (self.level <= 0)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Set Line
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def set_line(self, line: str = ""):

        # store line
        self.line = line
        self.line_no_comment = line.strip()
        self.line_no_value = self.line_no_comment

        # detect line attributes
        self.detect_empty_line()
        self.detect_comment()

        # filter inline comment
        if self.has_inline_comment:
            line_parts = self.line.split(" # ")

            self.comment_inline = line_parts[-1].strip()
            self.line_no_comment = self.line[:-(len(line_parts[-1]) + 2)]

        # filter full line comment
        if self.is_full_line_comment:
            self.line_no_comment = self.line[1:].strip()

        # store line separated from value
        try:
            self.line_no_value = self.line_no_comment.split(":")[0]
            self.line_value = self.line_no_comment.split(":")[1]
        except:
            pass

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Set Parent Section
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def set_parent_section(self, section):
        self.parent_section = section

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Format
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def format(self):

        pass

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : set ID
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def set_id(self, id):
        self.id = id

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get HTML Section
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_html_section(self) -> str:
        return self.get_html_line()

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get HTML Line
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_html_line(self) -> str:

        # return line
        line = ""

        # create and store individual id
        id_str = f'{self.line_no_comment.replace(":", "").strip()}'
        id_str = id_str.replace(" ", "")
        self.set_id(id_str)

        # line-wrapping div container
        line += f'<div ' \
                f'onclick="copyLine(event)" ' \
                f'class="{lookup.html_class_line_wrapper} {lookup.html_class_level}-{self.level}" '

        # add id for root entries, just close tag if not
        if self.is_root_entry:
            line += f'id="{id_str}">'
        else:
            line += f'>'

        # entry is a section header
        if self.is_section:

            line += f'<span class="' \
                    f'{lookup.html_class_section} ' \
                    f'{lookup.html_class_attribute}">' \
                    f'{self.line_no_comment}' \
                    f'</span>'

        # entry is a conventional line
        else:

            line += f'<span class="' \
                    f'{lookup.html_class_attribute} ' \
                    f'">' \
                    f'{self.line_no_value}:' \
                    f'</span>' \
                    f'<span class="' \
                    f'{lookup.html_class_value} ' \
                    f'">' \
                    f'{self.line_value}' \
                    f'</span>'

        # optional inline comment
        if self.has_inline_comment:
            line += " "

            line += f'<span class="' \
                    f'{lookup.html_class_comment} ' \
                    f'{lookup.html_class_comment_inline}' \
                    f'">' \
                    f'{self.comment_inline}' \
                    f'</span>'

        line += "</div>"

        return line
