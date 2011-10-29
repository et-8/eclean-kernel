#	vim:fileencoding=utf-8
# (c) 2010 Michał Górny <mgorny@gentoo.org>
# Released under the terms of the 2-clause BSD license.

from __future__ import print_function

import os.path, re

def get_grub_kernels(debug):
	kernel_re = re.compile(r'^\s*kernel\s*(\S+)',
			re.MULTILINE | re.IGNORECASE)

	f = open('/boot/grub/grub.conf')
	debug.print('grub.conf found')

	def _get_kernels(f):
		debug.indent(heading = 'matching grub.conf')
		try:
			for m in kernel_re.finditer(f.read()):
				path = m.group(1)
				debug.printf('regexp matched path %s', path)
				debug.indent()
				debug.printf('from line: %s', m.group(0))
				if os.path.relpath(path, '/boot').startswith('..'):
					path = os.path.join('/boot', os.path.relpath(path, '/'))
					debug.printf('appending /boot, path now: %s', path)
				debug.outdent()
				yield path
		finally:
			debug.outdent()
			f.close()

	return _get_kernels(f)
