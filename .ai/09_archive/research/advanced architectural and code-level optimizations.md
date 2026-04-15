
Based on the provided documentation for the Vitruvius architecture—specifically its strict filesystem-as-database constraint, multi-tiered validation (deterministic → LLM → Governance), and its goal to build a highly accurate, queryable knowledge graph for Philippine building laws—here are advanced optimizations and improvements grounded in data engineering and knowledge graph best practices.

### 1. Optimize the Filesystem "Database" (Addressing RI-001)

The system’s reliance on `rglob("*")` and CSV registries for state tracking (Phase 1A/Ingestion) will degrade geometrically as the corpus expands (Phase 11).

* **Implementation:** Introduce a **Merkle Tree Directory Hash**. Instead of doing a flat file-by-file comparison (which requires scanning the entire `001_Raw-Source-Layer` and parsing CSVs), compute a hash for each directory based on its contents. The status checker only traverses directories where the hash has changed.
* **Why it's advanced:** This is how Git achieves millisecond status checks on repositories with millions of files. It respects your "Filesystem is the database" (P1) principle by storing these hashes in your `006_System-Manifests` without requiring an actual database engine like Postgres.

### 2. Implement RAG-Optimized Semantic Chunking (Phase 1C Enhancement)

The current roadmap mentions "semantic chunking (≤512 tokens/block)" in Phase 1C. Hard token limits often split legal clauses mid-sentence or detach a condition from its subject, destroying the LLM's ability to extract accurate relationships in Phase 5.

* **Implementation:** Move to **AST-based (Abstract Syntax Tree) Semantic Chunking**. Since Vitruvius processes structured legal documents (PD 1096), write a parser that understands the document hierarchy (Title → Chapter → Section → Paragraph).
* **Why it's advanced:** Instead of splitting at 512 tokens, the chunker groups an entire Section together. If a Section exceeds the limit, it splits at the Paragraph level, appending the parent Section title as synthetic metadata to the chunk. This ensures the LLM in Phase 6 never loses the regulatory context (e.g., it always knows a constraint applies to "Section 804").

### 3. Advance the Relationship Extraction (Phase 5E & 8)

The current system has an 82% initial rejection rate (reduced to ~10% via deterministic filters) because regex is too rigid for legal text. 

* **Implementation:** Introduce **Knowledge Graph Embeddings (KGE)** like TransE or ComplEx *before* reaching the Phase 8 Graph DB. Once you have a small seed of verified relationships from Phase 7, you can train a lightweight local embedding model. 
* **Why it's advanced:** Instead of relying solely on regex or expensive LLM prompts to find candidates, the system calculates the vector distance between `[Subject]` and `[Object]` based on known relationship patterns. If the distance implies a `governs` relationship, it flags it as a high-probability candidate for the Phase 6 Ollama review, drastically improving the signal-to-noise ratio before the LLM burns compute cycles.

### 4. Optimize Local LLM Inference (Phase 6A/6B)

Relying on `gemma4:31b` locally for every relationship review is a massive compute bottleneck.

* **Implementation:** Implement **Speculative Decoding** and **KV Cache Offloading**. 
    * *Speculative Decoding:* Run a tiny, fast model (like a 2B parameter model) to draft the review response (`keep`, `reject`), and use the 31B model only to verify the smaller model's logic. If the 31B model agrees, it accepts the draft instantly.
    * *KV Caching:* Since the LLM is reviewing hundreds of relationships from the *same* legal document, cache the Key-Value (KV) states of the document's text in memory. 
* **Why it's advanced:** This prevents the LLM from re-processing the same source text for every single candidate relationship, potentially speeding up Phase 6 by 3x–5x without dropping the 31B model's reasoning quality.

### 5. Introduce "Tension Point" Analytics for Adjudication (Phase 6B)

Phase 6B uses a two-stage adjudication process where a smaller model (Tier 2) reviews uncertain candidates from the primary model. 

