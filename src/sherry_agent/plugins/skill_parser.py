from __future__ import annotations

import os
import re
from typing import Dict, List, Optional, Set, Any


class SkillMetadata:
    """技能元数据"""
    def __init__(self, name: str, version: str, description: str):
        self.name = name
        self.version = version
        self.description = description


class SkillDependency:
    """技能依赖"""
    def __init__(self, name: str, version: Optional[str] = None):
        self.name = name
        self.version = version


class SkillTrigger:
    """技能触发条件"""
    def __init__(self, type: str, condition: str):
        self.type = type
        self.condition = condition


class SkillDefinition:
    """技能定义"""
    def __init__(
        self,
        metadata: SkillMetadata,
        dependencies: List[SkillDependency],
        triggers: List[SkillTrigger],
        entry_point: str,
        env_vars: Dict[str, str],
    ):
        self.metadata = metadata
        self.dependencies = dependencies
        self.triggers = triggers
        self.entry_point = entry_point
        self.env_vars = env_vars


class SkillParser:
    """SKILL.md 文件解析器"""

    @staticmethod
    def parse(file_path: str) -> Optional[SkillDefinition]:
        """解析 SKILL.md 文件"""
        if not os.path.exists(file_path):
            return None

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 解析元数据
            metadata = SkillParser._parse_metadata(content)
            if not metadata:
                return None

            # 解析依赖
            dependencies = SkillParser._parse_dependencies(content)

            # 解析触发条件
            triggers = SkillParser._parse_triggers(content)

            # 解析入口点
            entry_point = SkillParser._parse_entry_point(content)
            if not entry_point:
                return None

            # 解析环境变量
            env_vars = SkillParser._parse_env_vars(content)

            return SkillDefinition(
                metadata=metadata,
                dependencies=dependencies,
                triggers=triggers,
                entry_point=entry_point,
                env_vars=env_vars,
            )
        except Exception as e:
            print(f"Error parsing SKILL.md: {e}")
            return None

    @staticmethod
    def _parse_metadata(content: str) -> Optional[SkillMetadata]:
        """解析元数据部分"""
        # 尝试不同的正则表达式模式
        lines = content.strip().split('\n')
        if not lines:
            return None

        # 解析名称
        if lines[0].startswith('#'):
            name = lines[0][1:].strip()
        else:
            return None

        # 解析版本和描述
        version = None
        description = None
        for line in lines[1:]:
            line = line.strip()
            if line.startswith('version:'):
                version = line[len('version:'):].strip()
            elif line.startswith('description:'):
                description = line[len('description:'):].strip()
            elif line.startswith('##'):
                break

        if not version or not description:
            return None

        return SkillMetadata(name=name, version=version, description=description)

    @staticmethod
    def _parse_dependencies(content: str) -> List[SkillDependency]:
        """解析依赖部分"""
        dependencies = []
        lines = content.strip().split('\n')
        in_dependencies = False

        for line in lines:
            line = line.strip()
            if line.startswith('## Dependencies'):
                in_dependencies = True
            elif line.startswith('##') and in_dependencies:
                break
            elif in_dependencies and line.startswith('-'):
                # 提取依赖名称和版本
                # 简化解析，直接分割字符串
                line = line[1:].strip()  # 移除 '-' 符号
                if '@' in line:
                    name, version = line.split('@', 1)
                    name = name.strip()
                    version = version.strip()
                else:
                    name = line.strip()
                    version = None
                dependencies.append(SkillDependency(name=name, version=version))
        return dependencies

    @staticmethod
    def _parse_triggers(content: str) -> List[SkillTrigger]:
        """解析触发条件部分"""
        triggers = []
        lines = content.strip().split('\n')
        in_triggers = False

        for line in lines:
            line = line.strip()
            if line.startswith('## Triggers'):
                in_triggers = True
            elif line.startswith('##') and in_triggers:
                break
            elif in_triggers and line.startswith('-'):
                # 提取触发类型和条件
                # 简化解析，直接分割字符串
                line = line[1:].strip()  # 移除 '-' 符号
                if ':' in line:
                    type, condition = line.split(':', 1)
                    type = type.strip()
                    condition = condition.strip()
                    # 移除引号
                    if (condition.startswith('"') and condition.endswith('"')) or (condition.startswith("'") and condition.endswith("'")):
                        condition = condition[1:-1]
                    triggers.append(SkillTrigger(type=type, condition=condition))
        return triggers

    @staticmethod
    def _parse_entry_point(content: str) -> Optional[str]:
        """解析入口点部分"""
        lines = content.strip().split('\n')
        in_entry_point = False

        for line in lines:
            line = line.strip()
            if line.startswith('## Entry Point'):
                in_entry_point = True
            elif line.startswith('##') and in_entry_point:
                break
            elif in_entry_point and line:
                return line.strip()
        return None

    @staticmethod
    def _parse_env_vars(content: str) -> Dict[str, str]:
        """解析环境变量部分"""
        env_vars = {}
        lines = content.strip().split('\n')
        in_env_vars = False

        for line in lines:
            line = line.strip()
            if line.startswith('## Environment Variables'):
                in_env_vars = True
            elif line.startswith('##') and in_env_vars:
                break
            elif in_env_vars and line and '=' in line:
                # 提取环境变量名和值
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
        return env_vars


