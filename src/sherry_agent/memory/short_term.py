"""Short-term memory implementation for SherryAgent.

This module provides the ShortTermMemory class, which handles short-term memory management
including token estimation and memory compression strategies.
"""

import re
from typing import Any

from ..infrastructure.token_estimator import TokenEstimator


class ShortTermMemory:
    """Short-term memory for SherryAgent.

    This class manages short-term memory with token estimation and compression capabilities.
    """

    def __init__(self, max_tokens: int = 4096, encoding_name: str = "cl100k_base"):
        """Initialize short-term memory.

        Args:
            max_tokens: Maximum number of tokens allowed in short-term memory.
            encoding_name: Name of tiktoken encoding to use for token estimation.
        """
        self.max_tokens = max_tokens
        self.memory_items: list[dict[str, Any]] = []
        self._token_estimator = TokenEstimator(encoding_name=encoding_name)

    def add_item(self, item: dict[str, Any]) -> None:
        """Add an item to short-term memory.

        Args:
            item: Item to add to memory, should contain 'content' key at minimum.
        """
        self.memory_items.append(item)
        self.compact()

    def estimate_tokens(self, text: str) -> int:
        """Estimate the number of tokens in a text.

        Uses TokenEstimator for accurate token counting with tiktoken,
        falling back to heuristic-based estimation when tiktoken is unavailable.

        Args:
            text: Text to estimate token count for.

        Returns:
            Estimated number of tokens.
        """
        return self._token_estimator.estimate(text)

    def get_total_tokens(self) -> int:
        """Get the total number of tokens in short-term memory.

        Returns:
            Total number of tokens in memory.
        """
        total_tokens = 0
        for item in self.memory_items:
            if 'content' in item:
                total_tokens += self.estimate_tokens(item['content'])
        return total_tokens

    def compact(self, level: str = "auto") -> None:
        """Compact short-term memory to stay within token limit.

        Args:
            level: Compression level: "auto", "session", "reactive", "micro"
        """
        max_attempts = 10
        attempts = 0

        while self.get_total_tokens() > self.max_tokens and attempts < max_attempts:
            attempts += 1
            if len(self.memory_items) == 1:
                # Only one item left, compact it based on level
                if level == "auto":
                    self._auto_compact()
                elif level == "session":
                    self._session_compact()
                elif level == "reactive":
                    self._reactive_compact()
                else:
                    self._micro_compact(self.memory_items[0])

                # 即使只有一个项目，也要确保它被充分压缩
                if self.get_total_tokens() > self.max_tokens:
                    # 如果仍然超过限制，使用更激进的压缩
                    self._reactive_compact()
                break
            else:
                # Remove oldest item
                self.memory_items.pop(0)
                # After removing an item, check if we need to compact the remaining items
                if len(self.memory_items) > 0:
                    # Force compaction of the remaining items
                    if level == "auto":
                        self._auto_compact()
                    elif level == "session":
                        self._session_compact()
                    elif level == "reactive":
                        self._reactive_compact()
                    else:
                        for item in self.memory_items:
                            self._micro_compact(item)

        # 再次检查并确保总token数在限制内
        attempts = 0
        while self.get_total_tokens() > self.max_tokens and attempts < max_attempts:
            attempts += 1
            # 如果仍然超过限制，使用最激进的压缩
            self._reactive_compact()
            # 如果只有一个项目且仍然超过限制，再次压缩
            if len(self.memory_items) == 1:
                # 进一步缩短内容
                item = self.memory_items[0]
                if 'content' in item:
                    # 只保留前50个字符
                    content = item['content'][:50] + '...'
                    item['content'] = content

        # 如果仍然超过限制，清空所有记忆
        if self.get_total_tokens() > self.max_tokens:
            self.clear()

    def _auto_compact(self) -> None:
        """Apply auto-compact strategy using LLM summary.

        This strategy uses a simulated LLM to create a concise summary of memory items.
        """
        if not self.memory_items:
            return

        # Simulate LLM summary
        content_list = [item.get('content', '') for item in self.memory_items]
        combined_content = ' '.join(content_list)

        # Create a summary (simulating LLM output)
        summary = f"Summary of recent interactions: {combined_content[:200]}..."

        # Replace all memory items with the summary
        self.memory_items = [{
            'content': summary,
            'compressed': True,
            'strategy': 'auto-compact'
        }]

    def _session_compact(self) -> None:
        """Apply session memory compact strategy with structured extraction.

        This strategy extracts key information and structures it for better recall.
        """
        if not self.memory_items:
            return

        # Extract key information from each item
        structured_items = []
        for item in self.memory_items:
            content = item.get('content', '')
            # Extract key points (simulated structured extraction)
            key_points = re.findall(r'\b(important|key|main|critical|essential)\b.*?(?=\.|$)', content, re.IGNORECASE)
            if key_points:
                structured_items.append({
                    'content': f"Key points: {', '.join(key_points)}",
                    'compressed': True,
                    'strategy': 'session-compact'
                })

        # If we extracted structured items, use them; otherwise use micro-compact
        if structured_items:
            self.memory_items = structured_items
        else:
            for item in self.memory_items:
                self._micro_compact(item)

    def _reactive_compact(self) -> None:
        """Apply reactive compact strategy with aggressive compression.

        This strategy aggressively compresses memory to free up space quickly.
        """
        if not self.memory_items:
            return

        # Keep only the most recent item and aggressively compress it
        if len(self.memory_items) > 1:
            self.memory_items = self.memory_items[-1:]

        # Aggressively compress the remaining item
        item = self.memory_items[0]
        if 'content' in item:
            content = item['content']
            # Keep only first 100 characters
            content = content[:100] + '...'
            item['content'] = content
            item['compressed'] = True
            item['strategy'] = 'reactive-compact'

    def _micro_compact(self, item: dict[str, Any]) -> None:
        """Apply micro-compact strategy to a single memory item.

        Args:
            item: Memory item to compact.
        """
        if 'content' in item:
            content = item['content']
            # Remove extra whitespace
            content = re.sub(r'\s+', ' ', content)
            # Remove redundant phrases
            redundant_phrases = [
                'in conclusion', 'to summarize', 'I think', 'you know',
                'basically', 'actually', 'really', 'very much'
            ]
            for phrase in redundant_phrases:
                content = content.replace(f' {phrase} ', ' ')
                content = content.replace(f' {phrase}.', '.')
            # Truncate long sentences
            sentences = content.split('. ')
            if len(sentences) > 3:
                # Keep first and last sentences, summarize middle
                content = '. '.join(sentences[:1] + ['...'] + sentences[-1:])
            item['content'] = content
            item['compressed'] = True

    def get_memory(self) -> list[dict[str, Any]]:
        """Get the current short-term memory items.

        Returns:
            List of memory items.
        """
        return self.memory_items

    def clear(self) -> None:
        """Clear all short-term memory."""
        self.memory_items = []
