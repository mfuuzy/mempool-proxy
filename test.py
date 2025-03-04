# @Time    : 2025/3/4 11:33
# @FileName: test.py
# @Software: PyCharm
# @author  : mfuuzy
import requests
import json
from time import sleep



addresses_uri = [
    'address/bc1qkd9wmdaqutlfej7uzkr8z83wmhahmtpx2kffjt/txs', # GET Address Transactions
    'address/bc1qkd9wmdaqutlfej7uzkr8z83wmhahmtpx2kffjt/utxo' # GET Address UTXO
]

blocks_uri = [
    'block/000000000000000015dc777b3ff2611091336355d3f0ee9766a2cf3be8e4b1ce', # GET Block
    'block-height/615615',  # GET Block Height
    'block/000000000000000015dc777b3ff2611091336355d3f0ee9766a2cf3be8e4b1ce/header', # GET Block Header
    'block/000000000000000015dc777b3ff2611091336355d3f0ee9766a2cf3be8e4b1ce/txids', # GET Block Transaction IDs
    'blocks/tip/hash' # GET Block Tip Hash
]


fees_uri = [
    'fees/mempool-blocks',
    'fees/recommended'
]

transactions_uri = [
    'tx/15e10745f15593a899cef391191bdd3d7c12412cc4696b7bcb669d0feadc8521',
    'tx/15e10745f15593a899cef391191bdd3d7c12412cc4696b7bcb669d0feadc8521/hex'
]
transactions_uri_post = [
    '02000000000101e1bdeaa385f99d093518bd05faae4bbcdb4df1d77839e2af24282e74f66e8bbe0100000000fdffffff020000000000000000076a5d04140114008826010000000000160014f18ea5c3773616d8c7a71e884b762de05e8787d20247304402207ee08473776e10c6d86392432985bfc8a788685dc1d142d5469164f5bd905ac60220420fb302c9cef008ba23bb2bfe02e74ae85e60d7b9f25e593c4b567484e7319c012102f6b9e8f91c5121ad3ad19f5426279b7abd423bbeb9bbc94e146674b0c71ab05200000000'
]


# 获取数据
def diff_data(url1, url2,uri):
    try:
        response1 = requests.get(url1, timeout=10)
        response2 = requests.get(url2, timeout=10)

        # 确保返回 200 状态码
        if response1.status_code == 200 and response2.status_code == 200:

            try:
                data1 = response1.json()
                data2 = response2.json()
            except json.JSONDecodeError:
                data1 = response1.text.strip()
                data2 = response2.text.strip()

            if isinstance(data1, str) or isinstance(data1, int) and isinstance(data2, str) or isinstance(data2, int):
                if data1 == data2:
                    print(f"两个请求返回的字符串一致 ✅  : {uri}")
                else:
                    print(f"两个请求返回的字符串不一致 ❌  : {uri}")

            # 解决列表顺序不一致的问题：转换为集合进行比较
            elif isinstance(data1, list) or isinstance(data1, dict)  and isinstance(data2, list) or isinstance(data2, dict) :
                set1 = {json.dumps(item, sort_keys=True) for item in data1}
                set2 = {json.dumps(item, sort_keys=True) for item in data2}

                if set1 == set2:
                    print(f"两个请求返回的数据一致 ✅  : {uri} ")
                else:
                    print(f"两个请求返回的数据不一致 ❌  : {uri} ")

                    # 详细对比
                    # diff1 = set1 - set2  # data1 中有但 data2 没有的项
                    # diff2 = set2 - set1  # data2 中有但 data1 没有的项

                    # if diff1:
                    #     print("URL1 多出的数据:",
                    #           json.dumps([json.loads(item) for item in diff1], indent=2, ensure_ascii=False))
                    # if diff2:
                    #     print("URL2 多出的数据:",
                    #           json.dumps([json.loads(item) for item in diff2], indent=2, ensure_ascii=False))
            else:
                print(f"两个请求返回的数据类型不同 ❌ : {uri}")
                print("🔸 URL1 返回:", type(data1))
                print("🔹 URL2 返回:", type(data2))
        else:
            print(f"请求失败: mempool 状态码 {response1.status_code}, electrs 状态码 {response2.status_code}. electrs 没有 {uri} 请求方法")

    except requests.exceptions.RequestException as e:
        print("请求异常:", e)

