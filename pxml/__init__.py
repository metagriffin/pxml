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

'''
Pretty-prints XML, nothing more :)
'''

#------------------------------------------------------------------------------
import sys, re, argparse, xml.dom, xml.dom.minidom, pkg_resources, six
import blessings

#------------------------------------------------------------------------------
class lib:
  @property
  def version(self):
    return pkg_resources.get_distribution('pxml').version
lib = lib()

#------------------------------------------------------------------------------
DEFAULT_ENCODING = 'UTF-8'
ACCEPTABLE_COLORIZATION_ENCODINGS = ('UTF-8', 'utf-8')
class UnsupportedEncoding(Exception): pass

#------------------------------------------------------------------------------
def removeIgnorableWhitespace(node):
  rem = []
  for n in node.childNodes:
    if n.nodeType == xml.dom.Node.ELEMENT_NODE:
      removeIgnorableWhitespace(n)
    if n.nodeType != xml.dom.Node.TEXT_NODE:
      continue
    if re.match('^\s*$', n.nodeValue):
      rem.append(n)
  for n in rem:
    node.removeChild(n)

#------------------------------------------------------------------------------
def indentXml(doc, node, indentString, level=0):
  if node.nodeType != node.ELEMENT_NODE \
      or len(node.childNodes) <= 0 \
      or len(filter(lambda n: n.nodeType != n.TEXT_NODE, node.childNodes)) <= 0:
    return

  # todo: this makes the sequence '<a><b>foo</b></a>' render un-indented...
  #       hm. generalize in a better way? ie. only if the total length is
  #       less than X?...
  # if ( len(node.childNodes) == 1
  #      and ( len(node.childNodes[0].childNodes) <= 0
  #            or ( len(node.childNodes[0].childNodes) == 1
  #                 and node.childNodes[0].childNodes[0].nodeType == node.TEXT_NODE ))
  #      ):
  #   return

  # i am an element with at least one non-text node... thus indent!
  indent = '\n' + (level * indentString)
  ins = []
  for n in node.childNodes:
    if n.nodeType == node.ELEMENT_NODE:
      indentXml(doc, n, indentString, level + 1)
    if n.nodeType != node.ELEMENT_NODE \
       or (n.previousSibling and n.previousSibling.nodeType == node.TEXT_NODE):
      continue
    ins.append(n)
  for n in ins:
    node.insertBefore(doc.createTextNode(indent + indentString), n)
  node.appendChild(doc.createTextNode(indent))

#------------------------------------------------------------------------------
def cxml_xmlescape(value, quote=False):
  value = value.replace('&', '&amp;')
  if quote:
    value = value.replace('"', '&quot;')
  return value \
         .replace('<', '&lt;') \
         .replace('>', '&gt;')

#------------------------------------------------------------------------------
def cxml_attribute(node, output, enc, cspec):
  output.write(' ' + cspec.attributeName(node.nodeName.encode(enc)))
  output.write(cspec.attributeDelim('="'))
  output.write(cxml_xmlescape(node.nodeValue.encode(enc), True))
  output.write(cspec.attributeDelim('"'))

#------------------------------------------------------------------------------
def cxml_text(node, output, enc, cspec):
  # tbd: maybe do a little analysis to determine it is better to escape
  #      or use a <![CDATA[...]]> section?...
  output.write(cxml_xmlescape(node.nodeValue.encode(enc)))

#------------------------------------------------------------------------------
def cxml_comment(node, output, enc, cspec):
  output.write(cspec.comment('<!--%s-->' % (node.nodeValue.encode(enc),)))

#------------------------------------------------------------------------------
def cxml_cdata(node, output, enc, cspec):
  output.write(cspec.xmlDeclaration('<![CDATA['))
  output.write(node.nodeValue.encode(enc))
  output.write(cspec.xmlDeclaration(']]>'))

#------------------------------------------------------------------------------
def cxml_element(node, output, enc, cspec):
  output.write(cspec.angleBracket('<'))
  output.write(cspec.elementName(node.nodeName.encode(enc)))
  if node.hasAttributes():
    for attr in node.attributes.values():
      cxml_attribute(attr, output, enc, cspec)
  if not node.hasChildNodes():
    output.write(cspec.angleBracket('/>'))
    return
  output.write(cspec.angleBracket('>'))
  for child in node.childNodes:
    # node types: ELEMENT_NODE, ATTRIBUTE_NODE, TEXT_NODE,
    # CDATA_SECTION_NODE, ENTITY_NODE, PROCESSING_INSTRUCTION_NODE,
    # COMMENT_NODE, DOCUMENT_NODE, DOCUMENT_TYPE_NODE, NOTATION_NODE
    func = None
    if child.nodeType == xml.dom.Node.ELEMENT_NODE:         func = cxml_element
    elif child.nodeType == xml.dom.Node.TEXT_NODE:          func = cxml_text
    elif child.nodeType == xml.dom.Node.COMMENT_NODE:       func = cxml_comment
    elif child.nodeType == xml.dom.Node.CDATA_SECTION_NODE: func = cxml_cdata
    if func is None:
      raise TypeError('unexpected node type "%d"' % (child.nodeType,))
    func(child, output, enc, cspec)
  output.write(cspec.angleBracket('</'))
  output.write(cspec.elementName(node.nodeName.encode(enc)))
  output.write(cspec.angleBracket('>'))

