import configparser
import string

from Builder.Config.BaseConfig import BaseConfig
from Builder.Config.IniWriter import IniWriter

class OptionsSafeConfigParser(configparser.ConfigParser):
    def optionxform(self, optionstr):
        return optionstr
        pass

    def _join_multiline_values(self):
        pass

class ConfigIni(BaseConfig):
    ## NEED FOR INI PARSER
    class BuilderMultiLineDictType(dict):
        def __init__(self):
            super(ConfigIni.BuilderMultiLineDictType,self).__init__()
            pass

        def __setitem__(self, key, val):
            #print ("VALUE!!!",val)
            #print ("KEY!!!",key)
            if isinstance(val,list) is True and len(val) == 1:
                val = val[0]
                pass

            realValue = None
            if key in self:
                oldValue = self[key]
                if isinstance( oldValue,list ) is True:
                    if val in oldValue:
                        realValue = oldValue
                        pass
                    else :
                        realValue = oldValue
                        if isinstance( val,list ) is True:
                            realValue += val
                            pass
                        else:
                            realValue.append(val)
                            pass
                        pass
                else:
                    if oldValue == val:
                        realValue = val
                        pass
                    else:
                        realValue = [oldValue,val]
                        pass
                    pass
            else:
                realValue = val
                pass

            if key in self:
                #print ("OLd ",self[key])
                pass
            #print (" real VALUE ",realValue)
            dict.__setitem__(self, key, realValue)
            pass

    def __init__(self):
        super(ConfigIni,self).__init__()
        self.config = OptionsSafeConfigParser(None,ConfigIni.BuilderMultiLineDictType,strict = False,empty_lines_in_values = False)
        pass

    def _read(self,path):
        self.config.read(path)
        sections = self.config.sections()
        for section in sections:
            self.data[section] = {}
            options = self.config.options(section)
            for option in options:
                value = self.config.get(section,option,raw = True)
                self.data[section][option] = value
                pass
            pass
        pass

    def _write(self,fp):
        writer = IniWriter()
        writer.write(fp, self.data)
        pass
