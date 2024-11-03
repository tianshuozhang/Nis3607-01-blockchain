from node import Node
from block import Block
from blockchain import Blockchain
import matplotlib.pyplot as plt
import asyncio
import random
import copy
import time
async def fork_simulate(num_nodes, malicious_ratio, rounds, fork_length, difficulty,attempts):

    
    num_malicious = int(num_nodes * malicious_ratio)
    nodes = [Node(i, is_malicious=(i < num_malicious)) for i in range(num_nodes)]
    
    blockchain = Blockchain(difficulty)
    initial_block = Block(0, "0")
    blockchain.add_block(initial_block)

    selfish_chain = Blockchain(difficulty)
    selfish_chain.add_block(initial_block)
    malicious_length = 0
    normal_length = 0
    # 注册所有节点
    for node in nodes:
        blockchain.register_node(f'http://node{node.node_id}', node)  # 使用节点ID作为地址

    
    malicious_successful_forks = 0
    attempt_forks = 0
    for round_num in range(rounds):
        normal_tasks = []
        malicious_tasks = []
        for id in range(num_malicious):
            latest_block = selfish_chain.get_latest_block()
            task = asyncio.create_task(nodes[id].mine(difficulty,attempts,latest_block.index + 1))
            malicious_tasks.append(task)
        for id in range(num_malicious,num_nodes):
            if malicious_length > normal_length:
                    # 恶意链更长，正常节点跟随恶意链挖矿
                    latest_block = selfish_chain.get_latest_block()
                    task = asyncio.create_task(nodes[id].mine(difficulty,attempts,latest_block.index + 1))
                    malicious_tasks.append(task) 
            elif malicious_length<normal_length:# 正常链更长，正常节点跟随正常链挖矿
                latest_block = blockchain.get_latest_block()
                task = asyncio.create_task(nodes[id].mine(difficulty,attempts,latest_block.index + 1))
                normal_tasks.append(task)  
            else:  # 链长度相同
                # 根据概率选择
                if random.random() <0.3:
                    latest_block = selfish_chain.get_latest_block()
                    task = asyncio.create_task(nodes[id].mine(difficulty,attempts,latest_block.index + 1))
                    malicious_tasks.append(task) 
                else:
                    latest_block = blockchain.get_latest_block()
                    task = asyncio.create_task(nodes[id].mine(difficulty,attempts,latest_block.index + 1))
                    normal_tasks.append(task)     
            
                  
            
        # 等待任意一个任务完成
        if normal_tasks !=[]:
            successful_task = await asyncio.wait(normal_tasks, return_when=asyncio.FIRST_COMPLETED)
            for task in successful_task[0]:
                successful, nonce,id = task.result()
                if successful:
                    # 挖矿成功，创建新块并添加到区块链
                    latest_block = blockchain.get_latest_block()
                    new_block = Block(latest_block.index + 1,latest_block.calculate_hash(),nonce,id)
                    blockchain.add_block(new_block)
                    normal_length +=1
                    nodes[id].add_block(new_block)
                    break  # 找到一个成功的挖矿后退出循环

        successful_task = await asyncio.wait(malicious_tasks, return_when=asyncio.FIRST_COMPLETED) 
            
        for task in successful_task[0]:
            successful, nonce,id = task.result()
            if successful:
                latest_block = selfish_chain.get_latest_block()
                new_block = Block(latest_block.index + 1,latest_block.calculate_hash(),nonce,id)
                selfish_chain.add_block(new_block)
                malicious_length += 1
                
                nodes[id].add_block(new_block)
                break  # 找到一个成功的挖矿后退出循环      

        # tasks = []
        # for id in range(num_nodes):
        #     if id<num_malicious:
        #         latest_block = selfish_chain.get_latest_block()
        #         task = asyncio.create_task(nodes[id].mine(difficulty,attempts,latest_block.index + 1))
        #         tasks.append(task)
        #     else:
        #         if malicious_length > normal_length:
        #             # 恶意链更长，正常节点跟随恶意链挖矿
        #             latest_block = selfish_chain.get_latest_block()
        #         else:# 正常链更长，正常节点跟随正常链挖矿
        #             latest_block = blockchain.get_latest_block()       
        #         task = asyncio.create_task(nodes[id].mine(difficulty,attempts,latest_block.index + 1))
        #         tasks.append(task)
        # # 等待任意一个任务完成
        # successful_task = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        # for task in successful_task[0]:
        #     successful, nonce,id = task.result()
            
        #     if successful:
        #         # 挖矿成功，创建新块并添加到区块链
                
        #         if id >=num_malicious:
        #             if malicious_length > normal_length:
        #                 # 恶意链更长，正常节点跟随恶意链挖矿
        #                 latest_block = selfish_chain.get_latest_block()
        #                 new_block = Block(latest_block.index + 1,latest_block.calculate_hash(),nonce,id)
        #                 selfish_chain.add_block(new_block)
        #                 malicious_length += 1
        #             elif normal_length > malicious_length:
        #                 # 正常链更长，正常节点跟随正常链挖矿
        #                 latest_block = blockchain.get_latest_block()
        #                 new_block = Block(latest_block.index + 1,latest_block.calculate_hash(),nonce,id)
        #                 blockchain.add_block(new_block)
        #                 normal_length +=1
        #             else:  # 链长度相同
        #                 # 根据概率选择
        #                 if random.random() <0.5:
        #                     latest_block = selfish_chain.get_latest_block()
        #                     new_block = Block(latest_block.index + 1,latest_block.calculate_hash(),nonce,id)
        #                     selfish_chain.add_block(new_block)
        #                     malicious_length += 1
        #                 else:
        #                     latest_block = blockchain.get_latest_block()
        #                     new_block = Block(latest_block.index + 1,latest_block.calculate_hash(),nonce,id)
        #                     blockchain.add_block(new_block)
        #                     normal_length +=1
                            

        #         else:
        #             latest_block = selfish_chain.get_latest_block()
        #             new_block = Block(latest_block.index + 1,latest_block.calculate_hash(),nonce,id)
        #             selfish_chain.add_block(new_block)
        #             malicious_length += 1
                
        #         nodes[id].add_block(new_block)
        #         break  # 找到一个成功的挖矿后退出循环
        
        
        if malicious_length>=fork_length or normal_length>=fork_length:
            
            if malicious_length>=normal_length:
                malicious_successful_forks+=1 
                blockchain = copy.deepcopy(selfish_chain)
            
            else:
                selfish_chain = copy.deepcopy(blockchain)
            attempt_forks += 1
            malicious_length = 0
            normal_length = 0
           
                


    blockchain_length = len(blockchain.chain)
    
    average_selfish_mined = sum(1 for block in blockchain.chain if block.id<num_malicious)
    print(malicious_successful_forks,attempt_forks)
    return blockchain_length, malicious_successful_forks/attempt_forks, average_selfish_mined/blockchain_length




