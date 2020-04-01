# satis-flow

构建 PHP 私有仓库自动工作流程

#### 安装

克隆项目

```shell
git clone https://github.com/kainonly/satis-flow.git
```

拉取 satis 项目

```shell
git submodule init
git submodule update
git submodule foreach git checkout master
git submodule foreach git pull
```

调整 php 配置内存上限，修改文件 `satis/bin/satis`

```php
// 加入
ini_set('memory_limit',-1);
```

执行流程

```shell
python ./bootstrap.py
```

#### 配置说明

- **external**
  - **url** 网络回调接口地址（生成satis.json）
- **oss** 阿里云 OSS 对象存储配置
  - **access_key_id** 
  - **access_key_secret**
  - **endpoint**
  - **bucket_name**