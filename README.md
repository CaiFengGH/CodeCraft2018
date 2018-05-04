# CodeCraft2018

[2018华为软件精英挑战赛总结](https://www.jianshu.com/p/b9c043bdefd5)

>题目解析

- 时间序列预测问题

训练数据为2015年1月2015年5月，及2015年12月到2016年1月，由这两段时间，线上预测需求；

比赛中常用的模型有MA/AR/ARMA/ARIMA/Garch/指数平滑等，在正式用例公布时，华为论坛上出现预测思路；

[二次指数平滑](https://forum.huaweicloud.com/thread-8021-1-1.html) [轻松理解指数平滑](https://grisha.org/blog/2016/01/29/triple-exponential-smoothing-forecasting/)

- 背包优化问题

在满足CPU和MEM的前提下，优化其中一个维度；

[二维背包问题](https://forum.huaweicloud.com/thread-8065-1-1.html)

>数据解读

- 数据量

用例训练数据统计之后，不到3000行数据，在机器学习的相关竞赛中，确实是少之又少，只能大概清楚其上升或者下降趋势；

- 数据特征

缺乏数据特征，只有时间和数量两个特征点，存在大量问题；

- 异常值

在数据中存在大量异常值，包括周末、节假日、大促活动、春节等特殊天分，对于这些异常值的处理，是本次比赛中最为重要的环节;


