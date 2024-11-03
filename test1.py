import argparse
import configparser
from tabulate import tabulate
from utils import normal_simulate
import asyncio
async def main():
    # 创建配置解析器并读取:配置文件
    config = configparser.ConfigParser()
    config.read('./config/normal_config.ini')

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
    args = parser.parse_args()

    difficulty = ''.join(['0']*args.difficulty + ['f'] *(64-args.difficulty))
    
    # blockchain_length, growth_speed=normal_simulate(args.num_nodes,args.rounds,difficulty)

    blockchain_length,growth_speed,generate_ability = await normal_simulate(args.num_nodes, difficulty,args.attempts, args.rounds)

    results=[[args.rounds,blockchain_length,growth_speed,generate_ability]]
    headers = ["Rounds","Final Blockchain Length", "Growth Speed (times/round)", "Block generate ability"
            ]
    print(tabulate(results, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    
    asyncio.run(main())
