import scrapy
from scrapy_splash import SplashRequest
from ..items import WedstrijdItem


class AtletiekSpider(scrapy.Spider):
    name = "atletiek"
    allowed_domains = ["atletiek.nu"]

    script = """
        function main(splash, args)
        splash.private_mode_enabled = false
        url = args.url
        assert(splash:go(url))
        btn = assert(splash:select_all('.ghostbuttons'))
        btn[3]:mouse_click()
        assert(splash:wait(1))
        return splash:html()
        end
    """
    # plaats = plaats[plaats.find(char1)+1 : plaats.find(char2)]
    custom_settings = {
        "DOWNLOAD_DELAY": 1,
    }
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"

    def start_requests(self):
        yield SplashRequest(
            url="https://atletiek.nu/",
            callback=self.parse,
            endpoint="execute",
            args={"lua_source": self.script},
            headers={"User-Agent": self.user_agent},
        )

    def parse(self, response):
        wedstrijden = response.xpath("//tr[@onclick]")
        for wedstrijd in wedstrijden:
            wedstrijd_item = WedstrijdItem()
            wedstrijd_item["wedstrijd"] = wedstrijd.xpath(".//td/a/span/text()").get()
            wedstrijd_item["datum"] = wedstrijd.xpath(
                ".//td[@class='datumCol']/span/text()"
            ).get()
            wedstrijd_item["plaats"] = wedstrijd.xpath(
                "normalize-space(.//td[3]/text())"
            ).get()
            wedstrijd_item["categorie"] = []

            link = wedstrijd.xpath(".//td/a/@href").get()

            # yield {"wedstrijd": wedstrijd_item}
            yield response.follow(url=link, callback=self.parse_wedstrijd)

    def parse_wedstrijd(self, response):
        verenigingen = response.xpath("//div[@id='verenigingenSelect']/a")
        for vereniging in verenigingen:
            naam = vereniging.xpath(".//span/text()").get()
            link = vereniging.xpath(".//@href").get()
            if naam == "AV Feniks":
                yield response.follow(url=link, callback=self.parse_categorie)

    # def parse_categorie(self, response):
    #     verenigingen = response.xpath("//div[@id='verenigingenSelect']/a")
    #     for vereniging in verenigingen:
    #         naam = vereniging.xpath(".//span/text()").get()
    #         link = vereniging.xpath(".//@href").get()
    #         if naam == "AV Feniks":
    #             yield response.follow(url=link, callback=self.parse_categorie)
