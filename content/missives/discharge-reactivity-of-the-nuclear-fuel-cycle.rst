Discharge Reactivity of the Nuclear Fuel Cycle
##############################################
:date: 2010-11-14 23:54
:author: Anthony Scopatz
:slug: discharge-reactivity-of-the-nuclear-fuel-cycle

Was Energy Ant was not technical enough for you? Well, have I got a post
for you...

The EIA, as mentioned before, houses monolithic databases on energy
generation and consumption in this country. One of them goes by the
affectionate name Form RW-859 , or the Nuclear Fuel Data Survey.

Essentially, this database is a record of every fuel assembly to ever
come out of a commercial nuclear reactor in the US. It contains
information such as where the fuel is being stored, if the fuel form
failed, the mass of the assembly, and when the reactor was operating.
 (Unfortunately, my version of the survey contains data only up until
2002, so I am missing eight years of history.)

However, good ol' RW-895 also contains some interesting neutronic data,
such as the inital U-235 enrichment [w/o, weight percent] of each
assembly as well as the burnup [MWd/kg].  In some sense, the enrichment
is a measure of how much energy you ***expect*** to get out of the fuel
and the burnup is a measure of how much energy you ***did*** get out of
the fuel.

Using the above two pieces of information and my burnup-criticality
model, `Bright`_, I calculated the isotopic composition and
multiplication factor of every fuel assembly at discharge (the time when
the fuel is permanently removed from the reactor).  This data was then
stored in a couple of different databases: one for immediately after
discharge and one for time 'now' in which the fuel was allowed to cool
down since it was removed.

If you really want, you can take a peak at `my databases`_ and `the code
that generated them`_. (As you may have guessed by the directory names
here, this was done for a collaborator to try and apply machine learning
algorithms to used fuel assemblies.)

Before I rant too much further, I should define the reactivity of a fuel
assembly.  If 'k' is the `multiplication factor`_, then the reactivity
'rho' is:

|image0|\ Thus, reactivities greater than one mean that the fuel still
has some 'juice' in it, while values less than one mean that the fuel
has to rely on the sweet juice of other fuel elements.

If you are anything like me, you may idly wonder what the mass-weighted
reactivity of the whole of the nuclear fuel cycle over the past 40 years
has been.  This would give you, Oh Intuitive Reader, some idea of how
efficient our system is at actually generating the energy it says it is
going to.  Look. No. Further.

**The mass-weighted average discharge reactivity is: ﻿﻿-0.1083**

Great! The above number is negative.  If it was positive, this would be
like throwing out batteries after only using them part way.

*"But how can this number be negative? Zero charge seems like it would
be the lowest you could go..."* I hear your cries.  This is where the
battery analogy falls apart.  The answer lies in the secret of
batch-averaging, which deserves its own post.

But really, isn't the distribution of these reactivities useful to know
too?  I can't deny you, Friendly Reader:

|image1|

.. _Bright: http://nukestar.me.utexas.edu/scopatz/Bright/
.. _my databases: http://nukestar.me.utexas.edu/scopatz/FuelLearning/
.. _the code that generated them: https://github.com/scopatz/FuelLearning
.. _multiplication factor: http://en.wikipedia.org/wiki/Neutron_multiplication_factor

.. |image0| image:: http://latex.codecogs.com/gif.latex?\huge&space;\rho&space;=&space;\frac{k-1}{k}
.. |image1| image:: http://lh4.ggpht.com/_KFdIKJVlj1w/TOAgjQBKL5I/AAAAAAAAF0U/ufqsJW_Xw5o/discharge_reactivity.png
