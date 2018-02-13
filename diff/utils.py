from re import match, compile

_tag_regexp = compile("(\{.*\})(.*)")


def parse_type_from_tag(tag, logger=None):
    if logger:
        logger.debug('Parse type from tag: %s', tag)

    if not tag:
        raise Exception('tag has to be string type')

    _matched_groups = _tag_regexp.match(tag).groups()
    _result = tag

    if len(_matched_groups) == 2:
        _result = _matched_groups[1]

    if logger:
        logger.debug('Parsed type is : %s', _result)
    return _result
