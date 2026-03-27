class Node:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = []

    def add_child(self, child_node):
        current = self
        while current is not None:    #ochrana proti cyklom
            if current is child_node:  
                return
            current = current.parent

        self.children.append(child_node)
        child_node.parent = self

    def find_node(self, name):  #vyhlada uzol podla nazvu pojmu
        if self.name == name:
            return self
        
        for child in self.children:
            result = child.find_node(name)
            
            if result is not None:
                return result
            
        return None

    def get_depth(self, name, current_depth=1):   #zisti hlbku uzla v strome
        if self.name == name:
            return current_depth
        
        for child in self.children:
            result = child.get_depth(name, current_depth + 1)
            
            if result is not None:
                return result
            
        return None

    def find_lcs(self, name1, name2):
        node1 = self.find_node(name1)
        node2 = self.find_node(name2)

        if node1 is None or node2 is None:
            return None

        ancestors1 = set()
        current_node = node1
        while current_node is not None:   #smerom hore prechadzame vsetkych predkov prveho pojmu
            ancestors1.add(current_node)
            current_node = current_node.parent
            
        current_node = node2
        while current_node is not None:   #prechadzame predkov druheho pojmu 
            if current_node in ancestors1:   #ak ma spolocneho predka tak ho vrati ako LCS
                return current_node 
            current_node = current_node.parent

        return None 

    def wupalmer(self, name1, name2):
        lcs_node = self.find_lcs(name1, name2)

        if lcs_node is None:
            return 0

        depth1 = self.get_depth(name1)
        depth2 = self.get_depth(name2)
        depth_lcs = self.get_depth(lcs_node.name)

        if depth1 == 0 or depth2 == 0: 
            return 0
        
        similarity = (2 * depth_lcs) / (depth1 + depth2)
        return similarity

    def count_nodes(self):
        count = 1
        for child in self.children:
            count += child.count_nodes()
        return count

    def max_depth(self, current_depth=1):
        if not self.children:
            return current_depth
        return max(child.max_depth(current_depth + 1) for child in self.children)

    def to_dict(self):
        return {
            "name": self.name,
            "children": [child.to_dict() for child in self.children]
        }


    
import requests, json, time
endpoint = "https://pojmy.kinit.sk/api/auth"
with open("udaje.txt", "r") as file:
    info = file.readline().split()
    email = info[0]
    password = info[1]
    file.close()
    
logindata = {"email": email, "password": password}    #ziskame api token
response = requests.post(endpoint, data=logindata)
data = response.json()
token = data.get("token")

def parse_concept_response(data, concepts_dict, lemma):    #spracuje udaje o pojme do stromu

    main_lemma = lemma   #rodic

    if main_lemma not in concepts_dict:
        concepts_dict[main_lemma] = Node(main_lemma)

    children = []
    for word in data["results"].get("synonymum", []):     #pripoji k nemu vsetky synonyma ako deti
        if word["lemma"] not in children:
            children.append(word["lemma"])
            
    for child in children:   #pripojime deti ako uzly k rodicovi
        if child not in concepts_dict:
            concepts_dict[child] = Node(child)
        concepts_dict[main_lemma].add_child(concepts_dict[child])

    return concepts_dict[main_lemma]


def extract_lemmas(sentence,token): 
    extractor_url = "https://pojmy.kinit.sk/api/extractor"
    extractor_headers = {"Authorization": f"Bearer {token}"}
    extractor_params = {"text": sentence}
    extractor_response = requests.get(extractor_url, params=extractor_params, headers=extractor_headers, timeout = 10)

    try:
        extractor_data = extractor_response.json()
    except:
        return []
    
    lemmas = []
    
    for word in extractor_data["results"]:
        lemma = word[0]["lemma"]

        if word[0]["concepts"] != []:
            lemmas.append(lemma)
        else:
            if lemma not in missing_lemmas:
                with open("missing_lemmas.csv", "a", encoding="utf-8-sig") as f:
                    f.write(f"{len(missing_lemmas)},{lemma}\n")

                missing_lemmas.add(lemma)

    return lemmas

try:
    
    with open("lemma_cache.json", "r", encoding = "utf-8-sig") as f:
        lemma_cache = json.load(f)
        
except FileNotFoundError:
    lemma_cache = {}

def get_sentence_lemmas(sentence, token):
    if sentence not in lemma_cache:
        lemma_cache[sentence] = extract_lemmas(sentence, token)

        with open("lemma_cache.json", "w", encoding="utf-8-sig") as f:
            json.dump(lemma_cache, f, ensure_ascii=False, indent=2)

    return lemma_cache[sentence]


