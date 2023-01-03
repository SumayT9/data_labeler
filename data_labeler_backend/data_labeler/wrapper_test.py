import json
from wrapper import WrapperInductor

if __name__ == "__main__":
    test_file = None
    with open("wrapper_test.json", "r") as f:
        test_file = json.load(f)
    tp = 0
    fn = 0
    fp = 0
    for school in ["UMD","Caltech","UCI", "Stanford", "Berkeley", "CMU", "Meta", "NVIDIA", "Purdue"]:#, "UCLA"]:
        train = test_file[school]["train"]
        urls = train["urls"]
        texts = train["texts"]
        labels = train["labels"]
        wi = WrapperInductor(urls, texts, labels)
        test = test_file[school]["test"]
        data = wi.extract_text(test["url"])
        wi.save("../../data_paths/")
        for field in data:
            if field not in test:
                print(field)
                fp += 1
        for field in test:
            if field == "url":
                continue
            found = False
            if field in data:
                tp_field = 0
                fp_field = 0
                fn_field = 0
                entireExpected = "".join(("".join(test[field])).split())
                for expected in test[field]:
                    itemFound = False
                    for item in data[field]:
                        if "".join(expected.split()) == "".join(item.split()) or "".join(item.split()) == entireExpected:
                            tp_field += 1
                            found = True
                            itemFound = True
                            break
                    if not itemFound: # if in expected but not in data
                        fn_field += 1
                for item in data[field]:
                    itemFound = False
                    for expected in test[field]:
                        if "".join(expected.split()) == "".join(item.split()) or "".join(item.split()) == entireExpected:
                            itemFound = True
                            break
                    if not itemFound: # if in data but not in expected
                        fp_field += 1
            tp += tp_field
            fp += fp_field
            fn += fn_field
            if field != "url":
                print(school, field, "found = ", found)
        

    print("false positives: ", fp, "true positives: ", tp, "misses: ", fn)
        
    print(tp/(tp+fp+fn))