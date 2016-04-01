from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://stuliving.com/Index/changeCity.html', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        link_list = []
        for each in response.doc('.city_list').find('li').find('a').items():
            self.crawl(each.attr.href,callback=self.list_page)

    @config(priority=2)
    def list_page(self, response):
        for each in response.doc('.list_on1').find('.drom_pad').find('a').items():
            self.crawl(each.attr.href,callback=self.detail_page)

    @config(priority=2)
    def detail_page(self,response):
        profile_content=''
        for each in response.doc('.datai_intr').find('p').items():
            if each.attr('class') !='ro_one':
                profile_content = profile_content+each.text()
        return {
            "url": response.url,
            "profile_content" : profile_content

        }