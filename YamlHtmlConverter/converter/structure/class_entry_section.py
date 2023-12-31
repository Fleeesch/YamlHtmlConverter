# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# -------------------------------------------------------------------------------
#   Class : Structure : Entry : Section
#
#   Section of content
#
# -------------------------------------------------------------------------------
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from .class_entry import Entry
from ..lookup import lookup


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class Section(Entry):

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self):
        super().__init__()

        # section indicator
        self.is_section = True

        # contained entries
        self.entries: list[Entry] = []

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Add Entry
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def add_entry(self, entry: Entry):

        # mark this section as parent section
        entry.set_parent_section(self)

        # add entry
        self.entries.append(entry)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Format Entries
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def format_entries(self):

        # format itself
        self.format()

        # format entries
        for entry in self.entries:
            entry.format()

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get Entries
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_entries(self) -> list[Entry]:

        # return list containing entries
        entry_return: list[Entry] = [self]

        # go through entries
        for entry in self.entries:

            # entry is a section?
            if isinstance(entry, Section):

                # collect entries from section
                section_entries = entry.get_entries()

                # add collected section entries to collector
                for section_entry in section_entries:
                    entry_return.append(section_entry)

            # entry is not a section...
            else:
                # add entry to collector
                entry_return.append(entry)

        # return collected entries
        return entry_return

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get HTML Section
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_html_section(self) -> str:

        # start with blank return string
        return_string: str = ""

        return_string += f'<ul class="' \
                         f'{lookup.html_class_level}{self.level + 1}">' \
                         f'\n'

        # go through entries
        for entry in self.entries:

            # skip full line comments
            if entry.is_full_line_comment:
                continue

            # create a list entry
            if entry.is_section:

                return_string += f'<li class="' \
                                 f'{lookup.html_class_section} ' \
                                 f'{lookup.html_class_level}{entry.level + 1}' \
                                 f'">'

            else:
                return_string += f'<li class="' \
                                 f'{lookup.html_class_entry} ' \
                                 f'{lookup.html_class_level}{entry.level + 1}' \
                                 f'">'


            # get line
            return_string += entry.get_html_line()

            return_string += "\n"

            # add section html
            if entry.is_section:
                return_string += entry.get_html_section()

            # bullet list closing tag
            return_string += '</li>\n'

        # closing tags
        return_string += "</ul>" + "\n"

        # return html string
        return return_string
