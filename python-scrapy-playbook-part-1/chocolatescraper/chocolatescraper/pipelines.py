## Storing to DB
import mysql.connector ## MySQL
import psycopg2 ## Postgres


from sqlite3 import adapters
from itemadapter import ItemAdapter
from scrapy import Item
from scrapy.exceptions import DropItem


class chocolatescraperpipeline:
    def process_item(self,item,spider):
        return item
   


class PriceToUSDPipeline:
    gbpToUsdRate = 1.3


    def process_item(self, item, spider):
        adapter = ItemAdapter(item)


        if adapter.get('price'):


            floatPrice = float(adapter['price'])


            adapter['price'] = floatPrice * self.gbpToUsdRate


            return item
        else:
            raise DropItem(f"Missing price in {item}")


class DuplicatesPipeline:


    def __init__(self):
        self.names_seen = set()


    def process_item(self, item, spider):
        adapter = ItemAdapter(item)


        if adapter['name'] in self.names_seen:


            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.names_seen.add(adapter['name'])
            return item



class SavingToMySQLPipeline(object):


    def __init__(self):
        self.create_connection()


    def create_connection(self):
        self.connection = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '123456',
            database = 'chocolate_scraping',
            port = '8889'
        )
        self.curr = self.connection.cursor()


    def process_item(self, item, spider):
        self.store_db(item)
        return item


    def store_in_db(self, item):
        self.curr.execute(""" insert into chocolate_products(name,price,url) values (%s,%s,%s)""", (
            item["title"][0],
            item["price"][0],
            item["url"][0]
        ))
        self.conn.commit()



class SavingToPostgresPipeline(object):


    def __init__(self):
        self.create_connection()


    def create_connection(self):
        self.connection = psycopg2.connect(
            host="localhost",
            database="chocolate_scraping",
            user="root",
            password="123456",
            )
        self.curr = self.connection.cursor()


    def process_item(self, item, spider):
        self.store_db(item)
        return item


    def store_in_db(self, item):
        try:
            self.curr.execute(""" insert into chocolate_products values (%s,%s,%s)""", (
                item["title"][0],
                item["price"][0],
                item["url"][0]
        ))
        except BaseException as e:
            print(e)
           
        self.conn.commit()