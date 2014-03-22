Adding Reflection to C++ with Python
####################################
:date: 2014-03-22 10:01
:author: Anthony Scopatz
:category: missives
:slug: adding-reflection-to-cpp

Or, Write a C++ Pre-Processor
==============================

.. note:: This post is mostly about how to write beautiful and intuitive interfaces
          in an atangonistic environment.

My main job these days is to be the benevolant dictator, fearless leader, and 
l'regexer extrodinaire for the `Cyclus fuel cycle simulator <http://fuelcycle.org>`_. 
In addition to being a general solver for the nuclear fuel cycle we have the 
additional design constraints that 3rd parties must be able to write their own 
dynamically loadable agent models (as in *agent-based*) in C++ and user input files
in XML must be validated using RelaxNG. This is not the software stack I would have 
chosen - challenge accepted(?).

Simulation code has a lot of competing concerns:

1. provide a kernel for solving a problem that performs 'well enough',
2. be modifiable and extensibilable to non-kernel developers, 
3. report results in a well-defined & inspectable way, and finally
4. easy and concise to use.

Failure on any of these implies overall effective failure.  Or the contra-positive, 
Overall success means the simulator is great at all of these!

Since (1) is domain specific, let's assume that a solution exists.  Requirement (2)
implies that there must be a formal public API into the kernel so that other people
can come in and add their piece to the puzzle.  Fine.  Requirement (4) say to make
that interface beautiful. Great. I wouldn't want to use an ugly API anyway. But then
along comes persistance (3) and you realize that to have your public API just got a 
lot more complicated and that users now have to make calls into the persistance 
infrastructe manually. Also that exercise exposed the fact that some of the APIs in
you wrote were probably not as extensible as you thought and need to be broadened
(ie made more complex).  At this point you have lost most sane users because it is 
not clear what they get by using your simulator. It it probably easier to roll their
own rather than interface with yours.

At this point why is it is easier for people to write their own simulator than use 
yours? For every action that you want to support in the core (saving, loading, 
validation, any problem setup steps) you now have to have a top-level API that 
model developer *must* use.  However, in the typical case they'll only want a 
small subset of these and would like to rely on default behaviour otherwise. 
Furthermore, for the API to be dynamic now the user has to pass around meta-data
information (type, default values, units, etc.) about each state variable to each 
top-level function.  This becomes very tedious and error-prone.

`Reflection <http://en.wikipedia.org/wiki/Reflection_(computer_programming)>`_ 
solves a lot of these problems. Roughly speaking reflection is the property 
that allows types to introspect themselves *at runtime*. From the core simulators
perspective this is great because it allows the core to ask 3rd party maodules what 
they think that they are.  **Unfortnately, most strongly typed languages lack reflection.**

Use That Other Language
=======================
Since we can't make C/C++ have reflection, we can fake it by using the preprocesor!
The whole point of the C preprocessor (``cpp``) is to modify how language it is 
processing works. We can just add some reflection macros that generate all of the 
nasty repeated code bits. Problem solved!  Now we can go back to sipping our Country 
Time lemonade at the pi day party.

Except! Like Eminem in 8-mile you only get one shot since ``cpp`` is one-pass. 
So you can't add reflection with the preproccessor either. You'd need the preprocessor 
to go through the code multiple times for any suite of reflection macros to work.
Snap back to reality.

Tepidly Step into Code Generation
=================================
At this point it is very tempting to start creating a template language that 
looks mostly like C++, has the reflection that is desired, and compiles down
to C++.  

However, defining custom domain-specific languages (DSLs) is its own headache
because you - now and forever - have to support a custom language that you 
invented and there is no external support for.  Your language won't be on 
Stack overflow.

The Pragma Trick
================
It turns out that part of the ``cpp`` language spec are hooks that let you 
write your own preproccessors! The preproccessor will ignore, but still include, 
any ``#pragma`` that it doesn't understand.  These will pass through the 
preproccessor.  Pick a token that no one else will ever use - such as your project
name. 

**The prime directive:**

.. code-block:: c++

    #pragma cyclus

Only the first token (``cyclus``) is matched by normal ``cpp`` to determine if
it is a known pragma.  This is great, because you can then add arguments to
it.  

**State variable annotation:**

.. code-block:: c++

    #pragma cyclus var {"default": 42.0}
    double flux;

Now you can go through your the code as many times you need, accumulating state & 
annotations, and interting whatever C++ code needs to be generated elsewhere.
This let's user write fully compatible and compilable C++ code that can hook into
your simulation or not!

Python & cycpp
==============
We have chosen to write the cyclus preprocessor (``cycpp``) in Python - though 
truly it could have been written in any language.  Writing it in Python gave us
access to some awesome parts of the Python interpreter. 

You may have noticed that the variable annotations above look a lot like a 
Python dictionary.  That is because they are!  (Or more generally, they are 
any expression which evaluates to a mapping.  Most JSON is valid here too.)
This is awesome.  This means that not even our annotations exist in their own
DSL.  Every part of simulator is valid in a language that we are not the sole
proprieters of.  If a 3rd party developer has already gone through the process
of learning C++ to add a model to our simulator, learning Python dictionaries
is not a barrier to entry.

Furthermore, since these 

