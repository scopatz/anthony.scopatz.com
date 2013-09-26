The (Real) Grand Challenge
##########################
:date: 2010-10-28 12:17
:author: Anthony Scopatz
:slug: the-real-grand-challenge

Having spent the past couple of days a the Fuel Cycle Research and
Development meeting in Washington DC (Gaithersburg, MD really), there
has been a lot of talk about the "Fuel Cycle Simulator Grand Challenge."

On the one hand this is very, very exciting.  It is an opportunity for
the DoE to replace a system that doesn't work.  Or at the very least, it
is a workflow that does not meet current and expected needs.  I have
been saying this for years...

...Another thing I have been saying for years is that, 'Good science is
good software development.'  Not everyone believes me; fine.  But if you
are going to build out a huge code infrastructure you may as well give
it the old college try.

I am fearful though.  They are calling it a 'Grand Challenge' because
there exists this permeating belief that:

#. Nuclear engineers are not software developers.
#. This problem is hard.
#. This problem is new.

At the heart of the proposed simulator is classic framework problem that
is easily solved by a Model-View-Controller (MVC) approach with good
test-driven development around the physical models.  And they are far
from the first scientists to have a issue with storing and
visualizing large amounts of data.

I am fearful because if they choose the wrong API now, it will have
effects for years and years to come.  (Thankfully, from experience, they
seem to recognize this.)

I am also fearful because they are talking about a three-year time frame
just to build the framework and maybe some sample physics models [1].
This is the easy part!  And every day that you spend debating whether
you should be passing an array or a pointer to an array is a day that
you are not doing new science and engineering [2].

So I am excited because it truly is an excellent idea.  I am just not
sure that it is as VISIONary as they make it out to be.  Give me three
months, a coffee-shop, and  *BAM* you'll have the architecture that
has been proposed.

The real grand challenge is making nuclear engineers into become
software developers.

**[1]:** It may well take three years to put in meaningful models, but
that is science not infrastructure.

**[2]:** I count views as new science, because without the shiny
figure at the end, all you have is a bunch of numbers.
