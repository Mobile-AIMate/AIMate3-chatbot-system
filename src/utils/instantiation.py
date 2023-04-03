from importlib import import_module


def instantiate(cls, *args, **kwargs):
    """Instantiate a class with the given arguments.

    This is a wrapper around the built-in `cls(*args, **kwargs)` that
    also handles the case when `cls` is a string, in which case it
    will be imported and instantiated.

    Parameters
    ----------
    cls : class or str
        The class to instantiate, or the string name of the class to
        import and instantiate.
    args
        Positional arguments to pass to the class constructor.
    kwargs
        Keyword arguments to pass to the class constructor.

    Returns
    -------
    instance
        The instantiated class.

    Raises
    ------
    ImportError
        If the class cannot be imported.
    """
    if isinstance(cls, str):
        module_name, class_name = cls.rsplit(".", 1)
        module = import_module(module_name)
        cls = getattr(module, class_name)

    entity = cls(*args, **kwargs)
    return entity
