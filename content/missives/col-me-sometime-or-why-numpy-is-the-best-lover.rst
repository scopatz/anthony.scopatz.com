Col Me Sometime (or Why NumPy is the Best Lover)
################################################
:date: 2010-11-25 13:26
:author: Anthony Scopatz
:tags: table4one
:slug: col-me-sometime-or-why-numpy-is-the-best-lover

Whether you know, or care, most database software has hard coded limits
on the number of columns that you can store in a single table.

Often, if you hit this limit for some reason, it indicates that 'you are
doing it wrong.'  However, this is not always the case.

For instance, say you want to store some information that is a function
of isotope.  Well, exist some 3000+ nuclides that are known to exist in
nature.  If you want to store this data in a single table and your
database allows 4096 columns per table, you are in luck!  However, if
you go down by a single power of two, there are only 2048 columns per
table and you are in trouble.

Below is a list of different table structures and their implicit table
limits:

-  `MySQL 5`_: 4,096
-  `MSSQL`_: 1,024
-  `Oracle`_: 1,000
-  `Excel 2003`_: 256
-  `Excel 2007`_: ﻿16,384
-  `HDF5`_: ~1,260
-  NumPy: +inf

That's right; NumPy structured (or record) arrays seem to allow as many
columns as you can fit into memory!  Below is some code that
demonstrates this.  I tested it up to a million columns, but I am
certain that it could handle a few more orders of magnitude.

This situation is peculiar since traditional databases are limited by
disk size, not memory, like NumPy.  (HDDs, of course, being much larger
than RAM.)

--- Go to the Source ---

import numpy as np

| import uuid
|  from random import sample, randint
|  population = [int, float, 'S']

def rand\_dtype(n):

| dt = []    for i in xrange(n):
|  dt.extend( [(str(uuid.uuid1()), np.dtype(d)) for d in
sample(population, 1)] )
|  dt = np.dtype(dt)
|  return dt

if \_\_name\_\_ == "\_\_main\_\_":

| dt = rand\_dtype(1000000)
|  z = np.zeros(10, dtype=dt)﻿

.. _MySQL 5: http://dev.mysql.com/doc/refman/5.0/en/column-count-limit.html
.. _MSSQL: http://msdn.microsoft.com/en-us/library/ms143432.aspx
.. _Oracle: http://download.oracle.com/docs/cd/B19306_01/server.102/b14237/limits003.htm
.. _Excel 2003: http://office.microsoft.com/en-us/excel-help/excel-specifications-and-limits-HP005199291.aspx
.. _Excel 2007: http://office.microsoft.com/en-us/excel-help/excel-specifications-and-limits-HP010073849.aspx
.. _HDF5: http://www.hdfgroup.org/hdf5-quest.html#dtcmpmaxfld
