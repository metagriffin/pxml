#!/usr/bin/env python
#------------------------------------------------------------------------------
# file: $Id: pxml.py 346 2012-08-12 17:22:39Z griffin $
# desc: pretty-prints xml, nothing more :)
# auth: metagriffin <metagriffin@uberdev.org>
# date: 2009/06/05
# copy: (C) CopyLoose 2009 UberDev <hardcore@uberdev.org>, No Rights Reserved.
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

# TODO: enable this when attribute order is canonicalized...
#   #----------------------------------------------------------------------------
#   def test_canonicalAttributeOrder(self):
#     src = StringIO('<root><zig a="1" c="2" b="3">foo</zig></root>')
#     chk = '''\
# <?xml version="1.0" encoding="UTF-8"?>
# <root>
#   <zig a="1" b="3" c="2">foo</zig>
# </root>
# '''
#     out = StringIO()
#     self.assertTrue(pxml.prettify(src, out))
#     self.assertMultiLineEqual(out.getvalue(), chk)

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
