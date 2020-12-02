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

    def _iter_json(self, dict_json: Dict) -> str:
        with add_html_tag(self.table_style) as _:
            html_string, table = _  # type: ValueHolder, list
            for k, v in dict_json.items():
                if v is None:
                    v = ''
                with add_html_tag('<tr>') as (tr_, tr):
                    tr.append(f'<th>{str(k)}</th>')

                    if isinstance(v, (str, int, float)):
                        tr.append(f'<td>{v}</td>')
                    elif isinstance(v, Dict):
                        tr.append(f'<td>{self._iter_json(v)}</td>')
                    elif isinstance(v, list):
                        with add_html_tag('<td><ul>') as (tudl_, tdul):  # <td><ol>
                            for idx, e in enumerate(v):
                                idx += 1
                                if isinstance(e, (str, float, int)):
                                    tdul.append(f'<li>{e}</li>')
                                elif isinstance(e, Dict):
                                    tdul.append(self._iter_json(e))
                                elif isinstance(e, List):
                                    tdul.append(self._iter_json({f'{idx}.': e}))
                        tr.append(tudl_.data)
                table.append(tr_.data)
        return html_string.data

    def convert(self, current_result: Union[List, Dict] = None) -> str:
        source = self.obj_source if current_result is None else current_result

        html_string = ''
        if isinstance(source, Dict):
            """ do some modify if you want.
            for k, v in source.items():
                ...
            """
            html_string = self._iter_json(source)
        elif isinstance(source, List):
            for idx, val in enumerate(source):
                idx += 1
                if isinstance(val, (str, int, float)):
                    html_string += f'<li>{str(val)}</li>'
                elif isinstance(val, Dict):
                    html_string += self.convert({f'{idx}.': self.convert(val)})
                elif isinstance(val, List):
                    html_string += self.convert({f'{idx}.': val})  # change value to dict
        return html_string
