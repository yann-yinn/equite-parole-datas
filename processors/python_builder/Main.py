# -*-coding: utf8 -*-

import os
from os import listdir
from os.path import isdir, isfile, join

from Config import Config
from Generator import Generator


class Main:
	def __init__(self):
		"""Initialise les configuration et lance le process "rapports"."""
		Config.root(os.path.realpath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
		# self.processRapports()
		self.processRapports()

	def processRapports(self):
		"""Exploite le dossier src/rapports pour produire des données par groupe de chaines"""
		src = Config.ROOT + Config.SOURCES + Config.RAPPORTS
		intervals = [f for f in listdir(src) if isdir(join(src, f))]

		for interval in intervals:
			path_categories = src + interval + "/" + Config.PARSED
			categories = [f for f in listdir(path_categories) if isdir(join(path_categories, f))]
			for categorie in categories:
				sources_path = path_categories + categorie + "/"
				output_dir = Config.ROOT + Config.DIST + interval + "/"
				if not os.path.exists(output_dir):
					os.mkdir(output_dir)
				generator = Generator(output_dir + categorie + ".json")
				sources = [f for f in listdir(sources_path) if isfile(join(sources_path, f))]
				for source in sources:
					generator.addFile(sources_path + source)
				generator.writeFile()

	def processReleves(self):
		"""Exploite le dossier src/releves pour produire des données par chaines et par semaine"""

Main()
