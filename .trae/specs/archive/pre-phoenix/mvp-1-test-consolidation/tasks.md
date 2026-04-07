# SherryAgent - MVP-1 测试整合与覆盖分析 实施计划

## [x] 任务 1: 整合临时测试脚本
- **Priority**: P0
- **Depends On**: None
- **Description**:
  - 分析根目录的临时测试脚本，保留有用的
  - 将有用的测试脚本移动到 `tests/` 目录的适当位置
  - 清理不再需要的临时测试脚本
  - 确保移动的测试能正常运行
- **Acceptance Criteria Addressed**: [AC-1]
- **Test Requirements**:
  - `programmatic` TR-1.1: 验证根目录不再有临时测试脚本
  - `programmatic` TR-1.2: 验证移动的测试能正常运行
  - `programmatic` TR-1.3: 验证测试文件位置符合项目规范
- **Notes**: 保留 test_fully_automated.py 作为完全自动化测试的基础

## [x] 任务 2: 创建 Ollama 集成测试
- **Priority**: P0
- **Depends On**: [任务 1]
- **Description**:
  - 在 `tests/integration/` 目录下创建 Ollama 集成测试
  - 测试与 qwen3:0.6b 模型的实际交互
  - 测试简单对话功能
  - 添加跳过标记，在 Ollama 不可用时跳过测试
- **Acceptance Criteria Addressed**: [AC-3]
- **Test Requirements**:
  - `programmatic` TR-2.1: 验证 Ollama 客户端能正常连接
  - `programmatic` TR-2.2: 验证能与 qwen3:0.6b 模型对话
  - `programmatic` TR-2.3: 验证测试在 Ollama 不可用时能正常跳过

## [x] 任务 3: 增强 Agent Loop 集成测试
- **Priority**: P0
- **Depends On**: [任务 1]
- **Description**:
  - 增强现有的 Agent Loop 集成测试
  - 测试完整的工具调用流程（使用 Mock）
  - 测试多轮对话
  - 测试 token 预算控制
  - 测试取消功能
- **Acceptance Criteria Addressed**: [AC-2, AC-5]
- **Test Requirements**:
  - `programmatic` TR-3.1: 验证完整的工具调用流程
  - `programmatic` TR-3.2: 验证多轮对话能正常进行
  - `programmatic` TR-3.3: 验证 token 预算控制有效
  - `programmatic` TR-3.4: 验证任务取消功能正常

## [x] 任务 4: 创建权限系统集成测试
- **Priority**: P0
- **Depends On**: [任务 1]
- **Description**:
  - 创建权限系统的端到端测试
  - 测试危险命令被拦截
  - 测试安全命令能正常执行
  - 测试沙箱隔离功能
- **Acceptance Criteria Addressed**: [AC-6]
- **Test Requirements**:
  - `programmatic` TR-4.1: 验证 `rm -rf /` 被拦截
  - `programmatic` TR-4.2: 验证安全命令能正常执行
  - `programmatic` TR-4.3: 验证沙箱路径隔离有效

## [x] 任务 5: 创建端到端测试套件
- **Priority**: P1
- **Depends On**: [任务 2, 任务 3, 任务 4]
- **Description**:
  - 在 `tests/e2e/` 目录下创建完整的端到端测试
  - 整合所有核心功能测试
  - 创建测试分组和标记
  - 确保测试可独立运行
- **Acceptance Criteria Addressed**: [AC-2]
- **Test Requirements**:
  - `programmatic` TR-5.1: 验证端到端测试套件能完整运行
  - `programmatic` TR-5.2: 验证测试标记和分组工作正常
  - `programmatic` TR-5.3: 验证测试可并行运行

## [x] 任务 6: 分析测试覆盖率
- **Priority**: P1
- **Depends On**: [任务 5]
- **Description**:
  - 配置 pytest-cov 生成覆盖率报告
  - 识别测试覆盖率低的模块
  - 补充缺失的单元测试
  - 确保核心逻辑覆盖率 > 80%
- **Acceptance Criteria Addressed**: [AC-7]
- **Test Requirements**:
  - `programmatic` TR-6.1: 验证能生成覆盖率报告
  - `programmatic` TR-6.2: 验证核心模块覆盖率 > 80%
  - `programmatic` TR-6.3: 验证新增的测试能正常运行

## [x] 任务 7: 文档和最佳实践
- **Priority**: P2
- **Depends On**: [任务 6]
- **Description**:
  - 更新测试相关的文档
  - 编写测试运行指南
  - 建立测试最佳实践
  - 确保测试易于维护
- **Acceptance Criteria Addressed**: [AC-1, AC-2]
- **Test Requirements**:
  - `human-judgement` TR-7.1: 验证测试文档完整清晰
  - `human-judgement` TR-7.2: 验证测试代码易于理解和维护
