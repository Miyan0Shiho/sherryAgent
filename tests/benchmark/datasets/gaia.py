
"""GAIA dataset loader for benchmarking."""

from __future__ import annotations

import logging
from collections.abc import Iterator
from dataclasses import dataclass
from enum import IntEnum
from pathlib import Path

try:
    from datasets import load_dataset  # type: ignore[import-untyped]
    HAS_DATASETS = True
except ImportError:
    HAS_DATASETS = False

logger = logging.getLogger(__name__)


class GaiaLevel(IntEnum):
    """GAIA difficulty levels."""
    LEVEL_1 = 1
    LEVEL_2 = 2
    LEVEL_3 = 3


@dataclass
class GaiaTestCase:
    """Standardized GAIA test case format."""
    id: str
    task: str
    level: GaiaLevel
    expected_answer: str
    file_ref: str | None = None


class GaiaDatasetLoader:
    """
    GAIA dataset loader for benchmarking.

    Loads the GAIA dataset from Hugging Face and provides
    standardized test cases with difficulty filtering.
    """

    DATASET_NAME = "gaia-benchmark/GAIA"
    DEFAULT_CACHE_DIR = Path.home() / ".cache" / "sherry_agent" / "datasets"

    def __init__(
        self,
        cache_dir: Path | None = None,
        split: str = "validation",
    ):
        """
        Initialize the GAIA dataset loader.

        Args:
            cache_dir: Directory to cache the downloaded dataset
            split: Which split to load (train/validation/test)
        """
        if not HAS_DATASETS:
            raise ImportError(
                "The 'datasets' library is required to use GaiaDatasetLoader. "
                "Install it with: uv add datasets"
            )

        self.cache_dir = cache_dir or self.DEFAULT_CACHE_DIR
        self.split = split
        self._dataset: object | None = None

    def download(self, force: bool = False) -> None:
        """
        Download the GAIA dataset.

        Args:
            force: Force re-download even if cached
        """
        logger.info(f"Downloading GAIA dataset (split: {self.split})")
        self._dataset = load_dataset(
            self.DATASET_NAME,
            split=self.split,
            cache_dir=str(self.cache_dir),
            download_mode="force_redownload" if force else None,
        )
        if self._dataset is not None:
            logger.info(f"Downloaded {len(self._dataset)} test cases")  # type: ignore[arg-type]

    def load(self) -> None:
        """Load the dataset if not already loaded."""
        if self._dataset is None:
            self.download()

    def get_all_cases(self) -> Iterator[GaiaTestCase]:
        """
        Get all test cases from the dataset.

        Yields:
            GaiaTestCase objects
        """
        self.load()

        if self._dataset is not None:
            for item in self._dataset:  # type: ignore[attr-defined]
                yield self._convert_to_test_case(item)

    def get_cases_by_level(
        self,
        level: GaiaLevel,
    ) -> Iterator[GaiaTestCase]:
        """
        Get test cases filtered by difficulty level.

        Args:
            level: The difficulty level to filter by

        Yields:
            GaiaTestCase objects matching the level
        """
        for case in self.get_all_cases():
            if case.level == level:
                yield case

    def get_cases_by_levels(
        self,
        levels: list[GaiaLevel],
    ) -> Iterator[GaiaTestCase]:
        """
        Get test cases filtered by multiple difficulty levels.

        Args:
            levels: List of difficulty levels to filter by

        Yields:
            GaiaTestCase objects matching any of the levels
        """
        level_set = set(levels)
        for case in self.get_all_cases():
            if case.level in level_set:
                yield case

    def get_case_by_id(self, case_id: str) -> GaiaTestCase | None:
        """
        Get a specific test case by ID.

        Args:
            case_id: The ID of the test case

        Returns:
            GaiaTestCase if found, None otherwise
        """
        for case in self.get_all_cases():
            if case.id == case_id:
                return case
        return None

    def _convert_to_test_case(self, item: dict[str, object]) -> GaiaTestCase:
        """
        Convert a raw dataset item to a standardized test case.

        Args:
            item: Raw dataset item

        Returns:
            Standardized GaiaTestCase
        """
        level = GaiaLevel(int(item.get("Level", 1)))  # type: ignore[call-overload]

        file_ref = None
        if item.get("file_name"):
            file_ref = str(item["file_name"])

        return GaiaTestCase(
            id=str(item.get("task_id", "")),
            task=str(item.get("Question", "")),
            level=level,
            expected_answer=str(item.get("Final answer", "")),
            file_ref=file_ref,
        )

    def __len__(self) -> int:
        """Return the number of test cases in the dataset."""
        self.load()
        if self._dataset is not None:
            return len(self._dataset)  # type: ignore[arg-type]
        return 0

    def __iter__(self) -> Iterator[GaiaTestCase]:
        """Iterate over all test cases."""
        return self.get_all_cases()

