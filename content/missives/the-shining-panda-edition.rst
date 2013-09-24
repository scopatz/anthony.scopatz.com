The Shining: Panda Edition
==========================

:date: 2013-01-19 
:author: Anthony Scopatz

Or, Adventures in CI Py
-----------------------
As some of you may know I help run an open source nuclear engineering project called 
`PyNE <http://www.pynesim.org/>`_.  It is awesome, and complicated.  It isn’t 
complicated because it is nuclear related.  It is complicated because we provide 
C++ and Python APIs (which are idiomatic to each language) and data.  We also have 
the dream of being truly multiplatform (someday Windows, someday).  From this point 
on I’ll only be speaking for myself, and not on behalf of other PyNE devs.

About 6 months ago, I gave up and admitted that since we develop a Python-independent 
C++ library [1] we should start acting like one.  Driven largely by Katy Huff and 
enabled by Matt McCormick’s 
`cmake-cython-example <https://github.com/thewtex/cython-cmake-example>`_, 
we rightly ditched my ridiculously monkey patched version of distutils in favor 
of CMake, subprocess, and out-of-the-box distutils.  It has been fantastic.

The natural next step to this is continuous integration (CI).  After all, most other projects I have worked on in the SciPy community have gone to some form of CI.  It couldn’t be that hard, right?  Wrong.  Very wrong.  Sad panda wrong.

Attempt 1: Travis CI
--------------------
Travis CI seems like a great tool: github integration, ubuntu vm with sudo access, 20 minute build times before timeout.  It certainly works for a lot of big projects, but it failed for PyNE.  The first issue that you are faced with in CI is the packaging problem.  Since I enjoy not reinventing the wheel, the depth of our dependency stack is kept in check only by social pressures that I feel from other developers.

With Travis CI, for compiled library dependencies you are supposed to use “sudo apt-get install” to install packages during your pre-build.   Fine. We have an HDF5 dependency.  Easy peasy.  However, for Python code you have to use  pip and virtualenv.  What?  Really?

We have a SciPy dependency, which I feel is a pretty normal thing to have.  But the Cheese Shop version of SciPy is source-only.  This means for a SciPy dependency you have to first apt-get gfortran, BLAS, lapack, and the rest of the SciPy dependencies.  THEN you have to compile SciPy.  You can kiss half of your 20 minute allocation goodbye.

Since our compile times our a couple of minutes and it can take a few minutes to pull down all of the data we need, build times were easily 15+ mins.  And we haven’t even gotten to testing yet.  What is really frustrating is that most of this time was unnecessarily spent compiling SciPy…. which has its own CI services  doing this all the time! Furthermore the python-scipy debian package is sitting there, taunting you the whole time.  (“Look at me all pretty and built!”)

Still it almost works.  The build times remained under 20 minutes.  
Then when we started getting `random segfaults in testing <https://travis-ci.org/pyne/pyne/builds/4224346>`_ 
with no good method to debug them, I eventually gave up.

Attempt 2: Shining Panda
------------------------
This story has a happier, if no less frustrating, ending.  The kind folks at 
`Shining Panda <https://www.shiningpanda-ci.com/>`_ (SP) have provided PyNE with 
a Jenkins instance.  (Thanks a million bamboo stalks!)  Compared to Travis CI:

**Pros:**

    * ssh access to the VM
    * can completely avoid virtualenv
    * and commit changes to the VM

**Cons:**

    * no sudo access (and installing debian packages in user space sucks)
    * default packages not as up-to-date
    * less well documented

I finally got SP up and running and all of the tests passing, but it took a lot of trial and error.  This is because, unlike Travis CI where you can look at other project’s ‘.travis.yml’ files, you can’t inspect the configurations of other SP projects.  I even have user access to the yt-project’s SP Jenkins instance, but because I am not an admin or a super-admin I couldn’t see the config.  To add to the frustration, every time you wanted to start up a new VM to test the build or ssh into the machine it took 5 – 10 minutes.  I am complaining because The 47 iterations I needed to get this right took me 2.5 days [2].  It is a good thing I really believe in these tools…

Additionally, after the Travis CI experience, I was dead set against compiling anything that wasn’t PyNE.  Since SP doesn’t give you sudo access I ended up using 
`Anaconda CE <https://www.shiningpanda-ci.com/>`_.    Why Anaconda CE and not 
`EPD Free <http://www.enthought.com/products/epd_free.php>`_ or something else?  
Anaconda has PyTables and a compiler (but sadly no CMake).

