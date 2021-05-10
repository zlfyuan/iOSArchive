import os, sys
import configparser

conf_path = os.path.expandvars('$HOME') + "/.dabao_config.ini"

pgySection = "pgySection"
TargetSection = "TargetSection"


class ARCConfig:

    def Config(path=conf_path):
        cf = configparser.ConfigParser()
        if not os.path.exists(path):
            print("❌无法获取到{0},请检查配置文件".format(conf_path))
            sys.exit(1)
        cf.read(path)
        return cf

    def getConfig(section, key):
        cf = ARCConfig.Config()
        ret = cf.has_section(section)
        if ret is True:
            val = cf.get(section, key)
            return val
        else:
            # print("❌无法获取到{0},请检查配置文件".format(key))
            pass

    def saveConfig(section, key, value):
        cf = ARCConfig.Config()
        ret = cf.has_section(section)
        if ret is True:
            cf.set(section, key, value)
        else:
            cf.add_section(section)
            cf.set(section, key, value)
        cf.write(open(conf_path, "w"))

    def remove(section,key):
        cf = ARCConfig.Config()
        ret = cf.has_section(section)
        if ret is True:
            cf.remove_option(section, key)
            cf.write(open(conf_path, "w"))
        else:
            pass


if __name__ == "__main__":

    # ARCConfig.saveConfig(pgySection, "api_key", "1039013023029302392039")
    # ARCConfig.getConfig(pgySection, "api_key")
    ARCConfig.remove(pgySection,"api_key")
