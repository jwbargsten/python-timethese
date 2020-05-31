# -*- coding: utf-8 -*-
from __future__ import unicode_literals

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.extlinks",
    "sphinx.ext.ifconfig",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
]
source_suffix = ".rst"
master_doc = "index"
project = "TimeThese"
year = "2020"
author = "Joachim W. Bargsten"
copyright = "{0}, {1}".format(year, author)
version = release = "0.0.6"

pygments_style = "trac"
templates_path = ["."]
extlinks = {
    "issue": ("https://github.com/jwbargsten/python-timethese/issues/%s", "#"),
    "pr": ("https://github.com/jwbargsten/python-timethese/pull/%s", "PR #"),
}

html_use_smartypants = True
html_last_updated_fmt = "%b %d, %Y"
html_split_index = False
html_sidebars = {
    "**": ["searchbox.html", "globaltoc.html", "sourcelink.html"],
}
html_short_title = "%s-%s" % (project, version)

napoleon_use_ivar = True
napoleon_use_rtype = False
napoleon_use_param = False
