# CarbonFootprint-CloudRearing
A Python-based carbon footprint calculation engine for the "Cloud Rearing" industry, featuring the calculation formula, code implementation, and data visualization for quantifying carbon neutrality participation.
# CarbonFootprint-CloudRearing
**云养行业碳中和碳足迹计算与积分系统**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 🌟 核心目标
本项目旨在建立**行业领先的碳积分系统**，通过科学计算云养殖各环节的碳排放与固碳量，让用户可**量化参与碳中和**。通过结合区块链技术，将虚拟养殖与真实低碳行动绑定，实现碳资产的可信溯源与交易。

## 🧮 碳积分计算公式
本系统基于IPCC标准与本地林草业参数构建碳资产计算模型：

$$I_{user} = [(A \times EF_{grass} + M \times EF_{manure}) - (E_{feed} + E_{enteric} + E_{energy})] \times W_{user} \times T_{hold}$$

### 参数说明
| 符号 | 英文名称 | 中文含义 | 数据来源/计算逻辑 | 单位 |
| :--- | :--- | :--- | :--- | :--- |
| $I_{user}$ | User Carbon Credit | 用户个人碳积分 | 最终计算得出的可兑换积分 | 吨CO₂e |
| $A$ | Grassland Area | 草场面积 | 牧场实际分配面积 | 公顷(ha) |
| $EF_{grass}$| Grass Emission Factor | 草场固碳因子 | 本地林业局/IPCC默认值 | 吨CO₂/ha |
| $M$ | Manure Management | 粪便管理量 | 实际处理量 | 吨 |
| $EF_{manure}$| Manure Emission Factor| 粪便减排因子 | 厌氧发酵/堆肥折算系数 | 吨CO₂/吨 |
| $E_{feed}$ | Feed Emission | 饲料碳排放 | 饲料生命周期排放 | 吨CO₂e |
| $E_{enteric}$| Enteric Fermentation | 肠道发酵排放 | 反刍动物肠道甲烷排放 | 吨CO₂e |
| $E_{energy}$| Energy Emission | 能耗碳排放 | 牧场日常用电/燃油消耗 | 吨CO₂e |
| $W_{user}$ | User Weight/Equity | 用户持有权益 | 智能合约记录的份额占比 | 百分比(%) |
| $T_{hold}$ | Holding Time | 持有时间 | 用户持有该资产的时长 | 年(Year) |

**应用场景：** 生成的碳积分 ($I_{user}$) 可用于平台商城兑换、公益捐赠、甚至通过智能合约上链进行碳资产交易。

## 🚀 快速开始

### 1. 依赖安装
```bash
pip install -r requirements.txt
