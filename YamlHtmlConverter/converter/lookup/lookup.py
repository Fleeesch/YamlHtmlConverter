# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# -------------------------------------------------------------------------------
#   Lookup Module
#
#   Contains Lookup-Data used across the project
#
# -------------------------------------------------------------------------------
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#   HTML
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

# ::: Classes


# Wrapper for a single-line entry
html_class_line_wrapper = "line-wrapper"

html_class_section = "section"
html_class_level = "level"
html_class_entry = "entry"
html_class_attribute = "entry-attribute"
html_class_value = "entry-value"
html_class_comment = "comment"
html_class_comment_inline = "comment-inline"
html_class_comment_block = "comment-block"
html_class_file_reference = "file-reference"

# ::: IDs

# Page Layout
html_id_grid_wrapper = "grid-wrapper"  # grid-container
html_id_content = "content"  # entries
html_id_sidebar = "sidebar"  # sidebar (table-of-contents)
html_id_settings_bar = "settings-bar"  # top bar (filter)

# Sidebar Container
html_id_sidebar_wrapper = "sidebar-wrapper"  # grid-container
html_id_sidebar_collapse = "sidebar-collapse"  # collapse button container
html_id_sidebar_collapse_button = "sidebar-collapse-button"  # collapse button
html_id_table_of_contents = "table-of-contents"  # table-of-contents container
html_id_table_of_contents_list = "table-of-contents-list"  # list for table-of-contents

# Filter
html_id_filter = "input-filter"  # list for table-of-contents

# ::: String Formatting

# use the following syntax:
# {class-name to apply} : [{opening tag}, {closing tag}]
#
# Alternatively, you can leave out to closing tag to spread#
# the formatting to the end of the line

markdown = {
    "comment-type": [".t.", ".t."],
    "comment-format": [".f.", ".f."],
    "comment-appendix": ["++"],
    "string-header": [".h.", ".h."],
    "string-warning": ["!!", "!!"],
    "string-hint": ["??", "??"],
    "font-bold": ["**", "**"],
    "font-italic": ["//", "//"],
    "font-underline": ["__", "__"],
    "font-strike": ["--", "--"]
}

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#   Javascript
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

# File
js_file = "toc.js"

# Methods
js_method_filter_input = "filterInput()"  # apply filter
js_method_toggle_side_panel = "toggleSidePanel()"  # toggle side panel
js_method_copy = "copyLine(event)"  # toggle side panel
