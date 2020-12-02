__all__ = ('add_html_tag', 'ValueHolder')

import re
from contextlib import contextmanager
from typing import List, Tuple, ContextManager


class ValueHolder:
    __slots__ = ('data',)

    def __init__(self):
        self.data = []


@contextmanager
def add_html_tag(tag: str, content: str = '') -> ContextManager[Tuple[ValueHolder, List]]:
    """
    Automatic adding of end labels

    USAGE:

        msg = 'Hi'
        with add_html_tag('<table><th class="ok"><td>', msg) as (html, content):
            html: ValueHolder
            content: List
            content.append('123')
            ...
    >> print(html.data)  #  Hi<table><th class="ok"><td>123</td></th></table>
    """
    regex = re.compile('<([a-z]+)')
    tag_list: List = regex.findall(tag)

    end_string = ''
    if tag_list:
        tag_list.reverse()
        for t in tag_list:
            end_string += f'</{t}>'

    value_holder = ValueHolder()
    try:
        value_holder.data.extend([content + tag])
        yield value_holder, value_holder.data
    finally:
        value_holder.data = ''.join([str(_) for _ in value_holder.data]) + end_string
