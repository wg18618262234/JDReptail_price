from urllib import parse, request
from http import cookiejar
from lxml.html import etree
import time, csv, re,json


class Request_jd():
    def __init__(self, url, sku):
        # https: // item.jd.com / 3165584.html
        # 'https://c0.3.cn/stock?skuId=3621191&cat=1320%2C1583%2C1595&venderId=1000074961&area=1_72_2799_0&buyNum=1&choseSuitSkuIds=&extraParam=%7B%22originid%22%3A%221%22%7D&ch=1&fqsp=0&pduid=2021477417&pdpin=&callback=jQuery9134244'
        self.url = url+'?skuId='+parse.quote(str(sku))+'&cat=1320%2C1583%2C1595&venderId=1000074961&area=1_72_2799_0&buyNum=1&choseSuitSkuIds=&extraParam=%7B%22originid%22%3A%221%22%7D&ch=1&fqsp=0&pduid=2021477417&pdpin=&callback=jQuery9134244'

    def Request_get_read(self):
        self.req = request.Request(url=self.url)
        self.req.add_header('Cookie','c3cn=Ef9Ms03P')
        self.response = request.urlopen(self.req)
        self.html = self.response.read().decode('gb18030','ignore')
        # print(self.html)

    def Get_html(self):
        return self.html

    def Get_jdprice(self):
        return json.loads(self.Get_html()[14:-1])

    def Crow(self):
        html = etree.HTML(self.html)

        self.html_data = html.xpath('//*[@class="summary summary-first"]')
        self.Csv_save(self.html_data)
        return self.html_data

    # 没用
    @staticmethod
    def Csv_save(html_data):
        with open('JD_goods.csv', 'a', newline='', encoding='utf-8')as f:
            write = csv.writer(f)
            for data in html_data:
                if not data.xpath('div/div[@class="p-name p-name-type-2"]/a/em'):
                    p_name = data.xpath(
                        'div/div/div[2]/div[1]/div[@class="p-name p-name-type-2"]/a/em')
                    p_price = data.xpath(
                        'div/div/div[2]/div[1]/div[@class="p-price"]/strong/i/text()')
                    p_href = data.xpath(
                        'div/div/div[2]/div[1]/div/a/@href')
                    p_name1 = data.xpath(
                        'div/div/div[2]/div[2]/div[@class="p-name p-name-type-2"]/a/em')
                    # p_price1 = data.xpath(
                    #     'div/div/div[2]/div[2]/div[@class="p-price"]/strong/i/text()')
                    p_price1 = data.xpath(
                        'div/div/div[2]/div[2]/div[@class="p-price"]/strong/em/text()')
                    p_href1 = data.xpath(
                        'div/div/div[2]/div[2]/div/a/@href')
                    try:
                        p_skuid = re.findall("//item.jd.com/(.+?).html", p_href[0])
                        p_skuid1 = re.findall("//item.jd.com/(.+?).html", p_href1[0])
                    except:
                        p_skuid = []
                    if len(p_price) == 0:
                        p_price = data.xpath('div/div[@class="p-price"]/strong/@data-price')
                        p_price1 = data.xpath('div/div[@class="p-price"]/strong/@data-price')

                    try:
                        print(p_skuid[0], p_name[0].xpath('string(.)'), p_price[0])
                        write.writerow([p_skuid[0], p_name[0].xpath('string(.)'), p_price[0]])
                        print(p_skuid1[0], p_name1[0].xpath('string(.)'), p_price1[0])
                        write.writerow([p_skuid1[0], p_name1[0].xpath('string(.)'), p_price1[0]])
                    except:
                        print(p_skuid, p_name[0].xpath('string(.)'), p_price[0])
                        write.writerow([p_skuid, p_name[0].xpath('string(.)'), p_price[0]])
                        print(p_price1)
                        print(p_skuid1, p_name1[0].xpath('string(.)'), p_price1)
                        write.writerow([p_skuid1, p_name1[0].xpath('string(.)'), p_price1])
                else:
                    p_name = data.xpath('div/div[@class="p-name p-name-type-2"]/a/em')
                    p_price = data.xpath('div/div[@class="p-price"]/strong/i/text()')
                    p_href = data.xpath('div/div/a/@href')
                    try:
                        p_skuid = re.findall("//item.jd.com/(.+?).html", p_href[0])
                    except:
                        p_skuid = []
                    if len(p_price) == 0:
                        p_price = data.xpath('div/div[@class="p-price"]/strong/@data-price')

                    try:
                        print(p_skuid[0], p_name[0].xpath('string(.)'), p_price[0])
                        write.writerow([p_skuid[0], p_name[0].xpath('string(.)'), p_price[0]])
                    except:
                        print(p_skuid, p_name[0].xpath('string(.)'), p_price[0])
                        write.writerow([p_skuid, p_name[0].xpath('string(.)'), p_price[0]])
        f.close()


