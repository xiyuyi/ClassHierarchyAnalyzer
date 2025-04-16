import random
import networkx as nx

def get_mock_graph(num_nodes=1000) -> nx.DiGraph:
    G = nx.DiGraph()
    modules = ["core", "vision", "nlp", "audio"]

    node_count = 0
    node_queue = ["root"]
    G.add_node("root", module="root")

    while node_queue and node_count < num_nodes:
        parent = node_queue.pop(0)
        branching = random.choice([1,1,2,2,2,3,10,12])  # 从指定列表中随机选择分支因子
        for _ in range(branching):
            if node_count >= num_nodes:
                break
            mod = random.choice(modules)
            child = f"{mod}_Class{node_count}"
            G.add_node(child, module=mod)
            G.add_edge(parent, child)
            node_queue.append(child)
            node_count += 1

    return G


def get_mock_graph_class_inheritance(num_nodes=1000) -> nx.DiGraph:
    G = nx.DiGraph()
    modules = ["core", "vision", "nlp", "audio"]
    
    # 创建基础类
    base_classes = ["Object", "BaseModel", "BaseView", "BaseController"]
    for base in base_classes:
        G.add_node(base, module="core", is_abstract=True)
    
    node_count = 0
    node_queue = base_classes.copy()
    all_nodes = base_classes.copy()
    
    while node_count < num_nodes:
        # 随机选择一个或多个父类
        num_parents = random.choice([1,1,1,2,2,3])  # 允许多重继承
        available_parents = [n for n in all_nodes if not G.nodes[n].get('is_leaf', False)]
        
        if not available_parents:
            break
            
        parents = random.sample(available_parents, min(num_parents, len(available_parents)))
        
        # 创建新类
        mod = random.choice(modules)
        child = f"{mod}_Class{node_count}"
        
        # 随机决定是否是抽象类
        is_abstract = random.random() < 0.3  # 30%的概率是抽象类
        is_leaf = random.random() < 0.2  # 20%的概率是叶子节点
        
        G.add_node(child, module=mod, is_abstract=is_abstract, is_leaf=is_leaf)
        
        # 添加继承关系
        for parent in parents:
            G.add_edge(parent, child, relation="inheritance")
        
        # 随机添加组合关系
        if random.random() < 0.4:  # 40%的概率有组合关系
            num_compositions = random.choice([1,1,2,2,3])
            available_compositions = [n for n in all_nodes if n != child]
            compositions = random.sample(available_compositions, min(num_compositions, len(available_compositions)))
            for comp in compositions:
                G.add_edge(child, comp, relation="composition")
        
        all_nodes.append(child)
        if not is_leaf:
            node_queue.append(child)
        node_count += 1
        
        # 随机移除一些节点，避免队列过大
        if len(node_queue) > 100:
            node_queue = random.sample(node_queue, 50)
    
    return G

