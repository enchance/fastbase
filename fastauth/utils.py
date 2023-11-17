

# TESTME: Untested
def modstr(instance, *attr: str, data: list | None = None, onlyid: bool = False) -> str:
    """
    The field to display for an object's __str__. If the field doesn't exist then an
    alternative is displayed.
    :param instance:    Instance object
    :param attr:        Field/s name to get data from if it exists
    :param data:        Any data that's not a field
    :param onlyid:      Only return the id
    :return:            str
    """
    clsname = instance.__class__.__name__
    data = data or []
    ll = [getattr(instance, i) for i in attr if hasattr(instance, i) and getattr(instance, i)]
    ll += [i for i in data if i]

    try:
        if onlyid or not ll:
            return f'<{clsname}: {instance.id}>'
        return f'<{clsname} {instance.id}: {", ".join(ll)}>'
    except AttributeError:
        return f'<{clsname}>'