"""
Blockchain Integration Module
处理碳积分在区块链上的铸造与智能合约交互。
"""
from web3 import Web3
import os
import json
import logging

logger = logging.getLogger(__name__)

class BlockchainManager:
    def __init__(self):
        # 从环境变量读取 RPC 节点和私钥，绝对不要在代码中硬编码
        self.rpc_url = os.getenv("WEB3_RPC_URL", "https://polygon-rpc.com")
        self.private_key = os.getenv("WEB3_PRIVATE_KEY")
        self.contract_address = os.getenv("CONTRACT_ADDRESS")
        
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        self.account = self.w3.eth.account.from_key(self.private_key) if self.private_key else None
        
        # 假设有一个标准的 ERC20 风格的碳积分合约 ABI
        self.abi = json.loads('[{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"mintCarbonCredit","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
        
        if self.contract_address:
            self.contract = self.w3.eth.contract(address=self.contract_address, abi=self.abi)

    def mint_credit_on_chain(self, user_wallet: str, credit_amount: float) -> str:
        """
        将计算所得的碳积分铸造到用户的钱包地址。
        注意：实际商业应用中，需考虑精度转换（如乘以 10^18）和 Gas 费用的动态计算。
        """
        if not self.account or not self.contract_address:
            logger.warning("未配置区块链密钥或合约地址，跳过上链操作。")
            return "skipped_no_config"
            
        try:
            # 转换为智能合约的整型精度 (假设 18 位小数)
            amount_wei = int(credit_amount * (10 ** 18))
            
            # 构建交易
            tx = self.contract.functions.mintCarbonCredit(
                Web3.to_checksum_address(user_wallet), 
                amount_wei
            ).build_transaction({
                'from': self.account.address,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'gas': 2000000,
                'gasPrice': self.w3.eth.gas_price
            })
            
            # 签名并发送
            signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=self.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            
            logger.info(f"碳积分上链成功, 交易哈希: {tx_hash.hex()}")
            return tx_hash.hex()
            
        except Exception as e:
            logger.error(f"上链失败: {str(e)}")
            raise
