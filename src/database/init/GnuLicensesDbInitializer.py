#!/usr/bin/env python
# -*- coding: utf-8 -*-
from database.init.DbInitializer import DbInitializer
class GnuLicensesDbInitializer(DbInitializer):
    @property
    def DbFileName(self): return 'Gnu.Licenses.sqlite3'

    """
    def InsertInitData(self):
        super().InsertInitData()
        from database.init.GnuLicenses.insert.py.Inserter import Inserter
        inserter = Inserter(self.DbFilePath)
        inserter.Insert()
    """

        """
        上記の処理も共通化できる？
        # https://qiita.com/progrommer/items/abd2276f314792c359da
        import importlib
        path_root = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))))
        path_insert_py = os.path.join(path_root, 'database/init/{0}/insert/py/'.format(self.DbId))
        if os.path.isdir(path_insert_py):
            namespace_insert_py = path_insert_py.replace('/', '.')
            module = importlib.import_module(namespace_insert_py + 'Inserter')
            inserter = module.Inserter(self.DbFilePath)
            inserter.Insert()
        """
