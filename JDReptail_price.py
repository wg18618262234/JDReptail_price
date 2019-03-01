from urllib import parse, request
from http import cookiejar
from lxml.html import etree
import time, csv, re, json
import xlrd, xlwt


class Request_jd():
    def __init__(self, url, sku):
        # https: // item.jd.com / 3165584.html
        # 'https://c0.3.cn/stock?skuId=3621191&cat=1320%2C1583%2C1595&venderId=1000074961&area=1_72_2799_0&buyNum=1&choseSuitSkuIds=&extraParam=%7B%22originid%22%3A%221%22%7D&ch=1&fqsp=0&pduid=2021477417&pdpin=&callback=jQuery9134244'
        self.url = url + '?skuId=' + parse.quote(str(
            sku)) + '&cat=1320%2C1583%2C1595&venderId=1000074961&area=1_72_2799_0&buyNum=1&choseSuitSkuIds=&extraParam=%7B%22originid%22%3A%221%22%7D&ch=1&fqsp=0&pduid=2021477417&pdpin=&callback=jQuery9134244'

    def Request_get_read(self):
        self.req = request.Request(url=self.url)
        self.req.add_header('Cookie', 'c3cn=Ef9Ms03P')
        self.response = request.urlopen(self.req)
        self.html = self.response.read().decode('gb18030', 'ignore')
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


sku = []
price = []


def getsku():
    excel = xlrd.open_workbook(r'getsku.xlsx')
    table = excel.sheet_by_index(0)
    rows = table.nrows
    # print(rows)
    for row in range(1, rows):
        data = table.cell(row, 0).value
        sku.append(int(data))


def setprice():
    excel = xlwt.Workbook(encoding='utf-8')
    table = excel.add_sheet('Sheet 1', cell_overwrite_ok=True)
    table.write(0, 0, 'sku')
    table.write(0, 1, '京东价')
    for row in range(1, len(price)):
        # print(price[row - 1])
        table.write(row, 0, sku[row - 1])
        table.write(row, 1, price[row - 1])
        print('sku:', sku[row - 1],'京东价:', price[row - 1])
    excel.save(r'getprice.xls')


if __name__ == '__main__':
    getsku()
    print(sku)
    print('正在获取京东价...')
    for i in sku:
        a = Request_jd('https://c0.3.cn/stock', i)
        a.Request_get_read()
        # print(a.Get_jdprice()['stock']['jdPrice']['p'])
        price.append(a.Get_jdprice()['stock']['jdPrice']['p'])
        # html_data = a.Crow()
    print(price)
    print('正在保存京东价...')
    setprice()
