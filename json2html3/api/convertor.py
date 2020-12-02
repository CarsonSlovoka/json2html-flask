from flask import json
from typing import Union, List, Dict
from collections import OrderedDict
from .html_helper import add_html_tag, ValueHolder


def is_json(str_data: str) -> bool:
    try:
        json.loads(str_data)
    except ValueError:
        return False
    return True


class HTMLConvertor:
    __slots__ = ('obj_source', '_table_style')

    def __init__(self, json_string: str, table_style: str):
        try:
            self.obj_source: Union[List, OrderedDict] = json.loads(json_string, object_pairs_hook=OrderedDict)
            self._table_style = table_style
        except ValueError as e:
            raise str(e)

    @property
    def table_style(self) -> str:
        return self._table_style

    def _iter_json(self, dict_json: Union[OrderedDict, Dict]) -> str:
        with add_html_tag(self.table_style) as _:
            html_string, table = _  # type: ValueHolder, list
            for k, v in dict_json.items():
                if v is None:
                    v = ''
                with add_html_tag('<tr>') as (tr_, tr):
                    tr.append(f'<th>{str(k)}</th>')

                    if isinstance(v, (str, int, float)):
                        tr.append(f'<td>{v}</td>')
                    elif isinstance(v, (Dict, OrderedDict)):
                        tr.append(f'<td>{self._iter_json(v)}</td>')
                    elif isinstance(v, list):
                        with add_html_tag('<td><ul>') as (tudl_, tdul):
                            for e in v:
                                if isinstance(e, (str, float, int)):
                                    tdul.append(f'<li>{e}</li>')
                                else:  # is dict
                                    self._iter_json(e)
                        tr.append(tudl_.data)
                table.append(tr_.data)
        return html_string.data

    def convert(self, current_result: Union[List, OrderedDict, str] = None) -> str:
        source = self.obj_source if current_result is None else current_result

        html_string = ''
        if isinstance(source, OrderedDict):
            """ do some modify if you want.
            for k, v in source.items():
                ...
            """
            html_string = self._iter_json(source)
        elif isinstance(source, List):
            for val in source:
                if isinstance(val, (str, int, float)):
                    html_string += f'<li>{str(val)}</li>'
                elif isinstance(val, (Dict, OrderedDict)):
                    html_string += self.convert(val)
        return html_string
