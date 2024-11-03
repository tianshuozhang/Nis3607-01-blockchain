## NIS3607 区块链生成及攻击

区块链技术及其共识机制（如 PoW）为构建信任、透明和安全的数字环境提供了基础。随着数字资产和去中心化应用的不断发展，区块链及其相关技术将在多个领域发挥越来越重要的作用。

### 运行环境

使用`Python`语言进行编程开发，最好使用`Python 3.8`及以上的版本。核心代码的实现完全依赖于系统自带库，为了便于展示和查看使用其他库来完成。

``
pip install -r requirements.txt
``

### 文件目录

```bash
│ -block.py
│ -blockchain.py
│ -node.py
│ -readme.md
│ -test1.py
│ -test2.py
│ -test3.py
│ -utils.py
└─config
        │ -malicious_config.ini
		│ -normal_config.ini

```

- `block.py`: 提供区块的数据结构，作为区块链中的块，提供计算哈希的方法，存储前一个区块哈希值。
- `blockchain.py`:区块链主要实现了添加区块，获取当前区块，以及检验区块链有效性等函数。
- `node.py`:节点用于模拟矿工，这里主要关注 `mine() `函数，用于模拟挖矿过程。
- `utils.py`:实现模拟过程的关键文件`normal_simulate()`、`fork_simulate()`、`selfish_simulate()`三个函数分别模拟正常的区块链生成、分叉攻击和自私挖矿，三个函数都是通过异步来实现。
- `test.py`:作为函数的入口，提供需要的参数和介绍，1、2、3三个分别对应三个任务。
- `config`：此文件夹下存储提供默认参数值的文件，其中生成区块链的参数在normal文件，实现分叉和自私挖矿攻击的参数在malicious文件。

### 运行方法

可以先查看需要的参数及其介绍，并进行参数的设置，默认取值在`config`文件夹下的`normal_config.ini`。

```
python test1.py --help
```

也可以修改`config`中的参数值，然后直接运行`test`文件。

