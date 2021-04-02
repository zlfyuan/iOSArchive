import yaml
import os

conf_path = os.path.expandvars('$HOME') + "/.dabao_config.yml"


class Yaml:
    def __init__(self):
        pass

    def saveConfig(self, yaml_obj):
        try:
            with open(conf_path, "r") as yaml_file:
                main_yaml = open(conf_path, 'w')
                yaml.dump(yaml_obj, main_yaml)
                main_yaml.close()
        except IOError:
            print("\n读取配置文件失败，检查是否有{0}".format(conf_path))

    def readValue(self):
        try:
            # 打开文件
            with open(conf_path, encoding='utf8') as a_yaml_file:
                # 解析yaml
                parsed_yaml_file = yaml.load(a_yaml_file, Loader=yaml.FullLoader)
                # print(parsed_yaml_file)
                return parsed_yaml_file
        except IOError:
            print("\n读取配置文件失败，检查是否有{0}".format(conf_path))

if __name__ == "__main__":
    _yaml = Yaml()
    object = _yaml.readValue()
    print(object)
    pgy = object["pgy"]
    pgy["api_key"] = "api_key"
    pgy["user_key"] = "user_key"
    object["pgy"] = pgy
    _yaml.saveConfig(object)
