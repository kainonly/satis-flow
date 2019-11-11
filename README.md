# satis-flow

构建 PHP 私有仓库自动工作流程

#### 使用条件

- Docker 容器
- 阿里云 OSS 对象存储
- 生成 satis.json 的网络回调接口

#### 项目依赖

- [docker](https://docker-py.readthedocs.io/en/stable/client.html) Docker SDK for Python
- [requests](https://cn.python-requests.org/zh_CN/latest/) Requests: 让 HTTP 服务人类
- [oss2](https://help.aliyun.com/document_detail/32026.html?spm=a2c4g.11186623.6.814.105b5779id1Yf9) OSS Python SDK

#### 配置说明

- **docker**
  - **base_url** 连接地址
  - **username** 用户名(如果使用私有源)
  - **password** 用户密码
  - **registry** 私有源
  - **repository** 镜像地址
- **external**
  - **url** 网络回调接口地址（生成satis.json）
- **oss** 阿里云 OSS 对象存储配置
  - **access_key_id** 
  - **access_key_secret**
  - **endpoint**
  - **bucket_name**

#### 打包

安装 `pyinstaller`

```shell
pip install pyinstaller
```

如果使用了 `python>=3.8`，则需要安装开发版

```shell
pip install https://github.com/pyinstaller/pyinstaller/archive/develop.tar.gz
```

打包发布

```
pyinstaller bootstrap.py
```