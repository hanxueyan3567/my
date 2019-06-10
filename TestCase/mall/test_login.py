



import allure
import pytest
from Common import Request,Assert,read_excel


request = Request.Request()
assertions = Assert.Assertions()

excel_list = read_excel.read_excel_list('./document/test.xlsx')
ids_list =[]

for i in range(len(excel_list)):
    ids_pop = excel_list[i].pop()

    ids_list.append(ids_pop)

@allure.feature('登录模块')    #'http://192.168.60.132:8080/admin/login'   "username": "admin", "password": "123456"
class Test_login:

    @allure.story('登录')
    def test_login(self):
        login_resp =request.post_request(url='http://192.168.60.132:8080/admin/login',json={"username": "admin", "password": "123456"})

        assertions.assert_code(login_resp.status_code,200)

        print(login_resp.text)
        print(type(login_resp.text))

        login_resp_json = login_resp.json()

        print(type(login_resp_json))

        assertions.assert_in_text(login_resp_json['message'],'成功')




#@allure.feature('登录模块')    #'http://192.168.60.132:8080/admin/login'   "username": "admin", "password": "123456"
#class Test_login:

    @allure.story('登录')

    @pytest.mark.parametrize('name,pwd,msg',excel_list,ids=ids_list)
    def test_login1(self,name,pwd,msg):
        login_resp = request.post_request(url='http://192.168.60.132:8080/admin/login',json={"username": name, "password": pwd})

        assertions.assert_code(login_resp.status_code,200)

        print(login_resp.text)
        print(type(login_resp.text))

        login_resp_json = login_resp.json()

        print(type(login_resp_json))

        assertions.assert_in_text(login_resp_json['message'],msg)


