# -*- coding: utf-8 -*-
#
# Author: Sebastian.Lopienski@cern.ch
#
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
from os import path
from optparse import OptionParser

from . import tools
from .clues import Clues
from .detection import TIMEOUT, Detector
from .group import group
from .output import JSONOutput, CSVOutput, HumanReadableOutput

output_format_map = {
    'csv': CSVOutput,
    'json': JSONOutput,
    'txt': HumanReadableOutput,
}

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, '__version__.py'), encoding='utf-8') as f:
    __version__ = f.read().strip()

try:
    pass
except Exception:
    print("Something went wrong with installation. Please reinstall again. If error continues, submit an issue at https://github.com/0xcrypto/fingerprint/issues")
    exit(1)


def main(timeout=TIMEOUT):
    desc = """fingerprintweb -
This component analyzes given URL(s) and detects technologies, libraries,
frameworks etc. used by this application, from the OS and web server level,
to the programming platform and frameworks, and server- and client-side
applications, tools and libraries. For example: OS=Linux, webserver=Apache,
platform=PHP, cms=Drupal, analytics=Google Analytics, javascript-lib=jQuery
etc."""

    parser = OptionParser(description=desc,
                          usage="Usage: %prog -u <URLs|@URLfile>\nHelp:  %prog -h",
                          version="%prog " + __version__)

    parser.add_option("-u", "--url", dest="urls", metavar="URLS|@FILE",
                      help="list of URLs (comma-separated), or a file with a list of URLs (one per line)")

    parser.add_option("-l", "--limit", dest="limit", metavar="URLMASK",
                      help="in case of redirections, only include pages with URLs matching this mask - "
                           "e.g. 'https?://[^/]*\\.abc\\.com/'")

    parser.add_option("-x", "--exclude", dest="exclude", metavar="URLMASK",
                      help="in case of redirections, exclude pages with URL matching this mask - "
                           "e.g. 'https?://[^/]*/(login|logout)'")

    parser.add_option("-o", "--output", dest="output_file", metavar="FILE",
                      help="output file for detection results (default: STDOUT)")

    parser.add_option("-c", "--clues", dest="clues_file", metavar="FILE", default=None,
                      help="clues for detecting web applications and technologies")

    parser.add_option("-t", "--timeout", action="store", dest="TIMEOUT", default=timeout,
                      help="set timeout (in seconds) for accessing a single URL")

    parser.add_option("-f", "--format", action="store", dest="format", default='json',
                      help="output format, allowed values: csv, txt, json (default)")

    parser.add_option("-g", "--group", action="store_true", dest="group", default=False,
                      help="group results (i.e. technologies found on subpages of other scanned URL "
                           "aren't listed)")

    tools.add_log_options(parser)

    options = parser.parse_args()[0]

    tools.use_log_options(options)

    if not options.urls:
        parser.error("Argument -u missing")
        return

    timeout = int(options.TIMEOUT)

    if options.urls[0] == "@":
        try:
            f = open(options.urls[1:])
            urls = f.readlines()
            f.close()
        except Exception as e:
            # an I/O exception?
            logging.error("Error reading URL file %s, terminating: %s", options.urls[1:], tools.error_to_str(e))
            return
    else:
        urls = [x.strip() for x in options.urls.split(",") if x.strip() != ""]

    if options.format not in output_format_map.keys():
        parser.error("Invalid format specified")
        return

    Clues.get_clues(options.clues_file)

    results = Detector().detect_multiple(urls, limit=options.limit, exclude=options.exclude, timeout=timeout)

    if options.group:
        results = group(results)

    output = output_format_map[options.format]().retrieve(results=results)

    if options.output_file:
        try:
            f = open(options.output_file, "w")
            f.write(output)
            f.close()
            logging.debug("Results written to file %s", options.output_file)
        except Exception as e:
            # an I/O exception?
            logging.error("Error writing results to file %s, terminating: %s", options.output_file,
                          tools.error_to_str(e))
            return

    print(output)


if __name__ == "__main__":
    main()
