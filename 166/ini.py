from shlex import split
import configparser


class ToxIniParser:

    def __init__(self, ini_file):
        """Use configparser to load ini_file into self.config"""
        self.config = configparser.ConfigParser()
        self.config.read(ini_file)

    @property
    def number_of_sections(self):
        """Return the number of sections in the ini file.
           New to properties? -> https://pybit.es/property-decorator.html
        """
        return len(self.config.sections())

    @property
    def environments(self):
        """Return a list of environments
           (= "envlist" attribute of [tox] section)"""
        envs = split(self.config.get('tox', 'envlist').replace(',', '\n'))
        return envs

    @property
    def base_python_versions(self):
        """Return a list of all basepython across the ini file"""
        base_pythons = set()
        for section in self.config.sections():
            if 'basepython' in self.config[section]:
                base_python = self.config.get(section, 'basepython')
                base_pythons.add(base_python)
        return list(base_pythons)