sku = [3378602,
1831156,
1831149,
100001023409,
5298426,
3165584,
100000913639,
100000796984,
6834812,
2918972,
2816019,
2951508,
100001023399,
2918974,
7603390,
3378604,
100001286668,
4822384,
838860,
659171,
659169,
4159332,
100001286666,
838867,
1523681,
659184,
659181,
7118756,
838866,
1523698,
838864,
4239102,
4239074,
1523697,
4822392,
4018231,
1523682,
6356277,
838869,
1523699,
8201278,
4018241,
838870,
100001286654,
5436612,
2922989,
1975749,
8053326,
7400680,
8814705,
100000243586,
4720216,
1362719,
100000597124,
7574992,
5793608,
5793638,
837822,
5658307,
7787803,
5658291,
4342665,
5658273,
5800079,
5888258,
5793636,
5800089,
5793604,
626469,
5313248,
5536096,
4599105,
5274468,
4599147,
5126175,
4599115,
4204095,
5105152,
4969829,
4969831,
8031350,
4811016,
7250313,
7036780,
6536189,
7416398,
2375245,
4585793,
100002349412,
5030778,
6611354,
100001735077,
2375193,
3936477,
100000117129,
2231816,
2231822,
4614180,
2231828,
2232423,
2232439,
2232419,
2231836,
2231820,
7090171,
6873319,
6873327,
6873317,
2027364,
2027392,
2027385,
2027393,
1362721,
4913745,
5867655,
5384564,
626389,
7051286,
3948513,
4593226,
5105154,
5357840,
4593258,
4538290,
4593228,
3944399,
4593236,
6099539,
6099567,
5867425,
4204093,
4967235,
8551618,
4585024,
5436006,
4969825,
4969823,
4593230,
4969805,
4969783,
4969847,
4969803,
100001083558,
8739463,
4969827,
2375195,
2375237,
2374260,
4154714,
2375231,
3547974,
2375229,
2375235,
2375233,
4456409,
2375225,
3547992,
2375239,
2375241,
2374262,
2374264,
2374270,
2375227,
4062776,
2232429,
2232433,
2232425,
6824845,
2231834,
6824855,
6611356,
2231830,
2232415,
2232441,
4487462,
2232431,
2232437,
4599882,
6659616,
4487440,
3895789,
100000117101,
7416380,
8180604,
100000117121,
100000117123,
8764123,
100000117119,
100001721613,
100002329090,
100000117143,
100000244504,
100001255000,
100001002605,
100000244506,
100001254892,
100001003239,
100001254726,
990670,
5114033,
418655,
3112229,
5311092,
2386440,
1489967,
7036770,
3618035,
3944253,
4584794,
7950032,
4360445,
418657,
4705591,
7949944,
3944261,
2192019,
1865308,
3540714,
4908135,
3621191,
3764581,
6003001,
6003047,
100001816403,
100002472528,
6003025,
]

for i in sku:
    a = Request_jd('https://c0.3.cn/stock', i)
    a.Request_get_read()
    print(a.Get_jdprice()['stock']['jdPrice']['p'])
    # html_data = a.Crow()
