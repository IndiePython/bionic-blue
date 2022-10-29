"""Facility for custom deque class definition."""

from collections import deque
from functools import partialmethod
from copy import deepcopy

# XXX
# replace the walking deque implementations in other
# packages by this one, since it is much more advanced;

### main class definition


class WalkingDeque(deque):
    """A deque with custom rotation and memory operations.

    The complete docstring with plenty doctests can be
    found on common/wdeque/wdtests.py
    """

    def __init__(self, iterable):
        """Initialize superclass, perform additional setups.

        Extends collections.deque.__init__.

        iterable (any non-empty iterable object)
           Contains items for the walking deque.
        """
        ### initialize the superclass; notice a maxlen
        ### argument isn't provided, we don't use it
        ### (check the class docstring for details)
        super().__init__(iterable)

        ### store length
        self.length = len(self)

        ### raise value error if iterable is empty
        if not self.length:
            raise ValueError("iterable must not be empty")

        ### create attributes to support operations; they
        ### will work as accumulators regarding both the
        ### amount they represent and the direction (their
        ### signal);

        self.total_walking = 0
        self.loops_no = 0

    def walk(self, steps):
        """Perform custom rotation operation.

        steps (integer)
            number of steps to 'walk' the deque.

        Extends collections.deque.rotate by inverting its
        direction and performing additional setups.
        The class docstring has complete explanation and
        examples (doctests).
        """
        ### perform superclass rotation using steps with
        ### inverted signal
        super().rotate(-steps)

        ### accumulate the steps in the total walking
        ### attribute and also use it to store how many
        ### times we walked through all the items

        self.total_walking += steps
        self.loops_no = self.total_walking / self.length

    def restore_walking(self):
        """Walk the deque back to its initial rotation."""
        self.walk(-self.total_walking)

    def get_mem_value(self, original_index):
        """Return value from index as if had never walked.

        original_index (integer)
            original index of the value you want to retrieve.
            This is the index of any value in the deque as
            if the deque had never walked.

        Same as __getitem__ if no rotation had ever happened.

        ### [Off-topic] Interesting behaviour

        An interesting behaviour occurs if we replace the
        line:

        value = self[original_index]

        by:

        self.walk(original_index)
        value = self[0]
        self.walk(-original_index)

        What will happen is that, if the index passed is
        out of range, it will return a value as if the
        deque kept rotating to compensate the missing
        indices.

        For instance:

        wd = WalkingDeque([0, 1, 2]),

        wd.get_mem_value(-4) would return 2;
        wd.get_mem_value(-5) would return 1;
        wd.get_mem_value( 3) would return 0;
        wd.get_mem_value( 4) would return 1;
        and so on...
        """
        ### store total walking
        tw = self.total_walking

        ### walk back the total walking to assume the
        ### original rotation
        self.walk(-tw)

        ### now that the deque is in its original walking,
        ### store the value in the provided index, which is
        ### the value we desire
        value = self[original_index]

        ## now, before returning the value, revert back to
        ## the previous rotation
        self.walk(tw)

        ### return the desired value
        return value

    def get_original_index(self, index):
        """Return original index of value in given index.

        The original index is the index of the value stored
        in the given index as if the deque never walked.

        index (integer)
            current index of the value whose original index
            you want to retrieve.
        """
        ### check if index is within range; this is quicker
        ### than "-self.length <= index < self.length";
        ### always remember efficiency is our priority;
        self[index]

        ### the original index is equivalent to the
        ### remainder of the sum of the current index and
        ### the total walking divided by the length
        return (index + self.total_walking) % self.length

    get_index_of_first = partialmethod(get_original_index, 0)

    def get_unwalked_list(self):
        """Return an unwalked list of the contents.

        Useful for collecting the original sorting
        of the elements without having to manually
        walk back and forth.
        """
        ### store total walking
        tw = self.total_walking

        ### between walking forth and back to the original
        ### rotation, store an unrotated list

        self.walk(-tw)
        unwalked_list = list(self)
        self.walk(tw)

        ### then return it
        return unwalked_list

    def peek_loops_no(self, steps):
        """Return loops number after temporary rotation.

        Used, for instance, to check if we'll complete a
        specific number of loops after a given number
        of rotations.

        steps (integer)
            number of steps back or forth to walk before
            peeking.

        We walk a number of times, store the number of
        loops performed up to that walking, then revert
        back to original walking, then return the stored
        number of loops.
        """
        ### rotate a given number of steps
        self.walk(steps)

        ### store the number of loops in this rotation
        peeked_loops_no = self.loops_no

        ### revert the number of steps performed
        self.walk(-steps)

        ### finally return the peeked loops_no
        return peeked_loops_no

    def get_content_view(self):
        """Return a special copy of the deque.

        Such copy has its walking state totally independent
        from the original object, but it is automatically
        updated every time the original has an item
        reassigned. For the update, the current index is
        not considered, but rather the original index, the
        one before every walk operation, which means their
        original rotation are always equal.
        """
        ### instantiate content view
        content_view = ContentView(self)

        ### append the content view to the list in the views
        ### attribute
        try:
            self.views.append(content_view)

        ### if such attribute doesn't exist, just store a new
        ### list in it and append the content view
        except AttributeError:
            self.views = []
            self.views.append(content_view)

        ### finally return the content view
        return content_view

    def __setitem__(self, index, value):
        """Set new value and update views, if any.

        Extends collections.deque.__setitem__

        index (integer)
            the existing index number of the item in the
            deque whose value you want to replace.

        value (any python value/object)
            object/value to replace the current object/value
            stored in the index.

        The index update in the views is the original index,
        not the current one.
        """
        super().__setitem__(index, value)

        ### try retrieving the views list
        try:
            views = self.views

        ### if no view exists, just pass
        except AttributeError:
            pass

        ### otherwise iterate views, updating them
        else:
            orig_index = self.get_original_index(index)
            for view in self.views:
                view.set_mem_value(orig_index, value)

    ### custom deepcopy operation

    def __deepcopy__(self, memo):
        """Return a deepcopy of this walking deque.

        This method is executed automatically by the
        copy.deepcopy function.

        memo (dict)
            provided automatically by the copy.deepcopy
            function. Used by copy.deepcopy to keep track
            of objects which were already deepcopied, thus
            avoiding deepcopying the same object more than
            once.
        """
        ### gather objects/data needed

        cls = self.__class__
        unwalked_items = self.get_unwalked_list()

        ### instantiate new object
        new_walking_deque = cls(unwalked_items)

        ### record (id(self) -> new_walking_deque) data pair
        ### in the memo mapping
        memo[id(self)] = new_walking_deque

        ### try deepcopying content views
        try:
            ## deepcopy each view;
            ## notice we don't need to catch a reference
            ## to the deepcopied views, since they are
            ## automatically stored in the views attribute
            for view in self.views:
                deepcopy(view, memo)

        ### if an attribute error is raised, it means we
        ### have no content views, so we just pass
        except AttributeError:
            pass

        return new_walking_deque

    ### custom string representation

    def __repr__(self):
        """Return an unambiguous string representation.

        Extends collections.deque.__repr__.
        """
        return super().__repr__().replace("deque", "WalkingDeque", 1)

    ### behaviour for suppressed methods

    def _suppressed(self, *args, **kwargs):
        """Behaviour for suppressed operations (methods)."""
        raise RuntimeError("operation ruled out by the design")

    ## suppress all methods ruled out by the class design
    ## by overriding them with the _suppressed method

    append = (
        appendleft
    ) = (
        extend
    ) = (
        extendleft
    ) = (
        pop
    ) = (
        popleft
    ) = (
        rotate
    ) = insert = clear = remove = reverse = __delitem__ = __delattr__ = _suppressed


