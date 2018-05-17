# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring


CUSTOM_FIELDS = {
    'assignee': '',
    'initialEstimate': '',
    'caseimportance': 'high',
    'caselevel': 'component',
    'caseposneg': 'positive',
    'testtype': 'functional',
    'casecomponent': '-',
    'subtype1': '-',
    'subtype2': '-',
    'steps': '',
    'expectedresults': '',
}

MARKERS_FIELDS = {
    'caselevel': 'tier',
    'caseautomation': 'manual',
}

REQUIRED_FIELDS = (
    'assignee',
    'initialEstimate',
    'caseimportance',
)

CASELEVELS = {
    'component': '0',
    'integration': '1',
    'system': '2',
    'acceptance': '3',
}

CASEIMPORTANCE_VALID = (
    'critical',
    'high',
    'medium',
    'low',
)

CASECOMPONENT_VALID = (
    'cloud',
    'infra',
    'services',
    'control',
    'automate',
    'config',
    'appl',
    'candu',
    'report',
    'smartst',
    'prov',
    'ssui',
    'stack',
    'web_ui',
    'optimize',
    'ansible',
)

CASEPOSNEG_VALID = (
    'positive',
    'negative',
)

TESTTYPE_VALID = (
    'functional',
    'non-functional',
    'structural',
)

VALID_VALUES = {
    'caseimportance': CASEIMPORTANCE_VALID,
    'caseposneg': CASEPOSNEG_VALID,
    'testtype': TESTTYPE_VALID,
    'casecomponent': CASECOMPONENT_VALID,
}
