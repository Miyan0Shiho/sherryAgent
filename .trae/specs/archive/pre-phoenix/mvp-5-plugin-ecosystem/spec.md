# SherryAgent - MVP-5 Skill插件与生态 产品需求文档

## Overview
- **Summary**: 实现插件化能力扩展，支持动态加载Skill和连接MCP工具服务器。
- **Purpose**: 构建SherryAgent框架的插件生态，实现能力动态扩展。
- **Target Users**: 需要扩展Agent能力的开发者和第三方工具提供者。

## Goals
- 实现插件系统，基于pluggy的hook机制
- 实现Skill加载，支持SKILL.md描述和门控检查
- 实现MCP客户端，支持连接外部MCP工具服务器
- 完善权限系统，补充第3-5层

## Non-Goals (Out of Scope)
- 新的消息渠道集成
- 企业级权限管理
- 商业化Skill市场

## Background & Context
- MVP-5是框架的第五个里程碑，专注于插件生态
- 融合OpenClaw的Skill插件系统和Claude Code的MCP集成
- 采用pluggy作为插件框架

## Functional Requirements
- **FR-1**: 插件系统，支持基于pluggy的hook机制
- **FR-2**: Skill加载，支持SKILL.md描述、门控检查、热加载/卸载
- **FR-3**: MCP客户端，支持连接外部MCP工具服务器
- **FR-4**: 权限系统完善，补充第3-5层（自动模式分类器、用户配置规则、企业策略）

## Non-Functional Requirements
- **NFR-1**: 热加载，运行时动态加载Skill插件
- **NFR-2**: 隔离性，Skill卸载后Agent不再调用相关工具
- **NFR-3**: 连接性，MCP客户端成功连接外部工具服务器
- **NFR-4**: 准确性，自动模式分类器正确判断风险等级
- **NFR-5**: 配置性，用户配置规则正确生效

## Constraints
- **Technical**: Python 3.12+，依赖pluggy、mcp
- **Business**: 2周开发周期
- **Dependencies**: 需要MVP-1至MVP-4完成

## Assumptions
- MVP-1至MVP-4已全部实现
- 用户有可用的MCP工具服务器

## Acceptance Criteria

### AC-1: 动态加载Skill
- **Given**: Agent正在运行
- **When**: 加载新的Skill插件
- **Then**: Skill被正确加载，无需重启
- **Verification**: `manual-test`

### AC-2: Skill卸载隔离
- **Given**: Skill已加载
- **When**: 卸载Skill
- **Then**: Agent不再调用该Skill的工具
- **Verification**: `regression-test`

### AC-3: MCP连接成功
- **Given**: 配置了MCP服务器
- **When**: 启动MCP客户端
- **Then**: 成功连接外部工具服务器
- **Verification**: `integration-test`

### AC-4: 风险等级判断
- **Given**: Agent请求执行操作
- **When**: 自动模式分类器判断
- **Then**: 正确判断风险等级
- **Verification**: `unit-test`

### AC-5: 用户配置生效
- **Given**: 用户配置了权限规则
- **When**: Agent执行操作
- **Then**: 用户配置规则正确生效
- **Verification**: `config-test`

## Open Questions
- [ ] Skill的版本管理如何实现？
- [ ] MCP协议的完整支持范围？
- [ ] 企业策略的配置格式？
