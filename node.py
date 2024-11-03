import hashlib
class Node:
    def __init__(self, node_id, is_malicious=False):
        self.node_id = node_id
        self.is_malicious = is_malicious
        self.blockchain = []
        self.last_block_index = -1
        
    
    async def mine(self, difficulty,total_attempts,index):
        
        nonce = 0  # 记录尝试次数

        while nonce < total_attempts:

              # 随机生成一个初始 nonce 值
            # 计算当前 nonce 的哈希值
            block_hash = hashlib.sha256(f"{index}{self.node_id}{nonce}".encode()).hexdigest()
            
            
            if block_hash < difficulty:  # 检查哈希值是否符合难度
                return True,nonce,self.node_id  # 返回成功
            
            nonce += 1  # 增加尝试次数

        return False,nonce,self.node_id  # 返回失败和

    def add_block(self, block):
        self.blockchain.append(block)
        self.last_block_index = block.index

    
       

        