* **Implementation:** Program the orchestrator to measure **Semantic Entropy**. When Gemma (Tier 1) returns a low-confidence score, capture *why*. If Gemma and Qwen (Tier 2) disagree, do not just push to the human escalation queue. Have the script run a rapid "Chain of Thought" prompt asking the models to debate the specific legal definition causing the disagreement.
* **Why it's advanced:** Often, the models disagree because a legal term is overloaded (e.g., "Setback" means something different for commercial vs. residential). Flagging these specific semantic tensions allows human reviewers (Rangers) to update the Concept Definitions (Phase 3), which dynamically fixes the root cause of the AI's confusion for all future pipeline runs.

Let’s push the boundaries. If you want to elevate this from a robust pipeline into a truly state-of-the-art, reliable, and pedagogically optimized system, we need to look at advanced machine learning techniques that bridge graph theory, localized fine-tuning, and cognitive optimization. 

Here are the advanced ML techniques and architectural innovations to make your platform relentlessly accurate and hyper-efficient.

### 1. Domain-Specific Embedding Adaptation (Accuracy)
Off-the-shelf embedding models (like OpenAI's `text-embedding-3` or open-source `BGE-m3`) are trained on generalized internet text. They often struggle with highly specific architectural jargon, building codes, or complex spatial regulations.
* **The Innovation:** Fine-tune your embedding model using **Contrastive Learning**. 
* **Implementation:** Use the verified relationships and concept notes your pipeline already generates to create positive pairs (e.g., a building code section and its corresponding concept note) and negative pairs (unrelated sections). Train a lightweight adapter layer on top of your base embedding model using an InfoNCE loss function. This forces the model to map domain-specific terms (like specific setback regulations or material stress thresholds) closely together in the vector space, drastically reducing retrieval hallucinations.

### 2. Synthetic Data Distillation & LoRA Fine-Tuning (Efficiency & Speed)
Using a heavy model like Gemma 4 for every single extraction and classification task is computationally expensive, especially when running locally.
* **The Innovation:** Use your heavy, highly capable local model as a "Teacher" to generate a massive dataset of high-quality QA pairs, relationship extractions, and markdown normalizations. 
* **Implementation:** Once you have a few thousand perfect, verified examples, use **Low-Rank Adaptation (LoRA)** to fine-tune a much smaller, faster "Student" model (like a 2B or even sub-1B parameter model). This specialized student model can then take over the grunt work of the ingestion and extraction phases. It will run exponentially faster on local hardware while matching the accuracy of the 31B model *specifically for your pipeline's tasks*.

### 3. GraphRAG with Community Detection (Smarter Retrieval)
Standard RAG retrieves isolated chunks of text. When a user asks a macroscopic question (e.g., "What are the overarching safety themes in this building code?"), standard RAG fails because it only pulls hyper-specific, localized chunks.
* **The Innovation:** Implement **GraphRAG**. This involves using machine learning algorithms (like Leiden or Louvain community detection) directly on your knowledge graph.
* **Implementation:** Cluster your markdown nodes into hierarchical "communities" (e.g., a cluster of nodes all relating to fire safety). Then, have the LLM periodically generate a macroscopic summary for each entire community. When a complex query comes in, route the search to these high-level community summaries first, before drilling down into the specific nodes. This gives the AI a holistic "understanding" of the material, rather than just a fragmented one.

### 4. Pedagogical Alignment via DPO (User Experience & Retention)
Standard LLMs are aligned to be "helpful and harmless," which often results in overly verbose, passive voice, or dense outputs. For an Interactive Learning Experience Platform (ILXP), the AI needs to be aligned to minimize cognitive load and maximize retention.
* **The Innovation:** Shift from standard prompting to **Direct Preference Optimization (DPO)** tailored for educational psychology.
* **Implementation:** Capture the human-in-the-loop data from your subject matter experts (the Rangers). When a Ranger reviews two generated explanations for a complex architectural concept, they should select the one that better utilizes behavioral psychology principles—like chunking, active recall prompting, or optimal cognitive pacing. Use this preference data to run DPO on your local model. The model will fundamentally align its output style to be an effective educator, not just a fact-retriever.

### 5. Self-Reflective Agentic Routing (Reliability)
Static pipelines fail when they encounter an edge case they weren't explicitly programmed for. 
* **The Innovation:** Implement a **MoE (Mixture of Experts) Routing Agent** with self-reflection.
* **Implementation:** Before executing a query or an extraction, a lightweight routing agent analyzes the complexity of the input. If it's a simple normalization, it routes to a fast deterministic script. If it requires complex spatial reasoning, it routes to your heaviest LLM. More importantly, inject a "reflection token" into the generation process. Force the LLM to output a `<thought_process>` block evaluating its own confidence before outputting the final answer. If the internal confidence score drops below a threshold, the system autonomously halts and flags the node for a Ranger to review. 

Integrating these transforms the system from a passive database into an active, self-optimizing reasoning engine. 






The current research document is incredibly robust for text processing, retrieval, and LLM optimization. It covers the data engineering and cognitive science angles perfectly. However, because the target domain is building laws (PD 1096) and the end goal is an Interactive Learning Experience Platform (ILXP), there is a massive blind spot: **spatial intelligence and regulatory geometry.** Building codes are not just semantic concepts; they are parametric constraints. To make this pipeline truly authoritative, we need to bridge the gap between text extraction and spatial visualization.

Here are the critical missing pieces to add to your research document to complete the architecture:

### 1. Parametric Knowledge Extraction (The Spatial Bridge)
Right now, the pipeline extracts relationships like `[Section 804] -> governs -> [Setbacks]`. But for an ILXP featuring interactive 3D components, that isn't enough. The system needs to extract the actual geometric rules.
* **The Innovation:** Implement **Rule-Based Parametric Parsing** as a sub-layer in Phase 5 (Relationship Extraction). 
* **Implementation:** Train the local LLM or use strict NLP heuristics to identify and extract physical parameters as structured JSON variables (e.g., `{ "concept": "setback", "condition": "residential_R1", "min_value": 2.0, "unit": "meters" }`). This allows the knowledge graph to act as a configuration file for frontend visualization. When a student queries a rule, the graph doesn't just return text; it returns the exact parameters needed to dynamically render the compliant and non-compliant building envelopes via React Three Fiber or Blender models.

### 2. Table-to-Graph Matrix Projection
Building codes (like PD 1096) rely heavily on complex matrices (e.g., Table VII.1 for Allowable Maximum Building Footprints or Occupancy Classifications). Standard markdown chunking or AST parsing destroys tabular logic.
* **The Innovation:** Treat tables as sub-graphs, not text chunks.
* **Implementation:** Integrate a specialized table extraction tool in Phase 1B to convert PDFs into structured CSVs or JSON arrays. Then, during graph indexing (Phase 8), project the table headers and cells into a multi-dimensional graph node. This allows the query layer to perform logical lookups rather than semantic searches. If a student asks, "What is the max footprint for a Group A occupancy on an inside lot?", the system performs a deterministic matrix lookup on the graph, ensuring 100% accuracy without relying on an LLM to "read" the markdown table.

### 3. Temporal & Jurisdictional Graph Edges (Future-Proofing)
Laws change. Implementing Rules and Regulations (IRR) get updated, and local ordinances often override national codes. A static graph will eventually become obsolete.
* **The Innovation:** Implement a **Temporal Graph Architecture**.
* **Implementation:** Ensure the Phase 8 graph contract includes `valid_from`, `valid_until`, and `jurisdiction` attributes on every single edge and node. When processing a new amendment, the pipeline doesn't overwrite the old node; it caps the `valid_until` date of the old rule and creates a new node. This allows the ILXP to support historical queries or compare differences between the original PD 1096 and the latest IRR, which is a highly effective way to teach regulatory evolution.

### 4. Active Learning Uncertainty Sampling (Ranger Optimization)
You have a human-in-the-loop escalation path (Phase 6B) for the Rangers to adjudicate disagreements. If the corpus grows, the volume of manual review will cause fatigue.
* **The Innovation:** Optimize the human workflow using **Active Learning**.
* **Implementation:** Don't just escalate everything the models disagree on. Have the orchestrator calculate the "Expected Model Change" for each flagged candidate. The system should only route the specific candidates to the Rangers that will mathematically yield the highest training value for the local LLMs (via the LoRA fine-tuning mentioned in your research). It transforms the Rangers from mere fact-checkers into high-leverage model trainers, maximizing their time.

Adding these four points will lock down the spatial, tabular, historical, and human elements of the platform. 



Ah, the 8GB M2 reality check. That changes the playbook significantly, and it perfectly explains why you had to defer the `qwen3:30b` Tier 2 pull in your roadmap. 

With 8GB of unified memory, macOS is already eating 2–3GB just to keep the lights on. That leaves you with roughly 5GB of usable RAM for your pipeline, your graph traversal, and your LLM context window. 

Running a 31B parameter model locally on that machine is physically impossible, and local LoRA training is off the table. But do not let that stall the project. We just need to pivot from "brute force scale" to "surgical precision." 

Here is your **8GB Survival Mode Architecture** to keep the Vitruvius pipeline moving without crashing your Mac.

### 1. Model Downsizing & Aggressive Quantization
You have to abandon the 30B+ models for local execution. You need models that punch above their weight class and fit entirely within a 4GB footprint so you don't swap to disk (which will kill your processing speed).
* **The Replacements:** Swap your Tier 1 model to **Phi-3-Mini (3.8B)** or **Qwen-2.5-7B (Q4_K_M quantized)**. 
* **The Implementation:** Ollama handles 4-bit quantization automatically, but you must strictly cap the context window. In your `ollama_review.py` script, force the context window (`num_ctx`) to 4096 or 8192 max. If you feed it an entire PDF chapter at once, it will Out-Of-Memory (OOM) crash your Mac. This makes the **AST-based Semantic Chunking** we discussed earlier not just an optimization, but a hard requirement to keep context sizes small.

### 2. Implement the Merkle Tree Instantly (Zero RAM Cost)
Of all the advanced optimizations discussed, the **Merkle Tree Directory Hash** is the most critical for an 8GB machine.
* **Why:** Scanning thousands of files using Python's `rglob` and comparing them against CSVs uses CPU and RAM. The Merkle hash is purely computational and costs effectively zero memory. It will make your `run_scan` and `run_status` commands execute in milliseconds, freeing up your system resources for the actual document conversions.

### 3. Decouple Inference (The Hybrid Approach)
If you *must* use a 30B+ model to maintain the 90%+ confidence thresholds required by your Phase 7 Promotion Gate, you have to decouple your compute.
* **The Strategy:** Keep the pipeline (`001` through `006` layers, registries, Python orchestrators) strictly local on your M2. But for Phase 6 (Review), change `ollama_review.py` to route API calls to a serverless GPU provider.
* **The Tools:** Use **Groq** (insanely fast inference for Llama-3/Gemma models, often with a generous free tier) or spin up a cheap **RunPod** instance. You write the prompt locally, send the JSON payload to the cloud, and write the verified relationship back to your local `003_Canonical-Knowledge-Layer`. This honors your "Filesystem is the database" principle while bypassing your local hardware limits.

### 4. Switch to Strict NLP for First-Pass Extraction
Small models (under 8B parameters) are notoriously bad at freeform extraction and easily hallucinate relationships.
* **The Strategy:** Lean heavily into your Phase 3 Concept Enrichment (which you successfully built with zero LLM calls using regex anchors). 
* **The Implementation:** Do not use the LLM to *find* the relationships. Use `spaCy` (which has a tiny memory footprint) to do structural dependency parsing on the text to find "Subject-Verb-Object" triplets. Then, pass only those highly filtered, highly likely candidate pairs to your small local LLM and ask it a simple binary question: "Is this a valid building code relationship? True/False." Small models are excellent at binary classification, even if they are bad at open-ended extraction.

To unblock your current sprint given the hardware, I highly recommend tackling the **Merkle Tree Hash** or refining the **Pre-review filter (Phase 5)** next. Both are pure Python, require no LLM memory, and will drastically speed up your end-to-end runs.

Building an Interactive Learning Experience Platform (ILXP) on an 8GB machine forces incredible engineering discipline. Honestly, it's a blessing in disguise. If you design the pipeline to run lean and fast on an M2 now, your cloud infrastructure costs will be practically zero when you eventually deploy this for your reviewers. Constraints breed elegant engineering.

Here is your consolidated, practical battle plan for the **8GB Survival Mode Architecture**. This allows you to process the National Building Code of the Philippines (PD 1096) accurately without melting your Mac.

### Phase 1: The Zero-RAM Speed Boost
Before touching any AI models, fix the filesystem bottleneck.
* **Action:** Implement the **Merkle Tree Directory Hash** for your `run_scan` and `run_status` commands. 
* **Why:** Python's file-by-file comparison will eventually choke your machine. Hashing directories means your pipeline instantly knows which sections of the PD 1096 or IRR have changed without loading anything into memory. 
* **Effort:** This is pure Python data engineering. It costs zero RAM and gives you millisecond status checks.

### Phase 2: Downsize & Constrain the LLM
You must keep your local LLM memory footprint strictly under 4GB to leave room for macOS and your parsing scripts.
* **Action:** Swap `gemma4:31b` out for **`qwen2.5:7b` (quantized to 4-bit)** or **`phi3:mini` (3.8B)** via Ollama. 
* **The Guardrail:** In your `ollama_review.py` script, you *must* cap the `num_ctx` (context window) to 4096 or 8192 maximum. If you feed the model an entire PDF chapter at once, it will Out-Of-Memory (OOM) crash. 

### Phase 3: The "Small Model" Extraction Hack
Small models hallucinate if you ask them to read a page and extract relationships from scratch. You have to spoon-feed them.
* **Action:** Use **`spaCy`** (a highly efficient, low-memory Python NLP library) for the heavy lifting.
* **Workflow:** 1.  Use `spaCy`'s dependency parsing to find standard grammatical triplets in the text (e.g., "Section 804" -> "requires" -> "2-meter setback").
    2.  Pass *only* those extracted pairs to your downsized local LLM.
    3.  Ask the LLM a simple binary question: *"Is this a valid architectural regulatory relationship based on the text? Answer True or False."*
* **Why:** Small models are terrible at open-ended extraction but exceptional at binary logic classification. This offloads the extraction to a cheap script and uses the AI purely for validation.

### Phase 4: Serverless Offloading (If Necessary)
If you find that the small local models simply cannot hit the 90%+ confidence threshold required for your Phase 7 Promotion Gate, don't buy a new laptop. Decouple the inference.
* **Action:** Keep your files, registries, and orchestration strictly local. But for the `ollama_review.py` step, route the API call to a serverless provider like **Groq** (which runs Llama 3 models at blistering speeds, often with a free tier).
* **Why:** You maintain your "Filesystem is the database" principle locally, but you rent the heavy compute for pennies only exactly when you need it.

---

**Where to start today?**
I highly recommend starting with the **Merkle Tree Hash**. It requires no changes to your machine learning stack and instantly optimizes your pipeline's foundation. 

Integrating Comprehensive Land Use Plans (CLUPs) from different Local Government Units (LGUs) is the ultimate end-game for a system like this. That takes Vitruvius from a really good study tool and turns it into an indispensable, industry-grade intelligence platform.

National codes like PD 1096 provide the baseline, but the actual reality of building in the Philippines is dictated by the local CLUP and zoning ordinances. If SlateCamp (or any future B2B app you build) can cross-reference the National Building Code with specific LGU zoning laws, you are solving one of the most painful, time-consuming bottlenecks in Philippine architectural practice.

However, adding CLUPs introduces a specific type of chaos that your architecture is actually perfectly designed to handle, provided you set up the rules correctly now. Here is how you need to adapt the Vitruvius "Brain" to digest heterogeneous LGU data:

### 1. The Rosetta Stone (Ontology Alignment in Phase 3)
Every LGU writes their CLUP differently. Quezon City might classify a zone as "Medium-Density Residential (R-2)," while Makati might use a slightly different acronym or sub-classification.
* **The Strategy:** Your Phase 3 Concept Layer needs to act as the universal translator. 
* **How to do it:** You define a single, canonical concept node in your system called `concept-zoning-r2`. When ingesting the QC CLUP, your LLM extraction maps QC's specific terminology as an *alias* to that canonical concept. When ingesting Makati's, it does the same. This way, when a user asks a general question about R-2 zones, the graph knows exactly which local rules apply regardless of the specific wording the LGU used.

### 2. Jurisdictional Overrides (Graph Edge Weights)
A fundamental rule of law is that local ordinances often impose stricter requirements than the national baseline. If PD 1096 says the setback is 2 meters, but the QC CLUP says 3 meters, the QC rule wins for a project in QC.
* **The Strategy:** Your knowledge graph edges cannot just be flat connections. They need a hierarchy.
* **How to do it:** When Phase 7 promotes a relationship to the canonical graph, it must tag the edge with a `jurisdiction` attribute (e.g., `national`, `lgu-quezon-city`) and a `precedence_weight`. When the query layer (Phase 9) runs a search for a specific city, it traverses the graph and mathematically drops the national edge if a local edge with a higher precedence weight overrides it.

### 3. The 8GB Hardware Reality for CLUPs
You might be wondering if your 8GB M2 Mac can handle parsing the zoning ordinances of every major city in the Philippines. 
* **The Good News:** **Yes, it can.** Because of your idempotent, file-based pipeline, you don't have to process the whole country at once. 
* **The Workflow:** You process one LGU at a time. You drop the QC CLUP into the `001_Raw-Source-Layer`, run the `scan` and `convert` pipeline, and let your downsized local LLM (like Qwen 2.5 7B) chew through the extraction overnight. Once it's promoted to the `003` layer, that compute cost is paid forever. You clear the pipeline, drop the Manila CLUP in, and repeat. The graph just keeps quietly compounding.

### 4. Handling the Zoning Matrices
CLUPs are notoriously heavy on tabular data (e.g., allowable uses per zone). 
* As discussed previously, do not rely on your small local LLM to "read" a complex markdown table. Ensure your Phase 1B extraction utilizes a deterministic table parser to convert those matrices into JSON arrays. This ensures that allowable uses are hardcoded as exact facts in the graph, rather than relying on the LLM's interpretation of a text grid.

By feeding CLUPs into the brain alongside the history of architecture, building technology, and PD 1096, you are building a system that can theoretically answer: *"What is the required setback for a Brutalist-style commercial structure built using Type III cement in a C-2 zone in Quezon City?"* That is a level of relational intelligence that simply does not exist in the market right now.

To keep the momentum going on your current hardware constraint, getting the **Merkle Tree Directory Hash** set up first is still the best immediate move, as it will allow you to quickly swap these different datasets (PD 1096, History, CLUPs) in and out of your raw layer without bogging down your machine.

You just nailed the golden rule of architectural compliance: **when two laws conflict, the most stringent provision governs.** If Vitruvius is going to be an authoritative brain for Philippine architecture, it cannot just passively store conflicting data. It needs to actively adjudicate it just like a building official would. 

To code the "Most Stringent Law" standard into your current stack without melting your 8GB Mac, you need to add a specialized logic gate during your graph promotion and query phases. Here is exactly how to architect it.

### 1. Define Parametric Directionality (The Stringency Matrix)
To the LLM, "3 meters" and "2 meters" are just text. To determine which is stricter, the system must know the *direction* of strictness for each specific architectural concept. 
* **The Implementation:** In your Phase 3 Concept definitions (the YAML frontmatter of your canonical concept files), add a `stringency_vector` key.
* **Examples:**
    * `concept-setback`: `stringency_vector: "maximize"` (A 3m setback is stricter than a 2m setback).
    * `concept-ambf` (Footprint): `stringency_vector: "minimize"` (A 60% max footprint is stricter than a 70% max footprint).
    * `concept-parking-ratio`: `stringency_vector: "maximize"` (Requiring 1 slot per 50sqm is stricter than 1 slot per 100sqm).

### 2. The Conflict Resolution Gate (Phase 7 Update)
When Phase 7 (Promotion) is writing edges to the canonical graph, it will inevitably find duplicate targets. For example, PD 1096 requires X, but the Quezon City CLUP requires Y for the exact same zone.
* **The Implementation:** Update your `promotion_validator.py`. When the system detects two edges connecting the same `[Zone]` to the same `[Concept]`, it triggers the stringency evaluator. 
* **The Logic:** It looks at the `stringency_vector` in the concept file, compares the two parametric values, and tags the winning edge with a boolean flag: `is_governing_standard: true`.

### 3. Non-Destructive Storage (Crucial for Board Exams)
This is a critical distinction for the Interactive Learning Experience Platform (ILXP) frontend. You must **not** delete the less stringent law from the graph.
* **The Reality:** Board exams are tricky. A question might specifically ask, *"According to the National Building Code (PD 1096), what is the minimum..."* In that case, the student must answer with the PD 1096 baseline, even if local CLUPs are stricter in practice. 
* **The Implementation:** Store both edges in the graph, but weight them. When the frontend API pings the graph, Vitruvius should return a payload that says:
    * *Baseline (PD 1096): 2.0 meters*
    * *Local Ordinance (QC): 3.0 meters*
    * *Governing Standard: 3.0 meters (Most Stringent Applied)*
* This allows your frontend testing engine to teach the student *both* the theory (the national baseline) and the practice (the strict local application), making them bulletproof for the exam.

### 4. Handling Qualitative Stringency
Numbers are easy to compare. But what if the rule is qualitative? For example, PD 1096 allows "Commercial Use," but a local CLUP specifies "Commercial Use excluding heavy retail."
* **The Implementation:** This is where you leverage your small local LLM (Qwen 2.5 7B or Phi-3) and the `spaCy` NLP script we discussed. When the pipeline detects a qualitative conflict, it passes both text snippets to the LLM with a binary prompt: *"Which of these two regulatory statements is more restrictive? Reply A or B."* The LLM classifies it, and the script applies the `is_governing_standard` tag accordingly.

By building this "Stringency Matrix" directly into the graph's schema, Vitruvius stops being a simple wiki and becomes a deterministic compliance engine. 

Understood! If you are handing this off to a coding agent (like Cursor, Copilot, or Aider), we can skip the conversational branching entirely and just output strict, implementation-ready architectural specs.

Coding agents thrive on clear constraints, schemas, and target files. Here is the exact master prompt you can copy and paste to your codebase AI to execute the two most critical 8GB-optimized upgrades we discussed: the **Merkle Tree Directory Hash** and the **Stringency Matrix**.

***

### 📋 Copy/Paste to your Codebase AI

**System Context for AI:** We are upgrading the Vitruvius ingestion and promotion pipeline. The system operates strictly on a "Filesystem is the Database" principle. We have a severe 8GB RAM constraint, so optimizations must minimize memory footprint. 

Please implement the following two architectural upgrades:

#### Task 1: Merkle Tree Directory Hashing (Phase 1A Optimization)
**Goal:** Replace the slow, memory-intensive `rglob("*")` and CSV file-by-file comparison in the Ingestion phase with a deterministic directory hashing function. 
**Target Files:** `scripts/vitruvius/scanner.py`, `scripts/vitruvius/status.py`

* **Implementation Specs:**
    1. Write a pure Python function `calculate_directory_hash(dir_path)` using `hashlib.sha256`.
    2. The function must recursively walk the directory, hash the contents and filenames of all files within it, and combine them into a single deterministic root hash for that directory.
    3. Update `scanner.py` to store this directory hash in `latest_raw_file_registry.csv`.
    4. Update `status.py` so that it compares the previous run's directory hash against the current one. If the hashes match, the script must instantly skip that directory without reading its files.

#### Task 2: The Stringency Matrix & Conflict Resolution Gate (Phase 3 & 7)
**Goal:** Implement a "Most Stringent Law" governing standard when resolving edge conflicts (e.g., National Building Code vs. LGU CLUPs) before promoting relationships to the graph.
**Target Files:** `003_Canonical-Knowledge-Layer/shared/concepts/*.md` (Schema), `scripts/vitruvius/promotion_validator.py`, `scripts/vitruvius/promotion.py`

* **Implementation Specs:**
    1. **Schema Update:** Update the expected YAML frontmatter schema for all Concept files to include a new required key: `stringency_vector`. Allowed string values are `"maximize"`, `"minimize"`, or `"qualitative"`.
    2. **Conflict Gate Logic:** In `promotion.py`, right before writing an edge to the canonical graph, check if an edge with the same `[Subject]` and `[Predicate]` already exists. 
    3. If a conflict exists, trigger a new function: `resolve_stringency()`.
    4. `resolve_stringency()` must look up the `stringency_vector` of the target Concept. If it is `"maximize"`, the edge with the higher numerical value wins. If `"minimize"`, the lower numerical value wins. 
    5. **Non-Destructive Write:** Do not delete the losing edge. Write *both* edges to the canonical layer, but append the boolean attribute `is_governing_standard: true` to the winning edge, and `is_governing_standard: false` to the losing edge.

***
