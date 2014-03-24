Adding Reflection to C++ with Python
####################################
:date: 2014-03-22 10:01
:author: Anthony Scopatz
:category: missives
:slug: adding-reflection-to-cpp

Or, Write a C++ Pre-Processor
==============================

.. note:: This post is mostly about how to write beautiful and intuitive interfaces
          in an antagonistic environment.

My main job these days is to be the benevolent dictator, fearless leader, and 
l'regexer extrodinaire for the `Cyclus fuel cycle simulator <http://fuelcycle.org>`_. 
In addition to being a general solver for the nuclear fuel cycle we have the 
additional design constraints that 3rd parties must be able to write their own 
dynamically loadable agent models (as in *agent-based*) in C++ and user input files
in XML must be validated using RelaxNG. This is not the software stack I would have 
chosen - challenge accepted(?).

Simulation code has a lot of competing concerns:

1. provide a kernel for solving a problem that performs 'well enough',
2. be modifiable and extensible to non-kernel developers, 
3. report results in a well-defined & inspectable way, and finally
4. easy and concise to use.

Failure on any of these implies overall effective failure.  Or the contra-positive, 
Overall success means the simulator is great at all of these!

Since (1) is domain specific, let's assume that a solution exists.  Requirement (2)
implies that there must be a formal public API into the kernel so that other people
can come in and add their piece to the puzzle.  Fine.  Requirement (4) say to make
that interface beautiful. Great. I wouldn't want to use an ugly API anyway. But then
along comes persistence (3) and you realize that to have your public API just got a 
lot more complicated and that users now have to make calls into the persistence 
infrastructure manually. Also that exercise exposed the fact that some of the APIs in
you wrote were probably not as extensible as you thought and need to be broadened
(ie made more complex).  At this point you have lost most sane users because it is 
not clear what they get by using your simulator. It it probably easier to roll their
own rather than interface with yours.

At this point why is it is easier for people to write their own simulator than use 
yours? For every action that you want to support in the core (saving, loading, 
validation, any problem setup steps) you now have to have a top-level API that 
model developer *must* use.  However, in the typical case they'll only want a 
small subset of these and would like to rely on default behavior otherwise. 
Furthermore, for the API to be dynamic now the user has to pass around meta-data
information (type, default values, units, etc.) about each state variable to each 
top-level function.  This becomes very tedious and error-prone.

`Reflection <http://en.wikipedia.org/wiki/Reflection_(computer_programming)>`_ 
solves a lot of these problems. Roughly speaking reflection is the property 
that allows types to introspect themselves *at runtime*. From the core simulators
perspective this is great because it allows the core to ask 3rd party modules what 
they think that they are.  **Unfortunately, most strongly typed languages lack reflection.**

Use That Other Language
=======================
Since we can't make C/C++ have reflection, we can fake it by using the preprocessor!
The whole point of the C preprocessor (``cpp``) is to modify how language it is 
processing works. We can just add some reflection macros that generate all of the 
nasty repeated code bits. Problem solved!  Now we can go back to sipping our Country 
Time lemonade at the pi day party.

Except! Like Eminem in 8-mile you only get one shot since ``cpp`` is one-pass. 
So you can't add reflection with the preprocessor either. You'd need the preprocessor 
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
write your own preprocessors! The preprocessor will ignore, but still include, 
any ``#pragma`` that it doesn't understand.  These will pass through the 
preprocessor.  Pick a token that no one else will ever use - such as your project
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
annotations, and inserting whatever C++ code needs to be generated elsewhere.
This let's user write fully compatible and compilable C++ code that can hook into
your simulation or not!

Python & cycpp
==============
We have chosen to write the cyclus preprocessor (``cycpp``) in Python - though 
truly it could have been written in any language.  Writing it in Python gave us
access to some awesome parts of the Python interpreter. 

You may have noticed that the variable annotations above look a lot like a 
Python dictionary.  That is because they are! (Or more generally, they are 
any expression which evaluates to a mapping.  Most JSON is valid here too.)
This is awesome.  This means that not even our annotations exist in their own
DSL.  Every part of simulator is valid in a language that we are not the sole
proprietors of.  If a 3rd party developer has already gone through the process
of learning C++ to add a model to our simulator, learning Python dictionaries
is not a barrier to entry.

Furthermore, since these are Python expressions, we have wired it up so that 
the scope of these dicts matches that of the class they are declared within.
This let's users do neat things like the following:

.. code-block:: c++

    namespace mi6 {

    class Spy {
      #pragma cyclus var {"default": 7}
      int id;

      #pragma cyclus var {"default": "James Bond, {0:0>3}".format(id['default'])}
      std::string name;
    };

    class Friend {
      #pragma cyclus var {\
        "docstring": "Normally helps {0}".format(Spy.name['default'])}
      std::string help_first;
    };
    }; // namespace cyclus

    class Enemy {
        #pragma cyclus var {'default': mi6.Spy.name['default']}
        std::string nemesis;
    };

