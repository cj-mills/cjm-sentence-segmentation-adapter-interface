"""Tests for the sentence-segmentation adapter interface — protocol conformance + the generic pass-through."""
from typing import Any, Dict

from cjm_capability_primitives.sentence_segmentation import (SentenceSegmentationResult,
                                                             SentenceSpan)
from cjm_sentence_segmentation_adapter_interface.adapter import (
    SentenceSegmentationAdapter, SentenceSegmentationToolProtocol)
from cjm_sentence_segmentation_adapter_interface.generic import (
    GenericSentenceSegmentationAdapter)


class FakeSegmenterTool:
    """Minimal tool satisfying the structural protocol: splits on '. '."""

    def __init__(self):
        self.calls = 0

    def segment_text(self, text: str, **kwargs) -> SentenceSegmentationResult:
        self.calls += 1
        spans, start = [], 0
        while start < len(text):
            end = text.find(". ", start)
            end = len(text) if end < 0 else end + 1
            spans.append(SentenceSpan(start_char=start, end_char=end))
            start = end + 1
        return SentenceSegmentationResult(spans=spans,
                                          metadata={"sentence_count": len(spans)})

    def get_current_config(self) -> Dict[str, Any]:
        return {"language": "en"}


def test_fake_tool_satisfies_protocol():
    assert isinstance(FakeSegmenterTool(), SentenceSegmentationToolProtocol)


def test_adapter_declares_task_contract():
    assert SentenceSegmentationAdapter.task_name == "sentence_segmentation"
    assert (SentenceSegmentationAdapter.required_tool_protocol
            is SentenceSegmentationToolProtocol)


def test_generic_adapter_passes_through():
    tool = FakeSegmenterTool()
    adapter = GenericSentenceSegmentationAdapter(tool)
    text = "First sentence. Second one?"
    result = adapter.segment_text(text)
    assert tool.calls == 1
    assert [text[s.start_char:s.end_char] for s in result.spans] == [
        "First sentence.", "Second one?"]
