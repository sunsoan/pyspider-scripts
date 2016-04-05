from pyspider.libs.base_handler import *
from pyquery import PyQuery as pq

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
        dorm = {}
        profile = ''
        for each in response.doc('.datai_intr').find('p').items():
            if each.attr('class') !='ro_one':
                profile = profile+each.text()


        img_urls=[]
        for each in response.doc('.ulBigPic').find('a').items():
            img_urls.append(each.attr.href)

        service = []
        for each in response.doc('.serv').find('li').items():
            service.append(each.text())

        near_univer = []
        for each in response.doc('.near_na').items():
            univer_name = each.find('.near_na1').text()
            univer_distance = each.find('.near_na2').text()
            univer = {'univer_name':univer_name,'univer_distance':univer_distance}
            near_univer.append(univer)

        room_class = []
        for each in response.doc('.roomlist').items():
            rcn = each.find('.to_fname').text()
            price = each.find('.zt_mon1').text()
            square =  each.find('.to_dx').eq(1).text()
            room_profile = each.find('.list_open').find('.gk_1').find('p').text()
            bed_size = each.find('.list_open').find('.list_wrap').find('p').eq(3).text()
            bedroom = []
            bdr = each.find('.list_open').find('.fz_ub').eq(0)
            for each_i in pq(bdr).find('li').items():
                bedroom.append(each_i.text())

            bathroom = []
            bthr = each.find('.list_open').find('.fz_ub').eq(1)
            for each_i in pq(bthr).find('li').items():
                bathroom.append(each_i.text())

            kitchen = []
            ktn = each.find('.list_open').find('.fz_ub').eq(2)
            for each_i in pq(ktn).find('li').items():
                kitchen.append(each_i.text())

            room_service = {'bedroom':bedroom,'bathroom':bathroom,'kitchen':kitchen}
            room = {'rcn':rcn,'price':price,'aquare':square,'room_breif':room_profile,'bed_size':bed_size,'room_service':room_service}
            room_class.append(room)


        return {
            "url": response.url,
            "profile": profile,
            "service": service,
            "img_urls":img_urls,
            "near_univer":near_univer,
            "room":room_class
        }