### subclass definition


class ContentView(WalkingDeque):
    """View of walking deque content w/ autonomous walking.

    The complete docstring with plenty doctests can be
    found on common/wdeque/cvtests.py
    """

    def __init__(self, walking_deque):
        """Initialize super class and store proxied deque.

        Extends WalkingDeque.__init__.

        walking_deque
        (instance of common.walkingdeque.WalkingDeque)
            walking deque to be proxied.
        """
        super().__init__(walking_deque.get_unwalked_list())
        self.proxied = walking_deque

    def set_mem_value(self, original_index, value):
        """Set value for index as if we never "walked".

        original_index (integer)
            the existing original index of the item in the
            deque whose value you want to replace.

        value (any python value/object)
            object/value to replace the current object/value
            stored in the original index.
        """
        ### store total walking
        tw = self.total_walking

        ### walk back the total walking to assume the
        ### original rotation
        self.walk(-tw)

        ### now that the deque is in its original position,
        ### set the value in the provided index, which has
        ### the value we want to replace)
        self[original_index] = value

        ## now, revert back to teh previous rotation
        self.walk(tw)

    def __setitem__(self, index, value):
        """Set item value only if it complies to design.

        Extends WalkingDeque.__setitem__.

        According to the design, the value can only be set
        if it is identical (a is b) to the corresponding
        original index value of the proxied deque.

        index (integer)
            the existing index number of the item in the
            deque whose value you want to replace.

        value (any python value/object)
            object/value to replace the current object/value
            stored in the index.
        """
        ### retrieve value using the corresponding original
        ### index from the proxied deque

        orig_index = self.get_original_index(index)
        proxied_val = self.proxied.get_mem_value(orig_index)

        ### if the value retrieved is the same as the one
        ### passed as the argument, then proceed with the
        ### item setting
        if proxied_val is value:
            super().__setitem__(index, value)

        ### otherwise raise an error reporting the
        ### non-compliance of the value
        else:
            raise ValueError("value must be identical to proxied deque value")

    def get_content_view(self):
        """Return a "sibling" content view.

        Overrides WalkingDeque.get_content_view.
        """
        return self.proxied.get_content_view()

    ### custom deepcopy operation

    def __deepcopy__(self, memo):
        """Return a deepcopy of this content view.

        Overrides WalkingDeque.__deepcopy__.

        This method is executed automatically by the
        copy.deepcopy function.

        memo (dict)
            provided automatically by the copy.deepcopy
            function. Used by copy.deepcopy to keep track
            of objects which were already deepcopied, thus
            avoiding deepcopying the same object more than
            once.
        """
        ### get proxied deepcopy reference
        proxied_deepcopy = deepcopy(self.proxied, memo)

        ### instantiate new content view
        new_content_view = proxied_deepcopy.get_content_view()

        ### record (id(self) -> new_content_view) data pair
        ### in the memo mapping
        memo[id(self)] = new_content_view

        return new_content_view

    ### custom string representation

    def __repr__(self):
        """Return an unambiguous string representation.

        Extends WalkingDeque.__repr__.
        """
        return super().__repr__().replace("WalkingDeque", "ContentView", 1)
