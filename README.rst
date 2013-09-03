================
Pretty-Print XML
================

A python library and command-line tool to "prettify" and colorize XML.


Installation
============

.. code-block:: bash

  $ pip install pxml


On the Command-Line
===================

.. code-block:: bash

  $ echo '<root><node attr="value">foo</node></root>' | pxml
  <?xml version="1.0" encoding="utf-8"?>
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
  <?xml version="1.0" encoding="utf-8"?>
  <root>
    <node attr="value">foo</node>
  </root>
  ''')
