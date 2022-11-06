from operator import truediv
from lxml import html
import requests

url = 'https://profiles.stanford.edu/fei-fei-li'
print(url.split("/"))
page = requests.get(url)
tree = html.fromstring(page.text)
with open("webpageA.html", "w") as f:
    s = str(html.tostring(tree))
    f.write(s)

text_data = """Dr. Fei-Fei Li is the inaugural Sequoia Professor in the Computer Science Department at Stanford University, and Co-Director of Stanford’s Human-Centered AI Institute. She served as the Director of Stanford’s AI Lab from 2013 to 2018. And during her sabbatical from Stanford from January 2017 to September 2018, she was Vice President at Google and served as Chief Scientist of AI/ML at Google Cloud. Dr. Fei-Fei Li obtained her B.A. degree in physics from Princeton in 1999 with High Honors, and her PhD degree in electrical engineering from California Institute of Technology (Caltech) in 2005. She also holds a Doctorate Degree (Honorary) from Harvey Mudd College. Dr. Li joined Stanford in 2009 as an assistant professor. Prior to that, she was on faculty at Princeton University (2007-2009) and University of Illinois Urbana-Champaign (2005-2006).

Dr. Fei-Fei Li’s current research interests include cognitively inspired AI, machine learning, deep learning, computer vision and AI+healthcare especially ambient intelligent systems for healthcare delivery. In the past she has also worked on cognitive and computational neuroscience. Dr. Li has published more than 200 scientific articles in top-tier journals and conferences, including Nature, PNAS, Journal of Neuroscience, CVPR, ICCV, NIPS, ECCV, ICRA, IROS, RSS, IJCV, IEEE-PAMI, New England Journal of Medicine, Nature Digital Medicine, etc. Dr. Li is the inventor of ImageNet and the ImageNet Challenge, a critical large-scale dataset and benchmarking effort that has contributed to the latest developments in deep learning and AI. In addition to her technical contributions, she is a national leading voice for advocating diversity in STEM and AI. She is co-founder and chairperson of the national non-profit AI4ALL aimed at increasing inclusion and diversity in AI education.

Dr. Li is an elected Member of the National Academy of Engineering (NAE), the National Academy of Medicine (NAM) and American Academy of Arts and Sciences (AAAS). She is also a Fellow of ACM, a member of the Council on Foreign Relations (CFR), a recipient of the 2022 IEEE PAMI Thomas Huang Memorial Prize, 2019 IEEE PAMI Longuet-Higgins Prize, 2019 National Geographic Society Further Award, 2017 Athena Award for Academic Leadership, IAPR 2016 J.K. Aggarwal Prize, the 2016 IEEE PAMI Mark Everingham Award, the 2016 nVidia Pioneer in AI Award, 2014 IBM Faculty Fellow Award, 2011 Alfred Sloan Faculty Award, 2012 Yahoo Labs FREP award, 2009 NSF CAREER award, the 2006 Microsoft Research New Faculty Fellowship, among others. Dr. Li is a keynote speaker at many academic or influential conferences, including the World Economics Forum (Davos), the Grace Hopper Conference 2017 and the TED2015 main conference. Work from Dr. Li's lab have been featured in a variety of magazines and newspapers including New York Times, Wall Street Journal, Fortune Magazine, Science, Wired Magazine, MIT Technology Review, Financial Times, and more. She was selected as a 2017 Women in Tech by the ELLE Magazine, a 2017 Awesome Women Award by Good Housekeeping, a Global Thinker of 2015 by Foreign Policy, and one of the “Great Immigrants: The Pride of America” in 2016 by the Carnegie Foundation, past winners include Albert Einstein, Yoyo Ma, Sergey Brin, et al.

(Dr. Li publishes under the name L. Fei-Fei)"""

found = False
t = None
base = text_data.strip().replace("\n", "").replace(" ", "")
for tag in tree.iter():
    try:
        if tag.text and (tag.tag not in ["script", "noscript", "comment"]):
            test = tag.text_content().strip().replace("\n", "").replace(" ", "")
            if base == test:
                xpath = tag.getroottree().getpath(tag)
                print(xpath)
                found = True
        if found:
            break
    except:
        continue
    
    # if tag.tag == "p" and "inaugural" in tag.text_content():
    #     found = True
        
    #     with open("base.txt", "w") as base_file:
    #         base_file.write(base)
    #     test = tag.text_content().strip().replace("\n", "").replace(" ", "")
    #     with open("test.txt", "w") as base_file:
    #         base_file.write(test)
    #     xpath = tag.getroottree().getpath(tag)
    #     print(xpath)
    #     if base == test:
    #         print("made it")
    #         break
    #     for i in range(len(base)):
    #         if base[:i] != test[:i]:
    #             print(base[:i])
    #             print(test[:i])
    #             print(i)
    #             # print(i, text_data[:i])
    #             # print("-----")
    #             # print(tag.text_content()[i:])
    #             # print("..............")
    #             # print(text_data[i:])
    #             break
    #         else:
    #             print("good")

            # if tag.text and (tag.tag not in ["script", "noscript", "comment"]) and tag.text_content().strip().startsWith(text_data[:i].strip()):
            #     print(i, tag.tag)
            #     xpath = tag.getroottree().getpath(tag)
            #     print(xpath)
            #     found = True
            #     t = tag

# print(t.tag)
# print(t.text_content())

# url = 'https://profiles.stanford.edu/joel-neal'
# page = requests.get(url)
# tree = html.fromstring(page.text)
# with open("../data_paths/path_file.txt", "r") as xpaths:
#     for x in xpaths.readlines():
#         label, data = x.split("|")
#         if x:
#             relevant = tree.xpath(data)
#             for item in relevant:
#                 print(label, item.text_content())
