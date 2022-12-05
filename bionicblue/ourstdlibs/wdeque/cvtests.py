"""Documentation and tests for the Content View Class.

View of walking deque content w/ autonomous walking.

### Preliminary imports

Since some of our tests/examples use a standard library
import, let's go ahead and perform it:

standard library import
>>> from copy import deepcopy

let's also perform local imports
>>> from .main import WalkingDeque

### Introduction

WalkingDeque instances can generate instances of this
ContentView class. Instances of such class work like
read-only copies/proxies of the walking deques which
originated them.

Their rotations/walking state is totally independent, though.
The only difference is that when the original walking deques
have the value of their items reassigned, they also
automatically update the values of the corresponding items in
the content views.

Notice below, that the original walking deque and its content
view have independent walking (walking one doesn't change the
other):

>>> orig = WalkingDeque(range(4))
>>> view = orig.get_content_view()

>>> orig.walk(3)
>>> view.walk(1)

>>> orig
WalkingDeque([3, 0, 1, 2])
>>> view
ContentView([1, 2, 3, 0])

However, as stated, when we update the value of one of the
original deque items, the content view is also updated
accordingly:

>>> orig[0] = 45
>>> orig
WalkingDeque([45, 0, 1, 2])
>>> view
ContentView([1, 2, 45, 0])

Notice that though we updated the index 0 of the original
deque, it was the index 2 of the view that got updated. Why
is that? This is because the update is performed on the
corresponding original index of both deques. Here's the
proof:

>>> orig.get_original_index(0)
3
>>> view.get_original_index(2)
3

That is, both the current value of index 0 of the original
deque and the value of index 2 of the content view were
originally in the same original position when they were
instantiated, see:

>>> orig.get_unwalked_list() == view.get_unwalked_list()
True


### Item reassignment for content views

Since they are read-only objects, content views can't have
their items reassigned. Their contents depend only on the
contents of the "proxied" deque.

>>> view[0] = 47
Traceback (most recent call last):
...
ValueError: value must be identical to proxied deque value

Trying to reassign a value manually on the content view
will work, though, on only condition: when the corresponding
value in the original deque is identical. For instance, since
the index 0 of the view has the same original index of the
current index 2 of the original deque, which has the value 1,
if you assign 1 again to the index 0 of the view no error
will be raised:

>>> orig
WalkingDeque([45, 0, 1, 2])
>>> view
ContentView([1, 2, 45, 0])
>>> view[0] = 1
>>> # as you can see, no error was raised

This is a seemingly useless operation, at least in this
example, since the value replaced remains the same, but this
is an essential mechanism which works in synergy with both
the WalkingDeque and ContentView classes to allow then to
have their proxy-view relationship.

In summary, the views are tightly protected from
indiscriminate item reassignment.

## Item reassignment and identity check

But notice that it's not enough for the items to have equal
values, they must also be --the same-- object, which means
they must pass an identity check (a is b):

>>> names = ['Anne', 'Mary']
>>> orig = WalkingDeque([0, 1, 2, names])
>>> view = orig.get_content_view()

>>> names_copy = names.copy()

>>> # the reassignment bellow will raise an error even though
>>> # the values are the same
>>> view[3] = names_copy
Traceback (most recent call last):
...
ValueError: value must be identical to proxied deque value

The error above happens because...
>>> orig[3] is not names_copy
True

However...
>>> orig[3] is names
True

...so the reassignment below works, it doesn't raise errors:
>>> view[3] = names


### "proxied" attribute

The content views store a reference to their proxied deque
in the proxied attribute:

>>> view.proxied is orig
True

Conversely, though this is a detail of the WalkingDeque
class, it is useful to know that views are also referenced
in their proxied deque "views" attribute, which holds a
list of references:

>>> orig.views[0] is view
True


### Sibling content views

The content views can also generate sibling content views,
meaning the content view generated are content views of the
proxied deque, not of view that seemed to generate it.

This is because the get_content_view method in this class
works by asking their proxied deque to generate the new
content view for them. See examples below (notice that
sometimes we perform the walk method on some views; this
isn't necessary, but we do so to remember you that the
walking of all objects are independent):

>>> orig = WalkingDeque([0, 1, 2, 3])
>>> view = orig.get_content_view()
>>> other_view = view.get_content_view()
>>> other_view.walk(2)
>>> other_view
ContentView([2, 3, 0, 1])

Notice that though other_view was generated from the
"view" get_content_view method, it isn't a content view of
"view", but of "orig".

>>> other_view.proxied is orig
True

Thus, view and other_view are both content views of the same
walking deque, "orig"

>>> view.proxied is other_view.proxied
True

Additionaly, walking deques maintain a list of their content
views in a views attribute:

>>> orig.views
[ContentView([0, 1, 2, 3]), ContentView([2, 3, 0, 1])]
>>> view is orig.views[0]
True
>>> other_view is orig.views[1]
True


### Custom deepcopy operation

The custom deepcopy operation in the ContentView class was
designed to work together with the custom deepcopy operation
in its proxied deque's class (WalkingDeque).

As long as they are deepcopied recursively (when they are
stored in the same object, either as items, keys or
attributes), the relationship between the deepcopies remains. 

Example of behaviour after recursive deepcopy:

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
>>> new_w[0] = 43
>>> new_v1[2] == 43
True

What happened above, in other words, is that since the
original deque and its views are part of the same object (the
dictionary), when such object was deepcopied, they were
deepcopied recursively, and the relationship between the
deepcopies new_w, new_v1 and new_v2 remains, even though they
are copies.

However, when the deepcopying isn't recursive (you deepcopy
in more than one step), the relationship between deepcopied
objects is lost:

>>> walking_deque = WalkingDeque([0, 1, 2, 3])
>>> content_view  = walking_deque.get_content_view()

>>> new_wd  = deepcopy(walking_deque)
>>> new_cv = deepcopy(content_view)

>>> # notice how the proxied deque of the new_cv content
>>> # view isn't new_wd:
>>> new_cv.proxied is new_wd
False
>>> new_wd.views[0] is new_cv
False

That is, though their original versions had a relationship,
they haven't preserved such relationship between themselves,
even though they are deepcopies of the same objects. Thus,
changes in the walking deque deepcopy won't affect the
view deepcopy.

>>> new_w.walk(2)
>>> new_w[0] = 22
>>> new_v1[2] == 22
False

So, if you want to preserve the relationship between
deepcopies, at least put the original objects into a tuple
before deepcopying them, for instance: 

>>> walking_deque = WalkingDeque([0, 1, 2, 3])
>>> content_view  = walking_deque.get_content_view()

>>> # deepcopy them inside a tuple:
>>> new_wd, new_cv = deepcopy((walking_deque, content_view))
>>> # and now the deepcopies have preserved their
>>> # relationship:
>>> new_cv.proxied is new_wd
True
>>> new_wd.views[0] is new_cv
True

As long as the objects deepcopied are embedded in the same
object or contained there somehow, the deepcopy will be
recursive. Unless of course, it is a custom class which have
some customized deepcopy operation.

"""
