# MeropsSubstrateGet

![merops](https://ww1.sinaimg.cn/large/006Fzy5igy1g23f5lf07bj322t0u0x0e.jpg "merops")

### 版本

~~版本 2 采用`async`,`aiohttp`,`requests`,`beautufulsoup`等库实现~~异步抓去蛋白酶数据库数据
更新版本3
添加识别亚家族的功能，自动生成所需要的文件名
### 环境依赖

1. python >=3.6
2. requests
3. bs4
4. asyncio
5. aiohttp
6. lxml
7. pandas
8. ssl

### 使用方法

```python
python3 substrate_get.py -f [家族序号] -o [文件输出目录]
```

最终得到的数据为`result.csv`
