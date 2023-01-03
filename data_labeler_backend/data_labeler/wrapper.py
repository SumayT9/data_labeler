from lxml import html
import requests
import re
try:
    from data_labeler.stringmatch import RegexGenerator
except ModuleNotFoundError:
    from stringmatch import RegexGenerator
import json

class WrapperInductor:
    def __init__(self, urls : list=None, texts : list=None, labels : list=None, wrapper_file: str=None):
        """If wrapper file exists then load wrapper from existing file, otherwise use url, texts, labels to train wrapper"""
        if wrapper_file:
            self.load(wrapper_file)
        else:
            self.attrib_paths = {}
            self.xpaths = {}
            self.sibling_text = {}
            for url_chunk in labels:
                for label in url_chunk:
                    if label not in self.attrib_paths:
                        self.attrib_paths[label] = []
                        self.xpaths[label] = []
                        self.sibling_text[label] = []
            
            for i in range(len(urls)):
                url = urls[i]
                chunk_texts = texts[i]
                chunk_labels = labels[i]
                self.get_info_from_page(url, chunk_texts, chunk_labels)
                self.sitename = url.split("/")[2]
            self.generate_attrib_regex()
            self.generate_xpath_regex()
            self.decide_siblings()

    
    def get_info_from_page(self, url: str, texts : list, labels : list):
        """
        Given a url and relevant texts and their labels, extracts the sibling text, 
        attributes, and labels from the page specified by url and stores them by label 
        in class attributes
        inputs: url - url of page to analyze
                texts - texts labeled from that page
                labels - labels for that page
        """
        texts = ["".join(t.split()) for t in texts]
        labels = { text:label for (text,label) in zip(texts, labels)} 
        page = requests.get(url)
        seed_tree = html.fromstring(page.text)
        done = {text: False for text in texts}
        for tag in seed_tree.iter():
                try:
                    tag_xp = tag.getroottree().getpath(tag).replace("[1]", "")
                    if tag.text_content() and tag.tag not in ["script", "noscript", "comment"]:
                        tag_text = "".join(tag.text_content().split())
                        if tag_text in texts and not done[tag_text]:
                            attribs = []
                            curr = tag
                            while curr is not None:
                                attribs.append(curr.attrib)
                                curr = curr.getparent()
                            done[tag_text] = True
                            self.attrib_paths[labels[tag_text]].append(attribs)
                            if tag.tag == "li" or tag.tag == "dd":
                                tag = tag.getparent()
                            tag_xp = tag.getroottree().getpath(tag).replace("[1]", "")
                            self.xpaths[labels[tag_text]].append(tag_xp)
                            new_tag = tag.getprevious()
                            while new_tag is not None:
                                if new_tag.text_content() != None and len(new_tag.text_content().strip()) <= 15:
                                    self.sibling_text[labels[tag_text]].append(new_tag.text_content())
                                    break
                                new_tag = new_tag.getprevious()
                except:
                    continue

    def generate_attrib_regex(self):
        """
        Generates regex for the attribute paths extracted from seed sites 
        """
        for label in self.attrib_paths:   
            matching_regex = []
            if not self.attrib_paths[label]:
                continue
            for i in range(len(self.attrib_paths[label][0])): # for each mini-dict in the attrib path
                regex_node = {}
                level_nodes = [self.attrib_paths[label][0][i]]
                level_keys = list(self.attrib_paths[label][0][i].keys())
                for j in range(len(self.attrib_paths[label])):
                    try:
                        node = self.attrib_paths[label][j][i]
                        if list(node.keys()) == level_keys:
                            level_nodes.append(node)
                    except:
                        pass
                
                for key in level_keys:
                    vals = [node[key] for node in level_nodes]
                    regex_node[key] = RegexGenerator(vals).generate_regex()
                matching_regex.append(regex_node)
            self.attrib_paths[label] = matching_regex

    def generate_xpath_regex(self):
        """
        Generates regex for the xpaths extracted from seed sites
        """
        for label in self.xpaths:
            try:
                self.xpaths[label] = RegexGenerator(self.xpaths[label]).generate_regex()
            except:
                continue
    
    def decide_siblings(self):
        """
        Generates regex for the sibling texts from seed sites
        """
        for label in self.sibling_text:
            try:
                self.sibling_text[label] = RegexGenerator(self.sibling_text[label]).generate_regex()
            except:
                continue


    
    def extract_text(self, url: str):
        """ 
        Takes as input a URL and outputs data extracted using the wrapper
        """  
        page = requests.get(url)
        tree = html.fromstring(page.text)
        labels = list(self.attrib_paths.keys())
        out = {label : [] for label in labels}
        for tag in tree.iter():
            attribs = []
            curr = tag
            while curr is not None:
                attribs.append(curr.attrib)
                curr = curr.getparent()
            xpath = tag.getroottree().getpath(tag).replace("[1]", "")
            for label in labels:
                if self.xpaths[label]:
                    if not self.match_xpaths(self.xpaths[label],xpath):
                        continue
                if self.attrib_paths[label]:
                     if not self.match_attribs(self.attrib_paths[label],attribs):
                        continue
                if self.sibling_text[label]:
                    if not self.match_siblings(self.sibling_text[label], tag):
                        continue
                if self.xpaths[label] or self.attrib_paths[label] or self.sibling_text[label]:
                    out[label].append(tag.text_content().strip())
                    
        return out

    def match_xpaths(self, reference : str, sample : str):
        """
        Determines if the regex of two xpaths match
        inputs: reference - regex determined by generalizing from seed sites
                sample - xpath to match against regex
        output: boolean stating if the regexes match
        
        """
        return bool(re.match(reference, sample))

    def match_attribs(self, reference, sample):
        """
        Determines if the regex of two attribute paths match
        inputs: reference - regex determined by generalizing from seed sites
                sample - attribute path to match against regex
        output: boolean stating if the regexes match
        
        """
        if sample[0] == {}:
            sample = sample[1:]
        if reference[0] == {}:
            reference = reference[1:]
        for i in range(len(reference)):
            node = reference[i]
            for key in node.keys():
                if key not in sample[i].keys():
                    return False
                if not re.match(node[key], sample[i][key]):
                    return False
        return True
    
    def match_siblings(self, reference, tag):
        """
        Determines if the regex of the sibling texts match
        inputs: reference - regex determined by generalizing from seed sites
                tag - lxml tag element to find sibling of
        output: boolean stating if the regexes match
        """
        if not self.sibling_text:
            return True
        if tag.tag == "li" or tag.tag == "dd":
            tag = tag.getparent()
        new_tag = tag.getprevious()
        while new_tag is not None:
            if new_tag.text_content() != None:
                return new_tag.text_content() == reference
            new_tag = new_tag.getprevious()
        return False
    
    def load(self, filepath: str):
        """
        Loads pre-trained wrapper from filepath
        """
        json_obj = None
        with open(filepath, "r") as json_file:
            json_obj = json.load(json_file)
        self.attrib_paths = json_obj["attrib_paths"]
        self.xpaths = json_obj["xpaths"]
        self.sibling_text = json_obj["sibling_text"]
        self.sitename = json_obj["sitename"]

    
    def save(self, dir : str):
        """Saves wrapper in would be dir/sitename_wrapper.json"""
        data_dict = {
            "attrib_paths" : self.attrib_paths,
            "xpaths" : self.xpaths,
            "sibling_text" : self.sibling_text,
            "sitename" : self.sitename
        }
        with open(dir + self.sitename + "_wrapper.json", "w") as wrapper_file:
            json.dump(data_dict, wrapper_file)

        




