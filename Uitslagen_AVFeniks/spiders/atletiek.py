import scrapy
from scrapy_splash import SplashRequest
from ..items import WedstrijdItem, CategorieItem, AtleetItem, UitslagItem


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

    index = 1

    def parse(self, response):

        wedstrijden = response.xpath("//tr[@onclick]")
        for wedstrijd in wedstrijden:

            wedstrijd_item = WedstrijdItem()
            wedstrijd_item["id"] = self.index
            self.index += 1
            wedstrijd_item["wedstrijd"] = wedstrijd.xpath(".//td/a/span/text()").get()
            wedstrijd_item["datum"] = wedstrijd.xpath(
                ".//td[@class='datumCol']/span/text()"
            ).get()
            wedstrijd_item["plaats"] = wedstrijd.xpath(
                "normalize-space(.//td[3]/text())"
            ).get()
            wedstrijd_item["onderdeel"] = []

            link = wedstrijd.xpath(".//td/a/@href").get()
            yield response.follow(
                url=link,
                callback=self.parse_wedstrijd,
                meta={"wedstrijd_item": wedstrijd_item},
            )

    def parse_wedstrijd(self, response):
        wedstrijd_item = response.meta["wedstrijd_item"]

        verenigingen = response.xpath("//div[@id='verenigingenSelect']/a")
        for vereniging in verenigingen:
            naam = vereniging.xpath(".//span/text()").get()
            link = vereniging.xpath(".//@href").get()

            if naam == "AV Feniks":
                yield response.follow(
                    url=link,
                    callback=self.parse_categorie,
                    meta={"wedstrijd_item": wedstrijd_item},
                )

    def parse_categorie(self, response):
        wedstrijd_item = response.meta["wedstrijd_item"]

        categorieën = response.xpath("//table[@class='deelnemerstabel ']")
        for categorie in categorieën:
            tabel = categorie.xpath(".//preceding-sibling::h3[1]/text()").get()
            leeftijd = tabel.split("-")[0]
            onderdeelTitel = tabel.split("-")[1]

            categorie_item = CategorieItem()
            categorie_item["onderdeel"] = onderdeelTitel
            categorie_item["atleet"] = []

            atleten = categorie.xpath(".//tbody/tr")
            for atleet in atleten:
                naam = atleet.xpath(".//td[2]/a/text()").get().strip()
                if "x" in tabel:
                    naam = atleet.xpath(".//td/a/span[3]/text()").get().strip()
                elif not naam:
                    naam = atleet.xpath(".//td/a/span[2]/text()").get().strip()

                if atleet.xpath(".//td[4]/a/text()").get():
                    leeftijdCategorie = atleet.xpath(".//td[4]/a/text()").get().strip()
                else:
                    leeftijdCategorie = leeftijd

                atleet_item = AtleetItem()
                atleet_item["atleet"] = naam
                atleet_item["categorie"] = leeftijdCategorie
                atleet_item["uitslag"] = []

                uitslagen = atleet.xpath(".//td")
                for uitslag in uitslagen:

                    if "Combined-events" in tabel:
                        resultaat = uitslag.xpath(".//span/text()").get()
                        titel = uitslag.xpath(".//span/@title").get()
                    else:
                        resultaat = uitslag.xpath(".//b/span[2]/text()").get()
                        titel = uitslag.xpath(".//b/span[2]/@title").get()

                    if titel:
                        onderdeel = titel
                        if "<" in titel:
                            onderdeel = onderdeel.split("<")[0]

                        wind = titel
                        if "m/s" in titel:
                            wind = wind[wind.find("<br>") + 4 : wind.find("m/s<br />")]
                        else:
                            wind = "NT"

                        uitslag_item = UitslagItem()
                        uitslag_item["resultaat"] = resultaat
                        uitslag_item["onderdeel"] = onderdeel
                        uitslag_item["wind"] = wind

                        atleet_item["uitslag"].append(uitslag_item)

                categorie_item["atleet"].append(atleet_item)

            wedstrijd_item["onderdeel"].append(categorie_item)

        yield wedstrijd_item
