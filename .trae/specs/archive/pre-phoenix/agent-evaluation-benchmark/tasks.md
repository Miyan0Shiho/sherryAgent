
# SherryAgent 能力评估与框架反省 - 实施计划

## [x] Task 1: 评估数据集调研与选择
- **Priority**: P0
- **Depends On**: None
- **Description**:
  - 调研主流开源 Agent 评估数据集（AgentBench、GAIA、ToolBench、WebArena 等）
  - 对比各数据集的特点、难度分布、许可证、获取难度
  - 选择 1-2 个最适合 SherryAgent 的数据集
  - 确定抽样策略（每个难度级别抽取数量）
- **Acceptance Criteria Addressed**: [AC-1]
- **Test Requirements**:
  - `human-judgement` TR-1.1: 选定的数据集应有开源许可证，适合学术/项目使用
  - `human-judgement` TR-1.2: 数据集应包含工具调用、推理、多步骤任务等类型
  - `human-judgement` TR-1.3: 应有明确的难度分级（简单/中等/困难）
- **Notes**: 优先选择不需要复杂环境配置的数据集，避免 WebArena 这类需要浏览器环境的

## [x] Task 2: 数据集加载器实现
- **Priority**: P0
- **Depends On**: [Task 1]
- **Description**:
  - 创建数据集加载模块（`tests/benchmark/datasets/`）
  - 实现选定数据集的加载器
  - 支持测试用例过滤（按难度、类型）
  - 输出标准化的测试用例格式（任务描述、预期结果、评估标准）
- **Acceptance Criteria Addressed**: [AC-1]
- **Test Requirements**:
  - `programmatic` TR-2.1: 加载器能成功读取数据集并返回测试用例列表
  - `programmatic` TR-2.2: 能按难度级别过滤测试用例
  - `human-judgement` TR-2.3: 输出的测试用例格式标准化，包含所有必要信息
- **Notes**: 如果数据集太大，先只下载/加载小样例

## [x] Task 3: 测试执行框架实现
- **Priority**: P0
- **Depends On**: [Task 2]
- **Description**:
  - 创建测试执行引擎（`tests/benchmark/runner.py`）
  - 集成 SherryAgent 的 Agent Loop
  - 配置使用 qwen3:0.6b 模型
  - 实现完整的执行日志记录
- **Acceptance Criteria Addressed**: [AC-2, AC-3]
- **Test Requirements**:
  - `programmatic` TR-3.1: 能将测试用例输入 SherryAgent 并执行
  - `programmatic` TR-3.2: 完整记录执行过程（时间戳、事件、工具调用）
  - `human-judgement` TR-3.3: 日志格式清晰易读，便于后续分析
- **Notes**: 复用现有的 Agent Loop，只需添加日志记录层

## [x] Task 4: 执行过程记录增强
- **Priority**: P1
- **Depends On**: [Task 3]
- **Description**:
  - 增强日志记录，捕获思考链（如果模型输出）
  - 记录每个工具调用的详细信息（参数、返回值、耗时）
  - 记录中间结果和状态变化
  - 记录 Token 使用情况（如可用）
- **Acceptance Criteria Addressed**: [AC-3]
- **Test Requirements**:
  - `human-judgement` TR-4.1: 日志包含完整的工具调用序列，包括参数和返回值
  - `human-judgement` TR-4.2: 日志包含时间信息，可分析各阶段耗时
  - `programmatic` TR-4.3: 日志以结构化格式保存（JSON + 人类可读文本）
- **Notes**: 可以考虑使用现有的事件系统来记录

## [x] Task 5: 抽样测试执行（简单任务）
- **Priority**: P0
- **Depends On**: [Task 4]
- **Description**:
  - 从数据集中抽取 3-5 个简单任务
  - 使用 qwen3:0.6b 模型逐个执行
  - 观察执行过程，记录问题
  - 初步评估任务完成情况
- **Acceptance Criteria Addressed**: [AC-2, AC-3, AC-4]
- **Test Requirements**:
  - `programmatic` TR-5.1: 所有简单任务都能完整执行完毕（无崩溃）
  - `human-judgement` TR-5.2: 每个任务都有执行日志
  - `human-judgement` TR-5.3: 初步标记任务完成状态（成功/部分成功/失败）
- **Notes**: 从最简单的任务开始，建立信心

## [x] Task 6: 抽样测试执行（中等任务）
- **Priority**: P0
- **Depends On**: [Task 5]
- **Description**:
  - 从数据集中抽取 3-5 个中等难度任务
  - 使用 qwen3:0.6b 模型逐个执行
  - 详细观察执行过程，特别注意工具调用
  - 评估任务完成情况
- **Acceptance Criteria Addressed**: [AC-2, AC-3, AC-4, AC-7]
- **Test Requirements**:
  - `programmatic` TR-6.1: 所有中等任务都能完整执行完毕（无崩溃）
  - `human-judgement` TR-6.2: 详细记录工具调用尝试（成功/失败）
  - `human-judgement` TR-6.3: 评估至少 3 个中等任务的完成质量
- **Notes**: 重点观察模型是否主动使用工具

## [x] Task 7: 抽样测试执行（困难任务）
- **Priority**: P0
- **Depends On**: [Task 6]
- **Description**:
  - 从数据集中抽取 3-5 个困难任务
  - 使用 qwen3:0.6b 模型逐个执行
  - 详细观察多步骤推理和工具调用链
  - 评估任务完成情况
- **Acceptance Criteria Addressed**: [AC-2, AC-3, AC-4, AC-7]
- **Test Requirements**:
  - `programmatic` TR-7.1: 所有困难任务都能完整执行完毕（无崩溃）
  - `human-judgement` TR-7.2: 记录多步骤任务的规划过程（如有）
  - `human-judgement` TR-7.3: 评估至少 1 个困难任务的完成质量
- **Notes**: 即使失败也要完整执行，观察失败点

## [x] Task 8: 执行结果分析与问题识别
- **Priority**: P0
- **Depends On**: [Task 5, Task 6, Task 7]
- **Description**:
  - 回顾所有测试用例的执行日志
  - 分类整理问题（工具调用、提示工程、记忆系统、编排等）
  - 识别根本原因（是模型能力限制还是框架设计问题）
  - 统计成功率、平均耗时等指标
- **Acceptance Criteria Addressed**: [AC-4, AC-5]
- **Test Requirements**:
  - `human-judgement` TR-8.1: 识别出至少 5 个框架层面的问题
  - `human-judgement` TR-8.2: 每个问题都有对应的执行日志片段作为证据
  - `human-judgement` TR-8.3: 区分"模型能力限制"和"框架可改进"的问题
- **Notes**: 可以制作表格来整理问题

## [x] Task 9: 框架反省报告撰写
- **Priority**: P0
- **Depends On**: [Task 8]
- **Description**:
  - 撰写完整的框架反省报告
  - 包含：测试概览、结果统计、问题清单、根本原因分析
  - 提出改进建议并按优先级排序
  - 制定短期和长期改进路线图
- **Acceptance Criteria Addressed**: [AC-6, AC-7]
- **Test Requirements**:
  - `human-judgement` TR-9.1: 报告结构完整，包含所有要求的章节
  - `human-judgement` TR-9.2: 改进建议具体可行，有优先级
  - `human-judgement` TR-9.3: 明确回答"框架设计是否成功"这个问题
- **Notes**: 报告保存为 `docs/research/agent-evaluation-retrospective.md`

