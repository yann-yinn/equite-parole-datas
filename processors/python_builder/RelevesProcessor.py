# -*-coding: utf8 -*-

import os
from datetime import datetime
import json
from Config import Config

class Timeset:
	pass

class Report:
	""""""
	raport = {}
	categories = {
		"Total Temps de parole" : "total_temps_de_parole",
		"Total Temps d'antenne" : "total_temps_antenne",
	}

	def __init__(self, raport):
		self.raport = raport

	@staticmethod
	def createFromCSV(releve):
		raport = {}
		lines = releve.read().split('\n')

		for line in lines[1:]:
			cols = line.split(';')
			candidat = cols[0].replace('"', '')
			categorie = Report.categories[cols[1].replace('"', '')]
			if not candidat in raport:
				raport[candidat] = {}
			if not categorie in raport[candidat]:
				raport[candidat][categorie] = 0

			h, m, s = map(int, cols[2].split(':'))
			raport[candidat][categorie] += (h * 3600) + (m * 60) + s

		return Report(raport)

	def __operation(self, other, f):
		if isinstance(other, Report):
			candidats = list(set(self.raport.keys()).union(other.raport.keys()))
			for candidat in candidats:
				if candidat in self.raport and candidat in other.raport:
					for n, cat in self.categories.items():
						if cat in self.raport[candidat] and cat in other.raport[candidat]:
							self.raport[candidat][cat] = f(self.raport[candidat][cat], other.raport[candidat][cat])
						elif cat in other.raport[candidat]:
							self.raport[candidat][cat] = other.raport[candidat][cat]
				elif candidat in other.raport:
					self.raport[candidat] = other.raport[candidat]
		else :
			raise NotImplementedError

	def __add__(self, other):
		self.__operation(other, lambda a, b: a+b)
		return self

	def __sub__(self, other):
		self.__operation(other, lambda a, b: a-b)
		return self

	def __str__(self):
		return self.raport.__str__()

class RelevesProcessor:
	config = {}

	def __init__(self):
		""""""
		for key, value in Config.RELEVES.items():
			if key in ['SRC', 'DEST', 'METADATA']:
				self.config[key] = Config.ROOT + value
			else :
				self.config[key] = value

		with open(self.config['METADATA'], 'r') as meta_file:
			self.meta = json.load(meta_file)

		data = RelevesProcessor.crawl_sources(self.config, self.meta)

		with open(self.config['DEST'] + 'releve.json', 'w') as output:
			output.write(json.dumps({"data" : data}))

	@staticmethod
	def crawl_sources(config, meta):
		""""""
		folder = config['SRC']
		data = {}

		chaines = [d for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))]

		for chaine in chaines:
			type = meta['chaines'][chaine]['type']
			name = meta['chaines'][chaine]['name']
			if not type in data:
				data[type] = {}
			data[type][name] = {}

			chaine_path = folder + chaine + '/'
			dates = [d for d in os.listdir(chaine_path) if os.path.isdir(os.path.join(chaine_path, d))]

			organiser = {}
			for date in dates:
				report_date_path = chaine_path + date + '/releve-' + date + '.csv'
				if os.path.isfile(report_date_path):
					with open(report_date_path, 'r', encoding = config['SRC_ENCODING']) as report:
						organiser = RelevesProcessor.organise_reports(organiser, date, Report.createFromCSV(report), meta)

			data[type][name] = RelevesProcessor.subtract_intervals(organiser, meta)

		return data

	@staticmethod
	def organise_reports(organiser, date, report, meta):
		from_date_str = meta['dates'][date]['from']
		to_date_str = meta['dates'][date]['to']

		if from_date_str != None and to_date_str != None:
			from_date = datetime.strptime(from_date_str, '%Y-%m-%d')
			to_date = datetime.strptime(to_date_str, '%Y-%m-%d')

			if not from_date in organiser:
				organiser[from_date] = []

			organiser[from_date].append((to_date, report))
			organiser[from_date] = sorted(organiser[from_date], key = lambda tuple: tuple[0])


		return organiser

	@staticmethod
	def subtract_intervals(organiser, meta):
		""""""
		data = {}
		for src_date in sorted(organiser.keys()):
			prec = (src_date, Report({}))
			for date_raport in organiser[src_date]:
				sub = date_raport[1] - prec[1]
				date_key = datetime.strftime(prec[0], '%Y-%m-%d') +'--' + datetime.strftime(date_raport[0], '%Y-%m-%d')
				data[date_key] = sub.raport
				prec = date_raport

		return data