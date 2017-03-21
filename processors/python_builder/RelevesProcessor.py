# -*-coding: utf8 -*-

import os
from datetime import datetime
import json
from Config import Config

class ReleveJSONEncoder(json.JSONEncoder):
	def default(self, o):
		if isinstance(o, Timeset):
			return o.getData()
		return json.JSONEncoder.default(self, o)

class RelevesProcessor:
	config = {}

	def __init__(self):
		""""""

		# Préfix les chemin avec le dossier "root" (chemin absolu vers equite-paroles-datas/"
		# Puis exporte les config dans la clé config de l'object
		for key, value in Config.RELEVES.items():
			if key in ['SRC', 'DEST', 'METADATA']:
				self.config[key] = Config.ROOT + value
			else :
				self.config[key] = value

		# Lecture du fichier de metatdata, il contiens les informations sur les dates des intevales de temps et les
		# chaines
		with open(self.config['METADATA'], 'r') as meta_file:
			self.meta = json.load(meta_file)

		# Fonction de processing des valeurs, retourne un dictonnaire de données complètes
		data = RelevesProcessor.crawl_sources(self.config, self.meta)

		# écriture des données complètes
		# ----- : Type de Chaine -> Chaine -> periode -> candidats -> temps
		with open(self.config['DEST'] + 'releves-par-periode.json', 'w') as output:
			output.write(json.dumps(data, sort_keys=True, cls=ReleveJSONEncoder))

		# Réorganiser les données avec un dossier par période de temps, et un fichier avec le rapport de tous les
		# candidats
		# ----- : periode/ -> candidats -> temps

		# cumul des temps
		periodes = {}
		for type, chaines in data.items():
			for chaine, dates in chaines.items():
				for date, candidats in dates.items():
					if not date in periodes:
						periodes[date] = {}
					for candidat, timeset in candidats.items():
						if not candidat in periodes[date]:
							periodes[date][candidat] = timeset
						else:
							periodes[date][candidat] += timeset

		# Génération d'un fichier de méta données pour les périodes de temps
		meta_dates = {
			'periodes' : {}
		}
		for date, candidats in periodes.items():
			meta_dates['periodes'][date] = {
				'folder' : date,
				'text' : RelevesProcessor.periodeToReadable(date)
			}
			date_dir = self.config['DEST'] + date + '/'
			if not os.path.isdir(date_dir):
				os.mkdir(date_dir)

			# Ecriture d'un fichier {periode}/releves-par-candidats.json : candidats -> temps
			with open(date_dir + 'releves-par-candidats.json', 'w') as output:
				output.write(json.dumps(candidats, sort_keys=True, cls=ReleveJSONEncoder))

		# Ecriture du fichier de méta données
		with open(self.config['DEST'] + 'releves-hebdomadaires-metadonnees.json', 'w') as output:
			output.write(json.dumps(meta_dates, sort_keys=True))

	@staticmethod
	def periodeToReadable(periode):
		"""Prend un format période {AAAA-MM-JJ}--{AAAA-MM-JJ} et retourne un format lisible en français."""
		src_format = '%Y-%m-%d'
		dest_format = '%d/%m/%Y'
		f, t = periode.split('--')
		from_date = datetime.strptime(f, src_format)
		to_date = datetime.strptime(t, src_format)
		return "{0} au {1}".format(datetime.strftime(from_date, dest_format), datetime.strftime(to_date, dest_format))


	@staticmethod
	def crawl_sources(config, meta):
		"""Fonction de processing des données de temps pour toute les chaines, tous les intervales de temps, retourne un dictonnaire de données complètes"""
		folder = config['SRC']
		data = {}

		# Liste les chaines dans src/releves-par-chaines
		chaines = [d for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))]

		#Parcour des chaines
		for chaine in chaines:

			# extrait le type et le nom du media via les meta données fournies
			type = meta['chaines'][chaine]['type']
			name = meta['chaines'][chaine]['name']

			if not type in data:
				data[type] = {}
			data[type][name] = {}

			# Liste les périodes dans chaque dossier de chaine
			chaine_path = folder + chaine + '/'
			dates = [d for d in os.listdir(chaine_path) if os.path.isdir(os.path.join(chaine_path, d))]

			organiser = {}

			# Parcour des dates
			for date in dates:
				report_date_path = chaine_path + date + '/releve-' + date + '.csv'

				# Lis le fichier de rapport
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

class Timeset:
	categories = {
		"Total Temps de parole" : "total_temps_de_parole",
		"Total Temps d'antenne" : "total_temps_antenne",
	}

	def __init__(self):
		self.values = {
		'total_temps_de_parole' : 0,
		'total_temps_antenne' : 0
	}

	def addTo(self, categorie, value):
		if categorie in Timeset.categories:
			cat = Timeset.categories[categorie]
			if not cat in self.values :
				self.values[cat] = 0

			self.values[cat] += value

	def __operate(self, other, f):
		if isinstance(other, Timeset):
			for i, c in Timeset.categories.items():
				self.values[c] = f(self.values[c], other.values[c])
			return self
		else:
			raise NotImplementedError

	def __add__(self, other):
		return self.__operate(other, lambda x,y:x+y)

	def __sub__(self, other):
		return self.__operate(other, lambda x,y:x-y)

	def getData(self):
		data = {}

		for i, c in Timeset.categories.items():
			seconds = self.values[c]
			m, s = divmod(seconds, 60)
			h, m = divmod(m, 60)
			time = "%dh %02dmin %02s" % (h, m, s)
			data[c] = {
				'secondes' : seconds,
				'temps' : time
			}

		return data

	def __str__(self):
		return self.getData().__str__()

class Report:
	""""""
	raport = {}

	def __init__(self, raport):
		self.raport = raport

	@staticmethod
	def createFromCSV(releve):
		raport = {}
		lines = releve.read().split('\n')

		for line in lines[1:]:
			cols = line.split(';')
			candidat = cols[0].replace('"', '')
			categorie = cols[1].replace('"', '')
			if not candidat in raport:
				raport[candidat] = Timeset()

			h, m, s = map(int, cols[2].split(':'))
			secondes= (h * 3600) + (m * 60) + s

			raport[candidat].addTo(categorie, secondes)

		return Report(raport)

	def __operation(self, other, f):
		if isinstance(other, Report):
			candidats = list(set(self.raport.keys()).union(other.raport.keys()))
			for candidat in candidats:
				if candidat in self.raport and candidat in other.raport:
					self.raport[candidat] = f(self.raport[candidat], other.raport[candidat])
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
