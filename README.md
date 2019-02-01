# firefly

## 安装

1. 安装依赖
    ```sh
    pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
    ```
1. 安装 xadmin
    ```sh
    pip install https://codeload.github.com/sshwsfc/xadmin/zip/django2
    ```
1. 同步数据库
    ```sh
    python manage.py migrate
    ```
1. 创建初始化用户
    ```sh
    python manage.py createsuperuser
    ```

## 运行

```sh
python manage.py runserver
```

## 命令
 
- `python manage.py migrate myapp --fake` 同步表结构
