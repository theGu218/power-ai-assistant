# 电力负荷 AI 分析助手

> 用自然语言查电力负荷数据：问一句话，它生成 SQL、查库、给答案，并说明依据。
> 建立在 [power-load-analysis](https://github.com/theGu218/power-load-analysis) 的数据底座之上。

---

## 这个项目解决什么

数据在库里，但不会写 SQL 的人用不了。这个助手把「自然语言 → SQL → 结果 → 回答」这条链路打通，并且：

- 每个答案带来源（查了哪个视图 / 哪条 SQL / 哪份文档）；
- 查不到时明确拒答，不编；
- 有评测集和准确率，不是"看起来能用"。

---

## 结构

```
电力AI助手/
├── data/                 # 数据库（来自上游项目，不入 git）
│   └── power_load.db
├── models/               # 预测模型与指标
├── practice/             # 阶段 0 练手脚本
├── app/                  # 应用主体（阶段 1 开始写）
├── eval/                 # 评测集与跑分脚本
└── README.md
```

数据来源：`power-load-analysis` 的 `processed/power_load.db`（三表星型模型 + 4 个视图，121,269 行）。

---

## 状态

- [x] 项目骨架
- [ ] 阶段 0：API 调用 / 意图分类 / 工具循环
- [ ] 阶段 1：FastAPI 骨架 + Text-to-SQL
- [ ] 阶段 2：评测 / RAG / 拒答 / 部署
