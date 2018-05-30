# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring

from __future__ import absolute_import, unicode_literals

import ast


FORMATED_KEYS = ('setup', 'teardown')


class SECTIONS(object):
    polarion = 'Polarion'
    steps = 'testSteps'
    results = 'expectedResults'


def _get_section_start(doc_list, section):
    """Finds the line with "section" (e.g. "Polarion", "testSteps", etc.)."""
    section = '{}:'.format(section)
    for index, line in enumerate(doc_list):
        if section != line.strip():
            continue
        indent = len(line) - len(line.lstrip(' '))
        return index + 1, indent
    return None, None


def _lines_to_dict(lines, start=0, lineno_offset=0, stop=None):
    if stop:
        new_lines = lines[start:stop]
    else:
        new_lines = lines[start:]

    lines_dict = {}
    indent = len(new_lines[0]) - len(new_lines[0].lstrip(' '))
    prev_key = None
    for num, line in enumerate(new_lines, 1):
        line_stripped = line.strip()
        if not line_stripped:
            break

        curr_indent = len(line) - len(line.lstrip(' '))

        if curr_indent < indent:
            break

        word = line_stripped.split(' ')[0] or line_stripped
        if prev_key and curr_indent > indent and word[-1] != ':':
            sep = '\n' if prev_key in FORMATED_KEYS else ' '
            prev_lineno, prev_indent, prev_value = lines_dict[prev_key]
            lines_dict[prev_key] = (
                prev_lineno, prev_indent, '{}{}{}'.format(prev_value, sep, line_stripped))
            continue
        else:
            prev_key = None

        if curr_indent > indent:
            continue
        data = line.split(':')
        if len(data) == 1:
            data.append('')
        key = data[0].strip()
        value = ':'.join(data[1:]).strip()
        if value == 'None':
            value = None
        lines_dict[key] = num + lineno_offset, indent, value
        prev_key = key

    return lines_dict


def _lines_to_list(lines, start=0, lineno_offset=0, stop=None):
    if stop:
        new_lines = lines[start:stop]
    else:
        new_lines = lines[start:]

    lines_list = []
    indent = len(new_lines[0]) - len(new_lines[0].lstrip(' '))
    for num, line in enumerate(new_lines, 1):
        line_stripped = line.strip()
        if not line_stripped:
            continue
        curr_indent = len(line) - len(line.lstrip(' '))
        if curr_indent < indent:
            break

        word = line_stripped.split(' ')[0] or line_stripped
        if curr_indent > indent and word[-1] != ':':
            prev_lineno, prev_indent, prev_value = lines_list.pop()
            lines_list.append(
                (prev_lineno, prev_indent, '{} {}'.format(prev_value, line_stripped)))
            continue

        if curr_indent > indent:
            continue
        lines_list.append((num + lineno_offset, indent, line_stripped))

    return lines_list


def parse_docstring(docstring):
    """Parses docstrings to dictionary. E.g.:

    Polarion:
        assignee: mkourim
        testSteps:
            1. Step with really long description
               that doesn't fit into one line
            2. Do that
        expectedResults:
            1. Success outcome with really long description
               that doesn't fit into one line
            2. 2
        caseimportance: low
        title: Some test with really long description
               that doesn't fit into one line
        setup: Do this:
               - first thing
               - second thing
        foo: this is an unknown field

    This is not included.
    """
    doc_list = docstring.split('\n')

    polarion_start, __ = _get_section_start(doc_list, SECTIONS.polarion)
    if not polarion_start:
        return None

    docstring_dict = _lines_to_dict(doc_list, start=polarion_start)
    if SECTIONS.steps in docstring_dict and docstring_dict[SECTIONS.steps][2]:
        steps_start, __ = _get_section_start(doc_list, SECTIONS.steps)
        steps_list = _lines_to_list(
            doc_list, start=steps_start, lineno_offset=steps_start - polarion_start)
        docstring_dict[SECTIONS.steps] = steps_list
        del docstring_dict[SECTIONS.steps]
    if SECTIONS.results in docstring_dict and docstring_dict[SECTIONS.results][2]:
        results_start, __ = _get_section_start(doc_list, SECTIONS.results)
        results_list = _lines_to_list(
            doc_list, start=results_start, lineno_offset=results_start - polarion_start)
        docstring_dict[SECTIONS.results] = results_list
        del docstring_dict[SECTIONS.results]

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
        try:
            docstring = node.body[0].value.s.decode('utf-8')
        # pylint: disable=broad-except
        except Exception:
            continue
        doc_list = docstring.split('\n')
        polarion_start, polarion_column = _get_section_start(doc_list, SECTIONS.polarion)
        if not polarion_start:
            continue
        docstring_start = node.body[0].lineno - len(doc_list)
        polarion_offset = docstring_start + polarion_start
        docstrings.append((polarion_offset, polarion_column, parse_docstring(docstring)))

    return docstrings
