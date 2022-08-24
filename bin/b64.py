#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

__version__ = "3.1.1"

import os
import sys
import re
import binascii
import codecs

from base64 import b64decode, b64encode

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))  # nopep8

from splunklib.searchcommands import dispatch, StreamingCommand, Configuration, Option, validators


def hash_errors(exc):
    return "#", exc.end


def star_errors(exc):
    return "*", exc.end


codecs.register_error("replace_hash", hash_errors)
codecs.register_error("replace_star", star_errors)


def decode_base64(data, altchars='+/'):
    # Inspired from https://stackoverflow.com/a/9807138
    #               https://stackoverflow.com/a/2942127
    data = re.sub(r'[^a-zA-Z0-9%s]+' % altchars, "", data)  # normalize
    missing_padding = len(data) % 4
    if missing_padding:
        data += '=' * (4 - missing_padding)
    try:
        return b64decode(data, altchars)
    except binascii.Error:
        # Dropping last character and try again
        lens = len(data) - 1
        lenx = lens - lens % (4 if lens % 4 else 4)
        return b64decode(data[:lenx], altchars)


@Configuration()
class B64Command(StreamingCommand):
    """
    Encode a string to Base64
    Decode a Base64 content

     | base64 [action=(encode|decode)] field=<field> [mode=(replace|append)] [special_chars=(keep|remove|hash)]
     """

    field = Option(
        name='field',
        require=True)
    action = Option(
        name='action',
        require=False,
        default="encode")
    mode = Option(
        name='mode',
        require=False,
        default="replace")
    encoding = Option(
        name="encoding",
        require=False,
        default="utf-8")
    special_chars = Option(
        name='special_chars',
        require=False,
        default="keep")
    convert_newlines = Option(
        name='convert_newlines',
        require=False,
        default=True,
        validate=validators.Boolean())
    fix_padding = Option(
        name='fix_padding',
        require=False,
        default=True,
        validate=validators.Boolean())
    suppress_error = Option(
        name='suppress_error',
        require=False,
        default=False,
        validate=validators.Boolean())

    def stream(self, records):
        """ Streaming function that processes and yields event records 1:1 to
        the Splunk stream pipeline, in the same order as received.
        """

        if self.special_chars == "remove":
            errors = "replace"
        elif self.special_chars == "hash":
            errors = "replace_hash"
        elif self.special_chars == "star":
            errors = "replace_star"
        else:
            # replace unprintable characters by their hexadecimal
            # representation. Example: \x00
            errors = "backslashreplace"

        if self.action == "decode":
            def fct(s):
                # Detect URL-safe base64 encodings
                if "-" in s or "_" in s:
                    alt_chars = "-_"
                else:
                    alt_chars = "+/"
                # Fix padding
                if self.fix_padding:
                    s = decode_base64(s, alt_chars)
                else:
                    s = b64decode(s, alt_chars)
                return s.decode(self.encoding, errors=errors)
        else:
            def fct(s):
                if isinstance(s, str):
                    # Convert to bytes if encode and the field is a string
                    s = s.encode(self.encoding)
                # Splunk always sends data to us in UTF-8
                return b64encode(s).decode("utf-8")

        if self.mode == "append":
            dest_field = self.field + "_base64"
        else:
            dest_field = self.field

        for event in records:
            if not self.field in event:
                # Keep event (unmodified)
                yield event
                continue

            try:
                ret = fct(event[self.field])

                if not self.convert_newlines:
                    ret = ret.replace("\n", "\\n").replace("\r", "\\r")
                event[dest_field] = ret

            except Exception as e:
                if self.suppress_error:
                    # Put exception in the destination field so that the error isn't completely silent
                    event[dest_field] = "Exception: {}".format(e)
                else:
                    self.error_exit(e, "Failure due to {}".format(e))

            yield event


if __name__ == '__main__':
    dispatch(B64Command, sys.argv, sys.stdin, sys.stdout, __name__)
