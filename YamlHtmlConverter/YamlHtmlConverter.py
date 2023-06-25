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

def load_file(file=""):
    # try creating a converter, return its instance
    return Converter.create(file)
