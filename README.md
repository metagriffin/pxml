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

<pre>
$ echo '&lt;root&gt;&lt;node attr="value"&gt;foo&lt;/node&gt;&lt;/root&gt;' | pxml --color
<span style="color: green;">&lt;?xml version="1.0" encoding="utf-8"?&gt;</span>
&lt;root&gt;
  &lt;node attr="value"&gt;foo&lt;/node&gt;
&lt;/root&gt;
</pre>

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
