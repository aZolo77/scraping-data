# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from itemadapter import ItemAdapter
from pymongo import MongoClient
import sqlite3

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

# скрэпинг цитат
class QuotesSqlDbPipeLine:
    def open_spider(self, spider):
        # create DB
        self.connection = sqlite3.connect('quotes.db')
        self.cursor = self.connection.cursor()
    
    def process_item(self, item, spider):
        # create tables
        create_tables_query = '''
            CREATE TABLE IF NOT EXISTS quotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL UNIQUE
            );

            CREATE TABLE IF NOT EXISTS authors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            );

            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tag TEXT NOT NULL UNIQUE
            );
        '''
        
        try:
            self.cursor.executescript(create_tables_query)
            self.connection.commit()
        except sqlite3.OperationalError as e:
            print("Ошибка подключения:", e)
            pass
        
        # insert values
        
        # -- insert quote
        insert_quote = '''
            INSERT INTO quotes(text)
            VALUES(?)
        '''
        quote_tpl = (item.get('text'),)        
        self.cursor.execute(insert_quote, quote_tpl)
        self.connection.commit()
        
        # -- insert author
        author_name = item.get('author')
        
        author_tpl = (author_name, )
        insert_author = '''
            INSERT INTO authors(name)
            VALUES(?)
        '''
        
        self.cursor.execute(insert_author, author_tpl)
        self.connection.commit()
        
        # -- insert tag
        tags = item.get('tags')
        for t in tags:
            insert_tags = '''
                INSERT INTO tags(tag)
                VALUES(?)
            '''
            
            self.cursor.execute(insert_tags, (t,))
            self.connection.commit()
        
    
    def close_spider(self, spider):
        self.connection.close()
    

# скрэпинг одежды
class ClothesSqlDbPipeLine:
    def open_spider(self, spider):
        self.connection = sqlite3.connect('clothes.db')
        self.cursor = self.connection.cursor()
    
    def process_item(self, item, spider):
        # create DB
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS items (
                image_link TEXT UNIQUE,
                item_name TEXT NOT NULL,
                item_price TEXT NOT NULL,
                item_description TEXT
            );  
        '''
        
        try:
            self.cursor.execute(create_table_query)
            self.connection.commit()
        except sqlite3.OperationalError as e:
            print("Ошибка подключения:", e)
            pass
        
        # insert item
        insert_items_query = '''
            INSERT INTO items(image_link, item_name, item_price, item_description)
            VALUES(?, ?, ?, ?)
        '''
        
        item_tpl = (
            item.get('image', 'No link'),
            item.get('name', 'No name'),
            item.get('price', '0'),
            item.get('description', 'lorem ipsum')
        )
        
        self.cursor.execute(insert_items_query, item_tpl)
        self.connection.commit()
    
    def close_spider(self, spider):
        self.connection.close()


class MongoDbPipeLine:
    def open_spider(self, spider):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['test_items']
    
    def process_item(self, item, spider):
        collection_name = 'items'
        self.db[collection_name].insert_one(item)
    
    def close_spider(self, spider):
        self.client.close()