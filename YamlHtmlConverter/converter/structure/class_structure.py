# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# -------------------------------------------------------------------------------
#   Class : Structure
#
#   Structure containing an OOP version of a YAML
#
# -------------------------------------------------------------------------------
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
from YamlHtmlConverter.converter.structure.class_entry import Entry
from YamlHtmlConverter.converter.structure.class_entry_section import Section


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class Structure:

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, converter):
        from ..class_converter import Converter

        # headers for table of contents
        self.headers: list[str] = []

        # store converter reference
        self.converter: Converter = converter

        # converter file handler
        self.file_handler = self.converter.file_handler

        # entries
        self.entries: list[Entry] = []

        # collect all entries from file
        self.collect_entries_from_file()

        # always create lowest-level section
        self.root_section: Section = Section(self)

        # start constructing the html file
        self.create_structure_from_file(self.root_section)

        # format entries
        self.root_section.format_entries()

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Create Structure from File
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def create_structure_from_file(self, section: Section):

        # -----------------------------------
        #   Sub-Method : Iterate Section
        # -----------------------------------

        def iterate_section(sec: Section):

            # keep track of index
            nonlocal entry_index, break_count

            # go on until break
            while entry_index < len(self.entries):

                if break_count:
                    break_count -= 1
                    break

                # store current entry and next neighbours, based on current index
                entry_current = self.entries[min(max(entry_index, 0), len(self.entries) - 1)]
                entry_next = self.entries[min(entry_index + 1, len(self.entries) - 1)]

                # > > > > > > > > > > > > > > > > > > > >
                #   Start of new Section
                if entry_next.level > entry_current.level:

                    # create new section
                    section_new = Section(self)

                    # transfer attributes
                    section_new.set_level(entry_current.level)
                    section_new.set_line(entry_current.line)

                    # add new section as entry of current section
                    sec.add_entry(section_new)

                    # increment index
                    entry_index += 1

                    # iterate over created section
                    iterate_section(section_new)

                # > > > > > > > > > > > > > > > > > > > >
                #   Entry / End of Section
                else:

                    # create new entry
                    entry_new = Entry(self)

                    # transfer attributes
                    entry_new.set_level(entry_current.level)
                    entry_new.set_line(entry_current.line)

                    # increment index
                    entry_index += 1

                    # add entry to current section
                    sec.add_entry(entry_new)

                # stop while loop on last section entry
                if entry_next.level < entry_current.level:
                    break_count = abs(entry_current.level - entry_next.level)

        # reset entry iterating index
        entry_index: int = 0

        # recursion break counter
        break_count: int = 0

        # iterate through entries as long as entries are available
        while entry_index < len(self.entries):
            iterate_section(section)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Analyze Line
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def line_to_entry(self, line: str) -> Entry | None:

        # calculate indent
        indent = int((len(line) - len(line.lstrip())) / 2)

        # skip empty line
        if line.strip() == "":
            return None

        # entry creation
        entry = Entry(self)

        # set level
        entry.set_level(indent)

        # set line
        entry.set_line(line)

        # add entry to lookup list
        self.add_entry(entry)

        return entry

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Collect Entries from File
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def collect_entries_from_file(self):

        # collect entries
        while self.file_handler.lines_available():

            # get raw line string
            line = self.file_handler.get_line_inc()

            # skip yaml header
            if line.strip() == "---":
                continue

            # create entry using line
            self.line_to_entry(line)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Add Entry
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def add_entry(self, entry):
        self.entries.append(entry)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get Data
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_data(self) -> Section:
        return self.root_section

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Add Header
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def add_header(self, header) -> str:
        self.headers.append(header)

        return header
