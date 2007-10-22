# -*- encoding: utf-8 -*-
#
# Copyright (c) 2007 The PyAMF Project. All rights reserved.
# 
# Arnar Birgisson
# Thijs Triemstra
# Nick Joyce
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import unittest

import pyamf
from pyamf import amf0, util

class TypesTestCase(unittest.TestCase):
    def test_types(self):
        self.assertEquals(amf0.ASTypes.NUMBER, 0x00)
        self.assertEquals(amf0.ASTypes.BOOL, 0x01)
        self.assertEquals(amf0.ASTypes.STRING, 0x02)
        self.assertEquals(amf0.ASTypes.OBJECT, 0x03)
        self.assertEquals(amf0.ASTypes.MOVIECLIP, 0x04)
        self.assertEquals(amf0.ASTypes.NULL, 0x05)
        self.assertEquals(amf0.ASTypes.UNDEFINED, 0x06)
        self.assertEquals(amf0.ASTypes.REFERENCE, 0x07)
        self.assertEquals(amf0.ASTypes.MIXEDARRAY, 0x08)
        self.assertEquals(amf0.ASTypes.OBJECTTERM, 0x09)
        self.assertEquals(amf0.ASTypes.ARRAY, 0x0a)
        self.assertEquals(amf0.ASTypes.DATE, 0x0b)
        self.assertEquals(amf0.ASTypes.LONGSTRING, 0x0c)
        self.assertEquals(amf0.ASTypes.UNSUPPORTED, 0x0d)
        self.assertEquals(amf0.ASTypes.RECORDSET, 0x0e)
        self.assertEquals(amf0.ASTypes.XML, 0x0f)
        self.assertEquals(amf0.ASTypes.TYPEDOBJECT, 0x10)
        self.assertEquals(amf0.ASTypes.AMF3, 0x11)

class GenericObject(object):
    def __init__(self, dict):
        self.__dict__ = dict

    def __cmp__(self, other):
        return cmp(self.__dict__, other)

class EncoderTester(object):
    """
    A helper object that takes some input, runs over the encoder and checks
    the output
    """

    def __init__(self, encoder, data):
        self.encoder = encoder
        self.buf = encoder.output
        self.data = data

    def getval(self):
        t = self.buf.getvalue()
        self.buf.truncate(0)

        return t

    def run(self, testcase):
        for n, s in self.data:
            self.encoder.writeElement(n)

            testcase.assertEqual(self.getval(), s)

class EncoderTestCase(unittest.TestCase):
    """
    Tests the output from the Encoder class.
    """

    def setUp(self):
        self.buf = util.BufferedByteStream()
        self.e = amf0.Encoder(self.buf)

    def _run(self, data):
        e = EncoderTester(self.e, data)
        e.run(self)

    def test_number(self):
        data = [
            (0,    '\x00\x00\x00\x00\x00\x00\x00\x00\x00'),
            (0.2,  '\x00\x3f\xc9\x99\x99\x99\x99\x99\x9a'),
            (1,    '\x00\x3f\xf0\x00\x00\x00\x00\x00\x00'),
            (42,   '\x00\x40\x45\x00\x00\x00\x00\x00\x00'),
            (-123, '\x00\xc0\x5e\xc0\x00\x00\x00\x00\x00'),
            (1.23456789, '\x00\x3f\xf3\xc0\xca\x42\x83\xde\x1b')]

        # XXX nick: Should we be testing python longs here?

        self._run(data)

    def test_boolean(self):
        data = [
            (True, '\x01\x01'),
            (False, '\x01\x00')]

        self._run(data)

    def test_string(self):
        data = [
            ('', '\x02\x00\x00'),
            ('hello', '\x02\x00\x05hello'),
            # unicode taken from http://www.columbia.edu/kermit/utf8.html
            (u'ᚠᛇᚻ', '\x02\x00\t\xe1\x9a\xa0\xe1\x9b\x87\xe1\x9a\xbb')]

        self._run(data)

    def test_null(self):
        data = [(None, '\x05')]

        self._run(data)

    def test_list(self):
        data = [
            ([], '\x0a\x00\x00\x00\x00'),
            ([1, 2, 3], '\x0a\x00\x00\x00\x03\x00\x3f\xf0\x00\x00\x00\x00\x00'
                '\x00\x00\x40\x00\x00\x00\x00\x00\x00\x00\x00\x40\x08\x00\x00'
                '\x00\x00\x00\x00'),
            ((1, 2, 3), '\x0a\x00\x00\x00\x03\x00\x3f\xf0\x00\x00\x00\x00\x00'
                '\x00\x00\x40\x00\x00\x00\x00\x00\x00\x00\x00\x40\x08\x00\x00'
                '\x00\x00\x00\x00')]

        self._run(data)

    def test_longstring(self):
        self._run([('a' * 65537, '\x0c\x00\x01\x00\x01' + 'a' * 65537)])

    def test_dict(self):
        self._run([
            ({'a': 'a'}, '\x08\x00\x00\x00\x00\x00\x01\x61\x02\x00\x01\x61\x00'
                '\x00\x09'),
            ({1: 1, 2: 2, 3: 3}, '\x08\x00\x00\x00\x03\x00\x01\x31\x00\x3f\xf0'
                '\x00\x00\x00\x00\x00\x00\x00\x01\x32\x00\x40\x00\x00\x00\x00'
                '\x00\x00\x00\x00\x01\x33\x00\x40\x08\x00\x00\x00\x00\x00\x00'
                '\x00\x00\x09')])

    def test_date(self):
        import datetime, time

        self._run([
            (datetime.datetime(1999, 9, 9), '\x0b\x42\x35\xcf\xf3\x93\xc0\x00'
                '\x00\x00\x00')])

    # TODO testing for timezones

    def test_xml(self):
        self._run([
            (util.ET.fromstring('<a><b>hello world</b></a>'), '\x0f\x00\x00'
                '\x00\x3f<?xml version=\'1.0\' encoding=\'utf8\'?>\n<a><b>'
                'hello world</b></a>')])

    def test_unsupported(self):
        self._run([
            (ord, '\x0d')])

    def test_object(self):
        self._run([
            (GenericObject({'a': 'b'}),
                '\x03\x00\x01a\x02\x00\x01b\x00\x00\x09')])

