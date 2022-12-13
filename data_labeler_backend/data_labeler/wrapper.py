from lxml import html
import requests
import re
from data_labeler.stringmatch import RegexGenerator
import json

class WrapperInductor:
    def __init__(self, urls=None, texts=None, labels=None, wrapper_file=None):
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
            # print(self.sibling_text)
            
            self.generate_attrib_regex()
            self.generate_xpath_regex()
            self.decide_siblings()
    
    def get_info_from_page(self, url, texts, labels):
        texts = ["".join(t.split()) for t in texts]
        labels = { text:label for (text,label) in zip(texts, labels)} 
        page = requests.get(url)
        seed_tree = html.fromstring(page.text)
        done = {text: False for text in texts}
        for tag in seed_tree.iter():
                try:
                    attribs = []
                    curr = tag
                    while curr is not None:
                        attribs.append(curr.attrib)
                        curr = curr.getparent()
                    tag_xp = tag.getroottree().getpath(tag).replace("[1]", "")
                    if tag.text_content() and tag.tag not in ["script", "noscript", "comment"]:
                        tag_text = "".join(tag.text_content().split())
                        if tag_text in texts and not done[tag_text]:
                            done[tag_text] = True
                            self.attrib_paths[labels[tag_text]].append(attribs)
                            if tag.tag == "li":
                                tag = tag.getparent()
                            tag_xp = tag.getroottree().getpath(tag).replace("[1]", "")
                            self.xpaths[labels[tag_text]].append(tag_xp)
                            new_tag = tag.getprevious()
                            while new_tag is not None:
                                if new_tag.text != None:
                                    self.sibling_text[labels[tag_text]].append(new_tag.text)
                                    break
                                new_tag = new_tag.getprevious()
                except:
                    continue

    def generate_attrib_regex(self):
        for label in self.attrib_paths:
            matching_regex = []
            for i in range(len(self.attrib_paths[label][0])): # for each mini-dict in the attrib path
                regex_node = {}
                level_nodes = [self.attrib_paths[label][0][i]]
                level_keys = list(self.attrib_paths[label][0][i].keys())
                for j in range(len(self.attrib_paths[label])):
                    node = self.attrib_paths[label][j][i]
                    if list(node.keys()) == level_keys:
                        level_nodes.append(node)
                
                for key in level_keys:
                    vals = [node[key] for node in level_nodes]
                    regex_node[key] = RegexGenerator(vals).generate_regex()
                matching_regex.append(regex_node)
            self.attrib_paths[label] = matching_regex

    def generate_xpath_regex(self):
        """
        Inputs:
        path_dict
            label : list of paths for that label
        """
        for label in self.xpaths:
            self.xpaths[label] = RegexGenerator(self.xpaths[label]).generate_regex()
    
    def decide_siblings(self):
         for label in self.sibling_text:
            self.sibling_text[label] = RegexGenerator(self.sibling_text[label]).generate_regex()


    
    def extract_text(self, url):
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
                if self.match_xpaths(self.xpaths[label],xpath) and self.match_attribs(self.attrib_paths[label], attribs) and self.match_siblings(self.sibling_text[label], tag):
                    out[label].append(tag.text_content().strip())
        return out

    def match_xpaths(self, reference, sample):
        return bool(re.match(reference.replace("[", "\[").replace("/", "\/"), sample))

    def match_attribs(self, reference, sample):
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
        if tag.tag == "li":
            tag = tag.getparent()
        new_tag = tag.getprevious()
        while new_tag is not None:
            if new_tag.text != None:
                return new_tag.text == reference
            new_tag = new_tag.getprevious()
    
    def load(self, filepath):
        json_obj = None
        with open(filepath, "r") as json_file:
            json_obj = json.load(json_file)
        self.attrib_paths = json_obj["attrib_paths"]
        self.xpaths = json_obj["xpaths"]
        self.sibling_text = json_obj["sibling_text"]

    
    def save(self, filepath):
        data_dict = {
            "attrib_paths" : self.attrib_paths,
            "xpaths" : self.xpaths,
            "sibling_text" : self.sibling_text
        }
        with open(filepath, "w") as wrapper_file:
            json.dump(data_dict, wrapper_file)

        





