# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class WebshellCrawlerPipeline(object):

    def process_item(self, item, spider):
        return item


class WriterPipeline(object):
    """
    写一般get的
    """
    def __init__(self):
        self.file = open('/Users/gavia/File/Gavia/Lab/work/webshell_crawler/webshell_pages/webshell_index', 'w')
        self.column_list = ['request_url', 'post', "transHeader", "transBody", 'response_status']
        self.writeColumnName(self.column_list, self.file)

    def process_item(self, item, spider):
        if spider.name != "webshell_index":
            return item

        return self.output(item)

    def output(self, spider, item):
        print("==="*40)
        print("[", spider.name, "] :", item['request_url'])
        print("==="*40)

        transHeader = {key.decode('utf-8'): [x.decode("utf-8") for x in value] for (key, value) in item['response_header'].items()}
        transBody = item['response_body'].decode("utf-8")

        if transBody.strip() == "":
            transBody = str(None)

        if "post" not in item.keys() or str(item['post']).replace("{","").replace("}","").strip() == "":
            item['post'] = str(None)

        line = str(item['request_url']) + "\t" + str(item['post']) + "\t" +str(transHeader) + "\t" \
               + transBody.replace("\n","").replace("\r","") + "\t" + str(item['response_status']) + "\n"
        self.file.write(line)
        return item

    def writeColumnName(self, column_list, file):
        first_line = ""
        for colName in column_list:
            first_line += colName + "\t"

        first_line = first_line.strip("\t")
        first_line += "\n"
        file.write(first_line)


class WriterSafePipeline(WriterPipeline):
    """
    写只爬两层的
    """
    def __init__(self):
        super(WriterSafePipeline, self).__init__()
        self.file = open('/Users/gavia/File/Gavia/Lab/work/webshell_crawler/webshell_pages/webshell_safe', 'w')
        self.writeColumnName(self.column_list, self.file)

    def process_item(self, item, spider):
        if spider.name != "webshell_safe":
            return item

        return self.output(spider, item)


class WriterPostPipeline(WriterPipeline):
    """
    写Post的
    """
    def __init__(self):
        super(WriterPostPipeline, self).__init__()
        self.file = open('/Users/gavia/File/Gavia/Lab/work/webshell_crawler/webshell_pages/webshell_post', 'w')
        self.writeColumnName(self.column_list, self.file)

    def process_item(self, item, spider):
        if spider.name.find("webshell_post") < 0:
            return item

        print(spider.name.find("webshell_post"))
        return self.output(spider, item)