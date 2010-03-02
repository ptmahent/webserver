# CTK: Cherokee Toolkit
#
# Authors:
#      Alvaro Lopez Ortega <alvaro@alobbs.com>
#
# Copyright (C) 2009 Alvaro Lopez Ortega
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of version 2 of the GNU General Public
# License as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

from consts import *
from Container import Container
from Template import Template
from PageCleaner import Postprocess
from Help import HelpEntry, HelpMenu
from util import formater

DEFAULT_PAGE_TEMPLATE = """\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
       "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
 <head>
%(head)s
 </head>
 <body%(body_props)s>
%(body)s
 </body>
</html>
"""

HEADERS = [
    '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />',
    '<link rel="stylesheet" type="text/css" href="/CTK/css/CTK.css" />',
    '<script type="text/javascript" src="/CTK/js/common.js"></script>',
    '<script type="text/javascript" src="/CTK/js/jquery-1.3.2.js"></script>',
    '<script type="text/javascript" src="/CTK/js/Help.js"></script>',
]

def uniq (seq):
    noDupes = []
    [noDupes.append(i) for i in seq if not noDupes.count(i)]
    return noDupes

class Page (Container):
    def __init__ (self, template=None, headers=None, helps=[], **kwargs):
        Container.__init__ (self, **kwargs)

        if headers:
            self._headers = HEADERS + headers
        else:
            self._headers = HEADERS

        if template:
            self._template = template
        else:
            self._template = Template (content = DEFAULT_PAGE_TEMPLATE)

        self._helps = []
        for entry in helps:
            self._helps.append (HelpEntry (entry[0], entry[1]))

    def AddHeaders (self, headers):
        if type(headers) == list:
            self._headers += headers
        else:
            self._headers.append (headers)

    def Render(self):
        # Get the content render
        render = Container.Render(self)

        # Build the <head> text
        self._headers += render.headers
        head = "\n".join (uniq(self._headers))

        # Helps
        all_helps  = self._helps
        all_helps += render.helps

        render_helps = HelpMenu(all_helps).Render().html

        # Javascript
        if render.js:
            js = formater (HTML_JS_ON_READY_BLOCK, render.js)
        else:
            js = ''

        # Build the <body>
        body = render.html + render_helps
        if render.js:
            body += js

        # Set up the template
        self._template['head']  = head
        self._template['html']  = render.html
        self._template['js']    = js
        self._template['body']  = body
        self._template['helps'] = render_helps

        if not self._template['body_props']:
            self._template['body_props'] = ''

        txt = self._template.Render()
        return Postprocess (txt)
