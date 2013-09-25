Python 3000
###########
:date: 2007-05-10 02:58
:author: Anthony Scopatz
:category: missives
:slug: python-3000

So I have been reading about Python 3000, the forthcoming next stage of
my favorite programming language. Initially I was appalled, frightened.
They are doing a couple of things that are scary but take a lot of
courage. First, they are breaking backwards compatibility. Furthermore,
knowing how I code, nothing I have written so far is inane enough to
make it past this barrier. This partially because they are making print
into a function rather than a syntactical element like for, if, etc.
This really annoyed me until (who wants to type parentheses anyways?)
they pointed out that as a function it could be overwritten in your
module! How fun would that be to have a version of print that highlights
every letter 'e' in red when it prints. Furthermore, I think this helps
with some of the otherwise weird issues in running external programs
inside of python with respect to printing stout.

However, one of the main philosophies about Python is that everything
(that can be) is a list. This makes refereeing to elements inside of
otherwise bulky structures ease, and iterating over them simple
(imported files for example are lists of lines read from that file, or
can be). This adherence is going away and being replaced for some
structures (like dictionarys) with iterators. The dict.keys() object
won't be a list...which is odd, but instead will be an iterator over the
list of the dictionary's keys. Similarly, range() will be an iterator
that is know known as xrange(). Iterators tend to be more effiecent than
lists, especially for large lists. This is good as it will force me, and
others, to write better code. I like the idea of going to iterators
where you can. I hope they make this a full Philisophical change though,
rather than simple a couple, often used special cases.

Python is amazing because of its solidness of philosophy and adherence
not "natural coding". The obvious fear is that if the excitement to come
up with something better they may make the product more unusable.
All-in-all I am still excited to see how it all works. It should be fun
to dick around with at the least. It just seems that all of my favorite
CS projects out there are changing or dying. First my window manager has
ended support and the project is dead. Python is changing. Gentoo had
some internal shake up earlier this year. If all I have to look forward
to is Ubuntu on a Dell, then I will be one Peeved Panda v16.
