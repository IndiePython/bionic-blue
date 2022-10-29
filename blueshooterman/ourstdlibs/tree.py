"""Common utilities for handling tree-structured data."""


def get_tree_values(tree, key_name, children_key_name):
    """Return all values of given key in tree mapping.

    It walks all the tree recursively retrieving the
    value in the key provided.

    tree
        A mapping structured as a tree.
    key_name
        String representing field whose value you want to
        retrieve.
    children_key_name
        String with which to retrieve a list of
        children mapping.
    """
    values = []
    try:
        value = tree[key_name]
    except KeyError:
        pass
    else:
        values.append(value)

    try:
        children_data = tree[children_key_name]
    except KeyError:
        pass
    else:
        for child_data in children_data:
            child_values = get_tree_values(child_data, key_name, children_key_name)
            values.extend(child_values)

    return values


def get_tree_height(tree, height=0):
    """Get the height of the tree.

    tree
        A mapping structured as a tree.
    height
        Integer indicating height of the tree argument.
        When passing the entire tree, it should be 0.

    ### doctests

    >>> dir_tree = {
    ...   "type": "directory",
    ...   "name": "hello",
    ...   "children": [
    ...     {
    ...       "type": "directory",
    ...       "name": "world",
    ...       "children": [
    ...         {"type": "file", "name": "one.txt"},
    ...         {"type": "file", "name": "two.txt"}
    ...       ]
    ...     },
    ...     {"type": "file", "name": "README"}
    ...   ]
    ... }
    >>> get_tree_height(dir_tree)
    2
    >>> dummy_tree = {
    ...   "name": "root",
    ...   "children": [
    ...     {
    ...       "name": "child1",
    ...       "children": [
    ...         {"name": "grandchild1"},
    ...         {
    ...           "name": "grandchild2",
    ...           "children" : [
    ...             {"name" : "grandgrandchild1"}
    ...           ]
    ...         },
    ...         {"name": "grandchild3"}
    ...       ]
    ...     },
    ...     {"name": "child2"}
    ...   ]
    ... }
    >>> get_tree_height(dummy_tree)
    3
    >>> another_tree = {"name" : "root"}
    >>> get_tree_height(another_tree)
    0

    """
    ### verify if tree has children
    try:
        children = tree["children"]

    ### if there are no children
    except KeyError:
        pass

    ### if it has children, increment the height
    ### and pass it on while calculating the height
    ### of each child recursively
    else:
        height += 1

        height = max(get_tree_height(child, height) for child in children)

    ### return final height
    return height
