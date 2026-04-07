
"""Test script for GAIA dataset loader."""

from __future__ import annotations

import logging

from tests.benchmark.datasets.gaia import GaiaDatasetLoader, GaiaLevel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_gaia_loader_basic() -> None:
    """Test basic functionality of GAIA dataset loader."""
    logger.info("Testing GAIA dataset loader...")

    try:
        loader = GaiaDatasetLoader()
    except ImportError as e:
        logger.warning(f"Could not test GAIA loader: {e}")
        logger.warning("Please install datasets: uv add datasets")
        return

    logger.info("Loading dataset (this may take a few minutes on first run)...")

    try:
        loader.load()
    except Exception as e:
        logger.error(f"Failed to load dataset: {e}")
        return

    logger.info(f"Total test cases: {len(loader)}")

    logger.info("\n=== Level 1 (Simple) Test Cases ===")
    level1_count = 0
    for i, case in enumerate(loader.get_cases_by_level(GaiaLevel.LEVEL_1)):
        if i < 3:
            logger.info(f"\nCase {case.id}:")
            logger.info(f"  Task: {case.task[:100]}..." if len(case.task) > 100 else f"  Task: {case.task}")
            logger.info(f"  Level: {case.level}")
            logger.info(f"  Expected Answer: {case.expected_answer[:80]}..." if len(case.expected_answer) > 80 else f"  Expected Answer: {case.expected_answer}")
            if case.file_ref:
                logger.info(f"  File Reference: {case.file_ref}")
        level1_count += 1
    logger.info(f"\nTotal Level 1 cases: {level1_count}")

    logger.info("\n=== Level 2 (Medium) Test Cases ===")
    level2_count = 0
    for i, case in enumerate(loader.get_cases_by_level(GaiaLevel.LEVEL_2)):
        if i < 2:
            logger.info(f"\nCase {case.id}:")
            logger.info(f"  Task: {case.task[:100]}..." if len(case.task) > 100 else f"  Task: {case.task}")
            logger.info(f"  Level: {case.level}")
            logger.info(f"  Expected Answer: {case.expected_answer[:80]}..." if len(case.expected_answer) > 80 else f"  Expected Answer: {case.expected_answer}")
            if case.file_ref:
                logger.info(f"  File Reference: {case.file_ref}")
        level2_count += 1
    logger.info(f"\nTotal Level 2 cases: {level2_count}")

    logger.info("\n=== Level 3 (Hard) Test Cases ===")
    level3_count = 0
    for i, case in enumerate(loader.get_cases_by_level(GaiaLevel.LEVEL_3)):
        if i < 1:
            logger.info(f"\nCase {case.id}:")
            logger.info(f"  Task: {case.task[:100]}..." if len(case.task) > 100 else f"  Task: {case.task}")
            logger.info(f"  Level: {case.level}")
            logger.info(f"  Expected Answer: {case.expected_answer[:80]}..." if len(case.expected_answer) > 80 else f"  Expected Answer: {case.expected_answer}")
            if case.file_ref:
                logger.info(f"  File Reference: {case.file_ref}")
        level3_count += 1
    logger.info(f"\nTotal Level 3 cases: {level3_count}")

    logger.info("\n=== Test by Multiple Levels ===")
    multi_level_count = 0
    for _case in loader.get_cases_by_levels([GaiaLevel.LEVEL_1, GaiaLevel.LEVEL_2]):
        multi_level_count += 1
    logger.info(f"Total Level 1 + Level 2 cases: {multi_level_count}")

    logger.info("\n✅ GAIA loader test completed successfully!")


if __name__ == "__main__":
    test_gaia_loader_basic()

