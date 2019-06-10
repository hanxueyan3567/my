import allure
import pytest
from Common import Request,Assert,read_excel,Login


request = Request.Request()
assertions = Assert.Assertions()

excel_list = read_excel.read_excel_list('./document/退货.xlsx')
ids_list =[]

for i in range(len(excel_list)):
    ids_pop = excel_list[i].pop()

    ids_list.append(ids_pop)
url = Login.url
head = Login.Login().get_token()
th_id = 0

@allure.feature('退货接口')
class Test_th:

    @allure.story('查询退货详情')
    def test_info(self):
        info_resp = request.get_request(url=url+'returnReason/list',
                                        params={'pageNum': 1, 'pageSize': 10})

        assertions.assert_code(info_resp.status_code, 200)
        info_resp_json = info_resp.json()

        assertions.assert_in_text(info_resp_json['message'], '成功')
        data_resp=info_resp_json['data']
        list_resp=data_resp['list']
        item = list_resp[0]
        global th_id
        th_id = item['id']


    @allure.story('删除退货')
    def test_del(self):
        del_resp = request.post_request(url=url + 'returnReason/delete',params={'ids':th_id})

        assertions.assert_code(del_resp.status_code, 200)
        del_resp_json = del_resp.json()

        assertions.assert_in_text(del_resp_json['message'], '成功')

    @allure.story('添加退货')
    @pytest.mark.parametrize('name,sort,status,msg',excel_list,ids=ids_list)
    def test_add(self,name,sort,status,msg):
        add_resp = request.post_request(url=url + 'returnReason/create',
                                        params={'pageNum': 1, 'pageSize': 10},
                                       json ={'name': name, 'sort': sort, 'status': status,
                                              'createTime': ''})
        assertions.assert_code(add_resp.status_code, 200)
        add_resp_json = add_resp.json()

        assertions.assert_in_text(add_resp_json['message'], msg)
