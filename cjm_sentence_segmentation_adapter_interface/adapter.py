"""The typed sentence-segmentation task contract — the `SentenceSegmentationAdapter` ABC + the `SentenceSegmentationToolProtocol` structural contract (capability-unit Option C; B.5 work item 81e43606)."""

from abc import abstractmethod
from typing import Any, ClassVar, Dict, Protocol, runtime_checkable

from cjm_capability_primitives.sentence_segmentation import SentenceSegmentationResult
from cjm_substrate.core.adapter import TaskAdapter


# Canonical home (stage 8 / PILLAR 1c): the data noun lives in
# cjm-capability-primitives, so the pure-compute tool depends on it, never on
# this adapter machinery.


@runtime_checkable
class SentenceSegmentationToolProtocol(Protocol):
    """Structural contract for sentence-segmentation tool capabilities.

    Pure compute: `segment_text` reads the original (punctuated) text and
    returns ordered character spans over it. `get_current_config` supplies the
    effective config whose canonical hash joins downstream identity composites
    (the decomp skeleton hash)."""

    def segment_text(self, text: str, **kwargs) -> SentenceSegmentationResult: ...
    def get_current_config(self) -> Dict[str, Any]: ...


class SentenceSegmentationAdapter(TaskAdapter):
    """Typed sentence-segmentation task adapter: original punctuated text in,
    `SentenceSegmentationResult` (ordered char spans over that text) out.

    Input contract: the caller passes the ORIGINAL text whose offsets it needs
    preserved — spans in the result always index into exactly that string
    (a tool that normalizes internally must map spans back).

    Unlike the VAD/FA adapters there are NO cache/persist bookends here:
    rule-based segmentation is deterministic sub-millisecond CPU work with no
    model-load cost to amortize, so a cache DB would cost more than the
    compute it saves. A future model-backed segmenter (wtpsplit/SaT) that
    changes that calculus adds bookends in its own generic adapter revision.

    Implementations run in-worker beside their tool capability and are
    constructed with the bound tool instance: `AdapterClass(tool)`. The result
    DTO is wire-registered ("sentence_segmentation.result"): returned values
    cross the worker boundary typed.
    """

    task_name: ClassVar[str] = "sentence_segmentation"
    required_tool_protocol: ClassVar[type] = SentenceSegmentationToolProtocol

    def __init__(
        self,
        tool: SentenceSegmentationToolProtocol,  # The bound tool capability instance (worker-side binding)
    ):
        self.tool = tool

    @abstractmethod
    def segment_text(
        self,
        text: str,  # The original (punctuated) text to segment
        **kwargs,   # Provenance + tool options
    ) -> SentenceSegmentationResult:  # Ordered sentence spans over `text`
        """Segment text into ordered sentence character spans."""
        ...
