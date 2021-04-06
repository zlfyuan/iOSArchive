from ruamel.yaml import YAML
import os

conf_path = os.path.expandvars('$HOME') + "/.dabao_config.yml"


class Yaml:
    def __init__(self):
        pass

    def saveConfig(self, yaml_obj):
        try:
            with open(conf_path, "w", encoding="utf8") as yaml_file:
                yaml = YAML(typ='safe', pure=True)
                yaml.dump(yaml_obj, yaml_file)
        except IOError:
            print("\n读取配置文件失败，检查是否有{0}".format(conf_path))

    def readValue(self):
        try:
            # 打开文件
            with open(conf_path, encoding='utf8') as a_yaml_file:
                # 解析yaml
                yaml = YAML(typ='safe', pure=True)
                parsed_yaml_file = yaml.load(a_yaml_file)
                # print(parsed_yaml_file)
                return parsed_yaml_file
        except IOError:
            print("\n读取配置文件失败，检查是否有{0}".format(conf_path))

if __name__ == "__main__":
    _yaml = Yaml()
    pgy = {"api_key": "api_key", "user_key": "user_key"}
    _yaml.saveConfig(pgy)
