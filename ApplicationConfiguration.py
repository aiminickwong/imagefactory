#!/usr/bin/env python
# encoding: utf-8

# Copyright (C) 2010 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301, USA.  A copy of the GNU General Public License is
# also available at http://www.gnu.org/copyleft/gpl.html.

import os
import argparse
import json

class ApplicationConfiguration(object):
    instance = None
    
    def configuration():
        doc = "The configuration property."
        def fget(self):
            return self._configuration
        def fset(self, value):
            self._configuration = value
        def fdel(self):
            del self._configuration
        return locals()
    configuration = property(**configuration())
    
    def arguments():
        doc = "The arguments property."
        def fget(self):
            return self._arguments
        def fset(self, value):
            self._arguments = value
        def fdel(self):
            del self._arguments
        return locals()
    arguments = property(**arguments())
    
    
    def __new__(cls, *p, **k):
        if cls.instance is None:
            cls.instance = object.__new__(cls, *p, **k)
        return cls.instance
    
    def __init__(self):
        super(ApplicationConfiguration, self).__init__()
        self.configuration = {}
        self.arguments = self.parse_arguments()
        
        if (self.arguments):
            config_file_path = self.arguments.config
            if (os.path.isfile(config_file_path)):
                try:
                    config_file = open(config_file_path)
                    self.configuration = json.load(config_file)
                except IOError, e:
                    logging.exception(e)
            argdict = self.arguments.__dict__
            for key in argdict.keys():
                self.configuration[key] = argdict[key]
    
    def parse_arguments(self):
        argparser = argparse.ArgumentParser(description='System image creation tool...', prog='imagefactory')
        argparser.add_argument('--version', action='version', version='%(prog)s 0.1', help='Version info')
        argparser.add_argument('-v', '--verbose', action='store_true', default=False, help='Set verbose logging.')
        argparser.add_argument('--debug', action='store_true', default=False, help='Set really verbose logging for debugging.')
        argparser.add_argument('--config', default='/etc/imagefactory.conf', help='Configuration file to use. (default: %(default)s)')
        argparser.add_argument('--output', default='/tmp', help='Build image files in location specified. (default: %(default)s)')
        argparser.add_argument('--warehouse', help='URL of the warehouse location to store images.')
        subparsers = argparser.add_subparsers(dest='command', title='commands')
        command_qmf = subparsers.add_parser('qmf', help='Provide a QMFv2 agent interface.')
        command_qmf.add_argument('--broker', default='localhost', help='URL of qpidd to connect to. (default: %(default)s)')
        command_build = subparsers.add_parser('build', help='NOT YET IMPLEMENTED: Build specified system and exit.')
        command_build.add_argument('--template', help='Template file to build from.')
        return argparser.parse_args()
    
