"""Documentation/tests for the Walking Deque Class

A deque with custom rotation and memory operations.

### Preliminary imports

Since some of our tests/examples use some standard library
imports, let's go ahead and perform them:

>>> from collections import deque
>>> from random      import seed, randint
>>> from copy        import deepcopy

Let's also import the class we are testing
>>> from .main import WalkingDeque

### Purpose and general usage

This class was first designed to assist in game animation.
Basically it is a good solution for any problem which demands
quick switching between a finite set of values many times
over.

In that respect, it is specially useful for animation,
because it can be used to quickly switch between animation
values like surfaces (images) and positions in 2d space
(containers of x, y coordinates representing 2d points).

To be more precise, we use the walking deque to switch
between indices which point to these values in other
containers like lists.

>>> # animation values (positions):
>>> position_list = [(0, 0), (5, 0), (10, 0), (15, 0)]
>>> # indices:
>>> walking_deque = WalkingDeque([0, 0, 1, 1, 2, 3])

>>> # loop:
>>> while True:
...     index = walking_deque[0]
...     print(position_list[index])
...     walking_deque.walk(1)
...     if walking_deque.loops_no == 2.0: break
... 
(0, 0)
(0, 0)
(5, 0)
(5, 0)
(10, 0)
(15, 0)
(0, 0)
(0, 0)
(5, 0)
(5, 0)
(10, 0)
(15, 0)

The while loop above illustrates the animation process. It
could be said that each index represents a frame of
animation and is used to retrieve a specific animation value.
Each loop the deque walks and the value in its first index
is retrieved and used as the index to retrieve the position
value in the position_list.

Additionally, we added a condition to break out of the while
loop when the deque reaches 2 complete loops around its own
content.

Because lots of problems can be generalized as an animation
problem, this class usage has grown beyond of its animation
"role". For instance, I also use it to switch between GUI
items by binding the "walk" method to keys so the user can
walk the different GUI items instead of having them
automatically walked as in the example above illustrating an
animation.

In summary, any future changes on this class and its
dependencies must be done with the goal of keeping the
efficiency of the switching process in mind, mostly for
animation but also for other more general purposes related
to switching between finite sets of values.


### Introduction

This deque uses a different nomenclature for rotation which
is called "walk". Walking means rotating the deque so that
the items closer to the end get closer to the beginning. This
means that, apart from other extra administrative tasks the
walk operation have, the walk is the opposite operation of
the regular deque rotation. As you can observe:

>>> items = [0, 1, 2, 3]

>>> # though both deques will perform rotation operations
>>> # with 1, the effects will be opposite:

>>> regular_deque = deque(items)
>>> regular_deque.rotate(1)
>>> print(items, regular_deque)
[0, 1, 2, 3] deque([3, 0, 1, 2])

>>> walking_deque = WalkingDeque(items)
>>> walking_deque.walk(1)
>>> print(items, walking_deque)
[0, 1, 2, 3] WalkingDeque([1, 2, 3, 0])

The "walk" analogy works perfectly when we think of walking
in real life, where things which are farther begin to get
closer as we walk further. In the example above, for instance,
by walking one step, the walking deque first index went from
0 to 1. By rotating 1 step, on the other hand, the regular
deque first index went from 0 to 3, a much more radical
difference.

We could just use the "rotate" nomenclature and invert its
signal in this class, but we believe different things must be
named differently, to avoid confusion. Thus, we created a new
method called walk.


### Memory operations

Apart from its different rotation operation, the walking
deque also has memory operations and related attributes. For
instance, it accumulates the number of steps performed in the
"total_walking" attribute, regardless of the direction used.

>>> items = [0, 1, 2, 3]
>>> w = WalkingDeque(items)
>>> w.walk( 3) # walk    3 steps
>>> w.walk(-1) # go back 1 step
>>> w.total_walking
2

You can also see the total number of loops performed

>>> # the result of the operation above is 0.5 because
>>> # it is of length 4 and walked 2 steps in total
>>> w.loops_no
0.5

Notice that both the total_walking and loops_no attributes
would be holding negative numbers now if we used regular
rotation, but we are -- advancing -- through the items in the
deque, so again, for our purposes, "walk" is a much more
intuitive operation, which uses positive steps to advance
and negative steps to go back.

The loops_no is actually the result of dividing the total
walking by the length of the deque

>>> w.total_walking / len(w)
0.5
>>> w.total_walking / len(w) == w.loops_no
True

As we discuss further ahead, the length of a walking deque
can't be changed, so the length is stored in the 'length'
attribute for speed, since acessing the attribute is slightly
faster then using the builtin "len".

>>> w.total_walking / w.length == w.loops_no
True

Remember that all attributes above have their signals changed
when the walking is performed with negative steps.

>>> items = [0, 1, 2, 3]
>>> w = WalkingDeque(items)
>>> w.walk(-1) # walk 1 steps back
>>> w.walk(-1) # walk 1 steps back
>>> w.total_walking
-2
>>> w.loops_no # we walk half a loop backwads
-0.5

Also, since it remembers the steps, it can revert back to its
initial state. That is, no matter how many times you walk and
in which diretion, by calling the "restore_walking" method
the deque returns to its original order, when it was
instantiated.

>>> seed()
>>> w = WalkingDeque(range(4))
>>> w
WalkingDeque([0, 1, 2, 3])
>>> # let's now walk a random amount of steps
>>> seed()
>>> w.walk(randint(-3, 3))

>>> # now notice that, no matter the steps walked,
>>> # we'll really go back to the starting position
>>> w.restore_walking()
>>> w
WalkingDeque([0, 1, 2, 3])

As regular deques, indexing works fine and slicing isn't
allowed:

>>> w[0]
0
>>> w[-1]
3
>>> w[1:3]
Traceback (most recent call last):
...
TypeError: sequence index must be integer, not 'slice'

In addition to getting items in their current indexes by
using the usual self[index] syntax as seen above, you can
also pass any integer to the get_mem_value method and it will
return the value for that position as if the deque had never
walked.

>>> w = WalkingDeque([11, 22, 33, 44])
>>> w
WalkingDeque([11, 22, 33, 44])
>>> w.walk(2)
>>> w
WalkingDeque([33, 44, 11, 22])
>>> # give me the value of 0 when deque was instantiated:
>>> w.get_mem_value(0)
11
>>> # give me the value of -2 when deque was instantiated:
>>> w.get_mem_value(-2)
33

>>> # now let's walk a random amount and see if get_mem_value
>>> # still works properly
>>> w.walk(randint(1, 3))
>>> w.get_mem_value(0)
11
>>> w.get_mem_value(-2)
33
>>> # yes, it works fine!

>>> # however, the index pased must be within range:
>>> w.get_mem_value(-5)
Traceback (most recent call last):
...
IndexError: deque index out of range

Additionaly, the 'get_unwalked_list' method will return a
list of all the items in their original positions.

>>> w.get_unwalked_list()
[11, 22, 33, 44]

>>> # notice that passing an index to get_mem_value or
>>> # trying to get it from the returned unwalked list
>>> # produces the same result:

>>> # walk a random amount of steps just to illustrate
>>> # how this operations is totally independent of the
>>> # walked steps
>>> w.walk(randint(-3, 3)) 
>>> # now the proof:
>>> w.get_mem_value(-3) == w.get_unwalked_list()[-3]
True

Another useful method of the walking deque is the
get_original_index. The get_original_index works similarly to
the get_mem_value method, but instead of passing a index to
know which value was sitting there when the deque had not
walked, you pass the current index of a value in the deque
and the method will return the index where the value was
located when the deque was instantiated, that is, before any
walking was ever performed.

For instance:

>>> w = WalkingDeque([11, 22, 33, 44])
>>> w.walk(2)
>>> w[0] # 33 is currently on the 0 (zero-eth) index
33
>>> # but in which index was 33, before any walking was ever
>>> # performed? Easy: we just pass its current index, which
>>> # is 0 (zero), to the get_original_index method:
>>> w.get_original_index(0)
2
>>> # now we now the original index of the item in 0 (33)
>>> # was 2.

More examples:

>>> w = WalkingDeque([11, 22, 33, 44])
>>> w.walk(2)
>>> w.get_original_index(0)
2
>>> w.get_original_index(1)
3
>>> # negative indices work too:
>>> w.get_original_index(-1)
1
>>> # we have a functools.partialmethod for
>>> # "get_original_index(0)", since we used it a lot in
>>> # animation
>>> w.get_index_of_first()
2
>>> # the index must be within range, though:
>>> w.get_original_index(4)
Traceback (most recent call last):
...
IndexError: deque index out of range

The walking deque class also has the peek_loops_no method,
which returns the loops_no value as if you had walked a given
number of steps. This is useful to find out how much more
steps it will take to complete a certain number of loops.

For instance:

>>> w = WalkingDeque([0, 1, 2, 3])
>>> w.walk(3)
>>> # the result below means in one more step you'll
>>> # reach 1 complete loop around its content
>>> w.peek_loops_no(1)
1.0
>>> # the result below on the other hand means that if
>>> # I go one step back I'll be at 0.5 loops around
>>> # the deque's content
>>> w.peek_loops_no(-1)
0.5

This is specially useful when you need to do additional
setups before the walking deque reaches a given number of
loops.


### Empty instantiation not allowed

The walking deque must also have its items fed to it upon
instantiation. It doesn't allow length altering operations
(more about it in the 'Immutable length' discussion ahead).
Thus, you must not ommit an iterable upon instantiation, nor
must you pass an empty one:

>>> # no iterable was passed:
>>> w = WalkingDeque() # doctest: +ELLIPSIS
Traceback (most recent call last):
...
TypeError: __init__() missing 1 required positional...
>>> # the error raised above default behaviour triggered by
>>> # not complying with the collections.deque.__init__
>>> # method signature

>>> # a value error is also triggered if the iterable
>>> # passed is empty:
>>> items = []
>>> w = WalkingDeque(items)
Traceback (most recent call last):
...
ValueError: iterable must not be empty


### Item reassignment

Item reassignment is allowed though. The deque will treat the
new item as if it were the old one, that is, the rotation
information will remain unchanged (the values of loops_no and
total_walking attributes). This causes no harm nor confusion
regarding the problems this class was designed to handle.

Using an analogy, you can think of item reassignement as an
exchange of "passengers". The old passenger is replaced, but
the mileage of the vehicle is the same.

>>> # let's create a deque, walk it a bit, and display
>>> # it's memory related data
>>> w = WalkingDeque([0, 1, 2, 3])
>>> w.walk(3)
>>> w.walk(-1)

>>> w
WalkingDeque([2, 3, 0, 1])
>>> w.total_walking
2
>>> w.loops_no
0.5

>>> # now notice that even though we reassigned a value,
>>> # the walking related data stays the same
>>> w[0] = 7
>>> w
WalkingDeque([7, 3, 0, 1])
>>> w.total_walking
2
>>> w.loops_no
0.5

Remember that, as we discussed before, the default deque
rotation operation (collections.deque.rotate) was
suppressed. So, it can't be used:

>>> w = WalkingDeque(range(4))
>>> w.rotate(1)
Traceback (most recent call last):
...
RuntimeError: operation ruled out by the design

Ahead in the documentation you'll learn about more methods
which were suppressed and thus raise the same error.

### Content views

Another ability of the walking deque is to generate special
proxy-like objects called "content views". They work like
read-only copies/proxies of the walking deques which
originated them.

Content views have their walking independent of the walking
of their original deque, but their contents are linked to
the contents in their "proxied" deque, which means every
time you change a value in the proxied deque the
corresponding value changes in the view. Such corresponding
value is the value which sits in the same original index.

Notice, below, that the content view create isn't affected
by the walking of the walking deque which generated it:

>>> w = WalkingDeque(range(4))
>>> v = w.get_content_view()
>>> w.walk(2)
>>> w
WalkingDeque([2, 3, 0, 1])
>>> v
ContentView([0, 1, 2, 3])

When we change the value of the index 0 of the original
walking deque, the index 2 of the view is changed
accordingly:

>>> w[0] = 45
>>> w
WalkingDeque([45, 3, 0, 1])
>>> v
ContentView([0, 1, 45, 3])

This is so because both they are corresponding values, that
is, they were in the same position when the deques were
created. In other words, the original index of w[0] and v[0]
are the same:

>>> w.get_original_index(0) == v.get_original_index(2)
True

See how their items are aligned when "unwalked":
>>> print(w.get_unwalked_list(), v.get_unwalked_list())
[0, 1, 45, 3] [0, 1, 45, 3]

## Reassigning indices in content views

Content views are protected from external changes. Notice you
can't assign values in the view:

>>> v[0] = 13
Traceback (most recent call last):
...
ValueError: value must be identical to proxied deque value

However, there's a way to do that: if you assign a value
which is the same value as the one present in the proxied
deque's corresponding original index, then the operation is
considered legal. Though in this cases it changes nothing,
it is also a harmless operation.

>>> v[0]
0
>>> v[0] = 0
>>> # notice that nothing changed, since v[0] already held
>>> # the value 0 (zero) before we reassigned it.
>>> # Nonetheless, the operation didn't raise any errors.

Though it is a seemingly useless operation here, it is
crucial for the automatic update process between walking
deques and their respective view instances.

The custom item reassignment implemented in the walking
deque class, which sits at the __setitem__ method, first
changes the value in its own item, then proceed to change
the value in its views, if the deque has any view.

Normally, reassigning values on the views would raise errors,
but since the new values are now also present in the proxied
deque, the operation is legal. See the
ContentView.__setitem__ to learn how this works exactly.

Notice, however, that it's not enough for the objects/values
to be equal: they must be --the same-- object, which means
they must pass an identity check (a is b):

>>> d = dict(hello='world')
>>> w = WalkingDeque([0, 1, 2, d])
>>> c = w.get_content_view()

>>> d_copy = d.copy() # generate an equal dict
>>> d == d_copy
True
>>> # this will cause an error even though, as we saw above
>>> # the dicts have the same value
>>> c[3] = d_copy
Traceback (most recent call last):
...
ValueError: value must be identical to proxied deque value
>>> # This is ok
>>> c[3] = d


## self.views attribute

All the content views generated by a walking deque are also
automatically stored in a list in the views attribute:

>>> w.views
[ContentView([0, 1, 2, {'hello': 'world'}])]

For more information and examples, check the docstring in the
ContentView class.


### Immutable length

Finally, as previously stated, this class was designed from
the premisse that it would receive its complete set of values
when instantiated.

No thought was spared about its behaviour in the case it was
built little by little by appending values or in the case it
started with values but would have some of those values poped
out.

It doesn't mean the design process was lax. On the contrary,
the methods were built and refined little by little based on
real problems related to its main purpose of serving as a
value switcher for game animation values. It is just that
such cases were never necessary, even for the most complex
problems.

However, out of sheer curiosity, I tried to come up with a
design which would allow the existence of those cases.
This was also done as a preventive measure, since the need
for such "feature" might come up one day and it would be
good to have the design at least sketched out for it.

This turned out to be a far complex task than I anticipated,
though. Suppose, for instance, that you have a walking deque
with some values which walked a number of times. In case you
want to remove an item, should you reset the memory related
attributes when doing so?

In case you want to add a new value, should you restore the
walking, add the value and just pretend the deque was just
created? How to recalculate the loops_no attribute in such
cases?

And the total_walking? What should the get_unwalked_list
method return then? Should you restore the original unwalked
state, add the item and them walk back the total walking or
walk back until the loops_no is the same or roughly the same?

As you can see, many questions pop up when trying to
implement that and the solutions often have lots of trade
offs. Thus, I decided to visit this problem again only when
I truly need said feature. I won't deny this is a very
interesting problem, though.

Most importatly, it is a fact, however, that none of the
use cases I handle --need-- said feature, including problems
related to game animation which is the main purpose of this
class. Hence it would be difficult to assess the efficacy of
possible solutions without any context/use case on which to
test it. Thus, even if I were to come up with a solution, it
would remain recorded on paper until the day came when it
would be implemented.

In conclusion, having no time to spare due to the amount of
work to be done, I chose to leave this "design challenge"
aside for now. I call it a design challenge since it isn't
something we need, so it would be inaproppriate to say the
absence of this specific design is a problem per se. 


### Consequences of the immutable length design

Since instances of this class must not have their lengths
altered, all method which do so were suppressed and won't work,
as you can see:

>>> w = WalkingDeque(range(4))

>>> w.append(1)
Traceback (most recent call last):
...
RuntimeError: operation ruled out by the design
>>> w.extend([11, 22, 33])
Traceback (most recent call last):
...
RuntimeError: operation ruled out by the design
>>> del w[0] # __delitem__ method
Traceback (most recent call last):
...
RuntimeError: operation ruled out by the design

All suppressed methods were: append, appendleft, extend,
extendleft, pop, popleft, rotate, insert, clear, remove
and __delitem__ and the ones describe in the next subsection.


## Additional suppressed methods

Other methods, though they don't alter the length of the
deque were also suppressed to prevent errors since they don't
serve any purpose in this class and/or have effects which
prevent the correct usage of the class. Those methods were
"reverse" and "__delattr__":

>>> w = WalkingDeque(range(4))
>>> w.reverse()
Traceback (most recent call last):
...
RuntimeError: operation ruled out by the design
>>> del w.loops_no # __delattr__
Traceback (most recent call last):
...
RuntimeError: operation ruled out by the design


## suppressing behaviour

The suppressing behaviour was implemented by creating a
method with general signature (*args and **kwargs) called
"_suppressed" which simply raises an error explaining the
suppression. This method is then used to override all the
methods we want to suppress by assigning _suppressed to their
names. Thus, every suppressed method name now stores the
_suppressed method:

>>> WalkingDeque.rotate == WalkingDeque._suppressed
True


### Custom deepcopy operation

A custom deepcopy operation was implemented in the
__deepcopy__ method, as instructed by the standard library
copy module official documentation (for python version 3.5).

It is needed for two reasons:

1) Besides the walking deque data, we also generate
   content view objects (special copies/proxies) which
   are referenced in the walking deque and which contain
   references to the walking deque which generated them.
   Because of that, the content views also have their own
   custom deepcopy operation to guarantee that the
   proxy-view relationship is preserved between deepcopies
   of those objects when they are deepcopied recursively.

2) We ommit the maxlen parameter from the signature of
   the collections.deque.__init__ method, which also causes
   problems when using the inherited __deepcopy__ operation,
   which also makes a custom deepcopy operation needed.

>>> w = WalkingDeque(range(4))
>>> c = deepcopy(w)
>>> w.get_unwalked_list() == c.get_unwalked_list()
True
>>> w is c
False

When deepcopied, walking deques are often nested within
dictionaries. In some cases such dictionaries will also have
references to their respective content views. For instance:

>>> w  = WalkingDeque([0, 1, 2, 3])
>>> v1 = w.get_content_view()
>>> v2 = w.get_content_view()
>>> d = {
...   "original": w,
...   "view1"   : v1,
...   "view2"   : v2
... }
>>> new_dict = deepcopy(d)
>>> new_w    = new_dict["original"]
>>> new_v1   = new_dict["view1"]
>>> new_v2   = new_dict["view2"]
>>> new_v1.proxied is new_w
True
>>> new_v2.proxied is new_w
True
>>> new_w.walk(2)
>>> new_w[0] = 34
>>> new_v1[2] == 34
True

Notice that by deepcopying the dict, all objects inside were
deepcopied recursively which means no object was deepcopied
more than once. This is how deepcopying naturally works in
recursive deepcopy operations.

This kind of deepcopy, called recursive, which avoids
deepcopying objects more than once and keep their references
and therefore their relationships intact, only happens when
you deepcopy an object which has other objects embedded or
contained in it (via attributes, indices or keys, for
instance).

Unless, of course, the object in question is a custom object
with a custom deepcopy implementation, then you'll have to
check if the deepcopy operation performed behaves that way.

When you deepcopy objects one by one, though, then the
deepcopies generated won't keep their relationships. See:

>>> # creating walking deque and its view
>>> orig  = WalkingDeque([0, 1, 2, 3])
>>> view = orig.get_content_view()

>>> # deepcopying them one at a time
>>> new_orig = deepcopy(orig)
>>> new_view = deepcopy(view)

>>> # notice how the new_view proxied deque isn't new_orig:
>>> new_view.proxied is new_orig
False
>>> # the new view also isn't referenced in the new_orig
>>> # views attribute (a list):
>>> new_orig.views[0] is new_view
False

This means new_view lost its relationship with new_orig and
won't respond to changes on new_orig:

>>> new_orig[0] = 99
>>> new_view[0] == 99
False

Therefore, when you desire to keep the relationship between
the deepcopies, make sure to deepcopy them recursively, that
is, by storing references to them in the same objects. For
instance, deepcopy them inside a dictionary as we did before
or maybe inside a tuple:

>>> w  = WalkingDeque([0, 1, 2, 3])
>>> v1 = w.get_content_view()

>>> # deepcopy them inside a tuple, for instance
>>> new_w, new_v1 = deepcopy((w, v1))

>>> # now they kept their relationship:
>>> new_v1.proxied is new_w
True
>>> new_w[0] = 144
>>> new_v1[0] == 144
True
>>> new_w.views[0] is new_v1
True

### Extra notes:


## maxlen parameter absence in __init__ method

Tests I performed showed that passing or not passing a maxlen
argument when creating deques don't have practically any
impact in rotation operation speed. Sometimes one case wins,
sometimes the other, but even so with roughly the same timing
(the difference almost reach the nanoseconds mark), indicating
that the presence or absence of the maxlen parameter isn't a
significant factor for speed.

Since walking deques aren't meant to have their length
altered though, the parameter was removed from the
constructor method (__init__). It's presence just doesn't
make sense and represents an useless additional parameter
about which to worry, so its removal is only natural.

As already explained, such removal was one of the causes of
the implementation of a custom deepcopy behaviour.


## About length, loops_no and total_walking attributes

I could protect those attributes against thoughtless meddling
by providing a setter for each of them or by implementing a
__setattr__ method with extra checks, but since this is a
class designed for efficiency, the extra overhead is an
undesirable trade off, thus such possibility was ignored.
At least until we have a better idea.
"""
