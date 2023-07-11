from brownie import network, config, accounts
import eth_utils

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_LOCAL_ENVIRONNEMENTS = ["mainnet-fork","mainnet-fork-dev"]

def get_account(index=None, id=None):
    # accounts[0]
    # accounts.add("env")
    # accounts.load("id")
    if id:
        return accounts.load(id)
    
    if index:
        return accounts[index]

    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIRONNEMENTS:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])
    
# Encodes the function call so we can work with an initializer : initializer = box.store 1
def encode_function_data(initializer=None, *args):
    if len(args) == 0 or not initializer:
        return eth_utils.to_bytes(hexstr="0x")
    if not len(args): args = b''
    if initializer: return initializer.encode_input(*args)
    return b''

def upgrade(
        account,
        proxy,
        new_implementation_address,
        proxy_admin_contract=None,
        initializer=None,
        *args
):
    transaction = None
    if proxy_admin_contract:
        if initializer:
            encoded_function_call = encode_function_data(initializer, *args)
            transaction = proxy_admin_contract.upgradeAndCall(
                proxy.address,
                new_implementation_address,
                encoded_function_call,
                {"from": account}
            )
        else:
            transaction = proxy_admin_contract.upgrade(
                proxy.address, new_implementation_address, {"from": account}
            )
    else:
        if initializer:
            encoded_function_call = encode_function_data(initializer, *args)
            transaction = proxy.upgradeToAndCall(
                new_implementation_address, encoded_function_call, {"from": account}
            )
        else:
            transaction = proxy.upgradeTo(new_implementation_address, {"from": account})
    return transaction 