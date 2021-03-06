#! /usr/bin/python

import sys

version = None

reload(sys)  
sys.setdefaultencoding('utf8')

try:
    # Jupyter
    from jupyter_nbformat import reads, write
except ImportError:
    try:
        # New IPython
        from IPython.nbformat import reads, write
    except ImportError:
        # Old IPython
        from IPython.nbformat.current import reads, write
        version = 'json'

to_parse = sys.stdin.read()

if not version:
    import json
    json_in = json.loads(to_parse)
    version = json_in['nbformat']

json_in = reads(to_parse, version)

if hasattr(json_in, 'worksheets'):
    # IPython
    sheets = json_in.worksheets
else:
    # Jupyter
    sheets = [json_in]

for sheet in sheets:
    for cell in sheet.cells:
        if "outputs" in cell:
            cell.outputs = []
        for field in ("prompt_number", "execution_number"):
            if field in cell:
                del cell[field]
        for field in ("execution_count",):
            if field in cell:
                cell[field] = None

if 'signature' in json_in.metadata:
    json_in.metadata['signature'] = ""

write(json_in, sys.stdout, version)