class SkillValidator:
    """技能验证器"""

    @staticmethod
    def validate_dependencies(dependencies: List[SkillDependency]) -> bool:
        """验证依赖"""
        # 这里可以实现依赖检查逻辑
        # 例如检查依赖是否已安装，版本是否匹配等
        for dep in dependencies:
            print(f"Checking dependency: {dep.name} {dep.version or 'latest'}")
        return True

    @staticmethod
    def validate_environment(env_vars: Dict[str, str]) -> bool:
        """验证环境"""
        # 检查必要的环境变量是否存在
        for key, value in env_vars.items():
            if not os.environ.get(key) and not value:
                print(f"Missing required environment variable: {key}")
                return False
        return True

    @staticmethod
    def validate_triggers(triggers: List[SkillTrigger]) -> bool:
        """验证触发条件"""
        # 验证触发条件是否有效
        valid_trigger_types = {'keyword', 'event', 'schedule'}
        for trigger in triggers:
            if trigger.type not in valid_trigger_types:
                print(f"Invalid trigger type: {trigger.type}")
                return False
        return True

    @staticmethod
    def validate_skill(skill: Optional[SkillDefinition]) -> bool:
        """验证技能定义"""
        if not skill:
            print("Skill definition is None")
            return False

        # 验证元数据
        if not skill.metadata.name or not skill.metadata.version:
            print("Missing required metadata")
            return False

        # 验证依赖
        if not SkillValidator.validate_dependencies(skill.dependencies):
            return False

        # 验证环境
        if not SkillValidator.validate_environment(skill.env_vars):
            return False

        # 验证触发条件
        if not SkillValidator.validate_triggers(skill.triggers):
            return False

        # 验证入口点
        if not skill.entry_point:
            print("Missing entry point")
            return False

        return True


class SkillLoader:
    """技能加载器"""

    @staticmethod
    def load_skill(skill_dir: str) -> Optional[SkillDefinition]:
        """加载技能"""
        skill_file = os.path.join(skill_dir, 'SKILL.md')
        skill = SkillParser.parse(skill_file)
        if skill and SkillValidator.validate_skill(skill):
            return skill
        return None

    @staticmethod
    def load_skills_from_directory(directory: str) -> List[SkillDefinition]:
        """从目录加载技能"""
        skills = []
        if not os.path.exists(directory):
            return skills

        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                skill = SkillLoader.load_skill(item_path)
                if skill:
                    skills.append(skill)
        return skills
