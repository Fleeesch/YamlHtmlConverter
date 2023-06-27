# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# -------------------------------------------------------------------------------
#
#   YAML HTML CONVERTER
#
#   Tool for converting a yaml file to a html file,
#   mainly for purposes of documentation
#
# -------------------------------------------------------------------------------
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from . import Converter


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Load File
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def yaml_to_html(file: str | list[str], html: str = "out.html") -> Converter | None:
    # try creating a converter, return its instance
    return Converter.create(file, html)
