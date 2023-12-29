

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


def split_fullname(fullname: str | None, default: str = '',
                   prefix: str | list | tuple | None = None,
                   suffix: str | list | tuple | None = None) -> tuple:
    """
    Splits a fullname into their respective first_name and last_name fields.
    If only one name is given, that becomes the first_name
    :param fullname:    The name to split
    :param default:     The value if only one name is given
    :param prefix:      Custom prefixes to append to the default list
    :param suffix:      Custom suffixes to append to the default list
    :return:            tuple
    """
    if not fullname:
        return '', ''

    if prefix and not isinstance(prefix, (str, list, tuple)):
        raise TypeError('`prefix` must be a list/str for multi/single values.')

    if suffix and not isinstance(suffix, (str, list, tuple)):
        raise TypeError('`suffix` must be a list/str for multi/single values.')

    prefix = isinstance(prefix, str) and [prefix] or prefix or []
    suffix = isinstance(suffix, str) and [suffix] or suffix or []
    prefix_lastname = ['dos', 'de', 'delos', 'san', 'dela', 'dona', *prefix]
    suffix_lastname = ['phd', 'md', 'rn', *suffix]

    list_ = fullname.split()
    lastname_idx = None
    if len(list_) > 2:
        for idx, val in enumerate(list_):
            if val.lower() in prefix_lastname:
                lastname_idx = idx
                break
            elif val.lower().replace('.', '') in suffix_lastname:
                lastname_idx = idx - 1
            else:
                if idx == len(list_) - 1:
                    lastname_idx = idx
                else:
                    continue
        list_[:lastname_idx] = [' '.join(list_[:lastname_idx])]
        list_[1:] = [' '.join(list_[1:])]
    try:
        first, last = list_
    except ValueError:
        first, last = [*list_, default]
    return first, last