from brownie import accounts, network, config

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev", "polygon-mainnet-fork"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

def get_account(index=None, id=None): 
    if index:
        return accounts[index]
    elif id:
        return accounts.load(id)
    elif (network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS):
        return accounts[0]
    
    return accounts.add(config["wallets"]["from_key"])
