# SherryAgent - Cost Latency Ops Spec

## Overview
- **Summary**: 定义预算、缓存、限流、观测、告警、容量规划和 SRE 运行口径。
- **Purpose**: 让质量、延迟、成本和稳定性之间的取舍可见且可运营。

## Goals
- 固定 `strict / balanced / premium` 预算档位
- 固定缓存、模型路由、限流、降级顺序
- 固定 10x / 100x 观测与容量规划指标

## Non-Goals
- 不实现监控或缓存系统

## Acceptance Criteria
- 预算和降级顺序没有歧义
- 扩容、告警、值班和事故管理都有明确口径

