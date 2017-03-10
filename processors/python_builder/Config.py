# -*-coding: utf8 -*-

class Config:

	ROOT = ""
	SOURCES = "src/"
	RELEVE = "releves-par-chaine/"
	RAPPORTS = "releves-par-groupe-de-chaines/"
	PARSED = "csv/"
	ORIGIN = "originaux/"
	DIST = "dist/api/v1/"

	@staticmethod
	def root(d):
		d = d.replace("\\", "/")
		Config.ROOT = d + "/"
		return True
