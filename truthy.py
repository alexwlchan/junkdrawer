#!/usr/bin/env python3
"""
https://twitter.com/nedbat/status/1542851970184216583
"""

def true_or_false(value):
	"""
	Say if a value if "true" or "false".
	"""
	return "FTarlusee"[int(bool(value)) :: 2]

>>> true_or_false(1 + 2 == 2)
'True'

>>> true_or_false('spam' not in 'spam, spam, eggs and spam')
'False'
