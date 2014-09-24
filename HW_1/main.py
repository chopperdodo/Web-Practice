#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import webapp2
import cgi

body = """
<html>
    <head>
        <title> Rot 13 </title>
    </head>
    <body>
        <h2> Enter some text to ROT13: </h2>
        <form method="post">
            <textarea name="text" style="height: 100px; width:500px;">%(usr_in)s</textarea>
            <br>
            <input type="submit" value="submit">
        </form>
        <br>
        <div>%(error)s</div>
    </body>
</html>
"""

class MainHandler(webapp2.RequestHandler):

    def get(self):
        self.report2usr("", "")
    def post(self):
        text_in = self.request.get('text')

        # if input is null
        if not text_in:
            self.report2usr("Input is null", "")
        else:
            self.report2usr("", text_in)

    def start_rot(self, text):
        str_len = len(text)
        text = list(text)
        for i in range(0, str_len):
            asc_c = ord(text[i])
            # c is in ["A", "Z"]
            if (asc_c >= 65 and asc_c <= 90):
                asc_c = (asc_c + 13 - 65) % 26 + 65
            elif (asc_c >= 97 and asc_c <= 122):
                asc_c = (asc_c + 13 - 97) % 26 + 97
            text[i] = chr(asc_c)
        text = ''.join(text)
        return text

    def report2usr(self, error="", usr_in=""):
        error = cgi.escape(error, quote = True)

        if not error:
            usr_in = self.start_rot(usr_in)

        usr_in = cgi.escape(usr_in, quote = True)

        self.response.write(body % {'error': error,
                                    'usr_in': usr_in})


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
