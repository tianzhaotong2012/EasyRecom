# Easy Recommend FrameWork #
## 一个简单的推荐框架 ##

## Version ##
- 1.0 支持基于物品相似度的推荐

## 安装步骤 ##
- 首先安装jieba，切换到jieba目录运行 python setup.py install
- 确认物料input目录user文件夹的以user_id命名的用户喜好文件
- 确认物料input目录post文件夹的post_online是要推荐的物料
- 执行src目录下的python run.py
- 查看output下的推荐结果

## 运行原理 ##
- 将物料库中的title一个个读取出来，用jieba对title做分词处理
- 把上一步中分割的词去词向量库中把每个词对应的词向量取出
- 把每个词的词向量相加，得到整个title的词向量
- 依次处理整个词向量库的title，转换为句子向量
- 将用户喜爱的物料的title也转换成句子向量
- 将用户喜爱的物料的向量依次与物料库每个向量，取余弦距离，计算相似度
- 取相似度高的物料，推荐给用户



