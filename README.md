# Regex Web Extraction

## Overview

This module is responsible for extracting information from semi-structured web pages using induction learning on features from DOM trees.
## Setup


1. Development and testing was done using Python 3.9 and pip 22.3.1, make sure your versions align

2. From the root directory of the repository, run the command ```pip install -r requirements.txt``` to install the dependancies needed.


3. To use the chrome extension, navigate to chrome://extensions, turn on developer mode in the top right corner of the page, and then click the "load unpacked" button and select the root of the repository when prompted to set up the extension on your chrome instance.

4. Repository Structure
```
sumay-thakurdesai-regex-web-extraction/
    - requirements.txt
    - manifest.json
    - index.html
    - index.js
    - background.js
    - scripts/ 
        -- hover.css
        -- hover.js
        -- label_visualization.js
    - data_paths/ (houses data files that are dynamically created)
    - data_labeler_backend/
        -- data_labeler/
            --- stringmatch.py 
            --- views.py
            --- wrapper_test.json
            --- wrapper_test.py
        -- data_labeler_backend/
            --- urls.py
            --- asgi.py
            --- settings.py
            --- wsgi.py
        -- manage.py
    - crawler
        -- crawler.py
```

File descriptions: 
* `data_labeler_backend/data_labeler_backend/`: Django files
* `data_labeler_backend/data_labeler/stringmatch.py`: Contains code to generate regular expression matching sets of strings
* `data_labeler_backend/data_labeler/views.py`: contains code to handle information extraction using chrome extension using "wrapper" code
* `data_labeler_backend/data_labeler/wrapper_test.json`: Contains test cases for information extraction
* `data_labeler_backend/data_labeler/wrapper_test.py`: Code to run test cases for information extraction
* `data_labeler_backend/data_labeler/wrapper.py`: Code to generalize "wrapper" for a certain site
* `index.html`: Interface of the chrome extension
* `index.js`: Code enabling interfacing with extension through browser
* `background.js`: Background script connecting chrome extension with django backend
* `scripts/hover.js`: Script allowing user to view html elements before selecting for accurate data labeling
* `scripts/hover.css`: Stylesheet corresponding to hover.js
* `scripts/label_visualization.js`: Script allowing users to visualize the extraction results of the system
* `crawler/crawler.py`: Given the name of a professor allows users to find information about them as per pre-trained "wrappers"

5. Testing
To run the tests, navigate to `data_labeler_backend/data_labeler/` and run `python wrapper_test.py`

### Important 
Go to [our shared google Drive space](https://drive.google.com/drive/folders/1rxPAdGTVcl-Xo6uuFovdKcCw5_FEaXIC?usp=sharing) and create a folder with the format `FirstnameLastName-Projectname` (e.g. `AshutoshUkey-KeywordTrie`). In here, make sure to include a zipped copy of any data files related to your module (including `.sql` dumps of necessary databases) as well as a backup zipped copy of your Github repo (i.e. all the files you upload to Github).



## Functional Design (Usage)
* Takes as input the name of a professor and if a wrapper exists for the professor's instiution outputs the data extracted from the site
```python
    def crawl(person: str):
        ... 
        return data # dictionary in the form {"Field" : [list of all items matching that field on the site]}
        
```

* WrapperInductor external-facing methods
```python
    def __init__(self, urls : list=None, texts : list=None, labels : list=None, wrapper_file: str=None):
        """If wrapper file exists then load wrapper from existing file, otherwise use url, texts, labels to train wrapper"""
    
    def extract_text(self, url: str):
        """ 
        Takes as input a URL and outputs data extracted using the wrapper
        """            
        return out
    
    def load(self, filepath: str):
        """
        Loads pre-trained wrapper from filepath
        """

    def save(self, dir : str):
        """Saves wrapper in would be dir/sitename_wrapper.json"""
```

## Demo video
![]("https://user-images.githubusercontent.com/63134346/210290297-99f05a08-297c-45b9-b89b-2c68489e58e6.png")(https://youtu.be/mQZqBdbyiJk)

    
## Algorithmic Design 

First, we select a set of 2-4 labeled "seed" pages representing researchers from a certain site, which are used to train the extraction system. The program takes the xpaths and attributes of the labeled text in addition to the text preceding the labeled data by analyzing the DOM tree, and generates regular expressions that match the attributes, xpaths, and preceding text for each data field. These are stored in the form of a dictionary with the keys as the labels of the extractable fields from a page and the values being the regular expression that matches all instances of that label across all seed sites.

To extract information from an unseen page, the system loops through nodes in the DOM tree of that page and applies regex matching on attributes, xpaths, and preceding text of each node. If all three regular expressions match for a certain data field, then the text of that node is labeled with that data field and extracted. 

The algorithm for generating regular expressions for a set of strings is as follows:
First, all the strings in the set are inserted into the trie, which also keeps track of the number of times it is used. Then, the trie is traversed in post-order. During the traversal, if a node in the trie is identical to a node previously seen (it has the same letter and the same outgoing transitions), then the nodes are merged and count increased (because it is then used multiple times in traversing the string set), thus minimizing it. After minimization process is complete, then nodes that have a count equal to the number of strings are kept as literals in the regex, while sections in the trie that do not belong to all strings are replaced by ".*".


![design architecture](https://github.com/SumayT9/data_labeler/blob/main/F2022%20System%20Architecture.drawio.png)



## Issues and Future Work

* System is heavily dependent on the seed sites, if some attributes are present on many pages on the subject site but not in the seed sites, or there are multiple layouts for certain sections but only one of those layouts are represented in the seeds, then they will fail to be accurately recognized
* Regex generation does not work in cases where prefix and suffix are different across set of strings due to the reliance on FSMs
* System cannot handle tabular data
* More complicated sites, such as ucla's faculty information (i.e. https://samueli.ucla.edu/people/jason-jingsheng-cong/, where text is under a drop-down menu) are extracted incorrectly
* Future work must address these issues


## Change log

Use this section to list the _major_ changes made to the module if this is not the first iteration of the module. Include an entry for each semester and name of person working on the module. For example 

Fall 2022 (Sumay Thakurdesai)
* Week of 10/13/2022: Built base chrome extension allowing xpaths of selected text to be saved to a file along with a label
* Week of 11/03/2022: Fixed all issues with string matching, added hoverselect with click to chrome extension, added functionality to chrome extension enabling highlighting of selected text
* Week of 11/10/2022: Built base crawler script
* Week of 11/28/2022: Implemented functionality to generate regex based on set of strings and added it to induction system
* Week of 12/05/2022: Added alerts to show color/label matching and make them triggered by button click
* Week of 12/12/2022: Modified crawler to work with the new induction system



## References 
include links related to datasets and papers describing any of the methodologies models you used. E.g. 

* Regex Generation: https://aclanthology.org/J00-1002.pdf