def build_tree_from_concepts(lemmas, token):         #postavi strom a spoji ich do vztahov podla kategorii
    concept_url = "https://pojmy.kinit.sk/api/concept"
    headers = {"Authorization": f"Bearer {token}"}

    lemma_namespaces = dict(choose_namespace(lemmas))

    root = Node("root")
    concepts_dict = {"root": root}

    for lemma in lemmas:
        if lemma in concepts_dict:  
            continue

        data = {"results": {"synonymum": []}} 
        concept_info = get_concept_data(lemma)
        synonyms = concept_info["synonyms"]
        for syn in synonyms:
            data["results"]["synonymum"].append({"lemma": syn})

        node = parse_concept_response(data, concepts_dict, lemma)
        if not node:
            continue

        ns = lemma_namespaces.get(lemma, "Nezaradené")

        if ns not in concepts_dict:
            concepts_dict[ns] = Node(ns)
            root.add_child(concepts_dict[ns])

        if node not in concepts_dict[ns].children:
            concepts_dict[ns].add_child(node)

    return root

def sentence_similarity(lemmas1, lemmas2, root):   #pre kazde slovo z prvej vety sa najde najpodobnejsie slovo z druhej vety v strome a vypocita sa podobnost pomocou wupalmer
    scores = []
    
    for w1 in lemmas1:
        best = 0
        
        for w2 in lemmas2:
            score = root.wupalmer(w1, w2)
            if score > best:
                best = score
        scores.append(best)

    if not scores:
        return 0
    
    return sum(scores) / len(scores)

def symmetric_sentence_similarity(lemmas1, lemmas2, root):

    sim1 = sentence_similarity(lemmas1, lemmas2, root)
    sim2 = sentence_similarity(lemmas2, lemmas1, root)

    return (sim1 + sim2) / 2

def average_sentence_similarity(lemmas1, lemmas2, root):
    scores = []

    for w1 in lemmas1:
        for w2 in lemmas2:
            score = root.wupalmer(w1,w2)
            scores.append(score)
            
    if not scores:
        return 0

    return sum(scores) / len(scores)
    
def minimum_sentence_similarity(lemmas1, lemmas2, root):
    minimum = 1
    found = False

    for w1 in lemmas1:
        for w2 in lemmas2:
            score = root.wupalmer(w1, w2)
            found = True
            if score < minimum:
                minimum = score

    if not found:
        return 0

    return minimum

def weighted_sentence_similarity(lemmas1, lemmas2, root):
    weighted_sum = 0
    weight_sum = 0

    for i, w1 in enumerate(lemmas1):
        best = 0

        for w2 in lemmas2:
            score = root.wupalmer(w1, w2)
            if score > best:
                best = score

        weight = 5 ** i
        weighted_sum += weight * best
        weight_sum += weight

    if weight_sum == 0:
        return 0

    return weighted_sum / weight_sum

def one_to_many(lemmas1, lemmas2, root):
    result = []

    for w1 in lemmas1:
        word_result = []
        
        for w2 in lemmas2:
            score = root.wupalmer(w1,w2)
            word_result.append(score)
            
        result.append(word_result)
        
    return result

def all_to_all(lemmas1, lemmas2, root):
    result = []
    
    for w1 in lemmas1:
        for w2 in lemmas2:
            score = root.wupalmer(w1,w2)
            result.append(score)
                
    return result

def aggregate(scores, mode):
    if scores == []:
        return 0
    
    if mode == "max":
        return max(scores)
    elif mode == "min":
        return min(scores)
    elif mode == "avg":
        return sum(scores) / len(scores)

def aggregate_lists(scores, mode):
    result = []
    
    for score in scores:
        result.append(aggregate(score,mode))
        
    return result

def apply_score_weight(score, weight_type=None, power=2):
    if weight_type == "power":
        return score ** power
    return score

def apply_index_weight(word_scores, weight_type=None):
    if not word_scores:
        return 0

    weighted_sum = 0
    weight_sum = 0

    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

    for i, score in enumerate(word_scores):
        if weight_type == "linear":
            weight = i + 1
        elif weight_type == "prime":
            weight = primes[i % len(primes)]
        else:
            weight = 1

        weighted_sum += weight * score
        weight_sum += weight

    return weighted_sum / weight_sum if weight_sum != 0 else 0
    
