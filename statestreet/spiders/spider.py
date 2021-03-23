import json

import scrapy

from scrapy.loader import ItemLoader

from ..items import StatestreetItem
from itemloaders.processors import TakeFirst


class StatestreetSpider(scrapy.Spider):
	name = 'statestreet'
	start_urls = ['https://www.statestreet.com/bin/statestreet/insightsservice?parentPath=/content/ssbsr/en_US/ideas/articles&topic=statestreet:topics/all&business=statestreet:businessunits/all']

	def parse(self, response):
		data = json.loads(response.text)
		for post in data['results']['article']:
			url = post['pageURL']
			date = post['date']
			title = post['title']
			yield response.follow(url, self.parse_post, cb_kwargs={'date': date, 'title': title})

	def parse_post(self, response, date, title):
		description = response.xpath('//div[@class="flexi_par parsys"]//text()[normalize-space() and not(ancestor::a)]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=StatestreetItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
