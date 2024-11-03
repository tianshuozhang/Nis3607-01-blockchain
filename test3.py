import numpy as np
from tabulate import tabulate
from utils import selfish_simulate
import argparse
import configparser
import asyncio

async def main():
    # 创建配置解析器并读取配置文件
    config = configparser.ConfigParser()
    config.read('./config/malicious_config.ini')

    # 创建参数解析器
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_nodes', type=int,
                        help='节点数', default=config.getint('input_args', 'num_nodes'))
    
    parser.add_argument('--rounds', type=int,
                        help='轮数', default=config.getint('input_args', 'rounds'))
    
    parser.add_argument('--difficulty', type=int,
                        help='困难度: 表示哈希值前面几位是0', default=config.getint('input_args', 'difficulty'))
    parser.add_argument('--attempts', type=int,
                        help='尝试次数: 表示一轮挖矿中最多的计算次数', default=config.getint('input_args', 'attempts'))
    parser.add_argument('--malicious_ratio_min', type=float,
                        help='恶意比例下限', default=config.getfloat('input_args', 'malicious_ratio_min'))
    parser.add_argument('--malicious_ratio_max', type=float,
                        help='恶意比例上限', default=config.getfloat('input_args', 'malicious_ratio_max'))
    parser.add_argument('--malicious_ratio_perinterval', type=float,
                        help='恶意比例间隔', default=config.getfloat('input_args', 'malicious_ratio_perinterval'))

    # 解析参数
    args = parser.parse_args()

    difficulty = ''.join(['0']*args.difficulty + ['f'] *(64-args.difficulty))

    #simulate with the args in the field of malicious ratio
    results=[]
    for malicious_ratio in np.arange(args.malicious_ratio_min, args.malicious_ratio_max+args.malicious_ratio_perinterval, args.malicious_ratio_perinterval):
        print(f"\nSimulating with malicious ratio: {malicious_ratio:.2f}")
        
        blockchain_length, average_selfish_mined =await selfish_simulate(
            args.num_nodes, malicious_ratio, args.rounds,difficulty,args.attempts)
        
        results.append([malicious_ratio, blockchain_length, average_selfish_mined])
        

    # print the experiment result in the form of chart
    headers = ["Malicious Ratio", "Final Blockchain Length",
                "Average Selfish Mined Blocks"]
    print("\nResults:")
    print(tabulate(results, headers=headers, tablefmt="grid"))
if __name__ == "__main__":
    asyncio.run(main())
    
    
