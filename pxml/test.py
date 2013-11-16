# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# auth: metagriffin <mg.github@uberdev.org>
# date: 2009/06/05
# copy: (C) Copyright 2009-EOT metagriffin -- see LICENSE.txt
#------------------------------------------------------------------------------
# This software is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This software is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see http://www.gnu.org/licenses/.
#------------------------------------------------------------------------------

import unittest
from StringIO import StringIO
import pxml

#------------------------------------------------------------------------------
class TestPxml(unittest.TestCase):

  maxDiff = None

  #----------------------------------------------------------------------------
  def test_simple(self):
    src = StringIO('<root><zig><zog a="b">foo</zog><zog>bar</zog></zig></root>')
    chk = '''\
<?xml version="1.0" encoding="UTF-8"?>
<root>
  <zig>
    <zog a="b">foo</zog>
    <zog>bar</zog>
  </zig>
</root>
'''
    out = StringIO()
    self.assertTrue(pxml.prettify(src, out))
    self.assertMultiLineEqual(out.getvalue(), chk)

  #----------------------------------------------------------------------------
  def test_version(self):
    self.assertRegexpMatches(pxml.lib.version, r'^\d+\.\d+\.\d+$')

  #----------------------------------------------------------------------------
  def test_color(self):
    src = StringIO('<root><zog a="b">foo</zog></root>')
    chk = '''\
[32m<?xml version="1.0" encoding="UTF-8"?>(B[m
[1m[35m<(B[m[1m[34mroot(B[m[1m[35m>(B[m
  [1m[35m<(B[m[1m[34mzog(B[m [1m[34ma(B[m[1m[35m="(B[mb[1m[35m"(B[m[1m[35m>(B[mfoo[1m[35m</(B[m[1m[34mzog(B[m[1m[35m>(B[m
[1m[35m</(B[m[1m[34mroot(B[m[1m[35m>(B[m
'''
    out = StringIO()
    self.assertTrue(pxml.prettify(src, out, color=True))
    self.assertMultiLineEqual(out.getvalue(), chk)

  #----------------------------------------------------------------------------
  def test_encodingOverride(self):
    src = StringIO('<root><zog a="b">foo</zog></root>')
    chk = '''\
<?xml version="1.0" encoding="utf-8"?>
<root>
  <zog a="b">foo</zog>
</root>
'''
    out = StringIO()
    self.assertTrue(pxml.prettify(src, out, encoding='utf-8'))
    self.assertMultiLineEqual(out.getvalue(), chk)

  #----------------------------------------------------------------------------
  def test_canonicalAttributeOrder(self):
    src = StringIO('<root><zig a="1" c="2" b="3">foo</zig></root>')
    chk = '''\
<?xml version="1.0" encoding="UTF-8"?>
<root>
  <zig a="1" b="3" c="2">foo</zig>
</root>
'''
    out = StringIO()
    self.assertTrue(pxml.prettify(src, out))
    self.assertMultiLineEqual(out.getvalue(), chk)

#------------------------------------------------------------------------------
class TestPxmlTestMixin(unittest.TestCase, pxml.XmlTestMixin):

  #----------------------------------------------------------------------------
  def test_equivalent_xml(self):
    src = '<root  ><node a="1" b="0"/></root>'
    chk = '<root><node   b="0" a="1"  /></root  >'
    self.assertXmlEqual(src, chk)

  #----------------------------------------------------------------------------
  def test_different_xml(self):
    src = '<root  ><node a="1" b="0"/></root>'
    chk = '<root><node   b="1" a="0"  /></root  >'
    with self.assertRaises(AssertionError) as cm:
      self.assertXmlEqual(src, chk)
    self.assertMultiLineEqual(cm.exception.message, '''\
'<?xml version="1.0" encoding="UTF-8"?>\\n<root>\\n  <node a="1" b="0"/>\\n</root>\\ [truncated]... != '<?xml version="1.0" encoding="UTF-8"?>\\n<root>\\n  <node a="0" b="1"/>\\n</root>\\ [truncated]...
  <?xml version="1.0" encoding="UTF-8"?>
  <root>
-   <node a="1" b="0"/>
+   <node a="0" b="1"/>
  </root>
''')

  #----------------------------------------------------------------------------
  def test_unicode(self):
    src = '<root><node>this &#x2013; that.</node></root>'
    chk1 = '<root  ><node	\n>this \xe2\x80\x93 that.</node\n></root  >'
    chk2 = '<?xml version="1.0" encoding="UTF-8"?>\n' + chk1
    self.assertXmlEqual(src, chk2)
    self.assertXmlEqual(src, chk1)

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
