# 快速使用

## 安装 xadmin
```
// 下载源码
git clone https://github.com/sshwsfc/xadmin.git

cd xadmin

// 切换分支 支持 django2
git checkout django2

// 安装依赖
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

// 安装 xadmin
python setup.py install
```

## 命令

- `pip install pipenv` 安装pipenv
- `pipenv shell` 激活虚拟环境
- `manage.py migrate` 同步数据库
- `manage.py runserver` 启动
- `pipenv install abc` 安装相关模块并加入到Pipfile