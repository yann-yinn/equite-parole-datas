# -*-coding: utf8 -*-

class Config:

	ROOT = ""
	SOURCES = "src/"
	RELEVE = "releves-par-chaine/"
	RAPPORTS = "releves-par-groupe-de-chaines/"
	PARSED = "csv/"
	ORIGIN = "originaux/"
	DIST = "dist/api"

	@staticmethod
	def root(d):
		d = d.replace("\\", "/")
		part = d.rpartition("/")
		Config.ROOT = part[0] + "/"
		return True
