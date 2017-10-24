import re

def parse_sen(bb):
    place = []

    try: place.append(int(bb[0]))
    except:
        text = bb
        return place, text
        
    if place != []:
        for i in re.split(r'[.]', bb[1:]):
            try: place.append(int(bb[i]))
            except:
                if i == '.': continue
                else: break
    text = bb[i:]
    return place, text

class contract():
    
    def __init__(self, raw, len_st = 100):
        
        pars = list(map(lambda x: x.strip(), raw.split('\n')))
        pars_big = ['']
        for par in pars:
            if par != '':
                pars_big[-1] += '\n' + par
            else:
                pars_big.append(par)
        m = []
        for par in pars_big:
            #reg = re.compile('[^a-zA-Z0-9а-яА-Я№ ]')
            #ans = reg.sub('', par)
            if len(par) > len_st:
                m.append(par)
        raw = '\n'.join(m)
        
        
        bag = re.split(r'\n', raw)    
        mas = [[[], '']]
        for bb in bag:
            p = []
            t  = ''
            err = True
            for i in re.split(r'[.]', bb):
                if err:
                    try:
                        p.append(int(i))
                        err = True
                    except:
                        err = False
                        t += i
                else: t += i
            if p == []:
                mas[-1][1] += t
            else:
                mas.append([p, t])
        
        mas[0][0] = [0]
        self.mas = mas
        
    
    def get_child_name(self):
        
        name = []
        
        for p, t in self.mas:
            if len(p) == 1  and p[0] != 0:
                name.append(t)
        
        return name
    
    def get_child_numb(self, numb):
        
        child = []
        
        for p, t in self.mas:
            if p[0] == numb and len(p) == 2:
                child.append(t)
                
        return child

def build_tree(text):
    root = doc_tree('root')
    nek_class = contract(text)
    arr = nek_class.mas
    for i, m in enumerate(arr):
        if i == 0:
            continue
        reg = re.compile('[^a-zA-Z0-9а-яА-Я№_()""<>.?, ]')
        data = ' '.join(reg.sub('', m[1]).split())
        root.add_child(m[0], data)
    return root
            
class doc_tree():
    def __init__(self, data, par = None):
        self.parent = par
        self.data = data
        self.childs = []
    
    def add_child(self, path, data):
        n = int(path[0]) - 1
        if n < 0:
            return
        while n >= len(self.childs): 
                self.childs.append(doc_tree('EMPTY', self))
        if len(path) == 1:
            self.childs[n].data = data
        else:
            self.childs[n].add_child(path[1:], data)
        
    def get_data(self):   
        return self.data
    
    def get_childs_data(self):
        return [ch.get_data() for ch in self.childs]
    
    def to_child(self, i):
        if i < len(self.childs):
            return self.childs[i]
        return None
