# CarbonFootprint-CloudRearing 🌿
**云养行业碳中和碳足迹计算与积分系统**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https  ://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25+-FF4B4B.svg?style=flat&logo=streamlit)](https://streamlit.io/)

**CarbonFootprint-CloudRearing** 是一个专为“云养殖”行业设计的全链条碳足迹计算与碳积分管理方案。该项目旨在通过科学的建模与量化工具，将牧场端的固碳减排数据转化为用户端可感知的碳积分资产，实现“行业领先”的碳中和商业化落地。

> **💡 核心理念**：让每一次云养宠，都成为对抗气候变化的实际行动。

---

## 🎯 核心目标

- **精准量化** 🧮：基于 IPCC 标准算法，实时计算用户的碳减排贡献。
- **资产确权** 💎：将碳积分通过区块链技术固化为数字资产，支持交易与流转。
- **可视决策** 📊：提供直观的可视化仪表盘，辅助牧场优化经营策略。

---

## 🧮 碳积分计算模型

本系统采用国际通用的 **IPCC (政府间气候变化专门委员会)** 标准，并融合本地林草业修正系数，确保计算结果的权威性与准确性。

### 核心计算公式

$$I_{user} = [(A \times EF_{grass} + M \times EF_{manure}) - (E_{feed} + E_{enteric} + E_{energy})] \times W_{user} \times T_{hold}$$

### 参数详表 (Parameter Reference)

| 符号 | 参数名称 (EN/CN) | 含义说明 | 数据来源 | 单位 |
| :--- | :--- | :--- | :--- | :--- |
| $I_{user}$ | **User Credit** / 用户积分 | 用户最终获得的碳积分 | 系统核心逻辑计算得出 | 吨CO₂e |
| $A$ | **Grassland Area** / 草场面积 | 牧场实际分配给该单位的面积 | 牧场地理信息系统(GIS) | 公顷(ha) |
| $EF_{grass}$ | **Grass EF** / 草场固碳因子 | 单位面积草场年固碳量 | IPCC或本地林业部门数据 | 吨CO₂/ha |
| $M$ | **Manure Mgmt** / 粪便管理量 | 实际进行无害化/资源化处理量 | 牧场物联网传感器数据 | 吨 |
| $EF_{manure}$ | **Manure EF** / 粪便减排因子 | 厌氧发酵/堆肥工艺的减排系数 | 《省级温室气体清单指南》 | 吨CO₂/吨 |
| $E_{feed}$ | **Feed Emission** / 饲料碳排放 | 饲料生产及运输生命周期排放 | 供应链LCA审计数据 | 吨CO₂e |
| $E_{enteric}$ | **Enteric Ferm** / 肠道发酵排放 | 反刍动物肠道甲烷排放折算 | 畜牧业温室气体排放标准 | 吨CO₂e |
| $E_{energy}$ | **Energy Emission** / 能耗碳排放 | 牧场运营电、油、煤等消耗 | 电力账单/能耗监控系统 | 吨CO₂e |
| $W_{user}$ | **User Weight** / 用户权益 | 用户认养份额在总群落中的占比 | 智能合约/业务系统权益表 | % (0~1) |
| $T_{hold}$ | **Holding Time** / 持有时间 | 用户认养资产的实际天数/年数 | 订单系统记录 | 年(Year) |

---

## 🛠 技术架构

- **核心引擎**: Python 3.8+，基于模块化设计实现复杂的碳核算逻辑。
- **持久层**: SQLAlchemy ORM，支持 SQLite (开发) / PostgreSQL (生产)。
- **API服务**: **FastAPI**，提供高性能异步 RESTful 接口。
- **可视化**: **Streamlit** 构建交互式 Web 仪表盘，支持 Plotly 动态图表。
- **区块链**: Web3.py 集成，支持 Polygon/Matic 等低能耗公链进行资产存证。

---

## 🚀 快速开始

### 1. 环境准备
确保已安装 Python 3.8 及以上版本。

```bash
# 1. 克隆仓库
git clone https://github.com/your-username/CarbonFootprint-CloudRearing.git
cd CarbonFootprint-CloudRearing

# 2. 创建并激活虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env 文件，填入你的 Web3 配置
uvicorn code.api:app --reload
streamlit run visualization/app.py
CarbonFootprint-CloudRearing/
├── README.md               # 项目说明文档
├── requirements.txt        # Python 依赖列表
├── .env                    # 环境变量文件
├── code/                   # 核心业务逻辑
│   ├── carbon_calculator.py # 核心算法模块 (含IPCC模型)
│   ├── api.py              # FastAPI 接口定义
│   ├── models.py           # 数据库模型
│   └── utils/              # 工具类 (含Web3区块链交互)
├── visualization/          # 数据可视化层
│   └── app.py              # Streamlit 交互式仪表盘
├── tests/                  # 单元测试
│   └── test_calculator.py
└── docs/                   # 补充文档
cd deployment
docker-compose up -d --build

### 💡 给您的操作建议：

1.  **文件保存**：请新建一个文本文件，将上述内容完整复制进去，保存为 `README.md`（注意后缀名必须是 `.md`）。
2.  **环境变量**：请务必创建一个 `.env` 文件（或者先创建 `.env.example`），内容如下，以便代码读取区块链配置：
    ```env
    DATABASE_URL=sqlite:///./carbon_rearing.db
    WEB3_RPC_URL=https://polygon-rpc.com
    WEB3_PRIVATE_KEY=your_test_private_key_here # 仅用于测试，请勿在生产环境硬编码
    CONTRACT_ADDRESS=0xYourSmartContractAddress
    ```
3.  **美化展示**：建议运行 `streamlit run visualization/app.py`，截取一张包含图表的界面截图，命名为 `demo.png`，然后在 README 的 `## 💼 商业化扩展能力` 上方插入一行 `![Demo](demo.png)`，这样 GitHub 仓库会立刻变得非常直观专业。
