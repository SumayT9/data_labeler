class TrieNode:
    def __init__(self, char):
        self.children = {}
        self.char = char
        self.count = 0

class RegexGenerator:
    def __init__(self, strings):
        self.strings = strings
        self.start = TrieNode("")
        self.state_set = set()
        self.register = {}

    def build_trie(self):
        curr = self.start
        for string in self.strings:
            for s in string:
                if s not in curr.children:
                    curr.children[s] = TrieNode(s)
                curr = curr.children[s]
                curr.count += 1
            curr = self.start  

    def postorder_minimize(self, state):
        for trans in state.children.keys(): # for each transition
            state.children[trans] = self.postorder_minimize(state.children[trans])
        if (state.char, str(state.children)) in self.register: # if there is a node equaling child
            self.register[(state.char, str(state.children))].count += 1
            return self.register[(state.char, str(state.children))]
        else:
            self.register[(state.char, str(state.children))] = state
            return state
    
    def minimize_trie(self):
        self.build_trie()
        self.postorder_minimize(self.start)
            
    
    def generate_regex(self):
        if max(self.strings, key=len) == min(self.strings, key=len):
            return self.generate_regex_equal_len()
        self.minimize_trie()
        a = sorted(self.strings)[-1]
        out = ""
        curr = self.start
        for s in a:
            curr = curr.children[s]
            if curr.count >= len(self.strings):
                out += curr.char
            else:
                out += "."
        while out.count("..") > 0:
            out = out.replace("..", ".")
        out = out.replace(".", ".*")
        out = out.replace("+", "\+")
        return out
    
    def generate_regex_equal_len(self):
        out = ""
        for i in range(len(self.strings[0])):
            agree = True
            c = self.strings[0][i]
            for string in self.strings[1:]:
                if string[i] != c:
                    agree = False
                    break
            if agree:
                out += c
            else:
                out += "."
        
        while out.count("..") > 0:
            out = out.replace("..", ".")
        out = out.replace(".", ".*")
        out = out.replace("+", "\+")
        return out



if __name__ == "__main__":
    
    a = """<body class="html not-front not-logged-in no-sidebars page-node page-node- page-node-10845 node-type-person user-role-anonymous" style="">"""
    b = """<body class="html not-front not-logged-in no-sidebars page-node page-node- page-node-345421 node-type-person user-role-anonymous" style="">"""
    rg = RegexGenerator([a, b])
    rg.minimize_trie()
    rg.generate_regex()
