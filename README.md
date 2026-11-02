# dsh-superagent playground

用来验证 [DeepSeek Harness 的 dsh-superagent 原型](https://github.com/deepseek-ai/dsh-superagent-prototype)（MIT，研究原型）的测试仓库。

## 这里是怎么干活的

在 Issue 里 @`gameplay19491001-alt` 提需求，常驻的 Super-agent 会：

1. 轮询到这个请求 → 模型评估是否值得做
2. 建工单，在独立目录里起一个 Worker 会话
3. Worker 克隆仓库、改代码、跑测试、开 PR
4. 回到原 Issue 回帖交付

人只在提需求和合并 PR 时出现。

## 已完成的验证

| PR | 内容 | 结果 |
| --- | --- | --- |
| #4 | 新建 `HELLO.md` | 已合并 |
| #6 | `scripts/wordcount.py` + `tests/` + GitHub Actions CI | 已合并，CI 通过 |

## 目录

- `scripts/wordcount.py` —— 词频统计命令行工具
- `tests/test_wordcount.py` —— pytest 用例
- `.github/workflows/test.yml` —— push / PR 时跑 pytest

> 注意：这是研究原型的试验场，不是生产代码。
