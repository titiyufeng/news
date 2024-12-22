import time
import pytest
import uiautomator2 as u2
import logging

class Test():
    device = u2.connect()
    app_name = "com.netease.newsreader.activity"
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    @pytest.fixture()
    def init(self):
        """
        初始化：打开app，并点击到头条栏目
        清理：关闭app
        """
        self.device.app_start(self.app_name)
        time.sleep(6)
        self.device(text="头条").click()
        yield
        self.device.app_stop(self.app_name)

    def test_change_tab(self, init):
        """
        测试内容：顶部tab切换检查
        检查规则：抽取3个tab进行切换，并检查切换后对应页面包含了当前tab的关键内容
        """
        tab_list = [("关注", "我的关注"), ("头条", "新闻"), ("体育", "英超")]
        # tab_list = [("关注", "我的关注"), ("体育", "英超")]
        for tab in tab_list:
            self.device(text=tab[0]).click()
            time.sleep(2)
            assert self.device(textContains=tab[1]).info, tab[0] + "tab切换检查失败"  ##检查对应的控件有展示
            print(tab[0]+"切换检查通过")
            self.logger.info(tab[0]+"切换检查通过")

    def test_all_tab(self, init):
        """
        检查内容：可能成功添加栏目，添加后首页有展示对应的栏目
        主要步骤：
            1、点击首页所有栏目控件，进入所有栏目页
            2、添加“独家”栏目，然后回到首页，检查独家栏目有展示
            3、再次进入所有栏目页
            4、将“独家”栏目删除
        """
        ##添加栏目
        self.device(resourceId="com.netease.newsreader.activity:id/edit_img").click()
        time.sleep(2)
        self.device(text="独家").click()
        time.sleep(2)
        self.device(resourceId="com.netease.newsreader.activity:id/close_button").click()
        time.sleep(2)
        assert self.device(text="独家").info,"栏目添加失败"  ##检查对应的控件有展示
        print("添加栏目检查通过")
        self.logger.info("添加栏目检查通过")

        #删除之前添加的栏目
        self.device(resourceId="com.netease.newsreader.activity:id/edit_img").click()
        time.sleep(2)
        self.device(text="编辑").click()
        time.sleep(2)
        self.device(text="独家").click()
        time.sleep(2)
        self.device(text="完成").click()
        time.sleep(2)