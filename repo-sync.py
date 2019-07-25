#!/usr/bin/env python3
#
# I manage my Arch Linux repo with this script.
# Copyright (C) 2018 Joffrey Darcq
#
# Repo-sync is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Repo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public licenses
# along with Repo.  If not, see <https://www.gnu.org/licenses/>.
#
"""\
[COMMON]

name = repo

srvdir = /public_html/repo
locdir = /home/packages
pkgpat = .*.pkg.tar.xz

[FTP]

host = sub.example.tld
user =
pswd =
"""

from configparser import ConfigParser
from getpass import getpass

import ftplib
import os
import re
import argparse
import sys
import subprocess


class Config(object):

    def __init__(self):
        self.confdir = os.path.join(os.environ['HOME'], '.config', 'repo')
        conf_file = os.path.join(os.path.join(self.confdir, 'config.ini'))

        try:
            os.mkdir(self.confdir, mode=0o700)
        except FileExistsError:
            pass

        try:
            with open(conf_file, 'x', encoding='utf-8') as conf:
                conf.write(__doc__)
            os.chmod(conf_file, mode=0o600)
        except FileExistsError:
            pass

        config = ConfigParser()
        config.read(conf_file)

        for key in ("name", "locdir", "srvdir", "pkgpat"):
            value = config["COMMON"][key]
            self.__setattr__(key, value)

        for key in ("host", "user", "pswd"):
            value = config[config.sections()[1]][key]
            self.__setattr__(key, value)


class Repo(Config, ftplib.FTP_TLS):
    """Override ftplib.FTP_TLS"""

    def __init__(self, debug=0):
        Config.__init__(self)

        if not self.user:
            self.user = input("user : ")
        if not self.pswd:
            self.pswd = getpass("password : ")

        ftplib.FTP_TLS.__init__(self, self.host, self.user, self.pswd)
        self.__delattr__("pswd")

        self.set_debuglevel(debug)
        self.set_pasv(True)

        self._pkgpat = re.compile(self.pkgpat)

    def __enter__(self):
        self.getwelcome()
        self.cwd(self.srvdir)
        os.chdir(self.locdir)
        return self

    def __exit__(self, *exc):
        self.quit()

    def locpkgs(self):
        """Return a "set" collection of local packages
        """
        return {pkg for pkg in os.listdir(".") if self._pkgpat.match(pkg)}

    def srvpkgs(self):
        """Return a "set" collection of server packages
        """
        pkgs = set()

        def callback(line):
            """Callback for "self.retrlines"

            Add in "pkgs set" only lines matched by the pattern
            """
            if self._pkgpat.match(line):
                pkgs.add(line)

        self.retrlines("NLST", callback)
        return pkgs

    def lspkgs(self):
        """List server packages as "ls -l | grep *.pkg.tar.xz"
        """

        def callback(line):
            """Callback for "self.retrlines"

            Print only lines matched by the pattern
            """
            p = re.compile(f".*{self.pkgpat}")
            if p.match(line):
                print(line)

        self.retrlines("LIST", callback)

    def upload(self, lst):
        """Upload list fname
        """
        for fname in lst:
            with open(fname, "rb") as f:
                self.storbinary(f"STOR {fname}", f)

    def remove(self, lst):
        """Remove list fname on server
        """
        for fname in lst:
            self.delete(fname)

    def syncpkgs(self):
        """Sync local and server Repo
        """
        srvpkgs = self.srvpkgs()
        locpkgs = self.locpkgs()

        try:
            self.upload(locpkgs - srvpkgs)
        except ftplib.error_perm:
            pass

        try:
            self.remove(srvpkgs - locpkgs)
        except ftplib.error_perm:
            pass

    def syncdbs(self):
        """Update databases procedure"
        """
        os.chdir(self.confdir)

        db = f"{self.name}.db.tar.gz"
        pkgs = os.path.join(self.locdir, "*.pkg.tar.xz")
        subprocess.run(f"/usr/bin/repo-add {db} {pkgs}", shell=True)

        self.upload((db, f"{self.name}.files.tar.gz"))

        os.chdir(self.locdir)

    def timestamp(self, filename):
        """Return file timestamp
        """
        try:
            timestamp = self.voidcmd(f"MDTM {filename}")[4:]
        except ftplib.error_perm:
            return None
        except TypeError:
            return None

        return timestamp


def main():
    """Run in command-line
    """
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-u", "--upload", type=str, nargs="+",
            help="upload packages list"
        )
        parser.add_argument(
            "-ls", "--lspkgs", action="store_true",
            help="list server packages"
        )
        parser.add_argument(
            "-la", "--lsall", action="store_true",
            help="list all"
        )
        parser.add_argument(
            "-d", "--debug", type=int, default=1,
            help="debug level (0, 1, 2), default 1"
        )
        args = parser.parse_args()

        with Repo(debug=args.debug) as repo:
            if args.upload:
                repo.upload(args.upload)
            elif args.lspkgs:
                repo.lspkgs()
            elif args.lsall:
                repo.dir()
            else:
                repo.syncdbs()
                repo.syncpkgs()

    except KeyboardInterrupt:
        print("KeyboarInterrupt")
        sys.exit(130)


if __name__ == "__main__":
    main()
