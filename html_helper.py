from html.parser import HTMLParser
import requests

import queue



class Item():
    pass



class Craftable():
    def __init__(self):
        self.components ={}
        self.name = ""

        self.tags=[]

    def add_component(self,name,amount):
        self.components[name] = amount

class ItemHandler():
    def __init__(self):
        self.recipies={}
        self.craftables ={}
        self.items ={}
        pass




def get_page(page):
    return requests.get(page,verify=False).text

class Collector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tree = {}
        self._level = 0

        self._in_body=False

        self._tag_stack = []

        self._tag_stack.append({"name":"body","attrs":[],"childs":[],"data":[]})

    def handle_starttag(self, tag, attrs):
        if tag == "body":
            self._in_body=True

        if self._in_body:
            print(self._level*" "+"start:",tag,attrs)


            self._tag_stack.append({"name":tag,"atrrs":attrs,"childs":[],"data":[]})
        self._level += 1



    def handle_data(self,data):
        if self._in_body:
            print(self._level*" "+"data",data)

    def handle_endtag(self, tag):
        if self._in_body:
            print(self._level*" "+"end:",tag)

            child=self._tag_stack.pop()
            self._tag_stack[-1]["childs"].append(child)

            #self.tag_stack[-1]["childs"].append(self.tag_stack.pop())
            #print(self._tag_stack[-1])

        if tag == "body":
            self.tree = self._tag_stack
            self._in_body = False

        self._level -= 1


class SearchHelper():
    def __init__(self,tree):
        self.tree = tree

        self.__tag_list={} #has all the tags in it  (a ,h1,p,body ... xyz) with the tag ids
        self.__single_tag =[] # all of the tags broken down



    @staticmethod
    def find_all_tags(tree,searched_tag):
        link_list = []
        for tag in tree:
            if tag["name"] == searched_tag:
                print(tag)
                link_list.append(tag)

            if len(tag["childs"]) > 0:
                links = SearchHelper.find_all_tags(tag["childs"],searched_tag)
                if len(links) > 0:
                    link_list.extend(links)
        return link_list


    def flatten(self,tree=None):
        if tree:
            for tag in self.tree:
                if len(tag["childs"]) >0:
                    child_ids = self.flatten(tree=tag["childs"])

                #add copy of self to list
                #add own id to the tag list
                #change childs of copy to ids or nothing



page = "https://idleon.miraheze.org/wiki/Smithing"
sample_html = "<htm><body><h1 color='ffffff'>my text <b>is here   <a href='abc.com'/></b> ... ahhhh</h1></body></html>"

#print(get_page(page))
main_parser = Collector()
main_parser.feed(get_page(page))


#main_parser.feed("<htm><body><h1 color='ffffff'>my text <b>is here   <a href='abc.com'/></b> ... ahhhh</h1></body></html>")
print(main_parser.tree)

links = SearchHelper.find_all_tags(main_parser.tree,"table")

for link in links:
    print(link)