def compute_similarity(lemmas1, lemmas2, root,
                       matching, word_agg, sentence_agg,
                       direction,
                       score_weight_type=None,
                       index_weight_type=None,
                       power=2):

    if direction == "single":

        if matching == "one_to_many":
            scores = []

            for i, w1 in enumerate(lemmas1):
                word_scores = []

                for w2 in lemmas2:
                    score = root.wupalmer(w1, w2)
                    score = apply_score_weight(score, score_weight_type, power)
                    word_scores.append(score)

                scores.append(word_scores)

            word_scores = aggregate_lists(scores, word_agg)

            if index_weight_type:
                return apply_index_weight(word_scores, index_weight_type)

            return aggregate(word_scores, sentence_agg)

        elif matching == "all_to_all":
            scores = []

            for w1 in lemmas1:
                for w2 in lemmas2:
                    score = root.wupalmer(w1, w2)
                    score = apply_score_weight(score, score_weight_type, power)
                    scores.append(score)

            return aggregate(scores, sentence_agg)

        return 0

    elif direction == "symmetric":

        if matching == "one_to_many":
            scores1 = []

            for i, w1 in enumerate(lemmas1):
                word_scores = []

                for w2 in lemmas2:
                    score = root.wupalmer(w1, w2)
                    score = apply_score_weight(score, score_weight_type, power)
                    word_scores.append(score)

                scores1.append(word_scores)

            word_scores1 = aggregate_lists(scores1, word_agg)

            if index_weight_type:
                s1 = apply_index_weight(word_scores1, index_weight_type)
            else:
                s1 = aggregate(word_scores1, sentence_agg)

            scores2 = []

            for i, w1 in enumerate(lemmas2):
                word_scores = []

                for w2 in lemmas1:
                    score = root.wupalmer(w1, w2)
                    score = apply_score_weight(score, score_weight_type, power)
                    word_scores.append(score)

                scores2.append(word_scores)

            word_scores2 = aggregate_lists(scores2, word_agg)

            if index_weight_type:
                s2 = apply_index_weight(word_scores2, index_weight_type)
            else:
                s2 = aggregate(word_scores2, sentence_agg)

            return (s1 + s2) / 2

        elif matching == "all_to_all":
            scores1 = []

            for w1 in lemmas1:
                for w2 in lemmas2:
                    score = root.wupalmer(w1, w2)
                    score = apply_score_weight(score, score_weight_type, power)
                    scores1.append(score)

            s1 = aggregate(scores1, sentence_agg)

            scores2 = []

            for w1 in lemmas2:
                for w2 in lemmas1:
                    score = root.wupalmer(w1, w2)
                    score = apply_score_weight(score, score_weight_type, power)
                    scores2.append(score)

            s2 = aggregate(scores2, sentence_agg)

            return (s1 + s2) / 2

        return 0

    return 0
    

def print_tree(node, level=0):
    print("  " * level + "- " + node.name)
    for child in node.children:
        print_tree(child, level + 1)

def choose_namespace(sentence):         #zisti do ktorej kategorie patria jednotlive slova z vety
    concept_url = "https://pojmy.kinit.sk/api/concept"
    headers = {"Authorization": f"Bearer {token}"}

    used_namespaces = []
    word_with_namespace = []

    for word in sentence:
        concept_info = get_concept_data(word)
        synonyms = concept_info["synonyms"]
        data = {"results": {"synonymum": [{"lemma": s, "namespace": "Nezaradené"} for s in synonyms]}}

        results = data.get("results", {})

        ns = None

        type_data = results.get("typeOf", [])   #najprv hladame namespace z typeof a potom zo synonymum a ked nie je ani tam ani tam tak to slovo dame ako nezaradene
        if type_data:
            ns = type_data[0].get("namespace")

        if not ns:
            syn_data = results.get("synonymum", [])
            if syn_data:
                ns = syn_data[0].get("namespace")

        if not ns:
            ns = "Nezaradené"

        if ns not in used_namespaces:
            used_namespaces.append(ns)
            word_with_namespace.append((word, ns))
        else:
            word_with_namespace.append((word, used_namespaces[-1]))

    return word_with_namespace


def load_dataset(dataset):        #nacitanie datasetu zo suboru
    data = []
    with open(dataset,"r",encoding = "utf-8-sig") as file:
        for line in file:
            line = line.strip().split("\t")
            data.append((line[1],line[2],float(line[0])))
    return data

try:
    
    with open("concept_cache.json", "r", encoding = "utf-8-sig") as f:
        concept_cache = json.load(f)
        
