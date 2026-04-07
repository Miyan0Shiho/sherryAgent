from __future__ import annotations

import os
import tempfile
import unittest

from sherry_agent.plugins.skill_parser import (
    SkillParser,
    SkillValidator,
    SkillLoader,
    SkillDefinition,
    SkillMetadata,
    SkillDependency,
    SkillTrigger,
)


class TestSkillParser(unittest.TestCase):
    """测试 SKILL.md 解析器"""

    def setUp(self):
        """设置测试环境"""
        # 创建临时目录
        self.temp_dir = tempfile.mkdtemp()
        # 创建测试 SKILL.md 文件
        self.skill_file = os.path.join(self.temp_dir, "SKILL.md")
        with open(self.skill_file, "w", encoding="utf-8") as f:
            f.write("""
# Test Skill
version: 1.0.0
description: A test skill

## Dependencies
- requests
- pytest@7.0.0

## Triggers
- keyword: test
- event: user_message
- schedule: "*/5 * * * *"

## Entry Point
main.py:run

## Environment Variables
API_KEY=secret
DEBUG=True
""")

    def tearDown(self):
        """清理测试环境"""
        # 删除临时文件
        if os.path.exists(self.skill_file):
            os.remove(self.skill_file)
        # 删除临时目录
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)

    def test_parse_skill(self):
        """测试解析 SKILL.md 文件"""
        skill = SkillParser.parse(self.skill_file)
        self.assertIsInstance(skill, SkillDefinition)
        self.assertEqual(skill.metadata.name, "Test Skill")
        self.assertEqual(skill.metadata.version, "1.0.0")
        self.assertEqual(skill.metadata.description, "A test skill")
        self.assertEqual(len(skill.dependencies), 2)
        self.assertEqual(skill.dependencies[0].name, "requests")
        self.assertIsNone(skill.dependencies[0].version)
        self.assertEqual(skill.dependencies[1].name, "pytest")
        self.assertEqual(skill.dependencies[1].version, "7.0.0")
        self.assertEqual(len(skill.triggers), 3)
        self.assertEqual(skill.triggers[0].type, "keyword")
        self.assertEqual(skill.triggers[0].condition, "test")
        self.assertEqual(skill.triggers[1].type, "event")
        self.assertEqual(skill.triggers[1].condition, "user_message")
        self.assertEqual(skill.triggers[2].type, "schedule")
        self.assertEqual(skill.triggers[2].condition, "*/5 * * * *")
        self.assertEqual(skill.entry_point, "main.py:run")
        self.assertEqual(skill.env_vars["API_KEY"], "secret")
        self.assertEqual(skill.env_vars["DEBUG"], "True")

    def test_validate_skill(self):
        """测试验证技能定义"""
        skill = SkillParser.parse(self.skill_file)
        self.assertTrue(SkillValidator.validate_skill(skill))

    def test_load_skill(self):
        """测试加载技能"""
        skill = SkillLoader.load_skill(self.temp_dir)
        self.assertIsInstance(skill, SkillDefinition)

    def test_load_skills_from_directory(self):
        """测试从目录加载技能"""
        # 创建另一个技能目录
        skill_dir2 = os.path.join(self.temp_dir, "skill2")
        os.makedirs(skill_dir2)
        skill_file2 = os.path.join(skill_dir2, "SKILL.md")
        with open(skill_file2, "w", encoding="utf-8") as f:
            f.write("""
# Test Skill 2
version: 2.0.0
description: Another test skill

## Dependencies
- requests

## Triggers
- keyword: test2

## Entry Point
main.py:run

## Environment Variables
API_KEY=secret2
""")

        skills = SkillLoader.load_skills_from_directory(self.temp_dir)
        self.assertEqual(len(skills), 1)  # 只加载子目录中的技能

        # 清理
        if os.path.exists(skill_file2):
            os.remove(skill_file2)
        if os.path.exists(skill_dir2):
            os.rmdir(skill_dir2)


if __name__ == "__main__":
    unittest.main()
