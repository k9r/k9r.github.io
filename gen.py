#!/usr/bin/env python 

import json

from collections import defaultdict
from itertools import izip_longest
import pandas as pd
import numpy as np

TABLE_FILE = "table.html"
VALUES_TABLE = "values_table.html"
VALUES_FILE = "values.json"

def addRow(values, is_header=False):
    content = ["  <tr>"]
    for k in values:
        k = '' if not k else k
        if is_header:
            content.append("    <th scope=\"col\">{}</th>".format(k))
        else: 
            content.append("    <td>{}</td>".format(k))
    content.append("  </tr>")
    return "\n".join(content)


def addTable(header, rows):
    content = ["""<table class="table">"""]
    if header:
        content.append("  <thead class=\"thead-dark\">")
        content.append(addRow(header, is_header=True))
        content.append("  </thead>")
        content.append("  <tbody>")
    
    for r in rows:
        content.append(addRow(r))
    content.append("  </tbody>")
    content.append("</table>")
    return "\n".join(content)

def readValues():
    with open(VALUES_FILE, "r") as fh:
        return json.load(fh)

def generateTable():
    values_map = readValues()
    reverseMap = defaultdict(list)
    for letter, value in values_map.iteritems():
        reverseMap[value].append(letter)
    arr = [reverseMap[k] for k in reverseMap.keys()]
    rows = []
    for _, row in pd.DataFrame(arr).T.iterrows():
        rows.append(row)
    fh = open(TABLE_FILE, 'w')
    fh.write(addTable(reverseMap.keys(), rows))
    fh.close()

def generateValuesTable(num_per_row=4):
    values_map = readValues()
    keys = sorted(values_map.keys())
    iter_keys = [iter(keys)]*num_per_row
    rows_gen = list(izip_longest(*iter_keys))
    rows = []
    for gen in rows_gen:
        rows.append(["{} = {}".format(k, values_map[k]) if k else '' for k in gen])
    fh = open(VALUES_TABLE, 'w')
    fh.write(addTable(None, rows))
    fh.close()

if __name__ == '__main__':
    generateTable()
    generateValuesTable()