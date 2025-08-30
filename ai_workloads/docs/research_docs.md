# Hungarian ↔ English Translator Model

## Current State

* **Best open-source baseline**:
  [`Helsinki-NLP/opus-mt-tc-big-en-hu`](https://huggingface.co/Helsinki-NLP/opus-mt-tc-big-en-hu) and `...hu-en`.

  * Strengths: lightweight (\~0.6–1 GB RAM), bilingual, production-ready, widely used (LibreTranslate, LibreOffice).
  * Weaknesses: trained mainly on OPUS (Europarl, subtitles, religious/legal text) → translations are grammatical but stiff, domain-limited, sometimes awkward.

* **Observation in community & research**:
  Many Hungarian researchers and hobbyists (e.g. Telex experiments, MSZNY 2022 paper) fine-tune MarianMT on better corpora.

  * This consistently yields more natural, domain-appropriate translations.
  * Model size isn’t the bottleneck → data quality/diversity is.

---

## Practical Path Forward

### Phase 1: Proof of Concept

* Use the **Marian “tc-big” EN↔HU** model as-is.
* Deploy via CTranslate2 int8 (fast runtime, fits <1 GB RAM).

### Phase 2: Data Collection

* Gather more diverse EN↔HU corpora:

  * **Hunglish2** (research corpus).
  * **Wikimatrix** / Wikipedia translations.
  * **News domain**: Telex, Index, 444.hu (scraped and aligned with EN articles).
  * **Conversational**: subtitles (OpenSubtitles, CCAligned).
  * **In-domain**: custom text (Discord chats, technical docs).
* Preprocess: deduplication, language ID filtering, balancing domains.

### Phase 3: Fine-tuning

* Load base checkpoint `opus-mt-tc-big-en-hu` / `hu-en`.
* Fine-tune with Hugging Face `Seq2SeqTrainer` or MarianNMT toolkit.

  * Small LR (3e-5).
  * Gradient accumulation for 12 GB GPU.
  * Mixed precision (fp16 on ROCm if stable).
* Evaluate with BLEU + chrF (chrF is more reliable for Hungarian morphology).

### Phase 4: Deployment

* Export to **CTranslate2 int8** for CPU inference (<1 GB RAM).
* Wrap in REST API (LibreTranslate-like) for integration with apps/bots.
* Maintain iterative fine-tuning cycles as new data is gathered.

---

## Key Insights

* **MarianMT is already the practical best open-source option for EN↔HU.**
* Its main weakness is **data**, not model architecture.
* **Fine-tuning on richer corpora** gives more benefit than scaling up model size.
* This approach is feasible on **consumer hardware (RX 6700XT, 12 GB)** with careful training setup.
