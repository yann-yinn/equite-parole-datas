# -*-coding: utf8 -*-

import json
import time

class Generator:
	output = {}
	output_file = ""

	sections = [
		"soutiens",
		"candidat",
		"total_temps_de_parole",
		"antenne",
		"total_temps_antenne"
	]

	def __init__(self, output_file):
		self.output_file = output_file


	def addFile(self, file):
		with open(file, 'r') as input:
			data = input.read()
			lines = data.split("\n")
			i = 0
			candidat = ""
			for line in lines[1:-6-((len(lines)-7) % 6)]:
				arr = line.split(',')
				if i == 0:
					candidat = arr[0]
					if not arr[0] in self.output:
						self.output[candidat] = {
							"nom" : candidat,
							"soutiens" : Generator.createTimeSection(),
							"candidat" : Generator.createTimeSection(),
							"total_temps_de_parole": Generator.createTimeSection(),
							"antenne" : Generator.createTimeSection(),
							"total_temps_antenne": Generator.createTimeSection()
						}
				else:
					self.addTimeToSection(candidat, self.sections[i-1], arr[1])

				if i == 5:
					i=0
				else:
					i+=1

		return True

	@staticmethod
	def createTimeSection():
		return {
			"temps" : "0h 00min 00s",
			"secondes" : 0,
			"pourcentage" : "0%"
		}

	def addTimeToSection(self, candidat, section, time_string):
		h, m, s = map(int, time_string.split(':'))
		secondes = (h*3600) + (m * 60) + s + self.output[candidat][section]["secondes"]
		self.output[candidat][section]["secondes"] = secondes
		m, s = divmod(secondes, 60)
		h, m = divmod(m, 60)
		self.output[candidat][section]["temps"] = "%dh %02dmin %02ds" % (h, m, s)
		return True


	def writeFile(self):
		with open(self.output_file, 'w') as output_file:
			output_file.write(json.dumps(self.output))
		return True