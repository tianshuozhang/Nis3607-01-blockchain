class Blockchain:
    def __init__(self,difficulty):
        self.chain = []
        self.nodes = {}  # 存储所有节点，键为节点地址，值为节点对象
        self.difficulty = difficulty

    def add_block(self, block):
        self.chain.append(block)

    def get_latest_block(self):
        return self.chain[-1] if self.chain else None

    def register_node(self, node_address, node):
        """ 注册新节点到区块链网络 """
        self.nodes[node_address] = node  # 存储节点对象

    def resolve_conflicts(self):
        """ 共识算法：检查网络中的所有节点，获取最长链 """
        neighbours = self.nodes.keys()
        new_chain = None
        max_length = len(self.chain)
        success_forks = 0
        for neighbour in neighbours:
            node = self.nodes.get(neighbour)
            length, chain = len(node.blockchain), node.blockchain
            
            if length > max_length and self.is_chain_valid(chain):
            # if length > max_length :
                max_length = length
                new_chain = chain
                success_forks+=1
                node.selfish_blockchain=[]
                

        if new_chain:
            self.chain = new_chain

        for neighbour in neighbours:
            node = self.nodes.get(neighbour)
            node.blockchain=self.chain.copy()
        return success_forks
    

    def is_chain_valid(self, chain=None):
        if chain is None:
            chain = self.chain
        for i in range(1, len(chain)):
            previous = chain[i - 1]
            current = chain[i]
            if current.previous_hash != previous.calculate_hash() or current.calculate_hash()>self.difficulty:
                print(False)
                return False
        return True