except FileNotFoundError:
    concept_cache = {}

def get_concept_data(lemma):   #nacita vsetky synonyma daneho slova a ak uz boli stiahnute predtym vrati ich z cache
    if lemma in concept_cache:
        return concept_cache[lemma]

    endpoint = "https://pojmy.kinit.sk/api/concept"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"lemma": lemma}

    time.sleep(0.5)
    response = requests.get(endpoint, params=params, headers=headers)
    data = response.json()

    results = data.get("results", {})

    syn_list = []

    if isinstance(results, dict):
        for word in results.get("synonymum", []):
            lemma_syn = word.get("lemma")
            if lemma_syn and lemma_syn not in syn_list:
                syn_list.append(lemma_syn)

    has_record = isinstance(results, dict) and len(results) > 0

    if not has_record and lemma not in missing_lemmas:
        with open("missing_lemmas.csv", "a", encoding="utf-8-sig") as f:
            f.write(f"{len(missing_lemmas)},{lemma}\n")

        missing_lemmas.add(lemma)

    concept_cache[lemma] = {
        "synonyms": syn_list,
        "has_record": has_record
    }

    with open("concept_cache.json", "w", encoding="utf-8-sig") as f:
        json.dump(concept_cache, f, ensure_ascii=False, indent=2)

    return concept_cache[lemma]
        

def get_terms_for_word(word):   #nacita vsetky slova z typeof a synonymum
    concept_url = "https://pojmy.kinit.sk/api/concept"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"lemma": word}
    response = requests.get(concept_url, params=params, headers=headers)
    data = response.json()

    results = data.get("results", {})

    if not isinstance(results, dict):
        results = {}

    words = []

    for relation in ["typeOf", "synonymum"]:
        for item in results.get(relation, []):
            lemma_str = item.get("lemma")
 
            if lemma_str and lemma_str != word and lemma_str not in words:
                words.append(lemma_str)
                
    return words

def merge_sets(word1,word2):
    set1 = set(get_terms_for_word(word1))
    set2 = set(get_terms_for_word(word2))

    set1.add(word1)
    set1.add(word2)
    set2.add(word2)
    set2.add(word1)

    return set1, set2



dataset = load_dataset("sick_sk.txt")

try:
    with open("scores.json", "r", encoding="utf-8-sig") as f:
        data = json.load(f)
        human_scores = data["human"]
        model_scores = data["model"]
        
except FileNotFoundError:
    human_scores = []
    model_scores = []

start_index = 0 #len(model_scores)


missing_lemmas = set()

try:
    with open("missing_lemmas.csv", "r", encoding="utf-8-sig") as f:
        next(f)  
        for line in f:
            idx, lemma = line.strip().split(",", 1)
            missing_lemmas.add(lemma)
except FileNotFoundError:
    with open("missing_lemmas.csv", "w", encoding="utf-8-sig") as f:
        f.write("idx,lemma\n")

try:
    with open("results.csv", "r", encoding="utf-8-sig"):
        pass
except FileNotFoundError:
    with open("results.csv", "w", encoding="utf-8-sig") as f:
        f.write("id,human_score,model_score,num_nodes,max_depth\n")


##for i, (veta1, veta2, skore) in enumerate(dataset[start_index:], start=start_index):
##
##    lemmas1 = get_sentence_lemmas(veta1, token)
##    lemmas2 = get_sentence_lemmas(veta2, token)
##
##    for lemma in set(lemmas1 + lemmas2):
##        get_concept_data(lemma)
##
##    all_lemmas = list(set(lemmas1 + lemmas2))
##    root = build_tree_from_concepts(all_lemmas, token)
##
##    tree_dict = root.to_dict()
##
##    tree_path = f"C:/Users/samue/OneDrive/Počítač/test/trees/tree_{i}.json"
##
##    try:
##        with open(tree_path, "r", encoding="utf-8-sig"):
##            pass
##    except FileNotFoundError:
##        with open(tree_path, "w", encoding="utf-8-sig") as f:
##            json.dump(tree_dict, f, ensure_ascii=False, indent=2)
##
##    similarity = sentence_similarity(lemmas1, lemmas2, root)
##
##    num_nodes = root.count_nodes()
##    max_depth = root.max_depth()
##
##    with open("results.csv", "a", encoding="utf-8-sig") as f:
##        f.write(f"{i},{skore},{similarity},{num_nodes},{max_depth}\n")
##
##    print(f"podobnost = {similarity:.4f}, ľudske = {skore}")
##    print("--------------------------------------------------")
##
##    model_scores.append(similarity)
##    human_scores.append(skore)
##
##    with open("scores.json", "w", encoding="utf-8-sig") as f:
##        json.dump({
##            "human": human_scores,
##            "model": model_scores
##        }, f, indent=2)




