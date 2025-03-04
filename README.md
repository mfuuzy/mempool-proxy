# 部署
## 构建镜像
```commandline
docker build -t mempool-proxy:v1 .
```
## 启动服务
```commandline
docker compose up -d
```


# 测试
## Addresses 接口

```commandline
两个请求返回的数据一致 ✅  : address/bc1qkd9wmdaqutlfej7uzkr8z83wmhahmtpx2kffjt/txs 
两个请求返回的数据一致 ✅  : address/bc1qkd9wmdaqutlfej7uzkr8z83wmhahmtpx2kffjt/utxo 
```

## Blocks 接口
```commandline
两个请求返回的数据一致 ✅  : block/000000000000000015dc777b3ff2611091336355d3f0ee9766a2cf3be8e4b1ce 
两个请求返回的字符串一致 ✅  : block-height/615615
两个请求返回的字符串一致 ✅  : block/000000000000000015dc777b3ff2611091336355d3f0ee9766a2cf3be8e4b1ce/header
两个请求返回的数据一致 ✅  : block/000000000000000015dc777b3ff2611091336355d3f0ee9766a2cf3be8e4b1ce/txids 
两个请求返回的字符串一致 ✅  : blocks/tip/hash
```

## Fees 接口
fees/mempool-blocks 接口有时会不一致，是因为 mempool 返回的数据是在变动的
```
两个请求返回的数据不一致 ❌  : fees/mempool-blocks 
两个请求返回的数据一致 ✅  : fees/recommended 
```

##  Transactions 接口
```
两个请求返回的数据一致 ✅  : tx/15e10745f15593a899cef391191bdd3d7c12412cc4696b7bcb669d0feadc8521 
两个请求返回的字符串一致 ✅  : tx/15e10745f15593a899cef391191bdd3d7c12412cc4696b7bcb669d0feadc8521/hex
```
##  Transactions post 接口
```
两个请求返回的数据一致 ✅  02000000000101e1bdeaa385f99d093518bd05faae4bbcdb4df1d77839e2af24282e74f66e8bbe0100000000fdffffff020000000000000000076a5d04140114008826010000000000160014f18ea5c3773616d8c7a71e884b762de05e8787d20247304402207ee08473776e10c6d86392432985bfc8a788685dc1d142d5469164f5bd905ac60220420fb302c9cef008ba23bb2bfe02e74ae85e60d7b9f25e593c4b567484e7319c012102f6b9e8f91c5121ad3ad19f5426279b7abd423bbeb9bbc94e146674b0c71ab05200000000
```