# 文本分析小组展示

小组成员：郭峻荣、代旭科、赵博涵、曾子桐

# Todo-list

- [ ] 爬虫获取B站评论【只要一级评论】
- [ ] 打Tag
- [ ] 部署BERT，炼丹炉，启动！
- [ ] 【展示部分】跟踪单一视频，生成时序图
- [ ] 可以添加更多种类的Tag（机器人检测，理性程度)
- [ ] 做WebUI

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
