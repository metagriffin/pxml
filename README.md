# Pretty-Print XML

A library and command-line tool to "prettify" XML.

## Installation

```
$ pip install pxml
```

## On the Command-Line

```
$ echo '<root><node attr="value">foo</node></root>' | pxml
<?xml version="1.0" encoding="utf-8"?>
<root>
  <node attr="value">foo</node>
</root>
```

And add some color:

```
$ echo '<root><node attr="value">foo</node></root>' | pxml --color
<?xml version="1.0" encoding="utf-8"?>
<root>
  <node attr="value">foo</node>
</root>
```

## As a Python Module

``` python
import pxml, StringIO

src = StringIO(data)
out = StringIO()

pxml.prettify(src, out, color=True)
```
