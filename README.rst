================
Pretty-Print XML
================

A python library and command-line tool to "prettify" and colorize XML.
It also provides a unittest.TestCase mixin that adds the
`assertXmlEqual` method and, on difference, shows a "pretty" diff.

Installation
============

.. code-block:: bash

  $ pip install pxml


On the Command-Line
===================

.. code-block:: bash

  $ echo '<root><node attr="value">foo</node></root>' | pxml
  <?xml version="1.0" encoding="UTF-8"?>
  <root>
    <node attr="value">foo</node>
  </root>

And add some color:

.. image:: https://raw.github.com/metagriffin/pxml/master/pxml-color.png
  :alt: pxml with color


As a Python Module
==================

.. code-block:: python

  import pxml, six

  src = six.StringIO('<root><node attr="value">foo</node></root>')
  out = six.StringIO()

  pxml.prettify(src, out)

  assert(out.getvalue() == '''\
  <?xml version="1.0" encoding="UTF-8"?>
  <root>
    <node attr="value">foo</node>
  </root>
  ''')


Unit Testing
============

The `pxml.XmlTestMixin` class adds the `assertXmlEqual` method to the
subclass which allows easy semantic comparison that two XML structures
are equivalent. It does so by ignoring ignorable whitespace, attribute
order, quote types, and other differences that are byte-level
differences when serialized, but don't actually represent semantic
differences. When differences are detected, displays the XML
differences in "prettified" XML for easier comparison.

.. code-block:: python

  import unittest, pxml

  class MyTestCase(unittest.TestCase, pxml.XmlTestMixin):

    def test_equivalent_xml(self):
      src = '<root  ><node a="1" b="0"/></root>'
      chk = '<root><node   b="0" a="1"  /></root  >'
      self.assertXmlEqual(src, chk)

    def test_different_xml(self):
      src = '<root  ><node a="1" b="0"/></root>'
      chk = '<root><node   b="1" a="0"  /></root  >'
      self.assertXmlEqual(src, chk)

      # this fails the test and produces the following error message:
      #   AssertionError: [truncated]... != [truncated]...
      #     <?xml version="1.0" encoding="UTF-8"?>
      #     <root>
      #   -   <node a="1" b="0"/>
      #   +   <node a="0" b="1"/>
      #     </root>
