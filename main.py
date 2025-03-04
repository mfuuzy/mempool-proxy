# @Time    : 2025/3/4 09:57
# @FileName: main.py
# @Software: PyCharm
# @author  : mfuuzy

from fastapi import FastAPI, HTTPException,Request
import httpx
from fastapi.responses import JSONResponse,PlainTextResponse


app = FastAPI()
API_BASE_URL = "https://mempool.space"


@app.get("/api/v1/fees/recommended")
async def getFeesRecommended():
    url = f"{API_BASE_URL}/api/v1/fees/recommended"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            # 返回原始响应内容
            return JSONResponse(
                content=response.json() if response.text else None,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
        except httpx.RequestError as e:
            return JSONResponse(
                content={"error": f"Request failed: {str(e)}"},
                status_code=500
            )


@app.get("/api/v1/fees/mempool-blocks")
async def calculateRecommendedFee():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f'{API_BASE_URL}/api/v1/fees/mempool-blocks')
            response.raise_for_status()
            print(response.json())
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/tx/{txid}")
async def getTx(txid: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{API_BASE_URL}/api/tx/{txid}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/tx/{txid}/hex",response_class=PlainTextResponse)
async def getTxHex(txid: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{API_BASE_URL}/api/tx/{txid}/hex")
            response.raise_for_status()
            return response.text
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/address/{address}/utxo")
async def getAddressTxsUtxo(address: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{API_BASE_URL}/api/address/{address}/utxo")
            response.raise_for_status()
            print(response.json())
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/address/{address}/txs")
async def getAddressTxs(address: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{API_BASE_URL}/api/address/{address}/txs")
            response.raise_for_status()
            print(response.json())
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/block/{hash}")
async def getBlock(hash: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{API_BASE_URL}/api/block/{hash}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/block/{hash}/header",response_class=PlainTextResponse)
async def getBlockHeader(hash: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{API_BASE_URL}/api/block/{hash}/header")
            response.raise_for_status()
            return response.text
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/block-height/{height}",response_class=PlainTextResponse)
async def getBlockHeight(height: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{API_BASE_URL}/api/block-height/{height}")
            response.raise_for_status()
            #print(response.text)
            result = response.text
            return result
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/block/{hash}/txids")
async def getBlockTxids(hash: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{API_BASE_URL}/api/block/{hash}/txids")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/blocks/tip/hash",response_class=PlainTextResponse)
async def getBlocksTipHash():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{API_BASE_URL}/api/blocks/tip/hash")
            response.raise_for_status()
            return response.text
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/tx",response_class=PlainTextResponse)
async def postTx(request: Request):
    try:
        tx_data = await request.body()  # 读取原始请求体
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{API_BASE_URL}/api/tx", content=tx_data)  # 发送原始数据
            response.raise_for_status()
            return response.text  # 返回 mempool 的响应
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 调试运行方式：
# 使用命令：uvicorn filename:app --reload
# 假设文件名为 main.py，则命令为：uvicorn main:app --reload