# def normal_simulate(num_nodes, rounds,difficulty):
#     nodes = [Node(i, is_malicious=0) for i in range(num_nodes)]
#     blockchain = Blockchain(difficulty)
#     initial_block = Block(0, "0")
#     blockchain.add_block(initial_block)

#     # 注册所有节点
#     for node in nodes:
#          blockchain.register_node(f'http://node{node.node_id}', node)  # 使用节点ID作为地址



#     growth_speeds = []  # 用于存储每轮的增长速度

#     for round_num in range(rounds):
#         for node in nodes:
#             latest_block = blockchain.get_latest_block()
#             successful,nonce = node.mine(difficulty,latest_block.index + 1)
#             # successful = node.mine(success_rate)
#             if successful:
                
#                 new_block = Block(latest_block.index + 1,latest_block.calculate_hash(),nonce)
#                 blockchain.add_block(new_block)
#                 node.add_block(new_block)
#         # 在每轮结束后执行共识算法
#         blockchain.resolve_conflicts()
#         # 计算并记录增长速度
#         blockchain_length = len(blockchain.chain)
#         growth_speed = blockchain_length / (round_num + 1)  # 每轮的平均增长速度
#         growth_speeds.append(growth_speed)


#     # 绘制增长速度图
#     plt.plot(range(1, rounds + 1), growth_speeds, marker='o')
#     plt.title('Blockchain Growth Speed Over Rounds')
#     plt.xlabel('Round Number')
#     plt.ylabel('Growth Speed (blocks/round)')
#     plt.grid()
#     plt.show()

#     blockchain_length = len(blockchain.chain)
#     growth_speed = blockchain_length / rounds  # 区块链的增长速度

#     return blockchain_length, growth_speed

