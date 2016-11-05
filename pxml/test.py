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
import six
import pxml
import sys

#------------------------------------------------------------------------------
class TestPxml(unittest.TestCase):

  maxDiff = None

  #----------------------------------------------------------------------------
  def test_simple(self):
    src = six.BytesIO(b'<root><zig><zog a="b">foo</zog><zog>bar</zog></zig></root>')
    chk = b'''\
<?xml version="1.0" encoding="UTF-8"?>
<root>
  <zig>
    <zog a="b">foo</zog>
    <zog>bar</zog>
  </zig>
</root>
'''
    out = six.BytesIO()
    self.assertTrue(pxml.prettify(src, out))
    self.assertEqual(out.getvalue(), chk)

  #----------------------------------------------------------------------------
  def test_version(self):
    self.assertRegexpMatches(pxml.lib.version, r'^\d+\.\d+\.\d+$')

  #----------------------------------------------------------------------------
  def test_color(self):
    src = six.BytesIO(b'<root><zog a="b">foo</zog></root>')
    chk = b'''\
[32m<?xml version="1.0" encoding="UTF-8"?>(B[m
[1m[35m<(B[m[1m[34mroot(B[m[1m[35m>(B[m
  [1m[35m<(B[m[1m[34mzog(B[m [1m[34ma(B[m[1m[35m="(B[mb[1m[35m"(B[m[1m[35m>(B[mfoo[1m[35m</(B[m[1m[34mzog(B[m[1m[35m>(B[m
[1m[35m</(B[m[1m[34mroot(B[m[1m[35m>(B[m
'''
    out = six.BytesIO()
    self.assertTrue(pxml.prettify(src, out, color=True))
    self.assertEqual(out.getvalue(), chk)

  #----------------------------------------------------------------------------
  def test_encodingOverride(self):
    src = six.BytesIO(b'<root><zog a="b">foo</zog></root>')
    chk = b'''\
<?xml version="1.0" encoding="utf-8"?>
<root>
  <zog a="b">foo</zog>
</root>
'''
    out = six.BytesIO()
    self.assertTrue(pxml.prettify(src, out, encoding='utf-8'))
    self.assertEqual(out.getvalue(), chk)

  #----------------------------------------------------------------------------
  def test_canonicalAttributeOrder(self):
    src = six.BytesIO(b'<root><zig a="1" c="2" b="3">foo</zig></root>')
    chk = b'''\
<?xml version="1.0" encoding="UTF-8"?>
<root>
  <zig a="1" b="3" c="2">foo</zig>
</root>
'''
    out = six.BytesIO()
    self.assertTrue(pxml.prettify(src, out))
    self.assertEqual(out.getvalue(), chk)

#------------------------------------------------------------------------------
class TestPxmlTestMixin(unittest.TestCase, pxml.XmlTestMixin):

  maxDiff = None

  #----------------------------------------------------------------------------
  def test_equivalent_xml(self):
    src = b'<root  ><node a="1" b="0"/></root>'
    chk = b'<root><node   b="0" a="1"  /></root  >'
    self.assertXmlEqual(src, chk)

  #----------------------------------------------------------------------------
  def test_different_xml(self):
    src = b'<root  ><node a="1" b="0"/></root>'
    chk = b'<root><node   b="1" a="0"  /></root  >'
    with self.assertRaises(AssertionError) as cm:
      self.assertXmlEqual(src, chk)
    if six.PY2:
      self.assertMultiLineEqual(str(cm.exception), '''\
u'<?xml version="1.0" encoding="UTF-8"?>\\n<root>\\n  <node a="1" b="0"/>\\n</root> [truncated]... != u'<?xml version="1.0" encoding="UTF-8"?>\\n<root>\\n  <node a="0" b="1"/>\\n</root> [truncated]...
  <?xml version="1.0" encoding="UTF-8"?>
  <root>
-   <node a="1" b="0"/>
+   <node a="0" b="1"/>
  </root>
''')
    elif sys.hexversion < 0x3040000:
      # python 3 to 3.4 (strings are always unicode)
      self.assertMultiLineEqual(str(cm.exception), '''\
'<?xml version="1.0" encoding="UTF-8"?>\\n<root>\\n  <node a="1" b="0"/>\\n</root>\\ [truncated]... != '<?xml version="1.0" encoding="UTF-8"?>\\n<root>\\n  <node a="0" b="1"/>\\n</root>\\ [truncated]...
  <?xml version="1.0" encoding="UTF-8"?>
  <root>
-   <node a="1" b="0"/>
+   <node a="0" b="1"/>
  </root>
''')
    else:
      # python 3.4+... (its truncation algorithm is different)
      self.assertMultiLineEqual(str(cm.exception), '''\
'<?xm[14 chars]" encoding="UTF-8"?>\\n<root>\\n  <node a="1" b="0"/>\\n</root>\\n' != '<?xm[14 chars]" encoding="UTF-8"?>\\n<root>\\n  <node a="0" b="1"/>\\n</root>\\n'
  <?xml version="1.0" encoding="UTF-8"?>
  <root>
-   <node a="1" b="0"/>
+   <node a="0" b="1"/>
  </root>
''')

  #----------------------------------------------------------------------------
  def test_unicode(self):
    src  = b'<root><node>this &#x2013; that.</node></root>'
    chkU = b'<root  ><node	\n>this \xe2\x80\x93 that.</node\n></root  >'
    chk1 = b'<?xml version="1.0" encoding="UTF-8"?>\n' + chkU
    chk2 = chkU
    self.assertXmlEqual(src, chk1)
    self.assertXmlEqual(src, chk2)
    if six.PY2:
      chk3 = '<root ><node >this – that.</node ></root >'
      self.assertXmlEqual(src, chk3)

  #----------------------------------------------------------------------------
  def test_prefixedWhitespace(self):
    src = '''
      <?xml version="1.0" encoding="UTF-8"?>
      <root   x="y" foo="bar"     />
    '''
    chk = '<root foo="bar" x="y"/>'
    self.assertXmlEqual(src, chk)


#------------------------------------------------------------------------------
# end of $Id$
# $ChangeLog$
#------------------------------------------------------------------------------
