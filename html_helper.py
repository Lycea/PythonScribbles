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
            #print(self._level*" "+"data",data)
            self._tag_stack[-1]["data"].append(data)

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
                #print(tag)
                link_list.append(tag)

            if len(tag["childs"]) > 0:
                links = SearchHelper.find_all_tags(tag["childs"],searched_tag)
                if len(links) > 0:
                    link_list.extend(links)
        return link_list



    def __process_tag(self,tag):
        child_ids = []
        own_id = len(self.__single_tag)

        #append the full tag to list
        self.__single_tag.append( tag.copy())

        if not tag["name"] in self.__tag_list: self.__tag_list[tag["name"]] = []
        self.__tag_list[tag["name"]].append(own_id)


        if len(tag["childs"]) > 0:
            child_ids = self.flatten(tree=tag["childs"])

        self.__single_tag[own_id]["childs"] = child_ids
        # add copy of self to list
        # add own id to the tag list
        # change childs of copy to ids or nothing

        return own_id

    def flatten(self,tree=None,parent=-1):
        child_ids =[]
        if not tree:
            for tag in self.tree:
                child_ids.append(self.__process_tag(tag))
        else:
            for tag in tree:
                child_ids.append(self.__process_tag(tag))

        return child_ids

    def _get_child_ids(self,ids):
        child_elements = []

        for id in ids:
            child_elements.extend(self.__single_tag[id]["childs"])
        return set(child_elements)

    def search_dyn(self,syntax):
        fit_elements = []

        fitting_element_ids =[]
        subseqent_elements = syntax.split("/")

        #iterate all subelements
        for element in subseqent_elements:
            #check if searched tag exists at all
            if element in self.__tag_list:
                all_element_ids = self.__tag_list[element]

                #diff the own list and the set list and return the ones from own
                #list which are the same
                #(only do if not the first element
                if len(fitting_element_ids) != 0:
                    print(" all tag ids :",all_element_ids)
                    fitting_element_ids = self._get_child_ids(fitting_element_ids)
                    print(" checking ids:",fitting_element_ids)
                    fitting_element_ids = fitting_element_ids.intersection(all_element_ids)
                    print(" Matching:",fitting_element_ids)
                else:
                    fitting_element_ids = self.__tag_list[element]

                #if no fits , just stop
                if len(fitting_element_ids) == 0:
                    print("No results found!")
                    break

            else:
                print("No result found for querry",syntax)
                break

        print("Ids",fitting_element_ids)

        #element ids to full tags
        for fit_id in fitting_element_ids:
            fit_elements.append(self.__single_tag[fit_id])

        return fit_elements






if __name__ == "__main__":

    page = "https://idleon.miraheze.org/wiki/Smithing"
    sample_html = """<htm>
                        <body>
                            <h1 color='ffffff'>my text <b>is here   <a href='abc.com'/></b> ... ahhhh</h1>
                            <p>
                                Hello there this is a <b> text </b> !!!
                            </p>
                            
                            <h1>test other </>
                            <p>
                                <h1>something</h1>
                                Something different
                            </p>
                        </body>
                    </html>"""

    #print(get_page(page))
    main_parser = Collector()
    #main_parser.feed(get_page(page))
    main_parser.feed(sample_html)
    #print(main_parser.tree)

    links = SearchHelper.find_all_tags(main_parser.tree,"table")

    searcher = SearchHelper(main_parser.tree)
    searcher.flatten()

    search_strings =[
        "p",
        "body",
        "body/p",
        "body/h1",
        "body/p/h1",
        "body/h1&color=ffffff"
    ]

    for querry_string in search_strings:
        print("\nStart searching for:",querry_string)
        results = searcher.search_dyn(querry_string)
        print("Search results:")

        for result in results:
            print(result)

    #txt="table/caption=Anvil Table/"
    for link in links:
        print("")
        print(link)