if __name__ == "__main__":
    test_file = None
    with open("wrapper_test.json", "r") as f:
        test_file = json.load(f)
    
    for school in ["Berkeley", "CMU"]:
        train = test_file[school]["train"]
        urls = train["urls"]
        texts = train["texts"]
        labels = train["labels"]
        wi = WrapperInductor(urls, texts, labels)
        print(wi.attrib_paths)
        test = test_file[school]["test"]
        data = wi.extract_text(test["url"]) 
        for field in data:
            found = False
            for item in data[field]:
                if "".join(item.split()) in "".join(test[field].split()):
                    found = True
                    break
            print(school, field, "found = ", found)
#     texts = [
#         [
#         """Dr. Fei-Fei Li is the inaugural Sequoia Professor in the Computer Science Department at Stanford University, and Co-Director of Stanford’s Human-Centered AI Institute. She served as the Director of Stanford’s AI Lab from 2013 to 2018. And during her sabbatical from Stanford from January 2017 to September 2018, she was Vice President at Google and served as Chief Scientist of AI/ML at Google Cloud. Dr. Fei-Fei Li obtained her B.A. degree in physics from Princeton in 1999 with High Honors, and her PhD degree in electrical engineering from California Institute of Technology (Caltech) in 2005. She also holds a Doctorate Degree (Honorary) from Harvey Mudd College. Dr. Li joined Stanford in 2009 as an assistant professor. Prior to that, she was on faculty at Princeton University (2007-2009) and University of Illinois Urbana-Champaign (2005-2006).

# Dr. Fei-Fei Li’s current research interests include cognitively inspired AI, machine learning, deep learning, computer vision and AI+healthcare especially ambient intelligent systems for healthcare delivery. In the past she has also worked on cognitive and computational neuroscience. Dr. Li has published more than 200 scientific articles in top-tier journals and conferences, including Nature, PNAS, Journal of Neuroscience, CVPR, ICCV, NIPS, ECCV, ICRA, IROS, RSS, IJCV, IEEE-PAMI, New England Journal of Medicine, Nature Digital Medicine, etc. Dr. Li is the inventor of ImageNet and the ImageNet Challenge, a critical large-scale dataset and benchmarking effort that has contributed to the latest developments in deep learning and AI. In addition to her technical contributions, she is a national leading voice for advocating diversity in STEM and AI. She is co-founder and chairperson of the national non-profit AI4ALL aimed at increasing inclusion and diversity in AI education.

# Dr. Li is an elected Member of the National Academy of Engineering (NAE), the National Academy of Medicine (NAM) and American Academy of Arts and Sciences (AAAS). She is also a Fellow of ACM, a member of the Council on Foreign Relations (CFR), a recipient of the 2022 IEEE PAMI Thomas Huang Memorial Prize, 2019 IEEE PAMI Longuet-Higgins Prize, 2019 National Geographic Society Further Award, 2017 Athena Award for Academic Leadership, IAPR 2016 J.K. Aggarwal Prize, the 2016 IEEE PAMI Mark Everingham Award, the 2016 nVidia Pioneer in AI Award, 2014 IBM Faculty Fellow Award, 2011 Alfred Sloan Faculty Award, 2012 Yahoo Labs FREP award, 2009 NSF CAREER award, the 2006 Microsoft Research New Faculty Fellowship, among others. Dr. Li is a keynote speaker at many academic or influential conferences, including the World Economics Forum (Davos), the Grace Hopper Conference 2017 and the TED2015 main conference. Work from Dr. Li's lab have been featured in a variety of magazines and newspapers including New York Times, Wall Street Journal, Fortune Magazine, Science, Wired Magazine, MIT Technology Review, Financial Times, and more. She was selected as a 2017 Women in Tech by the ELLE Magazine, a 2017 Awesome Women Award by Good Housekeeping, a Global Thinker of 2015 by Foreign Policy, and one of the “Great Immigrants: The Pride of America” in 2016 by the Carnegie Foundation, past winners include Albert Einstein, Yoyo Ma, Sergey Brin, et al.

