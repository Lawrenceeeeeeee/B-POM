# 文本分析小组展示

小组成员：郭峻荣、代旭科、赵博涵、曾子桐

# 项目介绍

Bilibili public opinion monitor

## 项目基本实现思路

本项目针对B站开发一个舆情管理工具（后期可能扩展到其他平台），能够及时获取B站视频的评论信息，用文本分析的方法对评论进行分析，得出不同视频评论的舆情变化情况，同时对用户进行画像，并且将结果可视化展示。

## 项目结构

### 文件夹及文件说明：

- **`data/`**: 包含所有与数据相关的子目录和文件。

  - **`crawler/`**: 包含网页爬虫爬取的CSV数据文件。
  - **`word_frequencies/`**: 存储词频分析结果的表格。
  - **`frequency_plots/`**: 存储从词频数据生成的柱状图。
  - **`wordclouds/`**: 包含从文本数据生成的词云图。
  - **`resources/`**: 用于存储辅助文件，如停用词列表。
    - **`stopwords.txt`**: 包含需在文本分析中排除的停用词的文本文件。
- **`src/`**: 包含数据分析的Python脚本。

  - **`word_frequency_analyzer.py`**: 用于分析词频的Python类。
  - **`word_cloud_generator.py`**: 用于生成词云的Python类。
  - **`bvav.py`:**
  - **`embedding`**:用于词嵌入的Python类。
  - **`get_bilbil_videos.py`**:获取bilbil视频并且进行内容概括的Python类。
  - **`transcribe.py`**:
  - **`videos`**:
- **`web.py`**: 设置并运行 Gradio 界面的脚本。
- **`examples`**: 列出测试样例。
- **`client.py`**: 提供。

这个 Markdown 结构用中文详细说明了项目的每一个组成部分，提供了透明的概览，便于开发者、用户或贡献者理解和维护。

## 项目所用工具

1. 爬虫工具，主要目的是获取B站的一级评论信息，提供模型训练的训练数据
2. 文本分析工具，例如jieba库的使用，停用词库等的构建和使用
3. BERT模型的使用，主要用来进行评论的情绪分析和理智度的分析
4. Gradio的使用，借助Gradio库较低成本制作出了监测的Web界面
5. 自研工具，例如辅助打Tag的工具

## 项目流程

第一步，编写爬虫获取B站一级评论数据并且标准化

第二步，组内成员分工对获取的几千条数据进行两个维度的标记

第三步，对获得的数据进行基本的文本分析，例如词频统计

第四步，部署BERT，对标记后的数据进行学习

第五步，跟踪单一视频，生成舆情监控时序图，对用户进行画像

第六步，制作WebUI，将结果可视化呈现出来，降低使用成本

最后，计划增加Tag维度，进而可以对用户进行较好的聚类分析；将数据库引入，提供一套可以常态化管理和维护的舆情监控方案。

# 打Tag的统一标准

## Tag的分类

第一类：情绪分类指标（1-3）【1是消极、2是中立、3是积极】

    其中，这个指标只基于评论自己的情感色彩，与视频内容无关；提问帖讨论帖这些无明显情感倾向的均为中立。

第二类：观众满意指标（1-3）【1是不满、2是不在意、3是满意】

    其中，出现玩梗、刷沙发这类的评论，一律按照不在意考虑。

第三类：是否为提问贴（1，2）【1是不属于，2是属于】

第四类：是否为讨论帖（1，2）【1是不属于，2是属于】

第五类：是否为玩梗帖（1，2）【1是不属于，2是属于】

## 分类逻辑

第一类指标主要围绕评论区的情绪变化进行监控。

第二类指标主要围绕观众对该视频是否满意，便于了解观众偏好。

第三、四、五类指标主要为了更加清晰展示评论区的结构，将一些理性讨论的评论区纳入监控范围。


# 评论相关度 correlation_score


通过B站API获取视频信息，包括视频的cid（分p)、视频的url等
下载视频音频，基于Whisper进行语音转写，并用gpt-4-turbo模型进行概括
基于视频内容的概要来分析用户评论的相关性

考虑到视频内容的长度，一个视频可能会涉及到多个主题内容，但评论大多数情况下最多只会涉及一到两个主题，因此我们基于gpt-4-turbo来对视频内容进行分段概括，然后计算评论与每个部分的相关性，取最大值作为最终的相关性评分。

相关性计算采用的是embedding，模型采用的是OpenAI的text-embedding-3-large模型。这个模型是基于Transformer的模型，能更好地结合上下文，并且相较于BERT来说可以接受更多的tokens，可以将文本转换为向量，然后计算向量之间的余弦相似度。


# Todo-list

- [X] 爬虫获取B站评论【只要一级评论】
- [X] 打Tag
- [X] 部署BERT，炼丹炉，启动！
- [ ] 【展示部分】跟踪单一视频，生成时序图
- [ ] 可以添加更多种类的Tag（机器人检测，理性程度)
- [X] 做WebUI
- [ ] PPT展示

目前进度：

已完成爬虫脚本，可以根据BV号获取视频

数据维度如下：

'oid','timestamp', 'rpid', 'uid', 'uname', 'content', 'likes', 'replies'

其中：

- oid：视频av号
- timestamp：时间戳
- rpid：评论id
- uid：用户id
- uname：用户名
- content：评论内容
- likes：点赞数
- replies：回复数（二级评论数)

统一了打Tag标准

构建了WebUI
