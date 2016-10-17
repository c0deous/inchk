# Inchk

Inchk (Internet Check) is a small utility written in python that quickly checks the scope of your network access.  The only dependency is Pyping (pip install pyping, apt-get install python-pyping)

Logic Path:
   Test Main Host (google.com default) 
   if failed then...
     Test Main DNS (8.8.8.8 default)
     if fails then...
       lookup gateway and attempt to ping...
       if fails then...
         You are not connected to a functional LAN network

In the future there will be a working -f option that will test a secondary set of hostnames and IP addresses.  I find that the default test is sufficient.

Copyright 2016 Jesse Wallace (@c0deous) - business@c0deo.us

This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

 