If this isn't expressive enough, we also added an ``exec`` pragma which 
allows users to execute arbitrary Python code, that is added to the global
namespace of the state variables.

.. code-block:: c++

    #pragma cyclus exec import uuid
    #pragma cyclus exec x = 10

    class TimeBomb {
      #pragma cyclus var {"default": int(uuid.uuid1(clock_seq=x))}
      int deactivation_code;
    };
    
This allows users to keep all of their state variable annotations in a 
separate sidecar ``*.py`` file and then import and use them rather than
cluttering up the C++ source code.

Mirror, Mirror
==============
*So where is the reflection?*

The reflection comes out of the fact that our state accumulation stage
is prior to any code that we generate.  ``cycpp`` is in fact a 3-pass
preprocessor. The three passes are:

1. run cpp normally to canonize all other preprocessor directives,
2. accumulate annotations for agents and state variables, and
3. generate code based on annotations.

Two is the minimum that you need, but having the first stage where we 
run the code through plain old ``cpp`` is ideal because this resolves
a lot of wacky things that people *can* do with the preprocessor:

.. code-block:: c++

    #define OPEN_CURLY_BRACE {
    #define CLOSED_CURLY_BRACE }

    class Spy OPEN_CURLY_BRACE
      int id;
    CLOSED_CURLY_BRACE;

If you don't use ``cpp`` as a first stage, than to be robust you need to 
implement ``cpp``. (Which is too much work.)

In the end, we have a whole suite of ``#pragma cyclus`` directives that 
let users specify what they want generated and where. These are based on:

1. the method they want generated, 
2. whether they want the declaration, definition, or implementation
   of this method, or
3. a wrap up of the above.

These pragmas are, of course, scope aware.  The code generation pragmas 
are not particularly interesting to someone not doing cyclus development 
so I will skip them here. To give you a taste though, in the simplest 
case for one state variable on a single class we transform the code the 
use has to write from:

.. code-block:: c++

    class Friend: public Spy {
       public:
        #pragma cyclus 

        #pragma cyclus var {\
          "default": "friend of " + Spy.name['default'], \
          }
        std::string friend;
    };

to this automatically:


.. code-block:: c++

    class Friend: public Spy {
     public:
      virtual void InitFrom(mi6::Friend* m) {
        mi6::Spy::InitFrom(m);
        friend = m->friend;
      };

      virtual void InitFrom(cyclus::QueryableBackend* b) {
        mi6::Spy::InitFrom(b);
        cyclus::QueryResult qr = b->Query("Info", NULL);
        friend = qr.GetVal<std::string>("friend");
      };

      virtual void InfileToDb(cyclus::InfileTree* tree, cyclus::DbInit di) {
        mi6::Spy::InfileToDb(tree, di);
        tree = tree->SubTree("agent/" + agent_impl());
        di.NewDatum("Info")
        ->AddVal("friend", cyclus::OptionalQuery<std::string>(tree, "friend", "friend of James Bond, 007"))
        ->Record();
      };

      virtual cyclus::Agent* Clone() {
        mi6::Friend* m = new mi6::Friend(context());
        m->InitFrom(this);
        return m;
      };

      virtual std::string schema() {
        return ""
          "<optional>\n"
          "    <element name=\"friend\">\n"
          "        <data type=\"string\" />\n"
          "    </element>\n"
          "</optional>\n"
          ;
      };

      virtual void InitInv(cyclus::Inventories& inv) {
      };

      virtual cyclus::Inventories SnapshotInv() {
        cyclus::Inventories invs;
        return invs;
      };

      virtual void Snapshot(cyclus::DbInit di) {
        di.NewDatum("Info")
        ->AddVal("friend", friend)
        ->Record();
      };

    #pragma cyclus var { "default": "friend of " + Spy.name['default'], }
    std::string friend;
    };

And The Moral, Mr. Aesop?
=========================
Many other simulators abuse APIs, build systems, code generators, and 
domain-specific languages in various ways. It almost seems that to be
user-developer friendly at all that such abuse is part of the game. However, 
you don't need custom languages to achieve this goal.  Existing languages
(cpp, C++, Python) are good enough and they give simulators the hooks
that they need.  There is no need to go beyond them.  Any custom build 
system support the simulators wants to have is great but not - strictly
speaking - required.

I am extraordinarily proud that in cyclus we can eat our cake and have it 
too!  We have user-friendly top-level APIs (the pragmas).  The are 
conveniences for lower level C++ APIs that do the real work and ``cycpp`` is
entirely optional (though recommended). Furthermore, writing a preprocessor 
is not hard.  It is only ~1300 lines of Python code in a single file and 
relies on nothing but the standard library.  About 600 of these lines are
the code generators, so there is only around 700 lines of code that act as
the preprocessor mechanics.  The hardest part remains dealing with C++!

