=========================
json2html3
=========================

簡介
=========================

json2html3的靈感至於: json2html_

而他的差異是改良\ json2html_\:

- 去除不必要的套件，以Python原生套件取代:

    - :ordereddict: 由 ``collection.OrderDict`` 取代
    - :HTMLParser: 這主要是要運用到 ``HTMLParser.HTMLParser().unescape()`` 可以被 ``html.unescape()`` [#unsecape]_ 取代

- 新增特殊的功能:

    - 比對
    - 格式化

關注
=========================
如果您喜歡我的專案，也請考慮給\ `原作者(Varun Malhotra) <http://softvar.github.io>`_\ `星星 <https://github.com/softvar/json2html-flask>`_，因為沒有他的專案，就不會有此專案的誕生！



.. [#unsecape] https://docs.python.org/3/library/html.html#html.unescape

.. _json2html: https://pypi.org/project/json2html/
