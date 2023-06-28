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
from .class_entry_comment import Comment
from .class_entry_comment_block import CommentBlock


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class ExampleBlock(CommentBlock):

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, structure):
        super().__init__(structure)

        self.comments: list[Comment] = []

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Add Comment
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def add_comment(self, comment: Comment):
        self.comments.append(comment)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get  HTML Line
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_html_line(self) -> str:
        line = f'<div class="{lookup.html_class_comment} {lookup.html_class_example_block}">'

        line += f'<div class="{lookup.html_class_example_block_header}">Example</div>'

        for comment in self.comments:
            comment_str = comment.line.lstrip()[2:]

            line += f'<pre class="{lookup.html_class_comment}">{comment_str}</pre>\n'

        line += '</div>'

        return line
