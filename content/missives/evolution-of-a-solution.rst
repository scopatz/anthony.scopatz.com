Evolution of a Solution
=======================

:date: 2012-03-31
:author: Anthony Scopatz
:slug: evolution-of-a-solution

The Thought Process of a Computational Scientist
------------------------------------------------
*This was originally published at* `inSCIght <http://inscight.org/2012/03/31/evolution_of_a_solution/>`_.

To appease the PI, our hero - the dashing, young scientist - faces down the 
following problem with moxie normally reserved for Marie Curie.

In 2D or 3D, we have two points (*p1* and *p2*) which define a line segment. 
Additionally there exists experimental data which can be anywhere in the domain. 
**Find the data point which is closest to the line segment.**  Please see Figure 1.

.. figure:: http://s3.amazonaws.com/inscight/img/blog/evo_sol1.png
    :align: center 
    :width: 325 

    Figure 1: The Problem

attempt 1
*********
Instinctually, our code-slinger reaches for an off-the-shelf solution.  
`Most of the time this is the correct thing to do. <http://www.codinghorror.com/blog/2009/02/dont-reinvent-the-wheel-unless-you-plan-on-learning-more-about-wheels.html>`_.
 This is essentially a minimization problem and we know that SciPy 
(and other similar packages) has an API that should be able to help us out.  
With about 2 minutes and Google, our hero finds the 
`scipy.optimize.fmin() <http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.fmin.html>`_
function and tries a solution like the following:

.. code-block:: python

    import numpy as np
    from scipy.optimize import fmin

    p1 = np.array([0.0, 0.0])
    p2 = np.array([1.0, 1.0])
    data = np.array([[0.3, 0.6], [0.25, 0.5], [1.0, 0.75]])

    def point_on_line(x):
        y = p1[1] + (x - p1[0])*(p2[1] - p1[1]) / (p2[0] - p1[0])
        return np.array([x, y])

    def dist_from_line(x, pdata):
        pline = point_on_line(x)
        return np.sqrt(np.sum((pline - pdata)**2))

    def closest_data_to_line():
        dists = np.empty(len(data), dtype=float)
        for i, pdata in enumerate(data):
            x = fmin(dist_from_line, p1[0], (pdata,), disp=False)[0]
            dists[i] = dist_from_line(x, pdata)
        imin = np.argmin(dists)
        return imin, data[imin]

    print closest_data_to_line()

While this approach certainly works it is a little like swatting a fly with a tank.  
In some sense, this solution is order O(n^2) because for every data point we perform 
and optimization. Then we have to solve for the minimum-distance data point 
afterwards.  For a large number of data points, all of the calls to 
`fmin() <http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.fmin.html>`_
can get quite expensive.  So while this solution works it lacks grace.

attempt 2
*********

At this point the plucky researcher notices that minimum the distance from the 
data point to the line has an analytic solution.  This is great!  It means that all 
of those nasty fmin()
calls can go away and we can make this problem O(n).  But what is the equation?  
Recalling back to trigonometry, the stalwart champion notes that in general 3 points 
(p1, p2, pdata) form a triangle.

.. figure:: http://s3.amazonaws.com/inscight/img/blog/triangle-with-cosines.png
    :align: center
    :width: 200

    Figure 2: Law of Cosines Diagram, From Wikipedia

From Figure 2, *a* may be calculated from the distance between *p1* & *pdata*, 
*b* from *p2* & *pdata*, and *c* from *p1* & *p2*.   Therefore shortest distance 
between the data point and the line is just the height of the triangle, which is 
given by *h = a sin(beta)*.  To calculate any of the angles the 
`Law of Cosines <http://mathworld.wolfram.com/LawofCosines.html>`_
can be used.  For instance, *beta = arccos((a^2 + c^2 - b^2)/(2ac))*.  
Furthermore, note the inverse identity *sin(arccos(w)) = sqrt(1 - w^2)*.  
Therefore, the new closest point and line distance functions would look like:

.. code-block:: python

    def dist_from_line(pdata):
        a = np.sqrt(np.sum((p1 - pdata)**2))
        b = np.sqrt(np.sum((p2 - pdata)**2))
        c = np.sqrt(np.sum((p2 - p1)**2))
        h = a * np.sqrt(1.0 - ((a**2 + c**2 - b**2) / (2.0 * a * c))**2)
        return h

    def closest_data_to_line():
        dists = np.empty(len(data), dtype=float)
        for i, pdata in enumerate(data):
            dists[i] = dist_from_line(pdata)
        imin = np.argmin(dists)
        return imin, data[imin]

attempt 3
*********
Unfortunately, attempt 2 is not quite right either.  The points circled in blue in 
Figure 3 lie closer to the line defined by *p1* & *p2* but 
**do not lie closer to the line segment!**

.. figure:: http://s3.amazonaws.com/inscight/img/blog/evo_sol3.png
    :align: center
    :width: 325

    Figure 3: Close to the line, but not the line segment.

These points have a very small height as compared to other data points but 
the triangles formed by them have a very large perimeter.  This leads us to 
the third and simplest implementation: minimize the perimeters!

.. code-block:: python

    def perimeter(pdata):
        a = np.sqrt(np.sum((p1 - pdata)**2))
        b = np.sqrt(np.sum((p2 - pdata)**2))
        c = np.sqrt(np.sum((p2 - p1)**2))
        return (a + b + c)

    def closest_data_to_line():
        peris = np.empty(len(data), dtype=float)
        for i, pdata in enumerate(data):
            peris[i] = perimeter(pdata)
        imin = np.argmin(peris)
        return imin, data[imin]

This has the advantage of performing fewer floating point operations than 
using the trig functions in option 2.  Moreover, it is conceptually simpler 
to understand what is happening just by looking at the code.  By minimizing 
the perimeter we are minimizing the area of the triangle which happens to 
minimize the height of the triangle for the data points we care about.

attempt 4
*********
Up until now, our hero has shied away from trying to do any code optimization.  
We were just trying to get to a solutions that works without excessive computation 
times.   However, almost immediately from attempt 3 we can see that the length *c* 
(between *p1* & *p2*) is the same for all data points.  Therefore this calculation 
is redundant for minimization. We can thus replace the perimeter function with 
something that is sufficiently perimeter-esque but requires even less floating 
point arithmetic.

.. code-block:: python

    def like_a_perimeter(pdata):
        a = np.sqrt(np.sum((p1 - pdata)**2))
        b = np.sqrt(np.sum((p2 - pdata)**2))
        return (a + b)

While this only works if *p1* & *p2* do not change, it will outperform any 
of the other options.  This makes it suitable to use on a large number of data 
points.  Finally because the above is so simple, we can use NumPy's vectorization 
capabilities to reduce this whole problem to a single line:

.. code-block:: python

    data[np.argmin(np.sqrt(np.sum((p1 - data)**2, axis=1)) + np.sqrt(np.sum((p2 - data)**2, axis=1)))]

summary
*******
By continuing to think about the problem we end up with the simplest and quickest 
solution which also happens to be the most concise to write.  We could have stopped 
at any point and had a solution that would have worked.  
**We went from a 25 line version to a single expression.**  
What is more, is that this solution works for any number of 
dimensions since three points always form a triangle.

Having the simplest, most general solution has distinct advantages.  
This code will not often need to modified in the future because of the 
variety of  cases it satisfies.  Moreover, should the code ever need to 
be revisited it is possible to look at the whole thing in a single glance.

Much of good software development - and scientific code in particular - must 
make the trade off between human time and computer time.  In general, human 
time always wins.  At any of the checkpoints in this evolution we could have 
stopped.   Thus they key engineering decision to make was at what attempt the 
code is "good enough" to satisfy the vast array of other requirements:

* easy to ready,
* easy to understand,
* easy to test,
* easy to maintain,
* speed,
* and making the PI happy.

With that, the triumphant hero returns home from the lonely cafe to have a 
delicious vegan victory cookie!
