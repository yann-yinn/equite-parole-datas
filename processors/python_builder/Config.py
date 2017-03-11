# -*-coding: utf8 -*-

class Config:

	ROOT = ""
	SOURCES = "src/"
	RELEVES_PAR_CHAINE = "releves-par-chaine/"
	RELEVES_PAR_GROUPE_DE_CHAINES = "releves-par-groupe-de-chaines/"
	PARSED = "csv/"
	ORIGIN = "originaux/"
	DIST = "dist/api/v1/"
	RAPPORT = {
		"DEST" : "dist/api/v1/",
		"SRC" : "src/releves-par-groupe-de-chaines/",
		"PARSED" : "csv/",
		"ORIGIN" : "originaux/"
	}
	RELEVES = {
		"DEST" : "dist/api/v1/",
		"SRC" : "src/releves-par-chaine/",
		"METADATA" : "src/releves-par-chaine-metadatas.json",
		"SRC_ENCODING" : "ISO-8859-1"
	}

	@staticmethod
	def root(d):
		d = d.replace("\\", "/")
		Config.ROOT = d + "/"
		return True
