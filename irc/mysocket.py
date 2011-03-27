#!/usr/bin/env python2.6
# Zeckviz IRC bot
# Copyright (C) 2011 Bruno Rahle
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import socket

class MySocket(socket.socket):
    """Extends socket.socket class and adds the functionality to reads the data
    from socket line by line.
    """
    BUFFER_SIZE = 4096      # size of the buffer to read

    def __init__(self, host, port):
        """Creates the socket.
        """
        super(MySocket, self).__init__()
        self.connect((host, port))
        self._buffer = ''
        self._pos = 0

    def readline(self):
        """Reads the next line from the socket.
        NOTE: Ignores the timeout and blocking status. It just waits for the
        complete line to be sent to the socket and returns it.

        TODO: account for timeout and blocking status.
        """
        line = ''
        i = 0
        while True:
            while (self._pos == len(self._buffer)):
                self._buffer = self.recv(self.BUFFER_SIZE)
                self._pos = 0
            end = self._buffer.find('\n', self._pos)
            line = line + self._buffer[self._pos:end]
            if end == -1:
                self._pos = len(self._buffer)
            else:
                self._pos = end + 1
                return line

