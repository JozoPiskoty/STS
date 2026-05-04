import math

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

    def distance(self, name1, name2):
        depth1 = self.get_depth(name1)
        depth2 = self.get_depth(name2)
        lcs_node = self.find_lcs(name1, name2)

        if lcs_node is None:
            return None

        depth_lcs = self.get_depth(lcs_node.name)

        return depth1 + depth2 - 2 * depth_lcs

    def shortest_path(self, name1, name2):
        dist = self.distance(name1, name2)

        if dist is None:
            return 0

        return 1 / (1 + dist)

    def leacock_chodorow(self, name1, name2):
        dist = self.distance(name1, name2)

        if dist is None:
            return 0

        if dist == 0:
            return 1  

        D = self.max_depth()

        return -math.log(dist / (2 * D))
        


    
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

def compute_word_similarity(root, w1, w2, similarity_type):
    if similarity_type == "wupalmer":
        return root.wupalmer(w1, w2)
    elif similarity_type == "spath":
        return root.shortest_path(w1, w2)
    elif similarity_type == "lch":
        return root.leacock_chodorow(w1, w2)
    else:
        return 0

def one_to_many(lemmas1, lemmas2, root, similarity_type):
    result = []

    for w1 in lemmas1:
        word_result = []
        
        for w2 in lemmas2:
            score = compute_word_similarity(root, w1, w2, similarity_type)
            word_result.append(score)
            
        result.append(word_result)
        
    return result

def all_to_all(lemmas1, lemmas2, root, similarity_type):
    result = []
    
    for w1 in lemmas1:
        for w2 in lemmas2:
            score = compute_word_similarity(root, w1, w2, similarity_type)
            result.append(score)
                
    return result

def element_wise(lemmas1, lemmas2, root, similarity_type):
    result = []

    for i in range(min(len(lemmas1), len(lemmas2))):
        score = compute_word_similarity(root, lemmas1[i], lemmas2[i], similarity_type)
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

def exponentiate_score(score, power):
    try:
        power = int(power.replace("power", ""))
    except:
        power = 1
    return score ** power

import sympy
primes = list(sympy.primerange(0,500))
    
def index_weighted_average(scores, weight_type=None):
    if weight_type not in ["linear", "prime", "exponential"]:
        raise ValueError("weight type must be prime, linear or exponential")
    
    if not scores:
        return 0
    
    weighted_sum = 0
    weight_sum = 0

    if weight_type == "linear":
        for i,score in enumerate(scores):
            weighted_sum += (i+1) * score
            weight_sum += i+1

    elif weight_type == "prime":
        for i,score in enumerate(scores):
            weighted_sum += primes[i] * score
            weight_sum += primes[i]

    elif weight_type == "exponential":
        for i,score in enumerate(scores):
            weighted_sum += 2**(i+1) * score
            weight_sum += 2**(i+1)

    return weighted_sum / weight_sum
            
    
def compute_similarity(lemmas1, lemmas2, root,
                       matching, word_agg, sentence_agg,
                       direction,
                       similarity_type, 
                       power=1,
                       index_weight_type=None):

    def directional(l1, l2):
        if matching == "one_to_many":
            scores = one_to_many(l1, l2, root, similarity_type)

            scores = [[exponentiate_score(s, power) for s in sublist] for sublist in scores]

            word_scores = aggregate_lists(scores, word_agg)

            if index_weight_type:
                return index_weighted_average(word_scores, index_weight_type)
            else:
                return aggregate(word_scores, sentence_agg)

        elif matching == "all_to_all":
            scores = all_to_all(l1, l2, root, similarity_type)

            scores = [exponentiate_score(s, power) for s in scores]

            return aggregate(scores, sentence_agg)

        elif matching == "element_wise":
            scores = element_wise(l1, l2, root, similarity_type)

            scores = [exponentiate_score(s, power) for s in scores]

            if index_weight_type:
                return index_weighted_average(scores, index_weight_type)
            else:
                return aggregate(scores, sentence_agg)

        return 0

    if direction == "single":
        return directional(lemmas1, lemmas2)

    elif direction == "symmetric":
        s1 = directional(lemmas1, lemmas2)
        s2 = directional(lemmas2, lemmas1)
        return (s1 + s2) / 2

    return 0

    
    

