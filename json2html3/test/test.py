if 'env path':
    from pathlib import Path
    import sys

    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from json2html3 import (
        __version__,
    )
    from json2html3.core import main

    sys.path.remove(sys.path[0])

main()