configs = [
    ("one_to_many", "max", "avg", "single", None, None),
    ("one_to_many", "max", "avg", "symmetric", None, None),
    ("one_to_many", "avg", "avg", "single", None, None),
    ("one_to_many", "avg", "avg", "symmetric", None, None),
    ("one_to_many", "min", "avg", "single", None, None),
    ("one_to_many", "min", "avg", "symmetric", None, None),
    ("one_to_many", "max", "avg", "single", "power", None),
    ("one_to_many", "max", "avg", "symmetric", "power", None),
    ("one_to_many", "avg", "avg", "symmetric", "power", None),
    ("one_to_many", "max", "avg", "single", None, "linear"),
    ("one_to_many", "max", "avg", "symmetric", None, "linear"),
    ("one_to_many", "max", "avg", "single", None, "prime"),
    ("one_to_many", "max", "avg", "symmetric", None, "prime"),
    ("one_to_many", "max", "avg", "symmetric", "power", "linear"),
    ("one_to_many", "max", "avg", "symmetric", "power", "prime"),
    ("all_to_all", None, "avg", "single", None, None),
    ("all_to_all", None, "avg", "symmetric", None, None),
    ("all_to_all", None, "avg", "single", "power", None),
    ("all_to_all", None, "avg", "symmetric", "power", None),
]

results = {i: [] for i in range(len(configs))}
human_scores = []

subset = dataset

for veta1, veta2, skore in subset:

    lemmas1 = get_sentence_lemmas(veta1, token)
    lemmas2 = get_sentence_lemmas(veta2, token)

    for lemma in set(lemmas1 + lemmas2):
        get_concept_data(lemma)

    root = build_tree_from_concepts(list(set(lemmas1 + lemmas2)), token)

    for i, config in enumerate(configs):
        matching, word_agg, sentence_agg, direction, score_w, index_w = config

        sim = compute_similarity(
            lemmas1,
            lemmas2,
            root,
            matching,
            word_agg,
            sentence_agg,
            direction,
            score_weight_type=score_w,
            index_weight_type=index_w,
            power=7
        )

        results[i].append(sim)

    human_scores.append(skore)

with open("experiment_scores1.json", "w", encoding="utf-8") as f:
    json.dump({
        "human": human_scores,
        "results": results,
        "configs": configs
    }, f, indent=2)


##0.5720 -> ['one_to_many', 'max', 'avg', 'symmetric', 'power', None]
##0.5714 -> ['one_to_many', 'max', 'avg', 'symmetric', 'power', 'linear']
##0.5696 -> ['one_to_many', 'max', 'avg', 'symmetric', 'power', 'prime']
##0.5373 -> ['one_to_many', 'max', 'avg', 'single', 'power', None]
##0.3971 -> ['one_to_many', 'avg', 'avg', 'symmetric', 'power', None]
##0.3971 -> ['all_to_all', None, 'avg', 'single', 'power', None]
##0.3971 -> ['all_to_all', None, 'avg', 'symmetric', 'power', None]
##0.3683 -> ['one_to_many', 'max', 'avg', 'symmetric', None, 'linear']
##0.3666 -> ['one_to_many', 'max', 'avg', 'symmetric', None, 'prime']
##0.3575 -> ['one_to_many', 'max', 'avg', 'symmetric', None, None]
##0.3479 -> ['one_to_many', 'max', 'avg', 'single', None, 'linear']
##0.3462 -> ['one_to_many', 'max', 'avg', 'single', None, 'prime']
##0.3411 -> ['one_to_many', 'max', 'avg', 'single', None, None]
##0.1367 -> ['all_to_all', None, 'avg', 'single', None, None]
##0.1367 -> ['all_to_all', None, 'avg', 'symmetric', None, None]
##0.1367 -> ['one_to_many', 'avg', 'avg', 'single', None, None]
##0.1367 -> ['one_to_many', 'avg', 'avg', 'symmetric', None, None]
##0.0037 -> ['one_to_many', 'min', 'avg', 'single', None, None]
##0.0027 -> ['one_to_many', 'min', 'avg', 'symmetric', None, None]
