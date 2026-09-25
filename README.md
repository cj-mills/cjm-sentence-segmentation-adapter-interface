# cjm-sentence-segmentation-adapter-interface

<!-- generated from the context graph by `cjm-context-graph readme` — do not edit by hand; edit the graph (the urge to hand-edit = move it on-graph) -->

Typed sentence-segmentation task-adapter interface for the cjm-substrate runtime. The task noun: segment_text(text) -> ordered (start_char, end_char) sentence spans over the ORIGINAL punctuated text — callers (the transcript decomposition pipeline's sentence-split stage) map sentence boundaries onto forced-alignment word spans, then onto word-gap cut times, so preserving the caller's character offsets is the whole contract. Ships the SentenceSegmentationToolProtocol structural contract, the SentenceSegmentationAdapter ABC (task_name sentence_segmentation), and the deliberately bookend-free GenericSentenceSegmentationAdapter (rule-based segmentation is deterministic sub-millisecond CPU work — no cache DB, unlike the VAD/FA generic adapters). The SentenceSpan/SentenceSegmentationResult data nouns live in cjm-capability-primitives (wire kind sentence_segmentation.result). First adapter: cjm-capability-pysbd; wtpsplit/SaT is the planned second if unpunctuated transcriber output creates demand.

## Modules

- **`cjm_sentence_segmentation_adapter_interface.__init__`**
- **`cjm_sentence_segmentation_adapter_interface.adapter`** — The typed sentence-segmentation task contract — the `SentenceSegmentationAdapter` ABC + the `SentenceSegmentationToolProtocol` structural contract (capability-unit Option C; B.5 work item 81e43606).
- **`cjm_sentence_segmentation_adapter_interface.generic`** — The generic (tool-agnostic) sentence-segmentation adapter — a thin typed pass-through to the bound tool's pure-compute `segment_text`. Reused across every tool capability satisfying `SentenceSegmentationToolProtocol`, exactly as `GenericVADAdapter` is reused across VAD tools.

## API

### `cjm_sentence_segmentation_adapter_interface.adapter`

- `SentenceSegmentationAdapter` _class_ — Typed sentence-segmentation task adapter: original punctuated text in,
- `SentenceSegmentationToolProtocol` _class_ — Structural contract for sentence-segmentation tool capabilities.

### `cjm_sentence_segmentation_adapter_interface.generic`

- `GenericSentenceSegmentationAdapter` _class_ — Generic sentence-segmentation adapter: invoke the pure-compute tool.

## Dependencies

**Depends on:** `cjm-capability-primitives`, `cjm-substrate`
**Used by:** `cjm-capability-pysbd`
