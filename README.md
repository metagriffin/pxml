# Pretty-Print XML

A library and command-line tool to "prettify" XML.

## Installation

``` bash
$ pip install pxml
```

## On the Command-Line

``` bash
$ echo '<root><node attr="value">foo</node></root>' | pxml
<?xml version="1.0" encoding="utf-8"?>
<root>
  <node attr="value">foo</node>
</root>
```

And add some color:

![pxml with color](https://raw.github.com/metagriffin/pxml/master/pxml-color.png "pxml with color")

## As a Python Module

``` python
import pxml, StringIO

src = StringIO('<root><node attr="value">foo</node></root>')
out = StringIO()

pxml.prettify(src, out)

assert(out.getvalue() == '''\
<?xml version="1.0" encoding="utf-8"?>
<root>
  <node attr="value">foo</node>
</root>
''')
```