class ParserTester(object):
    """
    A helper object that takes some input, runs over the parser and checks
    the output
    """

    def __init__(self, parser, data):
        self.parser = parser
        self.buf = parser.input
        self.data = data

    def getval(self):
        t = self.buf.getvalue()
        self.buf.truncate(0)

        return t

    def run(self, testcase):
        for n, s in self.data:
            self.buf.truncate(0)
            self.buf.write(s)
            self.buf.seek(0)

            testcase.assertEqual(self.parser.readElement(), n)

class ParserTestCase(unittest.TestCase):
    def setUp(self):
        self.buf = util.BufferedByteStream()
        self.parser = amf0.Parser()
        self.parser.input = self.buf

    def _run(self, data):
        e = ParserTester(self.parser, data)
        e.run(self)

    def test_types(self):
        for x in amf0.ACTIONSCRIPT_TYPES:
            self.buf.write(chr(x))
            self.buf.seek(0)
            self.parser.readType()
            self.buf.truncate(0)

        self.buf.write('x')
        self.buf.seek(0)
        self.assertRaises(pyamf.ParseError, self.parser.readType)

    def test_number(self):
        self._run([
            (0,    '\x00\x00\x00\x00\x00\x00\x00\x00\x00'),
            (0.2,  '\x00\x3f\xc9\x99\x99\x99\x99\x99\x9a'),
            (1,    '\x00\x3f\xf0\x00\x00\x00\x00\x00\x00'),
            (42,   '\x00\x40\x45\x00\x00\x00\x00\x00\x00'),
            (-123, '\x00\xc0\x5e\xc0\x00\x00\x00\x00\x00'),
            (1.23456789, '\x00\x3f\xf3\xc0\xca\x42\x83\xde\x1b')])

    def test_boolean(self):
        self._run([
            (True, '\x01\x01'),
            (False, '\x01\x00')])

    def test_string(self):
        self._run([
            ('', '\x02\x00\x00'),
            ('hello', '\x02\x00\x05hello'),
            (u'ᚠᛇᚻ', '\x02\x00\t\xe1\x9a\xa0\xe1\x9b\x87\xe1\x9a\xbb')])

    def test_longstring(self):
        self._run([('a' * 65537, '\x0c\x00\x01\x00\x01' + 'a' * 65537)])

    def test_null(self):
        self._run([(None, '\x05')])

    def test_list(self):
        # XXX no obvious way to convert back to sets here
        self._run([
            ([], '\x0a\x00\x00\x00\x00'),
            ([1, 2, 3], '\x0a\x00\x00\x00\x03\x00\x3f\xf0\x00\x00\x00\x00\x00'
                '\x00\x00\x40\x00\x00\x00\x00\x00\x00\x00\x00\x40\x08\x00\x00'
                '\x00\x00\x00\x00')])

    def test_dict(self):
        self._run([
            ({'a': 'a'}, '\x08\x00\x00\x00\x00\x00\x01\x61\x02\x00\x01\x61\x00'
                '\x00\x09'),
            ({1: 1, 2: 2, 3: 3}, '\x08\x00\x00\x00\x03\x00\x01\x31\x00\x3f\xf0'
                '\x00\x00\x00\x00\x00\x00\x00\x01\x32\x00\x40\x00\x00\x00\x00'
                '\x00\x00\x00\x00\x01\x33\x00\x40\x08\x00\x00\x00\x00\x00\x00'
                '\x00\x00\x09')])

    def test_date(self):
        import datetime, time

        self._run([
            (datetime.datetime(1999, 9, 9), '\x0b\x42\x35\xcf\xf3\x93\xc0\x00'
                '\x00\x00\x00')])

    # TODO testing for timezones

    def test_xml(self):
        self.buf.truncate(0)
        self.buf.write('\x0f\x00\x00\x00\x19<a><b>hello world</b></a>')
        self.buf.seek(0)

        self.assertEquals(
            util.ET.tostring(util.ET.fromstring('<a><b>hello world</b></a>')),
            util.ET.tostring(self.parser.readElement()))

    def test_object(self):
        self._run([
            (GenericObject({'a': 'b'}),
                '\x03\x00\x01a\x02\x00\x01b\x00\x00\x09')])

def suite():
    suite = unittest.TestSuite()

    suite.addTest(unittest.makeSuite(TypesTestCase, 'test'))
    suite.addTest(unittest.makeSuite(EncoderTestCase, 'test'))
    suite.addTest(unittest.makeSuite(ParserTestCase, 'test'))

    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