async def normal_simulate(num_nodes, difficulty,attempts, rounds):
    nodes = [Node(i) for i in range(num_nodes)]
    blockchain = Blockchain(difficulty)
    initial_block = Block(0, "0")
    blockchain.add_block(initial_block)


    nums_per_round = []  # 用于存储每轮的增长速度
    time_per_round = []

    for round_num in range(rounds):
        # 记录开始时间
        start_time = time.time()
        # 创建一个任务列表
        
        tasks = []
        latest_block = blockchain.get_latest_block()

        for id in range(num_nodes):
            task = asyncio.create_task(nodes[id].mine(difficulty,attempts,latest_block.index + 1))
            tasks.append(task)

        # 等待任意一个任务完成
        successful_task = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        
        for task in successful_task[0]:
            successful, nonce,id = task.result()
            if successful:
                # 挖矿成功，创建新块并添加到区块链
                new_block = Block(latest_block.index + 1,latest_block.calculate_hash(),nonce,id)
                blockchain.add_block(new_block)
                nodes[id].add_block(new_block)
                break  # 找到一个成功的挖矿后退出循环
        
        # 记录结束时间并计算花费的时间
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # 等待所有任务完成
        results = await asyncio.gather(*tasks)
        successful_mines = 0
        for id, result in enumerate(results):
            successful, nonce,id = result  # 假设每个任务返回 (successful, nonce, id)
            
            if successful:
                successful_mines += 1  # 增加成功挖矿的计数
        
        # 在每轮结束后执行共识算法
        blockchain.resolve_conflicts()

        
        
        
        nums_per_round.append(successful_mines)
        time_per_round.append(elapsed_time)

    

    plt_exhibition(rounds,nums_per_round,time_per_round)
    blockchain_length = len(blockchain.chain)
    growth_speed =sum(time_per_round)/len(time_per_round)
    generate_ability = sum(nums_per_round)/len(nums_per_round)

    return blockchain_length, growth_speed,generate_ability


def plt_exhibition(rounds,nums_per_round,time_per_round):
    # 创建图形和坐标轴
    fig, ax1 = plt.subplots()


    # 绘制成功挖矿的数量
    ax1.plot(range(1, rounds + 1), nums_per_round, marker='o', color='b', label='Successful Mines')
    ax1.set_xlabel('Round Number')
    ax1.set_ylabel('Number of Successful Mines', color='b')
    ax1.tick_params(axis='y', labelcolor='b')
    ax1.grid()

    # 创建第二个 y 轴
    ax2 = ax1.twinx()
    ax2.plot(range(1, rounds + 1), time_per_round, marker='x', color='r', label='Time per Round')
    ax2.set_ylabel('Time per Round (seconds)', color='r')
    ax2.tick_params(axis='y', labelcolor='r')

    # 添加标题和图例
    plt.title('Blockchain Growth Speed and Time per Round')
    fig.tight_layout()  # 自动调整布局以防止重叠
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    # 显示图形
    plt.show()


async def selfish_simulate(num_nodes, malicious_ratio, rounds, difficulty,attempts):

    
    num_malicious = int(num_nodes * malicious_ratio)
    nodes = [Node(i, is_malicious=(i < num_malicious)) for i in range(num_nodes)]
    
    blockchain = Blockchain(difficulty)
    initial_block = Block(0, "0")
    blockchain.add_block(initial_block)

    selfish_chain = Blockchain(difficulty)
    selfish_chain.add_block(initial_block)
    
    # 注册所有节点
    for node in nodes:
        blockchain.register_node(f'http://node{node.node_id}', node)  # 使用节点ID作为地址

    
    
    for round_num in range(rounds):
        normal_tasks = []
        malicious_tasks = []
        for id in range(num_malicious):
        
            latest_block = selfish_chain.get_latest_block()
            task = asyncio.create_task(nodes[id].mine(difficulty,attempts,latest_block.index + 1))
            malicious_tasks.append(task)
        for id in range(num_malicious,num_nodes):
            latest_block = blockchain.get_latest_block()       
            task = asyncio.create_task(nodes[id].mine(difficulty,attempts,latest_block.index + 1))
            normal_tasks.append(task)
        # 等待任意一个任务完成
        successful_task = await asyncio.wait(normal_tasks, return_when=asyncio.FIRST_COMPLETED)
        for task in successful_task[0]:
            successful, nonce,id = task.result()
            if successful:
                # 挖矿成功，创建新块并添加到区块链
                latest_block = blockchain.get_latest_block()
                new_block = Block(latest_block.index + 1,latest_block.calculate_hash(),nonce,id)
                blockchain.add_block(new_block)
                
                nodes[id].add_block(new_block)
                break  # 找到一个成功的挖矿后退出循环

        successful_task = await asyncio.wait(malicious_tasks, return_when=asyncio.FIRST_COMPLETED) 
            
        for task in successful_task[0]:
            successful, nonce,id = task.result()
            if successful:
                latest_block = selfish_chain.get_latest_block()
                new_block = Block(latest_block.index + 1,latest_block.calculate_hash(),nonce,id)
                selfish_chain.add_block(new_block)
                
                
                nodes[id].add_block(new_block)
                break  # 找到一个成功的挖矿后退出循环
        
        
        if len(selfish_chain.chain)>len(blockchain.chain):
            blockchain = copy.deepcopy(selfish_chain)
        if len(selfish_chain.chain)+1<len(blockchain.chain):
            selfish_chain = copy.deepcopy(blockchain)
           
           
                


    blockchain_length = len(blockchain.chain)
    
    average_selfish_mined = sum(1 for block in blockchain.chain if block.id<num_malicious)
   
    return blockchain_length,  average_selfish_mined/blockchain_length