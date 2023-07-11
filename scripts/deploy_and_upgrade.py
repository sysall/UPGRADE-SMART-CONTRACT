from scripts.helpful_scripts import get_account, encode_function_data, upgrade
from brownie import Box,network,ProxyAdmin, TransparentUpgradeableProxy, Contract, BoxV2
def main():
    account = get_account()
    print(f"Deploying to {network.show_active()}")
    # Implementation contract
    box = Box.deploy({"from": account})
    print(box.retrieve())
    # Hooking up a proxy to our implementation contract
    proxy_admin = ProxyAdmin.deploy({"from": account})
    # initializer = box.store, 1
    box_encoded_initializer_function = encode_function_data() #no initializer
    proxy = TransparentUpgradeableProxy.deploy(box.address,proxy_admin.address,box_encoded_initializer_function,{"from": account, "gas_limit":1000000})
    print(f"Proxy deployed to {proxy}, you can now upgrade to v2")
    # To call function through proxy address we have to assign ABI to a proxy
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    proxy_box.store(1, {"from": account})
    print(proxy_box.retrieve())
    box_v2 = BoxV2.deploy({"from": account})
    upgrade_transaction =  upgrade(account, proxy, box_v2.address, proxy_admin_contract=proxy_admin)
    print("Proxy has been upgrade!")
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    proxy_box.increment({"from": account})
    print(proxy_box.retrieve())