# (Dr. Li publishes under the name L. Fei-Fei)""", "Thomas S. Huang Memorial Prize, IEEE PAMI (2022)", "Professor (By courtesy), Operations, Information & Technology", "B.A., Princeton University, Physics (1999)"],[
# """Dr. Neal holds a medical degree and a doctoral degree in Tumor Cell Biology from Northwestern University in Chicago, Illinois. Subsequently, he completed a fellowship in oncology, 
# rotating through the Dana-Farber Cancer Institute and Massachusetts General Hospital in Boston, Massachusetts. He is currently an Associate Professor in the 
# Division of Oncology at the Stanford Cancer Institute at Stanford University in Palo Alto, California. Dr Neal’s primary clinical interest is in thoracic oncology.
#  In addition to maintaining an active practice, he focuses on the design and conduct of clinical trials involving targeted therapies and immunotherapy for lung cancer and 
#  mesothelioma. He has published dozens of articles in the field of thoracic oncology, including in Lancet Oncology, Nature Medicine, and the Journal of Clinical Oncology. 
#  He is a member of the International Association of the Study of Lung Cancer (IALSC), is a study chair and thoracic core committee member within the ECOG-ACRIN cooperative group, 
#  and has presented at a number of American Society of Clinical Oncology (ASCO) annual meetings.""", "Associate Professor - University Medical Line, Medicine - Oncology", "Residency: Beth Israel Deaconess Medical Center Internal Medicine Residency (2007) MA"]
# ]
#     labels = [["Biography", "Awards", "Appointments", "Education"], ["Biography", "Appointments", "Education"]]


