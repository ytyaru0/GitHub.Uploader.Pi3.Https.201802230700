#!python3
#encoding:utf-8
import os.path
import configparser
import shlex
import subprocess
import dataset
from web.service.github.api.v3.authentication.BasicAuthentication import BasicAuthentication
from web.service.github.api.v3.authentication.TwoFactorAuthentication import TwoFactorAuthentication
from web.service.github.api.v3.authentication.OAuthAuthentication import OAuthAuthentication
import web.service.github.api.v3.Client
"""
import database.language.Main
import database.api.Main
import database.gnu_license.create.Main
import database.gnu_license.Main
import database.license.Main
import database.account.Main
import database.repo.insert.command.repositories.Inserter
"""
import web.log.Log
import setting.Setting
import glob

from database.init.DbInitializer import DbInitializer
from database.init.AccountsDbInitializer import AccountsDbInitializer as Accounts
from database.init.ApisDbInitializer import ApisDbInitializer as Apis
from database.init.GnuLicensesDbInitializer import GnuLicensesDbInitializer as GnuLicenses
from database.init.LanguagesDbInitializer import LanguagesDbInitializer as Languages
from database.init.LicensesDbInitializer import LicensesDbInitializer as Licenses
from database.init.OtherRepositoriesDbInitializer import OtherRepositoriesDbInitializer as OtherRepositories
from database.init.RepositoriesDbInitializer import RepositoriesDbInitializer as Repositories

class DatabaseMeta(type):
    def __new__(cls, name, bases, attrs):
        #attrs['Initializers'] = {} # 3.6以降でないと順序保持されない。DB依存関係があるので順序必要
        from collections import OrderedDict
        attrs['Initializers'] = OrderedDict()
        for initer in [Apis(), Accounts(), Languages(), GnuLicenses(), Licenses(), OtherRepositories(), Repositories()]
            attrs['Initializers'][initer.DbId] = initer
            #attrs[initer.DbId] = property(lambda : initer)
            attrs[initer.DbId] = property(lambda : initer.Db)
        return type.__new__(cls, name, bases, attrs)
        """
        for initer in [Apis(), Accounts(), Languages(), GnuLicenses(), Licenses(), OtherRepositories(), Repositories()]
            initer.CreateDb()
            initer.ConnectDb()
            #initer.Db.query('PRAGMA foreign_keys = false')
            initer.CreateTable()
            initer.InsertInitData()
            #initer.Db.query('PRAGMA foreign_keys = true')
            attrs[initer.DbId] = property(lambda : initer)
            #self[initer.DbId] = initer # プロパティにしたいが方法不明。これは属性値になってしまう
            #self.__dbs[initer.DbId] = initer # Db, DbFilePathなどが得られる
            # https://www.python-izm.com/advanced/property/
            #property(get_url, set_url, del_url, 'url Property')
            #property(lambda self x: x+1)
        return type.__new__(cls, name, bases, attrs)
        """

    def __GetClient(self, username=None):
        if None is username: account = self.__dbs['account']['Accounts'].find().next()
        else:                account = self.__dbs['account']['Accounts'].find_one(Username=username)
        twofactor = self.__dbs['account']['TwoFactors'].find_one(AccountId=account['Id'])
        authentications = []
        if None is not twofactor:
            authentications.append(TwoFactorAuthentication(account['Username'], account['Password'], twofactor['Secret']))
        else:
            authentications.append(BasicAuthentication(account['Username'], account['Password']))
        return web.service.github.api.v3.Client.Client(self, authentications)
        
