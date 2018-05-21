"""
Helper module to generate the pydoc based
"""
import os
import settings
import sys

from glob import glob
from pydoc import writedoc

# So we can find the libs
sys.path.append('libs')

PACKAGES = ["net2base",
            "net2xs", "net2xs.conversions", "net2xs.deftypes",
            "net2dbxs",
            "network", "network.net2plus", "network.sqlserver"]

INDEX = "index.htm"


def read_file(file_name):
    """Read file content
    """
    with open(file_name) as f:
        return f.read()


def alter_doc(content):
    """Change doc content
    - Strip reference to local python file
    - Replace index with our own index file
    """
    pos1 = content.find("<a href=\"file:///")
    if pos1 >= 0:
        pos2 = content.find("</a>", pos1)
        content = content[:pos1] + content[pos2 + len("</a>"):]

    content = content.replace('<a href=".">index</a>',
                              '<a href="index.htm">index</a>')
    return content


def alter_index(content):
    """Change index content
    - Replace version place holder with actual version
    """
    content = content.replace('#VERSION#', settings.VERSION)
    return content


def write_file(file_name, content):
    """Write content as file
    """
    with open(file_name, "w") as f:
        f.write(content)


if __name__ == "__main__":

    # Create docs
    for p in PACKAGES:
        writedoc(p)

    # For each html, generated into src, write altered to docs
    for src in glob("*.html"):
        dest = '../docs/' + src
        content = read_file(src)
        content = alter_doc(content)

        write_file(dest, content)
        os.remove(src)

    # Write index with correct version to docs
    content = read_file(INDEX)
    dest = '../docs/' + INDEX
    content = alter_index(content)
    write_file(dest, content)
