
import allure
import pytest
from Common import Request,Assert,read_excel,Login,Tools

request = Request.Request()
assertions = Assert.Assertions()
url = 'http://192.168.60.132:1811/'
excel_list = read_excel.read_excel_list('../document/注册.xlsx')
ids_list =[]

for i in range(len(excel_list)):
    ids_pop = excel_list[i].pop()

    ids_list.append(ids_pop)

@allure.feature('用户注册接口')
class Test_zc:

    @allure.story('手机')
    def test_in(self):
        info_resp = request.post_request(url=url+'/user/signup',
                                        json={  "phone":Tools.phone_num(),"pwd": '123456aa', "rePwd":'123456aa',"userName":Tools.random_str_abc(6)+Tools.random_123(5) })

        assertions.assert_code(info_resp.status_code, 200)
        resp_json = info_resp.json()
        assertions.assert_in_text(resp_json['respCode'],'0')
    @allure.story('注册')
    @pytest.mark.parametrize('userName,pwd,repwd,	code', excel_list, ids=ids_list)
    def test_info(self,  userName, pwd, repwd, code):
        info_resp = request.post_request(url=url + '/user/signup',
                                         json={"phone":Tools.phone_num() , "pwd": pwd, "rePwd": repwd,
                                               "userName": userName})

        assertions.assert_code(info_resp.status_code, 200)
        resp_json = info_resp.json()
        assertions.assert_in_text(resp_json['respCode'], code)
