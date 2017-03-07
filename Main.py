# -*-coding: utf8 -*-

import os
from os import listdir
from os.path import isdir, isfile, join
from python_builder.Config import Config
from python_builder.Generator import Generator

class Main:

	def __init__(self):
		Config.root(__file__)

		src = Config.ROOT+Config.SOURCES
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

Main()