#     urls = ['https://profiles.stanford.edu/fei-fei-li', "https://profiles.stanford.edu/joel-neal"]
#    
    # attrib_paths, xpaths = generate_wrapper(urls, texts, labels)

    # texts = [["Cybersecurity, Distributed Systems", """Dr. Mustaque Ahamad is a professor in the School of Computer Science. 
    # He has served on the faculty at the Georgia Institute of Technology since 1985.  
    # Dr. Ahamad was director of the Georgia Tech Information Security Center (GTISC) from 2004 to 2012. As director of GTISC, 
    # he helped develop several major research thrusts in areas that include security of converged communication networks, identity and access management, 
    # and security of healthcare information technology.  Currently, he leads Georgia Tech’s educational programs in cyber security as associate director of 
    # its Institute for Information Security and Privacy. His research interests span distributed systems, computer security and dependable systems. 
    # Dr. Ahamad co-founded Pindrop Security and FraudScope and serves as chief scientist of these companies. He received his Ph.D. in computer science from the 
    # State University of New York at Stony Brook in 1985. He received his undergraduate degree in electrical and electronics engineering from the Birla Institute of Technology and Science, Pilani, India."""], 
    # ["Machine Learning", "I like to think about the mathematics behind Machine Learning and Game Theory, and I especially like discovering connections to Optimization, Statistics, and Economics."], 
    # ["Database systems, machine learning", """Joy Arulraj is an assistant professor in the School of Computer Science at Georgia Institute of Technology. His research interest is in database management systems, specifically large-scale data analytics, 
    # main memory systems,  machine learning, and big code analytics. At Georgia Tech, he is a member of the Database group."""]]
    # urls = ["https://www.scs.gatech.edu/people/mustaque-ahamad", "https://www.scs.gatech.edu/people/jacob-abernethy", "https://www.scs.gatech.edu/people/joy-arulraj"]
    # labels = [["Research Interests", "Biography"], ["Research Interests", "Biography"], ["Research Interests", "Biography"]]
    # wi = WrapperInductor(urls, texts, labels)
    # wi.extract_text("https://www.scs.gatech.edu/people/alexandra-boldyreva")
    # extract_text("https://www.scs.gatech.edu/people/alexandra-boldyreva", attrib_paths, xpaths)
    # <awards : nobel prize, pulitzer, university : UIUC, job: Professor of CS>
    # div/div/p
    #//*[@id="bioContent"]/div/p
    #//*[@id="node-10850"]/div/div[1]/div/div[2]/div[2]/div[2]/div/p[1]
    # {class : Personcontent}, {class bioContnent}, { class: text}

    #  //*[@id="bioContent"]/p
    #  /html/body/div/main/div/div/section[2]/div/div[2]/div/div[1]/div/div/div[1]/div[1]/div/p


    # urls = ["https://eas.caltech.edu/people/yaser","https://eas.caltech.edu/people/jess"]
    # texts = [
    #     ["machine learning, artificial intelligence, neural networks, computational finance, probability and statistics", """The Learning Systems Group at Caltech studies the theory and applications of Machine Learning (ML). 
    # The theory of ML uses mathematical and statistical tools to estimate the information (data and hints) needed to learn a given task. The 
    # applications are very diverse and continue to expand to every corner of science and technology. The group works on medical applications of ML, 
    # on e-commerce and profiling applications, and on computational finance, among other domains. These applications use the latest techniques of 
    # neural networks and other models, and often give rise to novel ML theory and algorithms. Our latest projects are data-driven approach to predicting
    #  the spread of COVID-19 in every U.S. county, and ML approach to medical diagnostics using low-resolution ultrasound."""],
    #  ["""geochemical investigations of past climates using corals, sediments and their interstitial waters, rate of deep ocean
    #   circulation and its relation to mechanisms of rapid climate changes, metals as tracers of environmental processes, radiocarbon 
    #   and U-series chronology, chemical oceanography""", """Professor Adkins focuses on geochemical investigations of past climates using corals, sediments and their interstitial waters; Rate of deep ocean circulation and its relation to mechanisms of rapid climate changes; 
    #   Metals as tracers of environmental processes; Radiocarbon and U-series chronology. Chemical oceanography."""]
    #   ]
    # labels = [["research interests", "Biography"],["research interests", "Biography"]]
    # wi = WrapperInductor(urls, texts, labels)
    # # attrib_paths, xpaths = generate_wrapper(urls, texts, labels)
    # wi.extract_text("https://eas.caltech.edu/people/adames")
    # # sample = "".join("""The Learning Systems Group at Caltech studies the theory and applications of Machine Learning (ML). 
    # The theory of ML uses mathematical and statistical tools to estimate the information (data and hints) needed to learn a given task. The 
    # applications are very diverse and continue to expand to every corner of science and technology. The group works on medical applications of ML, 
    # on e-commerce and profiling applications, and on computational finance, among other domains. These applications use the latest techniques of 
    # neural networks and other models, and often give rise to novel ML theory and algorithms. Our latest projects are data-driven approach to predicting
    # the spread of COVID-19 in every U.S. county, and ML approach to medical diagnostics using low-resolution ultrasound.""".split())
    # url = "https://profiles.stanford.edu/fei-fei-li"
    # sample = "".join("Thomas S. Huang Memorial Prize, IEEE PAMI (2022)".split())
    # page = requests.get(url)
    # seed_tree = html.fromstring(page.text)
    # for tag in seed_tree.iter():
    #         try:
    #             attribs = []
    #             curr = tag
    #             while curr is not None:
    #                 attribs.append(curr.attrib)
    #                 curr = curr.getparent()
    #             tag_xp = tag.getroottree().getpath(tag).replace("[1]", "")
    #             if tag.text_content() and tag.tag not in ["script", "noscript", "comment"]:
    #                 tag_text = "".join(tag.text_content().split())
    #                 if tag_text == sample:
                        
    #                     new_tag = tag.getprevious()
    #                     print(tag)
    #                     while new_tag is not None:
    #                         print("here")
    #                         if new_tag.text != None:
    #                             print(new_tag.text)
    #                             print(new_tag)
    #                             break
    #                         new_tag = new_tag.getprevious()

    #         except:      
    #             continue


