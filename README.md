# 快速使用

## 安装

1. 安装pipenv
    ```
    pip install pipenv
    ```
2. 安装依赖
    ```
    pipenv install --dev
    ```
3. 激活虚拟环境
    ```
    pipenv shell
    ```
4. 同步数据库
    ```
    manage.py migrate
    ```

## 命令

- `manage.py runserver` 启动
- `pipenv install ` 安装相关模块并加入到Pipfile