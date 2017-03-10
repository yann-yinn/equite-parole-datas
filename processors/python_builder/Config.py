# -*-coding: utf8 -*-

class Config:

	ROOT = ""
	SOURCES = "src/"
	RELEVES_PAR_CHAINE = "releves-par-chaine/"
	RELEVES_PAR_GROUPE_DE_CHAINES = "releves-par-groupe-de-chaines/"
	PARSED = "csv/"
	ORIGIN = "originaux/"
	DIST = "dist/api/v1/"

	@staticmethod
	def root(d):
		d = d.replace("\\", "/")
		Config.ROOT = d + "/"
		return True
