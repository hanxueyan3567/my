import allure
import pytest
from Common import Request,Assert,read_excel,Login

request = Request.Request()
assertions = Assert.Assertions()

excel_list = read_excel.read_excel_list('../document/优惠券.xlsx')
ids_list =[]

for i in range(len(excel_list)):
    ids_pop = excel_list[i].pop()

    ids_list.append(ids_pop)

head = Login.Login().get_token()
yhq_id = 0


@allure.feature('优惠券')
class Test_yhy:

    @allure.story('查询优惠券名称')
    def test_info(self):
        info_resp = request.get_request(url='http://192.168.60.132:8080/coupon/list',
                                        params={'pageNum': 1, 'pageSize': 10})

        assertions.assert_code(info_resp.status_code, 200)
        info_resp_json = info_resp.json()

        assertions.assert_in_text(info_resp_json['message'], '成功')

        resp_data= info_resp_json['data']
        data__list = resp_data['list']
        item = data__list[0]

        global yhq_id
        yhq_id = item['id']
    @allure.story('删除优惠券')
    def test_del(self):
        del_resp = request.post_request(url='http://192.168.60.132:8080/coupon/delete/'+str(yhq_id))
        assertions.assert_code(del_resp.status_code, 200)
        del_resp_json = del_resp.json()
        assertions.assert_in_text(del_resp_json['message'], '成功')

    @allure.story('添加优惠券')
    @pytest.mark.parametrize('name,amount,minPoint,publishCount,msg', excel_list, ids=ids_list)
    def test_add(self, name,amount,minPoint,publishCount,msg):
        login_resp = request.post_request(url='http://192.168.60.132:8080/coupon/create',
                                          json={"type":0,"name":name,"platform":0,"amount":amount,"perLimit":1,"minPoint":minPoint,
                                                 "startTime":"","endTime":"","useType":0,"note":"","publishCount":publishCount,
                                                 "productRelationList":[],"productCategoryRelationList":[]}, )
        assertions.assert_code(login_resp.status_code, 200)
        login_resp_json = login_resp.json()
        assertions.assert_in_text(login_resp_json['message'], msg)



