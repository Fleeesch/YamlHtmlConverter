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

        # section indicator
        self.is_section = False

        self.line_no_comment: str = ""
        self.comment_inline: str = ""

        # yaml comment flags
        self.is_empty: bool = False
        self.is_full_line_comment: bool = False
        self.has_comment: bool = False
        self.has_inline_comment: bool = False

        # reference to potential parent section
        self.parent_section: Section | None = None

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

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Set Line
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def set_line(self, line: str = ""):

        # store line
        self.line = line
        self.line_no_comment = line.strip()

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
    #   Method : Is Header
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def is_header(self):

        return isinstance(self.Section)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Is Root Header
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def is_root_header(self):

        from YamlHtmlConverter.converter.structure.class_entry_section import Section

        return self.level <= 0 and isinstance(self, Section)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get HTML Section
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_html_section(self) -> str:
        return self.get_html_line()

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get HTML Line
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_html_line(self) -> str:

        line = ""

        tag_id = ''
        tag_class = ''

        # additional tags for root headers
        if self.is_section and self.level <= 0:
            header_name = f'header-{self.line_no_comment.replace(":", "").strip()}'

            self.structure.add_header(header_name
                                      )
            tag_id = f'id="{header_name}"'
            tag_class = 'toc-header'

        # line wrapper
        line += f'<div onclick="copyLine(event)" class="{lookup.html_class_line_wrapper} {tag_class}" {tag_id}>'

        # entry is a section header
        if self.is_section:

            line += f'<span class="' \
                    f'{lookup.html_class_header} ' \
                    f'{lookup.html_class_level}{self.level + 1}' \
                    f'">' \
                    f'{self.line_no_comment}' \
                    f'</span>'

        # entry is a conventional line
        else:
            line += f'<span class="' \
                    f'{lookup.html_class_attribute} ' \
                    f'{lookup.html_class_level}{self.level + 1}' \
                    f'">' \
                    f'{self.line_no_comment}' \
                    f'</span>'

        # entry has an inline comment
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
