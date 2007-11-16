# -*- encoding: utf8 -*-
#
# Copyright (c) 2007 The PyAMF Project. All rights reserved.
# 
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

"""
Echo test client.

You can use this example with the echo test server.

@author: U{Thijs Triemstra<mailto:info@collab.nl>}
@author: U{Nick Joyce<mailto:nick@boxdesign.co.uk>}
"""

from pyamf import register_class

ECHO_NS = 'org.red5.server.webapp.echo'

class RemoteClass(object):
    """
    This class is mapped to a serverside Python class.
    """
    pass

class ExternalizableClass(object):
    """
    """
    pass

def read_ec(obj, input):
    """
    This function is invoked when the C{obj} needs to be unserialized.

    @type obj: L{ExternalizableClass}
    @param obj: The object in question.
    @param input: The input stream to read from
    @type input L{DataInput<pyamf.compat.DataInput>}
    """
    assert input.readBoolean() == True
    assert input.readBoolean() == False
    assert input.readByte() == 0
    assert input.readByte() == -1
    assert input.readByte() == 1
    assert input.readByte() == 127
    assert input.readByte() == -127
    assert input.readDouble() == 1.0
    assert input.readFloat() == 2.0
    assert input.readInt() == 0
    assert input.readInt() == -1
    assert input.readInt() == 1
    input.readMultiByte(7, 'iso-8859-1')
    input.readMultiByte(14, 'utf8')
    assert input.readObject() == [1, 'one', 1.0]
    assert input.readShort() == 0
    assert input.readShort() == -1
    assert input.readShort() == 1
    assert input.readUnsignedInt() == 0
    assert input.readUnsignedInt() == 1
    assert input.readUTF() == "Hello world!"
    assert input.readUTFBytes(12) == "Hello world!"

def write_ec(obj, output):
    """
    This function is invoked when the C{obj} needs to be serialized.

    @type obj: L{ExternalizableClass}
    @param obj: The object in question.
    @param input: The output stream to write to
    @type input L{DataOutput<pyamf.compat.DataOutput>}
    """
    output.writeBoolean(True)
    output.writeBoolean(False)
    output.writeByte(0)
    output.writeByte(-1)
    output.writeByte(1)
    output.writeByte(127)
    output.writeByte(-127)
    output.writeDouble(1.0)
    output.writeFloat(2.0)
    output.writeInt(0)
    output.writeInt(-1)
    output.writeInt(1)
    output.writeMultiByte(u"\xe4\xf6\xfc\xc4\xd6\xdc\xdf", 'iso-8859-1')
    output.writeMultiByte(u"\xe4\xf6\xfc\xc4\xd6\xdc\xdf", 'utf8')
    output.writeObject([1, 'one', 1])
    output.writeShort(0)
    output.writeShort(-1)
    output.writeShort(1)
    output.writeUnsignedInt(0)
    output.writeUnsignedInt(1)
    output.writeUTF("Hello world!")
    output.writeUTFBytes("Hello world!")

#: Map ActionScript class to Python class
register_class(RemoteClass, '%s.%s' % (ECHO_NS, 'RemoteClass'))
register_class(ExternalizableClass, '%s.%s' % (ECHO_NS, 'ExternalizableClass'),
    write_func=write_ec, read_func=read_ec)

def handleResult(data):
    """
    """    
    for res in data:
        print "Response:", res

    from twisted.internet import reactor
    reactor.stop()

def handleError(failure):
    """
    """
    print "Error:", failure.getErrorMessage()

    from twisted.internet import reactor
    reactor.stop()
        
if __name__ == '__main__':
    import sys
    from __init__ import parse_args, run_client

    options = parse_args(sys.argv[1:])
    
    service = {'echo':None}

    run_client('Echo Test', options[0], service, handleResult, handleError)