Having installed Anaconda inside ssh, I then cloned PyNE, built it, installed it, grabbed the data, and ran the tests.  Worked like a dream.  If only the pain ended there… (This is starting to sound like a broken record by the Police.)

It turns out the shell that Jenkins uses to build is different from the shell that ssh gives you.  Annoyingly, the source command isn’t available in the build shell so you can’t even start you build off with a “source ~/.bashrc” to recover most of your normal environment.  Damn.  To get around this I ended up exporting a lot of variables at the top of the build script, such as PATH, PYTHONPATH, LD_LIBARRY_PATH. (I never did figure out where source went.)

After that, all of the Python stuff works well.  However even though it is receiving the correct environment, CMake’s FindPythonInterp, FindPythonLib, and FindPythonLibsNew (PyNE and numexpr) totally failed to find the Anaconda install.  I have no idea why.  The environment really was being passed down properly (I verified this in Python and CMake).  To fix this problem, a bunch of environment variables have to be re-passed down into CMake!

Unfortunately not everything can even be passed in from the command line.  Thus, I had to create a special CI-mode in the CMakeLists.txt file, to optionally set a couple paths that are otherwise CLI unresponsive.

For posterity, my Jenkins build script is below:

.. code-block:: bash

    export PATH=${HOME}/anaconda/bin:$PATH
    export PATH=${HOME}/cmake-2.8.10.2/bin:$PATH
    export PATH=${HOME}/.local/bin:$PATH
    export PYTHONPATH=${HOME}/.local/lib/python2.7/site-packages:$PYTHONPATH
    export PYTHONPATH=${HOME}/anaconda/lib/python2.7:$PYTHONPATH
    export PYTHONPATH=${HOME}/anaconda/lib/python2.7/site-packages:$PYTHONPATH
    export PYTHONPATH=${HOME}/anaconda/lib/python2.7/lib-dynload:$PYTHONPATH
    export LD_LIBRARY_PATH=${HOME}/anaconda/lib:$LD_LIBRARY_PATH
    export C_INCLUDE_PATH=${HOME}/anaconda/include:${HOME}/anaconda/include/python2.7:${C_INCLUDE_PATH}
    export PYTHON_EXE=`which python`
    export CMAKE_MODULE_PATH=`pwd`/cmake:$CMAKE_MODULE_PATH
 
    echo '---- INFO ----'
    pwd
    ls -lh
    echo $PATH
    echo $PYTHON_EXE
    which $PYTHON_EXE
    $PYTHON_EXE -V
    $PYTHON_EXE -c "import sys; print 'sys.path =\n ' + '\n '.join(sys.path)"
    $PYTHON_EXE -c "import numpy; print 'numpy version:', numpy.__version__"
    $PYTHON_EXE -c "import scipy; print 'scipy version:', scipy.__version__"
    $PYTHON_EXE -c "import Cython; print 'cython version:', Cython.__version__"
    $PYTHON_EXE -c "import numexpr; print 'numexpr version:', numexpr.__version__"
    $PYTHON_EXE -c "import tables; print 'pytables version:', tables.__version__"
    cmake --version
    echo
 
    echo '---- BUILD ----'
    rm -rf build build_nuc_data ${HOME}/.local/lib/python2.7/site-packages
    $PYTHON_EXE setup.py install --user -- \
     -DIS_CI=TRUE \
     -DPYTHON_EXECUTABLE=$PYTHON_EXE \
     -DPYTHON_PREFIX=${HOME}/anaconda \
     -DPYTHON_LIBRARY=${HOME}/anaconda/lib/libpython2.7.so \
     -DPYTHON_INCLUDE_DIR=${HOME}/anaconda/include/python2.7
    $PYTHON_EXE scripts/nuc_data_make
    cd pyne/tests
    nosetests
    cd ../xs/tests
    nosetests

Summary
-------
Finally, everything works.  Shining Panda has already helped uncover a few bugs in our test suite.  So yippee for that!  But given how difficult this whole process was (as say compared to installing and running nosetests), continuous integration is ironically the least stable part of PyNE.  For now.

Here is to hoping these tools keep getting better!

-------

[1] From my point of view the C++ API is a carrot to get more people using Python.

[2] I don’t think that this is Shining Panda’s fault.  I think it is a limitation of the underlying tools.