def print_tree(node, level=0):
    print("  " * level + "- " + node.name)
    for child in node.children:
        print_tree(child, level + 1)

def choose_namespace(lemmas):
    return [(w, get_concept_data(w)["namespace"]) for w in lemmas]


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

    time.sleep(0.5)

    endpoint = "https://pojmy.kinit.sk/api/concept"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"lemma": lemma}

    
    response = requests.get(endpoint, params=params, headers=headers)
    data = response.json()

    results = data.get("results", {})

    if not isinstance(results, dict):
        results = {}

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

    namespace = None

    type_data = results.get("typeOf", [])
    if type_data:
        namespace = type_data[0].get("namespace")

    if not namespace:
        syn_data = results.get("synonymum", [])
        if syn_data:
            namespace = syn_data[0].get("namespace")

    if namespace:
        namespace = namespace.split("/")[0].strip()
    else:
        namespace = "Nezaradené"

    concept_cache[lemma] = {
        "synonyms": syn_list,
        "namespace": namespace,
        "has_record": has_record
    }



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




from itertools import product

matchings = ["one_to_many", "all_to_all", "element_wise"]
word_aggs = ["max", "avg", "min"]
sentence_aggs = ["max", "avg", "min"]
directions = ["single", "symmetric"]
powers = ["power1", "power2", "power7"]
index_weights = [None, "linear", "prime", "exponential"]
similarity_types = ["wupalmer", "spath", "lch"]

configs = []

for similarity_type, matching, direction, power, index_w in product(
        similarity_types, matchings, directions, powers, index_weights):

    if matching == "one_to_many":
        for word_agg, sentence_agg in product(word_aggs, sentence_aggs):
            configs.append((similarity_type, matching, word_agg, sentence_agg, direction, power, index_w))
    else:
        for sentence_agg in sentence_aggs:
            configs.append((similarity_type, matching, None, sentence_agg, direction, power, index_w))

results = {i: [] for i in range(len(configs))}
human_scores = []

subset = dataset

for i, (veta1, veta2, skore) in enumerate(dataset):
    print(f"Spracovávam: {i}/{len(dataset)}")

    lemmas1 = get_sentence_lemmas(veta1, token)
    lemmas2 = get_sentence_lemmas(veta2, token)

    root = build_tree_from_concepts(list(set(lemmas1 + lemmas2)), token)

    for j, config in enumerate(configs):
        similarity_type, matching, word_agg, sentence_agg, direction, power, index_w = config

        sim = compute_similarity(
            lemmas1,
            lemmas2,
            root,
            matching,
            word_agg,
            sentence_agg,
            direction,
            similarity_type=similarity_type,
            power=power,
            index_weight_type=index_w
        )

        results[j].append(sim)

    human_scores.append(skore)


with open("experiment_scoresF.json", "w", encoding="utf-8") as f:
    json.dump({
        "human": human_scores,
        "results": results,
        "configs": configs
    }, f, indent=2)


##subset = dataset[start_index:]   cisto cachovanie
##
##for i, (veta1, veta2, _) in enumerate(subset, start=start_index):
##    print(f"Cache: {i}/{len(dataset)}")
##
##    lemmas1 = get_sentence_lemmas(veta1, token)
##    lemmas2 = get_sentence_lemmas(veta2, token)
##
##    for lemma in set(lemmas1 + lemmas2):
##        get_concept_data(lemma)
##
##    if i % 50 == 0:
##        print("Ukladám cache...")
##        with open("concept_cache.json", "w", encoding="utf-8-sig") as f:
##            json.dump(concept_cache, f, ensure_ascii=False, indent=2)
##
##with open("concept_cache.json", "w", encoding="utf-8-sig") as f:
##    json.dump(concept_cache, f, ensure_ascii=False, indent=2)


