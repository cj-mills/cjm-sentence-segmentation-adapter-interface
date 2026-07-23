"""The generic (tool-agnostic) sentence-segmentation adapter — a thin typed pass-through to the bound tool's pure-compute `segment_text`. Reused across every tool capability satisfying `SentenceSegmentationToolProtocol`, exactly as `GenericVADAdapter` is reused across VAD tools."""

from cjm_capability_primitives.sentence_segmentation import SentenceSegmentationResult

from .adapter import SentenceSegmentationAdapter


class GenericSentenceSegmentationAdapter(SentenceSegmentationAdapter):
    """Generic sentence-segmentation adapter: invoke the pure-compute tool.

    Works against ANY tool satisfying `SentenceSegmentationToolProtocol`.
    Deliberately bookend-free (no cache DB, no force control): rule-based
    segmentation is deterministic and cheaper than a cache lookup, and the
    caller (the decomp pipeline) already folds the result into its own
    persisted skeleton identity. If a model-backed segmenter ever makes
    caching worthwhile, the bookends land here without touching any tool.
    """

    def segment_text(
        self,
        text: str,  # The original (punctuated) text to segment
        **kwargs,   # Provenance + tool options
    ) -> SentenceSegmentationResult:  # Ordered sentence spans over `text`
        """Invoke the bound tool's pure-compute `segment_text`."""
        return self.tool.segment_text(text, **kwargs)
