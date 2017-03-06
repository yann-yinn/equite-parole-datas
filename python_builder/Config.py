# -*-coding: utf8 -*-


class Config:
    """Configurations du buidler"""
    ROOT = ""
    CHAINES = [

    ]

    @staticmethod
    def root(d):
        d = d.replace("\\", "/")
        part = d.rpartition("/")
        Config.ROOT = part[0] + "/"
        return True
