# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring

from __future__ import absolute_import, unicode_literals

import ast


def _get_start(doc_list, string):
    for index, line in enumerate(doc_list):
        if string not in line.lower():
            continue
        indent = len(line) - len(line.lstrip(' '))
        return index + 1, indent + 1
    return None, None


def _lines_to_dict(lines, start=0, lineno_offset=0, stop=None):
    if stop:
        new_lines = lines[start:stop]
    else:
        new_lines = lines[start:]

    lines_dict = {}
    indent = len(new_lines[0]) - len(new_lines[0].lstrip(' '))
    for num, line in enumerate(new_lines, 1):
        if not line.strip():
            continue
        curr_indent = len(line) - len(line.lstrip(' '))
        if curr_indent < indent:
            break
        if curr_indent > indent:
            continue
        data = line.split(':')
        if len(data) != 2:
            continue
        key = data[0].strip()
        value = data[1].strip()
        lines_dict[key] = num + lineno_offset, indent + 1, value

    return lines_dict


def _lines_to_list(lines, start=0, lineno_offset=0, stop=None):
    if stop:
        new_lines = lines[start:stop]
    else:
        new_lines = lines[start:]

    lines_list = []
    indent = len(new_lines[0]) - len(new_lines[0].lstrip(' '))
    for num, line in enumerate(new_lines, 1):
        if not line.strip():
            continue
        curr_indent = len(line) - len(line.lstrip(' '))
        if curr_indent < indent:
            break
        if curr_indent > indent:
            continue
        lines_list.append((num + lineno_offset, indent + 1, line.strip()))

    return lines_list


def parse_docstring(docstring):
    """Parses docstrings to dictionary. E.g.:

    Polarion:
        assignee: mkourim
        steps:
            1. do this
            2. then that
        expectedresults:
            1. success
            2. 2
        caseimportance: mylow
        foo: bar

    This is not included.
    """
    doc_list = docstring.split('\n')

    polarion_start, __ = _get_start(doc_list, 'polarion:')
    if not polarion_start:
        return None

    docstring_dict = _lines_to_dict(doc_list, start=polarion_start)
    if 'steps' in docstring_dict and not docstring_dict['steps'][2]:
        steps_start, __ = _get_start(doc_list, 'steps:')
        steps_list = _lines_to_list(
            doc_list, start=steps_start, lineno_offset=steps_start - polarion_start)
        docstring_dict['steps'] = steps_list
    if 'expectedresults' in docstring_dict and not docstring_dict['expectedresults'][2]:
        results_start, __ = _get_start(doc_list, 'expectedresults:')
        results_list = _lines_to_list(
            doc_list, start=results_start, lineno_offset=results_start - polarion_start)
        docstring_dict['expectedresults'] = results_list

    return docstring_dict


def _get_tree(filename):
    with open(filename) as infile:
        source = infile.read()

    tree = ast.parse(source, filename=filename)
    return tree


def get_docstrings_in_file(tree, filename):
    if not tree:
        tree = _get_tree(filename)

    docstrings = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
            continue
        if not (node.body and isinstance(node.body[0], ast.Expr) and
                isinstance(node.body[0].value, ast.Str)):
            continue
        docstring = node.body[0].value.s
        doc_list = docstring.split('\n')
        polarion_start, polarion_column = _get_start(doc_list, 'polarion:')
        if not polarion_start:
            continue
        docstring_start = node.body[0].lineno - len(doc_list)
        polarion_offset = docstring_start + polarion_start
        docstrings.append((polarion_offset, polarion_column, parse_docstring(docstring)))

    return docstrings
