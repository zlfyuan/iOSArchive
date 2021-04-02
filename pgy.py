import os
import requests
import json
import getpass
from bs4 import BeautifulSoup

from yamlPare import Yaml

class Pgy:
    # 获取apikey
    def get_api_key(self):
        _yaml = Yaml()
        object = _yaml.readValue()
        pgy = object["pgy"]
        api_key = pgy["api_key"]
        if api_key == None or len(api_key) != 32:
            return self.pgy_api(self.login())[1]
        else:
            return api_key

    # 登录蒲公英
    def login(self):
        url = 'https://www.pgyer.com/user/login'
        email = input("请输入蒲公英账号 Enter结束：")
        password = getpass.getpass('请输入蒲公英密码 Enter结束：')
        data = {
            'email': email,
            'password': password
        }
        req = requests.post(url, data=data)
        req.encoding = 'UTF-8'

        rp = json.loads(req.text)
        # print(rp)
        status_code = rp['code']
        if status_code == 0:
            # print(req.cookies)
            return req.cookies
        else:
            print(rp['message'])
            self.login()

    # 获取蒲公英api_key user_k
    def pgy_api(self, cookies):
        user_url = 'https://www.pgyer.com/account/api'
        req_user = requests.get(url=user_url, cookies=cookies)
        req_user.encoding = 'UTF_8'
        b = BeautifulSoup(req_user.text, 'html.parser')
        code_tag = b.find_all("code")
        api_key = ''
        user_key = ''
        for i in range(len(code_tag)):
            n = code_tag[i]
            if i == 0:
                api_key = n.contents[0]
            else:
                user_key = n.contents[0]
        # print('api_key \t' + api_key)
        # print('user_key \t' + user_key)
        _yaml = Yaml()
        object = _yaml.readValue()
        pgy = object["pgy"]
        pgy["api_key"] = api_key
        pgy["user_key"] = user_key
        object["pay"] = pgy
        _yaml.saveConfig(object)

        return user_key, api_key

    def uploadIPA(self, ipa_path, updata_des):
        api_key = self.get_api_key()
        if (os.path.exists(ipa_path)):
            print("\n开始上传到蒲公英...")
            url = 'https://www.pgyer.com/apiv2/app/upload'
            data = {
                '_api_key': api_key,
                'buildInstallType': '3',
                'buildPassword': '',
                'buildUpdateDescription': updata_des
            }
            loading = True
            st = 'send.'
            # while loading:
            #     st += "."
            #     print(st)
            files = {'file': open(ipa_path, 'rb')}
            r = requests.post(url, data=data, files=files)
            r.encoding = 'UTF-8'
            r = json.loads(r.text)
            status_code = r['code']
            if status_code == 0:
                # loading = False
                print("上传成功...")
            else:
                # loading = False
                raise Exception("\n%s - %s..." % (r['message'], r['code']))
        else:
            raise Exception("\n没有找到iap包...")

    # 获取app信息
    def getCurrentAppDetail(self):
        api_key = self.get_api_key()
        # 获取所有app
        app_list = requests.post('https://www.pgyer.com/apiv2/app/listMy',
                                 data={'_api_key': api_key})
        json_app_list = json.loads(app_list.text)
        code = json_app_list['code']
        # print(json_app_list)
        if code == 0:
            app_key = json_app_list['data']['list'][0]['appKey']
            # print(app_key)
        else:
            print('获取appkey失败')
            return
        # 获取指定app详情
        pgy_data = {'_api_key': api_key,
                    'appKey': app_key}
        pgy = requests.post("https://www.pgyer.com/apiv2/app/view",
                            data=pgy_data)
        # print(pgy.text)
        json_data = json.loads(pgy.text)
        if code == 0:
            json_content = json_data['data']
            print("\n获取app详情成功...")
            return json_content
        else:
            print('获取app详情失败')
            return


if __name__ == "__main__":
    pgy = Pgy()

    json_content = pgy.getCurrentAppDetail()

    print(json_content)
