import os
import sys
import glob
import importlib.util

from PIL import Image

import sd_bmab
from sd_bmab import constants


filters = [constants.filter_default]


class BaseFilter(object):

	def __init__(self) -> None:
		super().__init__()

	def configurations(self):
		return {}

	def preprocess_filter(self, context, *args, **kwargs):
		pass

	def process_filter(self, context, base: Image, processed: Image, *args, **kwargs):
		pass

	def postprocess_filter(self, context, *args, **kwargs):
		pass


class NoneFilter(BaseFilter):

	def process_filter(self, context, base: Image, processed: Image, *args, **kwargs):
		return processed


def reload_filters():
	global filters
	filters = [constants.filter_default]

	path = os.path.dirname(sd_bmab.__file__)
	path = os.path.normpath(os.path.join(path, '../filter'))
	files = sorted(glob.glob(f'{path}/*.py'))
	for file in files:
		fname = os.path.splitext(os.path.basename(file))[0]
		filters.append(fname)


def get_filter(name):
	if name == 'None':
		return NoneFilter()
	print('Filter', name)
	path = os.path.dirname(sd_bmab.__file__)
	path = os.path.normpath(os.path.join(path, '../filter'))
	filter_path = f'{path}/{name}.py'
	mod = load_module(filter_path, 'filter')
	return eval(f'mod.Filter{name}()')


def load_module(file_name, module_name):
	spec = importlib.util.spec_from_file_location(module_name, file_name)
	module = importlib.util.module_from_spec(spec)
	sys.modules[module_name] = module
	spec.loader.exec_module(module)
	return module


def preprocess_filter(bmab_filter, context, *args, **kwargs):
	bmab_filter.preprocess_filter(context, *args, **kwargs)


def process_filter(bmab_filter, context, base: Image, processed: Image, *args, **kwargs):
	return bmab_filter.process_filter(context, base, processed, *args, **kwargs)


def postprocess_filter(bmab_filter, context, *args, **kwargs):
	bmab_filter.postprocess_filter(context, *args, **kwargs)

