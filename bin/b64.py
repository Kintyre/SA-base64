#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

__version__ = "3.0.0"

import os
import sys
import math

from base64 import b64decode, b64encode

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))  # nopep8

from splunklib.searchcommands import dispatch, StreamingCommand, Configuration, Option, validators


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

        if self.action == "decode":
            fct = b64decode
        else:
            fct = b64encode

        if self.mode == "append":
            dest_field = self.field + "_base64"
        else:
            dest_field = self.field

        for event in records:

            if not self.field in event:
                continue

            try:

                if fct is b64encode:
                    # Convert to bytes if encode and the field is a string
                    if isinstance(event[self.field], str):
                        original = event[self.field].encode("utf-8")
                    else:
                        original = event[self.field]

                elif fct is b64decode:
                    # Fix padding
                    if self.fix_padding:
                        # Can't we just use modulus '%' here? Something like
                        #  s += "=" * (len(s) % 4)
                        original = event[self.field].ljust(
                            int(math.ceil(len(event[self.field]) / 4)) * 4, '=')
                    else:
                        original = event[self.field]

                ret = fct(original)

                # replace unprintable characters by their hexadecimal
                # representation. Example: \x00
                event[dest_field] = ""

                # This feels very "C" to me. Q: Is there a built-in encoding that will do this directly?
                for c in ret:
                    x = c
                    if c < ord(' ') or c > ord('~'):
                        if self.convert_newlines and c == 10:
                            x = "\n"
                        elif self.convert_newlines and c == 13:
                            x = "\r"
                        elif self.special_chars == "remove":
                            continue
                        elif self.special_chars == "hash":
                            x = "#"
                        elif self.special_chars == "star":
                            x = "*"
                        else:
                            x = "\\x" + "{0:02x}".format(c)
                    else:
                        x = chr(x)

                    event[dest_field] += x

            except Exception as e:
                if not self.suppress_error:
                    self.error_exit("Failure due to {}".format(e))

            yield event


if __name__ == '__main__':
    dispatch(B64Command, sys.argv, sys.stdin, sys.stdout, __name__)
