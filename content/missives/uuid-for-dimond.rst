UUID for #include Diamond Problem 
=================================

:slug: uuid-fordimond
:date: 2012-06-22
:author: Anthony Scopatz

*This was originally published at* `inSCIght <http://inscight.org/2012/06/22/uuid-for-diamond/>`_.

Hello scientists!  Sorry it has been a while since we posted.  
We promise that there are episodes in the pipeline, coming soon to 
an eardrum near you!

In the meantime, if you have ever programmed in C/C++ you are well aware of the 
`#include diamond problem <href="http://en.wikipedia.org/wiki/Diamond_problem>`_.
Basically you can't have the same binary include the same header file twice, 
even if that include is implicit and somewhere father up the build tree 
(see the below figure).

.. figure:: http://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Diamond_inheritance.svg/200px-Diamond_inheritance.svg.png
    :width: 200
    :height: 300
    :align: center

    via wikipedia

The way many get around this is by creating #ifndef XXX - #def XXX - #endif 
blocks around all of their header files.  The prevents the XXX from being 
included more than once no matter what.  Most people use a system for naming 
XXX that is based on the project name and the file name.  However, the value of 
XXX could be anything.  *Anything*.

So my good friend, coworker at the FLASH center, and brilliant programmer John Bachan apparently just started using universally unique identifiers (UUIDs) for XXX years ago.  This is brilliant on so many levels.  He even has a bash one-liner for helping him out here.  For your aliasing pleasure:

.. code-block:: bash

    (id="_$(uuidgen|tr \\- _)";echo "#ifndef $id";echo "#define $id";echo "#endif")

will return, for example,

.. code-block:: C++

    #ifndef _7db3e753_0d81_43ea_beca_68a77189e28d
    #define _7db3e753_0d81_43ea_beca_68a77189e28d
    #endif

Feel free to thank me later...