def post_diff():
    data = '02000000000101e1bdeaa385f99d093518bd05faae4bbcdb4df1d77839e2af24282e74f66e8bbe0100000000fdffffff020000000000000000076a5d04140114008826010000000000160014f18ea5c3773616d8c7a71e884b762de05e8787d20247304402207ee08473776e10c6d86392432985bfc8a788685dc1d142d5469164f5bd905ac60220420fb302c9cef008ba23bb2bfe02e74ae85e60d7b9f25e593c4b567484e7319c012102f6b9e8f91c5121ad3ad19f5426279b7abd423bbeb9bbc94e146674b0c71ab05200000000'

    response1 = requests.post('https://mempool.space/api/tx', data=data)
    response2 = requests.post('http://127.0.0.1:8000/api/tx', data=data)

    # print(response1.text)
    # print(response2.text)
    print("response1",response1.text)
    print("response2",response2.text)
    if response1.text == response2.text:
        print(f"两个请求返回的数据一致 ✅ ")
    else:
        print(f"两个请求返回的数据不一致 ❌ ")


print("\n")
print("开始请求 Addresses 中的接口")
for x in addresses_uri:
    if x == "validate-address/tb1p932586q0vww8emf40t6q5aglzu33w4kpf2kml2jl682u2nukpfwq9eujld":
        mempool_url = f'{f"https://mempool.space/api/v1/{x}"}'
        electrs_url = f'{f"http://127.0.0.1:8000/api/v1/{x}"}'
    else:
        mempool_url = f'{f"https://mempool.space/api/{x}"}'
        electrs_url = f'{f"http://127.0.0.1:8000/api/{x}"}'

    diff_data(mempool_url,electrs_url,x)

sleep(2)
print("\n")
print("开始请求 Blocks 中的接口")
for x in blocks_uri:
    if x == "blocks-bulk/100000/100000" or x == "blocks/2091187" or x == "mining/blocks/timestamp/1672531200" or x == "block/000000000000009c08dc77c3f224d9f5bbe335a78b996ec1e0701e065537ca81":
        mempool_url = f'{f"https://mempool.space/api/v1/{x}"}'
        electrs_url = f'{f"http://127.0.0.1:8000/api/v1/{x}"}'
    else:
        mempool_url = f'{f"https://mempool.space/api/{x}"}'
        electrs_url = f'{f"http://127.0.0.1:8000/api/{x}"}'

    diff_data(mempool_url,electrs_url,x)


sleep(2)


print("\n")
print("开始请求 Fees 中的接口")
for x in fees_uri:
    mempool_url = f'{f"https://mempool.space/api/v1/{x}"}'
    electrs_url = f'{f"http://127.0.0.1:8000/api/v1/{x}"}'

    diff_data(mempool_url,electrs_url,x)

sleep(2)
print("\n")
print("开始请求 Transactions 中的接口")
for x in transactions_uri:
    if x == "transaction-times?txId[]=25e7a95ebf10ed192ee91741653d8d970ac88f8e0cd6fb14cc6c7145116d3964&txId[]=1e158327e52acae35de94962e60e53fc70f6b175b0cfc3e2058bed4b895203b4" or x == "cpfp/818da3d480697363fda33d6994636cd288da35284ad985bb33cce49dc786dfb5" or x == "tx/5faaa30530bee55de8cc896bdf48f803c2274a94bffc2842386bec2a8bf7a813/rbf":
        mempool_url = f'{f"https://mempool.space/api/v1/{x}"}'
        electrs_url = f'{f"http://127.0.0.1:8000/api/v1/{x}"}'
    else:
        mempool_url = f'{f"https://mempool.space/api/{x}"}'
        electrs_url = f'{f"http://127.0.0.1:8000/api/{x}"}'

    diff_data(mempool_url,electrs_url,x)

sleep(2)
print("\n")
print("开始请求 Transactions POST的接口")
post_diff()