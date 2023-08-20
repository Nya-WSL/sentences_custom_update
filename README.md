# Sentences Custom Update

![version](https://img.shields.io/badge/Version-1.0.8-cyan) ![python](https://img.shields.io/badge/Python-3.8.10-blue)

bot插件扩展，用于快速更新语录库，没有第三方库无需安装依赖

## 如何使用

![help](help.jpg)

## ChangeLog

### 语录库更新

- 发送语录支持图片，通过random函数随机抽取

- 修改语录合集上传的图片和其他语录一样为单独的路径避免产生未知的bug

- 十连合并为一条发送避免被风控

- 扩展楠桐语录和语录合集查询功能，支持查询占比和统计

- 楠桐语录和语录合集查询功能新增卡池

- 楠桐语录十连新增当次合计

- 楠桐语录查询新增累计抽卡次数

- 压缩楠桐语录查询的消息长度避免被风控

- 发送语录新增稀有度显示

注：该功能为实验性功能，目前可能存在超出预计的性能问题，届时可能会移除该功能

- 楠桐语录十连新增稀有度显示

注：该功能为实验性功能，目前可能存在超出预计的性能问题，届时可能会移除该功能

- 楠桐语录卡池新增总数

- 语录格式改为〔g{text["id"]}〕

- 在楠桐语录调用结束后尝试通过gc.collect()清理内存避免发生性能问题

- 楠桐语录除语录库外的path改为bot的path_config

经过短期测试如无问题其他语录将会一起适配，scu暂不确定是否适配

- 楠桐语录十连改为n抽，目前支持1抽-30抽，触发：楠桐语录.n抽 目前支持1抽-30抽

- 移除楠桐语录.n抽触发关键词，n抽触发与楠桐语录触发关键词合并，触发：楠桐语录 + n抽|单抽 目前支持1抽-30抽 例：楠桐语录30抽，楠桐语录14抽，楠桐语录单抽

n抽触发正则：([0-9]+抽|零抽|单抽|抽)

- 尝试通过延长核心超时时间修复n抽报Timeout的问题

- n抽默认上限改为50

- 新增配置上限命令，可配置n抽单次抽卡次数，默认5级以上权限才能触发，该配置目前为全局配置，所有群的上限都会被修改！

- 新增简易错误码系统，可使用帮助楠桐语录查看

- 配置上限触发格式改为：楠桐语录["配置上限", "修改上限"]

- 超限警告的值改为变量方便后续更新

- 修改抽卡超限报错提示

- n抽新增触发关键词：一井|抽卡

预计下下个版本会将抽卡上限改为对应每个群而不是现在的全局配置

- 修复单抽和抽卡不会触发的问题

- 楠桐语录新增单角色卡池 触发：楠桐语录[“限定”, “指定”] 角色 | 楠桐语录限定n抽 角色（角色必须为全名，可使用楠桐语录查询获取）

- 修复一个变量复用导致的bug

- 将n抽上限的键值对移到单独的配置文件避免与查询产生冲突
#### 1.0.9 | 2023.7.29

- 修复通过回复上传语录时如果回复中存在空格会导致语录作者出现错误的问题

#### 1.0.8 | 2023.7.27

- 上传语录支持回复，回复不需要填写作者，默认为群名称

例外：
”小丑竟是我自己“=”桑吉Sage“
“冰蓝艾思博录”=“毕方”

- 修复因为服务器在中国大陆导致的github无法推送使bot卡死的问题，现在为每天0点推送

#### 1.0.7 | 2023.7.26

##### add：

- 上传图片支持回复 ![example1](example1.jpg)

#### 1.0.6 | 2023.7.25

##### add：

- 新增查询功能，目前可查询已收录语录列表

##### change：

-  稍微优化了一下代码并移除了未使用的变量

#### 1.0.5 | 2023.7.19

##### change:

- 移除上传语录所需的权限要求

##### fix：

- 修复在同一个进程中多次上传图片时，当前时间不刷新的问题

#### 1.0.4 | 2023.7.19

##### add:

- 上传语录初步支持上传图片，上传的图片将会按照语录分类

#### 1.0.3 | 2023.7.18

##### add:

- 成功上传语录后发送的消息内容新增语录的当前id

##### fix：

- 修复一个逻辑bug，该bug不会影响程序的执行，但会抛出一个异常从而被except捕捉

#### 1.0.2 | 2023.7.17

##### add:

- 刷新数据库通过scu触发，不再通过监测文件变动，之后应该是即时刷新（强制延迟2-5s）而不是延迟30s了

#### 1.0.1

##### add:

- 适配语录合集

#### 1.0.1

##### add:

- 适配小晨语录

#### 1.0.1 | 2023.7.6

##### add:

- 添加权限管理，上传语录现在需要5级以上权限（群管理）

##### fix:

- 修复语录不存在时只会后台报错不会提示的问题

#### 1.0.0 | 2023.7.6