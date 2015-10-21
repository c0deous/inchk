Inchk (Internet Check) is a small utility written in python that quickly checks your network access.  The only dependency is ANSI enabled (which should be default on linux).
It takes the following steps to determine your network access
Ping Main Host (google.com default) 
if failed then...
Ping Main DNS (8.8.8.8 default)
if Main DNS ping succeeds then...
confirm by resolving with nslookup...
if Main DNS ping fails then...
lookup gateway and attempt to ping...
if fails...
You are not connected to a functional network

In the future there will be a working -f option that will ping secondary hostnames and IP addresses.  I find that the default test is sufficient.

Copyright 2015 Jesse Wallace
c0deous.business@gmail.com

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

 