#------------------------------------------------------------------------------
def cxml_document(doc, output, enc, cspec):
  if doc.nodeType == xml.dom.Node.DOCUMENT_NODE:
    doc = doc.documentElement
  if doc.nodeType != xml.dom.Node.ELEMENT_NODE:
    raise TypeError('expected to colorize either XML document or element (not %r)' %
                    doc.nodeType)
  output.write(cspec.xmlDeclaration(
      '<?xml version="1.0" encoding="%s"?>' % (enc,)) + '\n')
  return cxml_element(doc, output, enc, cspec)

#------------------------------------------------------------------------------
class ColorSpec(object):
  def __init__(self):
    t = blessings.Terminal(force_styling=True)
    self.reset          = t.normal
    self.xmlDeclaration = t.green
    self.angleBracket   = t.bold_magenta
    self.elementName    = t.bold_blue
    self.attributeName  = t.bold_blue
    self.attributeDelim = t.bold_magenta
    self.comment        = t.red

#------------------------------------------------------------------------------
def colorizeXml(dom, output, encoding=DEFAULT_ENCODING, colorspec=None):
  if encoding not in ACCEPTABLE_COLORIZATION_ENCODINGS:
    # restricting colorized output to UTF-8 encoding only. is there actually
    # a problem with other encodings?... not sure, just being paranoid.
    # todo: look into this and see if this is really necessary.
    raise UnsupportedEncoding(encoding)
  if colorspec is None or colorspec is True:
    colorspec = ColorSpec()
  cxml_document(dom, output, encoding, colorspec)
  output.write('\n')
  return True

#------------------------------------------------------------------------------
def prettify(input, output, strict=True, indentString='  ', color=False,
             encoding=DEFAULT_ENCODING):
  '''
  Converts the input data stream `input` (which must be a file input
  like object) to `output` (which must be a file output like object)
  by parsing the stream as XML and outputting "prettified"
  XML. Prettification involves the following aspects:

  * Collapsing ignorable whitespace.
  * Indenting nodes by `indentString`.
  * Colorizing the output to more easily identify elements if
    `color` is True or a color specification (see below).
  * Normalizing attribute rendering.
    TODO: that should include canonical ordering of attributes...

  :Parameters:

  strict : bool, default: true, optional
    If the input stream cannot be parsed by python's xml.dom.minidom,
    then if `strict` is True (the default), an exception is raised. If
    `strict` is False, then the input data is streamed to `output`
    as-is.

  indentString : str, default: '  ', optional
    The indentation to add to the output stream when entering into a
    sub-element. Note that this indentation is only added if it will
    remain "ignorable whitespace" according to the XML specification.

  color : bool, default: false, optional
    Whether or not to add *terminfo* terminal colorization sequences
    to add XML syntax highlighting, including element names, attribute
    names, and other XML syntax characters.

  encoding : str, default: 'UTF-8', optional
    Specify the encoding to use when rendering the XML. By default, it
    uses ``"UTF-8"``.

  :Returns:

  True
    the input stream was successfully converted.

  False
    a parsing error occurred and `strict` was False.

  Exception
    other errors (such as IOErrors) occurred.
  '''
  data = input.read()
  try:
    dom = xml.dom.minidom.parseString(data)
  except Exception:
    if strict:
      raise
    output.write(data)
    return False
  removeIgnorableWhitespace(dom)
  indentXml(dom, dom.documentElement, indentString)
  if color:
    return colorizeXml(dom, output, encoding=encoding, colorspec=color)
  xout = dom.toxml(encoding=encoding) + '\n'
  output.write(re.sub(r'^(<\?xml[^>]+?>)', '\\1\n', xout))
  return True

#------------------------------------------------------------------------------
class XmlTestMixin(object):
  def assertXmlEqual(self, xml1, xml2, msg=None):
    try:
      dom1 = xml.dom.minidom.parseString(xml1)
      dom2 = xml.dom.minidom.parseString(xml2)
    except Exception:
      return self.assertEqual(xml1, xml2, msg=msg)
    try:
      return self.assertEqual(dom1, dom2, msg=msg)
    except AssertionError:
      out1 = six.StringIO()
      out2 = six.StringIO()
      prettify(six.StringIO(xml1), out1)
      prettify(six.StringIO(xml2), out2)
      return self.assertMultiLineEqual(out1.getvalue(), out2.getvalue(), msg=msg)
  def assertNotXmlEqual(self, xml1, xml2, msg=None):
    try:
      self.assertXmlEqual(xml1, xml2)
      self.fail(msg or '%r == %r' % (xml1, xml2))
    except AssertionError: return

#------------------------------------------------------------------------------
def main(args=None):

  cli = argparse.ArgumentParser(
    usage='%(prog)s [options] [FILENAME | "-"]',
    description='Pretty-prints XML, nothing more :)',
    epilog='%(prog)s ' + lib.version,
    )

  cli.add_argument(
    '-s', '--strict',
    default=False, action='store_true',
    help='cause invalid XML to exit with an error rather than'
    ' just printing out the input data unaltered (default: %(default)s)')

  cli.add_argument(
    '-i', '--indent', metavar='STRING',
    default='  ', action='store',
    help='set the indentation string (default: two spaces)')

  cli.add_argument(
    '-c', '--color',
    default=False, action='store_true',
    help='colorize the XML output (default: %(default)s)')

  cli.add_argument(
    'filename', metavar='FILENAME',
    nargs='?',
    help='filename to parse; if not specified or "-", STDIN'
    ' is used instead')

  options = cli.parse_args(args)
  if options.filename is None or options.filename == '-':
    source = sys.stdin
  else:
    source = open(options.filename, 'rb')
  prettify(source, sys.stdout, options.strict, options.indent, options.color)
  return 0

#------------------------------------------------------------------------------
# end of $Id: pxml.py 346 2012-08-12 17:22:39Z griffin $
#------------------------------------------------------------------------------
