# Comparable systems, research and frameworks for a controlled Socratic math tutor

Compiled 2026-10-06. Scope: open-source projects, products and research (2023-2026, plus classic ITS foundations) relevant to our pipeline:

> DIAGNOSIS (LLM -> structured JSON: steps done, common errors, intent, disorientation) -> POLICY (deterministic Python: action + hint level 1-4 for the next unfinished step, from an authored sheet) -> REPLY (LLM sees only policy-allowed content) -> GUARD (regex leak checks + LLM judge, up to 3 rewrites, then authored fallback). Plus a "find the error" mode with LLM-generated worked solutions containing planted, independently verified errors.

Conventions: every claim carries a link. "Reported" numbers are as stated by the authors/summaries; anything I could not verify against the primary source is marked *(unverified detail)*. Two naming corrections to the brief: **StratL** (Puech et al.) and **"Stepwise verification and remediation"** (Daheim et al.) are two different ETH papers; **MWPTutor** is the system in "AutoTutor meets Large Language Models". Both are covered separately below.

---

## Part A. Per-project analysis

### A1. Classic ITS foundations

#### AutoTutor and Expectation-Misconception Tailored (EMT) dialogue
- **What**: Natural-language conversational tutor (Graesser et al., Univ. of Memphis, since late 1990s). Links: [AutoTutor: a tutor with dialogue in natural language](https://digitalcommons.memphis.edu/facpubs/7458), [AutoTutor's coverage of expectations](https://digitalcommons.memphis.edu/facpubs/7460), [FLAIRS 2005 paper](https://cdn.aaai.org/FLAIRS/2005/Flairs05-085.pdf), [overview notes](https://notes.andymatuschak.org/AutoTutor).
- **Architecture**: each question has an authored list of **expectations** (good-answer components) and **misconceptions**; the dialogue goal is to get the student to cover all expectations and correct misconceptions ([source](https://notes.andymatuschak.org/AutoTutor)). Student coverage was historically matched with LSA/regex semantic matching.
- **Graduated hints**: canonical **pump -> hint -> prompt -> assertion** ladder: pump asks for the next step; hint is triggered only if the student fails; prompt pushes closer without revealing; assertion gives the answer ([summary in MWPTutor paper](https://arxiv.org/pdf/2402.09216)).
- **Leak prevention / determinism**: entirely authored; the system can only say what is scripted.
- **Adopt**: our sheet (steps + common errors + Socratic questions) is essentially an EMT script; our hint levels 1-4 map directly onto pump/hint/prompt/assertion. Use this vocabulary in docs and evaluation so results are comparable with the literature.
- **Avoid**: brittle semantic matching of coverage (LSA era). Our LLM diagnosis is the modern replacement, but must be audited (see A3 "Stepwise verification" and A6 "LLMs cannot spot math errors").

#### Cognitive Tutors / CTAT (model tracing + knowledge tracing)
- **What**: Carnegie Mellon's Cognitive Tutors and the Cognitive Tutor Authoring Tools ([CTAT](https://ctat.pact.cs.cmu.edu/)). Model tracing matches each student step against a production-rule or example-tracing model; Bayesian Knowledge Tracing (BKT) estimates per-skill mastery.
- **Graduated hints**: per-step **hint ladders** ending in a **bottom-out hint** that gives the step. Known failure: students "game the system" by clicking through hints to the bottom-out hint ([LearnLab wiki: help abuse](https://learnlab.org/research/wiki/index.php/Help_abuse)). Aleven & Koedinger studied this help-seeking behaviour; a "try first, then hint, then self-explain the hint" metacognitive strategy improved learning ([summary](https://learnlab.org/research/wiki/index.php/Help_abuse), [cognitive-science paper on help-seeking](https://journalpub.escholarship.org/cognitivesciencesociety/article/28865/galley/18736/download)).
- **Determinism**: total; every step and hint is authored, correctness is checked by the model (or CAS-like matchers), not by a language model.
- **Adopt**: (1) step-level correctness checked by a formal matcher rather than judgement; (2) explicit anti-gaming rules on hint escalation; (3) knowledge components (KCs) tagged on each step/error to support knowledge tracing across exercises.
- **Avoid**: CTAT-level authoring cost (estimates in the literature are many hours per instructional hour). Our offline sheets are lighter; keep them that way and semi-automate (see Ruffle&Riley, MWPTutor cached).

#### OATutor (Open Adaptive Tutor, UC Berkeley CAHLR)
- **What**: first free, open-source adaptive ITS designed for rapid experimentation (CHI 2023). Repo: [CAHLR/OATutor](https://github.com/CAHLR/OATutor) (MIT, ~264 stars). Overview: [Never Work in Theory](https://neverworkintheory.org/2023/05/07/open-source-adaptive-tutoring-system.html), [KTH tutorial](https://www.digitalfutures.kth.se/event/tutorial-introducing-an-open-source-adaptive-tutoring-system-to-accelerate-learning-sciences-experimentation/).
- **Architecture**: content = Problems -> Steps -> **hint pathways** (hints, interactive scaffolds, bottom-out solution); BKT parameters (`probMastery`, `probTransit`, `probSlip`, `probGuess`) per KC in `bktParams.json`; BKT-driven mastery-based problem selection; A/B testing framework; LTI ([repo](https://github.com/CAHLR/OATutor)).
- **LLM use**: can interface with ChatGPT for hint generation ([KTH](https://www.digitalfutures.kth.se/event/tutorial-introducing-an-open-source-adaptive-tutoring-system-to-accelerate-learning-sciences-experimentation/)); the same group ran learning-gain RCTs of ChatGPT vs human hints: first study, human hints significantly better ([arXiv 2302.06871](https://arxiv.org/abs/2302.06871)); larger follow-up (N=274) found equivalent gains once **self-consistency** reduced hint errors from 32% to ~0% on algebra and 13% on statistics ([Stanford SCALE summary](https://scale.stanford.edu/publications/chatgpt-generated-help-produces-learning-gains-equivalent-human-tutor-authored-help)).
- **Adopt**: (1) its JSON content schema is a good reference for formalising our sheets (step -> hint pathway -> scaffold); (2) BKT over KCs is a cheap, interpretable learner model; (3) self-consistency (sample N, keep agreeing answers) as a cheap accuracy booster for generated content, e.g. in the find-the-error generator.
- **Avoid**: purely click-based hints give no diagnosis of free-text reasoning; that is our advantage.

#### TutorGym (Georgia Tech, AIED 2025)
- **What**: testbed that puts AI agents inside existing ITSs (CTAT, Apprentice Tutors, OATutor; 223 domains) and asks them, at each step, what they would do as tutor or learner ([arXiv 2505.01563](https://arxiv.org/abs/2505.01563), [lab page](https://tail.cc.gatech.edu/publications/weitekamp-aied-2025)).
- **Findings**: current LLMs were poor tutors at step level: **none better than chance at labelling incorrect actions**, next-step correctness only ~52-70% ([arXiv](https://arxiv.org/pdf/2505.01563)).
- **Adopt**: strong evidence that step correctness should not be left to raw LLM judgement. Supports CAS checking in our DIAGNOSIS.

---

### A2. LLM tutors with explicit state machines / strategy control (closest to our design)

#### MWPTutor ("AutoTutor meets Large Language Models", Learning@Scale 2024)
- **Link**: [arXiv 2402.09216](https://arxiv.org/abs/2402.09216), [HTML v3](https://arxiv.org/html/2402.09216v3).
- **Architecture**: a **finite state transducer** whose state space is the cross-product of (a) a **solution-step space** (problem decomposed into single-calculation steps; steps form a tree allowing alternative paths) and (b) a **strategy space** pump -> hint -> prompt -> assertion. LLMs only "fill in" the states ([HTML](https://arxiv.org/html/2402.09216v3)).
- **Leakage prevention**: hints may not mention arithmetic operations or output the RHS of the step equation; prompts must avoid the calculation answer; every generated utterance is checked and **resampled until checks pass**; only the assertion state reveals the number ([HTML](https://arxiv.org/html/2402.09216v3)).
- **Two variants**: *cached* (all utterances pre-generated at design time and checked; no LLM at runtime) vs *live* (LLM at runtime with dialogue context). Live was better: cached hints were redundant about a third of the time because they ignore context ([HTML](https://arxiv.org/html/2402.09216v3)).
- **Evaluation**: simulated/human-in-the-loop study on MultiArith and MathDial problems; metrics **success rate**, **telling rate** (tutor revealed the answer before the student), combined **tutoring score** (harmonic mean). Reported: live MWPTutor beat instructed free-form GPT-4 on overall tutoring score ([abstract](https://arxiv.org/abs/2402.09216)); on the 45 MathDial problems the summary table gives tutoring score 1.00 (live) vs 0.82 (GPT-4) *(unverified detail; check the table before quoting)*.
- **Adopt**: this is the nearest published design to ours. Adopt their **telling rate / success rate / tutoring score** metrics for our offline evaluation, and their "explicit forbidden vocabulary per state" idea (we have leak regexes; extend them to level-specific forbidden tokens, e.g. level 1-2 may not name the theorem or operator used in the step).
- **Behind/ahead**: our policy is equivalent; our information hiding (reply LLM never sees later steps) is stricter than theirs. They show cached-only is worse, which validates our live REPLY + authored fallback combination.

#### StratL ("Towards the Pedagogical Steering of LLMs for Tutoring: a case study with Productive Failure", Findings of ACL 2025)
- **Link**: [arXiv 2410.03781](https://arxiv.org/abs/2410.03781v2), code [RomainPuech/StratL](https://github.com/RomainPuech/StratL-Pedagogical-Steering-of-LLMs-for-Tutoring) (MIT), data [eth-lre/Productive-Failure-Problems](https://github.com/eth-lre/Productive-Failure-Problems).
- **Architecture**: (1) LLM multi-label classifier assigns **student-state features** per turn (error types, requests, conversation state, emotional signals; reported F1 0.77); (2) a **deterministic transition graph** over **tutoring intents** (Scaffolding, Problematizing, Affective, Generic) chooses the next intent; (3) the intent is injected into the generation prompt ([HTML](https://arxiv.org/html/2410.03781v2)).
- **Evaluation**: field study, 17 Singapore high-school students; significantly higher fidelity to Productive Failure (p=.046) and more solution representations generated (2.6 vs 1.0) without loss of coherence ([HTML](https://arxiv.org/html/2410.03781v2)).
- **Adopt**: this is our DIAGNOSIS -> POLICY split, validated in the field. Two ideas to borrow: an **Affective** intent branch (respond to frustration/low confidence explicitly; we have "disorientation level" but should map it to dedicated actions), and **reporting the classifier F1** of the diagnosis stage as a first-class metric.
- **Avoid**: small N; no learning-outcome measure.

#### Bridge (Stanford, NAACL 2024) and Tutor CoPilot
- **Bridge**: [arXiv 2310.10648](https://arxiv.org/abs/2310.10648v3), code/data [rosewang2008/bridge](https://github.com/rosewang2008/bridge). Cognitive task analysis turns an expert's latent remediation process into a **decision triple**: (A) student **error type**, (B) **remediation strategy**, (C) **intention**, made *before* the response is generated. GPT-4 responses conditioned on expert decisions were **+76% more preferred**; **random** decisions reduced quality by **-97%** relative to expert decisions ([arXiv](https://arxiv.org/html/2310.10648v2)).
- **Tutor CoPilot**: [arXiv 2410.03017](https://arxiv.org/abs/2410.03017). Uses the Bridge-style model of expert thinking to give live human tutors suggestions. RCT with 700+ tutors and 1,000+ students: +4 p.p. topic mastery overall, **+9 p.p. for students of lower-rated tutors**; more probing questions, less generic praise; ~$20/tutor/year ([Stanford SCALE](https://scale.stanford.edu/publications/tutor-copilot-human-ai-approach-scaling-real-time-expertise)).
- **Adopt**: the -97% result is the strongest evidence that **the decision layer matters more than the generator**, i.e. our POLICY is the critical asset and must be context-sensitive. Concretely: make the policy output an explicit (error, strategy, intention) triple and pass it to the REPLY prompt; log it for teacher review. Use Bridge's error/strategy taxonomies as a starting vocabulary for our sheets.
- **Avoid**: Bridge decisions come from human experts; if our DIAGNOSIS mislabels the error, we inherit the "random decision" penalty. Measure diagnosis accuracy.

#### TreeInstruct ("Instruct, Not Assist", Findings of EMNLP 2024)
- **Link**: [arXiv 2406.11709](https://arxiv.org/html/2406.11709v4), [ACL Anthology](https://preview.aclanthology.org/new-sigs/2024.findings-emnlp.553/).
- **Architecture**: Socratic code-debugging instructor with **state-space estimation**: each task the student must resolve is a boolean state variable; a **question tree** is dynamically built from the student's estimated knowledge state ([arXiv](https://arxiv.org/html/2406.11709v4)).
- **Adopt**: the boolean "resolved/unresolved" state per sub-goal is the same as our "steps done" vector. Their hierarchical questioning (sub-questions when a question fails) is a natural extension of our hint levels: a failed level-2 question can spawn an authored sub-question instead of jumping to level 3.

#### Ruffle&Riley (CMU, 2023-2024)
- **Links**: [arXiv 2310.01420](https://arxiv.org/abs/2310.01420), [arXiv 2404.17460](https://arxiv.org/abs/2404.17460), [NeurIPS 2023 workshop](https://neurips.cc/virtual/2023/79097).
- **Architecture**: **automatically induces a tutoring script from lesson text** (review questions -> solutions -> expectations -> compiled script) and orchestrates two GPT-4 agents (learner-agent Ruffle, professor Riley) in a learning-by-teaching format with ITS outer/inner loops; state = expectation coverage, tracked via the chat log only ([HTML](https://arxiv.org/html/2404.17460v1)).
- **Evaluation**: two online studies, N=200: higher perceived understanding/helpfulness but **no significant short-term learning gains vs. reading**; learners who did not request help learned most; **help-before-every-response "gaming" correlated with the lowest gains**; the system was **too lenient**, accepting partial coverage of an expectation ([HTML](https://arxiv.org/html/2404.17460v1)).
- **Adopt**: (1) LLM-assisted **draft generation of sheets** from course notes (we author offline; a generator + human edit pass would scale); (2) treat their leniency finding as a test case: our DIAGNOSIS must require all components of a step's objective before marking it done.
- **Avoid**: state "captured solely via the chat log" (no structured state) and engagement metrics as proxy for learning.

#### Socratic Playground for Learning (SPL)
- **Links**: [arXiv 2406.13919](https://www.arxiv.org/abs/2406.13919), follow-up [arXiv 2501.06682](https://arxiv.org/pdf/2501.06682).
- **Architecture**: GPT-4 dialogue ITS driven by extensive prompt engineering; generates learning scenarios and runs multi-turn Socratic dialogue; framed as an EMT/AutoTutor successor ([arXiv](https://arxiv.org/html/2406.13919v2)).
- **Evaluation**: pilot on essay writing / English skills with ~30 undergraduates ([summary](https://themoonlight.io/review/spl-a-socratic-playground-for-learning-powered-by-large-language-model)).
- **Adopt**: little beyond confirmation that EMT maps well to LLMs. **Avoid**: prompt-only control with no deterministic layer.

#### SocraticAI (CS, Ashoka University, 2025)
- **Link**: [arXiv 2512.03501](https://arxiv.org/abs/2512.03501).
- **Architecture**: guardrails as structure, not prohibition: **query validation** (students must formulate well-posed questions), reflection prompts, **daily usage limits**, RAG on course material ([arXiv](https://arxiv.org/pdf/2512.03501)).
- **Evaluation**: deployment; students moved from vague help-seeking to problem decomposition in 2-3 weeks, >75% produced substantive reflections ([arXiv](https://arxiv.org/pdf/2512.03501)).
- **Adopt**: a lightweight "show me your attempt first" gate before the first hint, which is also the classic anti-gaming rule.

#### Socratic RAG tutor for Calculus I (IFMG, Brazil)
- **Link**: [repository record](https://repositorio.ifmg.edu.br/items/50fd729e-2611-44f3-881d-2789ef7be6ff).
- **What**: GPT-4 tutor tested on 27 Calculus I questions; **RAG + few-shot reached ~93% compliance with Socratic style vs ~11% for RAG + one-shot** (as reported in the search summary of the record; *unverified detail*).
- **Adopt**: few-shot exemplars of good Socratic replies per action type in our REPLY prompt are cheap and apparently very effective. Closest in subject matter (university calculus) to our course.

#### Open-source hobby/applied state-machine tutors
- [redtachyon/tutor-at-home](https://awesome.ecosyste.ms/projects/github.com%2Fredtachyon%2Ftutor-at-home): explicit state automaton (partly correct / hint / feedback / full solution).
- [e-roy/ai-math-tutor](https://awesome.ecosyste.ms/projects/github.com%2Fe-roy%2Fai-math-tutor): Socratic multi-turn web app with progress tracking.
- Hostos (CUNY) "Socratic Math Tutor" bot: **hard reveal policy** requiring at least two verified reasoning steps before the final answer can be requested ([HALC guide](https://halcaiguide.commons.gc.cuny.edu/bots/socratic-math-tutor/)).
- [akshaybahadur21/Socratic](https://github.com/akshaybahadur21/Socratic).
- **Takeaway**: these validate the pattern but none has published evaluation; the Hostos "hard reveal" rule is a simple, quotable policy we could mirror for level 4.

---

### A3. Diagnosis / verification of student reasoning

#### Stepwise verification and remediation of student reasoning errors (ETH, EMNLP 2024)
- **Link**: [arXiv 2407.09136](https://arxiv.org/html/2407.09136v1), [ACL Anthology](https://preview.aclanthology.org/setup/2024.emnlp-main.478).
- **Architecture**: **verify first, then generate**. Verifier variants: (1) classify correctness / first error step, (2) free-text **error description**, (3) **step alignment** of student steps to the reference solution (modified Needleman-Wunsch with semantic similarity). The verifier output conditions the response generator ([HTML](https://arxiv.org/html/2407.09136v1)).
- **Data**: ~1K stepwise student solutions with teacher-annotated first error (kappa 0.75).
- **Results**: with GPT-3.5 + error description, human-rated **targetedness 29% -> 62%** and **correctness 37% -> 66%**; quality drops for problems with 5+ steps ([HTML](https://arxiv.org/html/2407.09136v1)).
- **Adopt**: our DIAGNOSIS already plays the verifier role. Add (a) an explicit **first-error step + one-sentence error description** field to the JSON, (b) the **step-alignment** idea to map free-form student work onto sheet steps, and (c) their dataset as an external test of the diagnoser.

#### "LLMs cannot spot math errors, even when allowed to peek into the solution" (EMNLP 2025)
- **Link**: [arXiv 2509.01395](https://arxiv.org/abs/2509.01395).
- **Finding**: state-of-the-art LLMs struggle to locate the **first error step** in student solutions **even with the reference solution**; generating an **intermediate corrected version of the student's own solution** (staying close to the student's path) improves localisation ([abstract](https://arxiv.org/abs/2509.01395)).
- **Adopt**: directly applicable to DIAGNOSIS: ask the model first to produce "the student's solution, minimally corrected", then diff against the original to locate the error. Also a warning for the "find the error" mode: never rely on an LLM to *grade* whether the student found the planted error without the authored ground truth (which we have).

#### Khanmigo math updates (Khan Academy, 2025)
- **Link**: [Khanmigo Math Computation and Tutoring Updates](https://blog.khanacademy.org/khanmigo-math-computation-and-tutoring-updates/).
- **Architecture**: (1) dedicated **calculator tool** instead of LLM arithmetic; (2) the model is instructed to **write out, hidden, all the ways the student may have arrived at their answer** before replying; (3) retrieves the existing **Khan exercise steps, hints and solutions** before responding, which manual review showed improves accuracy; (4) an internal **math tutoring benchmark** where Khanmigo catches errors better than raw GPT-4o; (5) a **quality dashboard** tracking math-error rates across releases ([blog](https://blog.khanacademy.org/khanmigo-math-computation-and-tutoring-updates/)).
- **Adopt**: (2) is a cheap upgrade to DIAGNOSIS ("enumerate plausible paths/errors that lead to this answer, then match against the sheet's common errors"). (3) validates our authored sheets. (5) is an operational practice we should copy (see top-10 #9).

#### LeanTutor / formal and CAS verification
- **LeanTutor** ([ICML 2025 workshop page](https://icml.cc/virtual/2025/52431)): autoformalises student proof steps into Lean, verifies them, generates the next step, then produces natural-language hints from the Lean state.
- **SymPy/numeric equivalence**: the standard robust check is evaluating both expressions at random points (SymPy `simplify` alone is incomplete) ([discussion in arXiv 2503.16460](https://arxiv.org/html/2503.16460v1)).
- **"Can LLMs correctly interpret equations with errors?"** ([arXiv 2505.10966](https://arxiv.org/pdf/2505.10966)) is relevant for parsing messy student input.
- **Adopt**: for multivariable calculus most step outcomes are checkable expressions (partial derivatives, gradients, Jacobians, critical points, Hessian determinants, integral bounds, Lagrange systems). Add `check:` fields in the sheet with the expected expression(s) and have the DIAGNOSIS extract the student's expression; equivalence is decided by SymPy + random-point numerics, not by the LLM.

---

### A4. Datasets, fine-tuned tutors and RL for pedagogy

#### MathDial (ETH / TU Darmstadt, Findings of EMNLP 2023)
- **Links**: [arXiv 2305.14536](https://arxiv.org/abs/2305.14536v2), data [eth-nlped/mathdial](https://github.com/eth-nlped/mathdial).
- **What**: ~3K one-to-one tutoring dialogues on GSM8K-style problems; **real teachers paired with an LLM role-playing a student with a typical misconception**; teacher moves annotated as **Focus, Probing, Telling, Generic**, grounded in Reiser's structuring vs problematizing scaffolding ([arXiv PDF](https://arxiv.org/pdf/2305.14536)).
- **Findings**: LLMs give factually wrong feedback or **reveal the solution too early**; fine-tuning on MathDial improves the success/telling trade-off ([abstract](https://arxiv.org/abs/2305.14536v2)).
- **Adopt**: (1) the **LLM-as-student-with-a-misconception** technique to build a regression suite: for each sheet's common error, simulate a student who holds it; (2) tag our policy actions with the Focus/Probing/Telling/Generic taxonomy for analytics.

#### SocraticLM (NeurIPS 2024 spotlight)
- **Links**: [NeurIPS paper](https://proceedings.neurips.cc/paper_files/paper/2024/file/9bae399d1f34b8650351c1bd3692aeae-Paper-Conference.pdf), code [Ljyustc/SocraticLM](https://github.com/Ljyustc/SocraticLM) (~180 stars).
- **What**: "Thought-provoking" teaching paradigm; **Dean-Teacher-Student multi-agent pipeline** generated **SocraTeach** (35K multi-round dialogues, 208K single-round) over math problems; student turns typed as irrelevant / question / incorrect / correct and six simulated student profiles; fine-tuned ChatGLM3-6B (later Qwen2.5-Math-7B); reported **>12% over GPT-4** on their teaching evaluation ([repo](https://github.com/Ljyustc/SocraticLM), [NeurIPS poster](https://neurips.cc/virtual/2024/poster/93477)).
- **Adopt**: the **Dean** agent (a supervisor that reviews and corrects the teacher's turn) is the same idea as our GUARD; their four-way student-turn typing is a minimal intent taxonomy to compare against ours.
- **Avoid**: fine-tuning a small model is unnecessary for a single course; our authored sheets + frontier model gives more control.

#### SocraticLLM / SocraticMATH (ECNU)
- **Link**: [arXiv 2407.17349](https://arxiv.org/pdf/2407.17349). Human-annotated Socratic math teaching dataset; fine-tuned model reported to beat GPT-4 in human evaluation on reliability and Socratic strategy ([summary](https://www.themoonlight.io/en/review/boosting-large-language-models-with-socratic-method-for-conversational-mathematics-teaching)).

#### TutorEval / TutorChat (Princeton, ICML 2024)
- **Links**: [arXiv 2402.11111](https://arxiv.org/html/2402.11111v2), code [princeton-nlp/LM-Science-Tutor](https://github.com/princeton-nlp/lm-science-tutor).
- **What**: TutorEval = 800+ expert-written questions about **long STEM textbook chapters**; TutorChat = 80K synthetic textbook-grounded dialogues; fine-tuned Llemma 7B/34B tutors with 32K context ([arXiv](https://arxiv.org/html/2402.11111v2)).
- **Adopt**: the evaluation framing "answer grounded in a long chapter of the course notes" matches our references-to-notes feature; TutorEval-style items could test our "explain concept from notes" path. Not a Socratic/leakage benchmark.

#### From Problem-Solving to Teaching Problem-Solving (ETH/EPFL et al., EMNLP 2025)
- **Links**: [arXiv 2505.15607](https://arxiv.org/abs/2505.15607v1), [ACL Anthology](https://aclanthology.org/2025.emnlp-main.15), code [eth-lre/PedagogicalRL](https://github.com/eth-lre/PedagogicalRL).
- **Method**: online RL (GRPO) of Qwen2.5-7B tutor against a simulated Llama-3.1-8B student; reward = **post-dialogue student solve rate**, with dialogues **rejected/penalised if an LLM judge detects solution leakage** and if **multiple independent pedagogy judges** (unanimity required, to avoid judge overfitting) disapprove; penalty weight lambda gives a controllable **Pareto frontier** between solve rate and pedagogy; optional hidden think tags ([HTML](https://arxiv.org/html/2505.15607v2)).
- **Results**: 7B model comparable to LearnLM-class tutors without human annotation; optimising only for student success leads to near-constant leakage (reported ~89.5%), the penalised model leaks far less *(exact numbers: unverified detail)* ([HTML](https://arxiv.org/html/2505.15607v2)).
- **Adopt** (without RL): (1) **multi-judge unanimity** for our GUARD judge, i.e. two cheap judges with different prompts, both must pass; (2) the **simulated-student post-dialogue solve rate + leak rate** as offline evaluation metrics; (3) the explicit insight that success and non-leakage trade off and must be tuned, not maximised separately.

#### Training LLM-based tutors to improve student learning outcomes (Scarlatos et al., 2025)
- **Link**: [arXiv 2503.06424](https://arxiv.org/abs/2503.06424v1).
- **Method**: candidate tutor turns scored by a **trained student model** (probability the student's next turn is correct) plus GPT-4o pedagogy rubric; DPO on Llama 3.1 8B. Increases predicted next-turn correctness with pedagogy comparable to GPT-4o; only simulated students ([arXiv](https://arxiv.org/html/2503.06424v1)).
- **Adopt**: "rank candidates by predicted student progress" could be a guard-time tie-breaker (generate 2 replies, choose by judge), as CodeHelp does.

#### Towards Pedagogically Aligned LLM Tutors for Math Mistake Remediation (MBZUAI, 2026)
- **Link**: [arXiv 2606.21502](https://arxiv.org/abs/2606.21502). SFT + DPO on synthetic preference pairs built from scaffolding/factuality principles; inputs include **solution correctness and gold answer** configurations; open model competitive with a proprietary baseline in human eval.
- **Adopt**: confirms that giving the tutor the **verified correctness signal** (our DIAGNOSIS) helps.

#### Exploring Knowledge Tracing in Tutor-Student Dialogues (LLMKT, LAK 2025)
- **Link**: [arXiv 2409.16490](https://arxiv.org/abs/2409.16490v1); follow-up difficulty-aware KT with IRT [arXiv 2605.01097](https://arxiv.org/pdf/2605.01097).
- **Method**: LLM labels the KCs involved in each turn and whether the student answered correctly; then classic KT (incl. BKT/DKT) or LLM-based KT tracks knowledge over the dialogue; LLMKT outperforms baselines in predicting correctness ([arXiv](https://arxiv.org/html/2409.16490v1)).
- **Adopt**: our DIAGNOSIS already produces "step done / error" labels per turn; tagging steps with KCs gives KT almost for free.

---

### A5. Big-lab products and pedagogy frameworks

#### Google LearnLM / "Towards Responsible Development of Generative AI for Education" (2024) and "LearnLM: Improving Gemini for Learning" (2024)
- **Links**: [arXiv 2407.12687](https://arxiv.org/abs/2407.12687) (v4 Dec 2025), [arXiv 2412.16429](https://arxiv.org/abs/2412.16429v1).
- **Evaluation design** (2407.12687): **seven benchmarks**: unguided conversations with learner feedback; turn-level teacher pedagogy ratings; conversation-level ratings; side-by-side comparisons; **LLM-critic evaluations**; evaluative-practice assessment; feedback on procedural homework. Rubric principles: **encourage active learning, manage cognitive load, deepen metacognition, motivate/stimulate curiosity, adapt to learner goals**. Automatic critics check: stays on topic, **doesn't reveal answer**, guides toward answer, promotes engagement, **identifies and addresses misconceptions**, responds to emotion, positive tone, adapts to level ([HTML v4](https://arxiv.org/html/2407.12687v4)). Fine-tuning data: human tutoring, gen-AI role-play, GSM8K dialogues, teacher-authored **golden conversations**.
- **2412.16429**: reframes pedagogy as **pedagogical instruction following** (system instructions specify desired behaviour), co-trained into Gemini SFT/RM/RL; expert raters preferred LearnLM by +31% over GPT-4o, +11% over Claude 3.5 Sonnet, +13% over Gemini 1.5 Pro ([abstract](https://arxiv.org/abs/2412.16429v1)).
- **Product**: Gemini **Guided Learning** (Aug 2025) builds on LearnLM ([Google blog](https://blog.google/products-and-platforms/products/education/guided-learning/)).
- **Adopt**: (1) **use the LLM-critic checklist as the rubric for our GUARD judge and for offline evaluation** (it is published and validated); (2) the "golden conversation" idea: author 1-2 ideal dialogues per exercise type and use them as few-shot exemplars in REPLY; (3) the pedagogical-instruction-following framing means a LearnLM-family model is a natural candidate for REPLY because it is trained to obey per-turn pedagogical instructions like the ones our POLICY emits.

#### Eedi + Google DeepMind human-in-the-loop trial (2025)
- **Link**: [Eedi news release](https://www.eedi.com/news/new-exploratory-research-from-eedi-and-google-deepmind-reveals-human-in-the-loop-ai-tutoring-outperforms-human-only-support), [The 74](https://www.the74million.org/article/ai-tutors-with-a-little-human-help-offer-reliable-instruction-study-finds/).
- **What**: RCT, 165 UK students aged 13-15; LearnLM tutor messages **reviewed/edited by expert human tutors before sending**; human-AI team equalled human-only on fixing the immediate mistake (93.0% vs 91.2%) and resolving misconceptions (95.4% vs 94.9%), and gave +10 p.p. learning vs +4.5 p.p. for human tutor alone, relative to standard hints ([Eedi](https://www.eedi.com/news/new-exploratory-research-from-eedi-and-google-deepmind-reveals-human-in-the-loop-ai-tutoring-outperforms-human-only-support)).
- **Adopt**: Eedi's platform is misconception-centric (diagnostic questions -> misconception -> remediation), the same as our sheets' common errors. Teacher review of transcripts is the realistic human-in-the-loop for a university course (asynchronous, not pre-send).

#### Khanmigo (Khan Academy)
- **Links**: [7-step approach to prompt engineering](https://blog.khanacademy.org/khan-academys-7-step-approach-to-prompt-engineering-for-khanmigo), [math computation & tutoring updates](https://blog.khanacademy.org/khanmigo-math-computation-and-tutoring-updates/), [AI Engineer talk](https://ai.engineer/talks/scaling-ai-in-education-a-khanmigo-case-study), [Common Sense Media rating](https://www.commonsensemedia.org/ai-ratings/khanmigo).
- **Design**: GPT-4-family Socratic tutor; prompts grounded in learning-science literature; calculator tool; hidden enumeration of student paths; retrieval of exercise steps/hints/solutions; internal tutoring benchmark; error-rate dashboard (see A3).
- **Caveats**: press/secondary reports describe students **abandoning sessions when answers were withheld** and engagement not reliably correlating with learning at scale ([AI Weekly](https://aiweekly.co/alerts/khanmigo-ai-tutor-falls-short-of-khan-academy-hype); secondary source, treat with care).
- **Adopt**: the operational practices. **Avoid**: rigid withholding for students who already did the work; give fast confirmation when the student is right and a clear path to the worked solution after genuine effort.

#### ChatGPT Study Mode (OpenAI, July 2025), Claude learning mode (Anthropic, 2025)
- **Links**: [OpenAI: Introducing study mode](https://openai.com/index/chatgpt-study-mode/), [Simon Willison's analysis incl. the system prompt](https://simonwillison.net/2025/Jul/29/openai-introducing-study-mode), [Claude learning modes coverage](https://www.tomsguide.com/ai/claudes-new-learning-modes-take-on-chatgpts-study-mode-heres-what-they-do).
- **Architecture**: **system-prompt only** (custom instructions written with educators: active participation, cognitive load, metacognition, curiosity, feedback) ([OpenAI](https://openai.com/index/chatgpt-study-mode/)). Willison notes it is a prompt and therefore easy to bypass ([blog](https://simonwillison.net/2025/Jul/29/openai-introducing-study-mode)).
- **Takeaway**: the market default is prompt-only control; our structural information hiding is a genuine differentiator (and the main argument for the project's novelty).

#### Harvard physics AI tutor RCT (Kestin et al., Scientific Reports 2025)
- **Link**: [PMC full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC12179260/).
- **What**: 194 Harvard undergraduates, crossover RCT; custom GPT-4 tutor with **pre-written step-by-step solutions in the prompt**, structured problem-solving and guided questioning; students learned **more than twice as much** in less time (median 49 vs 75 min) than in in-class active learning ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12179260/)).
- **Adopt**: strongest university-level evidence that **solution-grounded, structured** LLM tutoring works. Our design goes further (information hiding, deterministic policy). Their RCT design (crossover, two topics) is a template for evaluating ours in the course.

#### "Generative AI without guardrails can harm learning" (Bastani et al., PNAS 2025)
- **Links**: [SSRN](https://papers.ssrn.com/abstract=4895486), [PDF](https://nmdprojects.net/teaching_resources/bastani_generative_ai_can_harm_learning.pdf), [Wharton summary](https://knowledge.wharton.upenn.edu/article/without-guardrails-generative-ai-can-harm-education).
- **What**: ~1,000 Turkish high-school students. **GPT Tutor** prompt contained, per problem, **teacher-written solution(s) and a list of common mistakes and how to react**, and instructed incremental hints without the full solution. Practice +48% (Base) / +127% (Tutor); on the unassisted exam, GPT Base **-17%**, while GPT Tutor largely mitigated the harm ([PDF](https://nmdprojects.net/teaching_resources/bastani_generative_ai_can_harm_learning.pdf)). GPT Base made logical errors on 42% of problems and arithmetic errors 8% ([PDF](https://nmdprojects.net/teaching_resources/bastani_generative_ai_can_harm_learning.pdf)).
- **Adopt**: this is direct causal evidence for our **authored-sheet** approach (solutions + common errors per problem). Note GPT Tutor only reached "no harm" on the exam, not a gain: guardrails prevent the crutch effect but learning gains need more (active effort, retrieval, spacing).

#### Rori (Rising Academies, Ghana)
- **Links**: [arXiv 2402.09809](https://arxiv.org/abs/2402.09809v1), [RAG groundedness trade-off, EDM 2024](https://educationaldatamining.org/EDM2024/proceedings/2024.EDM-short-papers.28/index.html).
- **What**: WhatsApp math tutor, ~1,000 students, 8 months, effect size **0.37** ([arXiv](https://arxiv.org/pdf/2402.09809)). RAG over an open textbook improves groundedness but raters sometimes prefer less-grounded answers ([EDM](https://educationaldatamining.org/EDM2024/proceedings/2024.EDM-short-papers.28/index.html)).
- **Adopt**: groundedness vs preference trade-off is relevant to our "references to course notes": measure it, don't assume students prefer grounded replies.

---

### A6. Guardrails and leakage-focused work

#### CodeHelp (Liffiton et al., Koli Calling 2023)
- **Links**: [arXiv 2308.06921](https://arxiv.org/abs/2308.06921v1), code [liffiton/Gen-Ed](https://github.com/liffiton/Gen-Ed) (AGPL-3.0, framework containing CodeHelp), help-seeking study [arXiv 2310.16984](https://arxiv.org/pdf/2310.16984).
- **Pipeline** ([PDF](https://arxiv.org/pdf/2308.06921)): (1) **sufficiency check** prompt (with CoT) run in parallel; if insufficient, ask the student for clarification; (2) main response prompt appends "do not write any example code" and the **instructor's avoid-keyword list**; (3) **two completions generated and scored** for code blocks / avoided keywords, best kept; (4) if code remains, a **third LLM prompt rewrites the response to remove code** (an LLM rather than deletion, so the remaining text stays coherent). Authors note models are "strongly biased towards providing a complete solution" even when told not to.
- **Evaluation**: 52 students, 12 weeks; well received, complements rather than replaces instructors ([abstract](https://arxiv.org/abs/2308.06921v1)); cost of roughly $0.002/query and 95% of students wanting to keep using it are reported in secondary summaries *(unverified detail)*.
- **Adopt**: (1) **instructor avoid-list per exercise** = our leak regexes (good); (2) **best-of-2 generation before the guard** reduces rewrite loops and latency variance; (3) their **sufficiency check** = ask the student to show work/state the question when the input is too vague, a cheap pre-diagnosis gate.

#### CS50 Duck / CS50.ai (Harvard, SIGCSE 2024)
- **Links**: [paper PDF](https://cs.harvard.edu/malan/publications/V1fp0567-liu.pdf), [docs](https://cs50.readthedocs.io/cs50.ai/), [SIGCSE demo](https://sigcse2024.sigcse.org/details/sigcse-ts-2024-demos/4/Demo-2A-Teaching-CS50-with-AI-Leveraging-Generative-Artificial-Intelligence-in-Comp).
- **Architecture** ([paper](https://cs.harvard.edu/malan/publications/V1fp0567-liu.pdf)): CS50.ai backend between clients and Azure GPT-4; **PII anonymisation**; course-specific system prompts and templates in **YAML config files per use case**; **RAG over lecture captions** (30-second segments in ChromaDB); **prompt-injection guard** (pattern pre-filter, then a separate GPT-4 call classifies the request; session aborted on attack); **usage throttling via "hearts"** (10 hearts, +1 every 3 minutes) which the authors argue also has pedagogical value (fewer, better-formed questions); on the Ed forum, answers are subject to **human staff endorsement**.
- **Adopt**: (1) **injection pre-filter + LLM classifier on the input side** (our GUARD is output-side only); (2) **rate limit hint escalation** in time (hearts) to curb gaming; (3) **anonymise** student messages before LLM calls (GDPR, Catalan university context); (4) per-use-case YAML prompt configs, which we likely already have via sheets.

#### Jill Watson (Georgia Tech, 2024-2025)
- **Links**: [arXiv 2405.11070](https://arxiv.org/abs/2405.11070v1), large-scale evaluation [arXiv 2506.17363](https://arxiv.org/pdf/2506.17363).
- **Architecture**: skill-based modular VTA (XiaoIce-inspired), dense retrieval + RAG over instructor-approved courseware, multiple filters for hallucination/toxicity; deployed to ~1,300 students ([arXiv](https://arxiv.org/abs/2405.11070v1)).
- **Adopt**: the "skill" router is analogous to our intent -> action mapping; course-material-only grounding policy.

#### Answer-leakage robustness against adversarial students (Zhao, Knezevic, Käser; ACL 2026)
- **Links**: [alphaXiv 2604.18660](https://www.alphaxiv.org/abs/2604.18660), [ACL Anthology 2026.acl-long.1412](https://aclanthology.org/2026.acl-long.1412/).
- **What**: adapts **six groups of adversarial/persuasive techniques** to tutoring and evaluates many tutors (model families, pedagogically aligned models, a multi-agent design); generic adversarial student agents often fail, so they **fine-tune an adversarial student agent** as a standardised benchmark; propose simple defences that reduce leakage ([abstract](https://www.alphaxiv.org/abs/2604.18660)).
- **Adopt**: build an **adversarial student suite** (persuasion: "my exam is in 5 minutes", authority: "the professor said you can", role-play, partial-answer extraction "just confirm if it's 2x", incremental extraction across turns) and run it in CI against our pipeline. Our structural hiding should make us strong here; prove it.

#### Prompt-injection defences for educational tutors (2026)
- **Link**: [arXiv 2605.06669](https://arxiv.org/pdf/2605.06669).
- **What**: compares a domain-specific multi-layer pipeline (deterministic pattern filters, structural validation, contextual sandboxing, **session-level behavioural checks**) with NeMo Guardrails and Prompt Guard. Reported: NeMo Guardrails 0% bypass but **16.22% false positives** and ~1.5 s latency; Prompt Guard 38.48% bypass, 3.60% FP ([abstract summary](https://arxiv.org/pdf/2605.06669)).
- **Adopt**: measure our GUARD's **false-positive rate on benign pedagogical replies**, not only leaks caught; over-eager guards degrade pedagogy (and trigger the authored fallback too often).

#### Leakage definition (EduFair-Bench, 2026)
- **Link**: [arXiv 2609.12949](https://arxiv.org/pdf/2609.12949). Defines answer leakage as stating the final answer **or a key intermediate result the student was expected to derive, including equivalent or near-equivalent forms (rearrangements, partial decompositions)**.
- **Adopt**: our regex leak checks will miss equivalent forms (e.g. `2x·e^{y}` vs `2e^{y}x`, factored vs expanded, numeric vs symbolic). Add a **CAS-based leak check**: extract math from the candidate reply, and test equivalence against every not-yet-unlocked step result.

---

### A7. Evaluation benchmarks

#### MathTutorBench (ETH, EMNLP 2025)
- **Links**: [arXiv 2502.18940](https://arxiv.org/abs/2502.18940), code [eth-lre/mathtutorbench](https://github.com/eth-lre/mathtutorbench).
- **What**: holistic benchmark of tutoring abilities (problem solving, Socratic questioning, student understanding / mistake location, pedagogical response generation) with a **trained pedagogical reward model** that discriminates expert vs novice teacher responses; finding: **solving ability does not translate into teaching; pedagogy and subject expertise trade off** ([arXiv](https://arxiv.org/html/2502.18940v2)).
- **Adopt**: run its "mistake location" and "pedagogical response" tasks against our DIAGNOSIS and REPLY stages separately (stage-level evaluation). Use their reward model as an extra offline judge.

#### MRBench / "Unifying AI Tutor Evaluation" (MBZUAI, NAACL 2025) and BEA 2025 shared task
- **Links**: [arXiv 2412.09416](https://arxiv.org/abs/2412.09416), [ACL Anthology](https://aclanthology.org/2025.naacl-long.57), [BEA 2025 findings arXiv 2507.10579](https://arxiv.org/pdf/2507.10579).
- **What**: 8 pedagogical dimensions (incl. **mistake identification, mistake location, revealing of the answer, providing guidance, actionability, coherence, tutor tone, human-likeness**); 192 dialogues, 1,596 responses. BEA 2025 (50+ teams): best macro-F1 only **58.34 (guidance) to 71.81 (mistake identification)** on 3-class problems ([findings](https://arxiv.org/pdf/2507.10579)).
- **Adopt**: the 8 dimensions as our annotation scheme for human evaluation; the BEA numbers are a sober prior for how accurate any LLM judge (including our GUARD judge) will be: expect 60-70%, so pair it with deterministic checks.

#### TutorBench (2025, ICLR 2026)
- **Links**: [arXiv 2510.02663](https://arxiv.org/abs/2510.02663), [ICLR page](https://iclr.cc/virtual/2026/10019695).
- **What**: 1,490 expert-curated samples (high school/AP) with **sample-specific rubrics** judged by an LLM; tasks: adaptive explanations, actionable feedback on student work, hint generation; no frontier model above 56%; Claude models strong at active learning but weaker elsewhere ([abstract](https://arxiv.org/abs/2510.02663)).
- **Adopt**: **sample-specific rubrics** = per-exercise rubrics that we can derive automatically from our sheets (each step's objective/idea/detail + forbidden content) for the judge.

---

### A8. Popular open-source "AI tutor" repos

| Repo | Stars (approx.) | What it is | Relevance |
|---|---|---|---|
| [HKUDS/DeepTutor](https://github.com/HKUDS/DeepTutor) | ~40k | Agent-native learning assistant: RAG engines, multi-mode (chat/quiz/solve), mastery-gated guided learning, inspectable 3-layer memory | Memory and RAG architecture; **no explicit Socratic withholding or step policy** ([repo](https://github.com/HKUDS/DeepTutor)) |
| [JushBJJ/Mr.-Ranedeer-AI-Tutor](https://github.com/JushBJJ/Mr.-Ranedeer-AI-Tutor) (a mirror found in search: [ChinaNanSen fork](https://github.com/ChinaNanSen/Mr.-Ranedeer-AI-Tutor)) | ~30k | A single configurable system prompt (depth, style incl. Socratic) | Shows demand; prompt-only control ([article](https://starlog.is/articles/ai-dev-tools/jushbjj-mr-ranedeer-ai-tutor)) |
| [CAHLR/OATutor](https://github.com/CAHLR/OATutor) | ~264 | Open ITS with BKT and hint pathways | Content schema, BKT |
| [Ljyustc/SocraticLM](https://github.com/Ljyustc/SocraticLM) | ~180 | Fine-tuned Socratic math tutor + SocraTeach | Data, student-turn typing |
| [liffiton/Gen-Ed](https://github.com/liffiton/Gen-Ed) | ~42 | CodeHelp framework (LTI, guardrails) | Guard pipeline, LTI integration |
| [eth-lre/PedagogicalRL](https://github.com/eth-lre/PedagogicalRL), [eth-lre/mathtutorbench](https://github.com/eth-lre/mathtutorbench), [eth-nlped/mathdial](https://github.com/eth-nlped/mathdial), [rosewang2008/bridge](https://github.com/rosewang2008/bridge), [RomainPuech/StratL](https://github.com/RomainPuech/StratL-Pedagogical-Steering-of-LLMs-for-Tutoring), [princeton-nlp/LM-Science-Tutor](https://github.com/princeton-nlp/lm-science-tutor) | research | Datasets/eval code | Evaluation harnesses we can reuse |

No open-source repo found that combines all of: authored per-exercise solution sheets, deterministic hint policy, information-hidden generator, and layered leak guard. The closest published designs are MWPTutor (A2) and StratL (A2); the closest product evidence is Bastani's GPT Tutor and the Harvard physics tutor (A5).

---

### A9. Frameworks for enforcing determinism and control

| Framework | Link | What it gives | Fit for our pipeline |
|---|---|---|---|
| **Structured outputs / constrained decoding (Outlines)** | [dottxt-ai/outlines](https://github.com/dottxt-ai/outlines) | Guarantees JSON-schema/regex/grammar-valid output by constraining tokens | DIAGNOSIS JSON validity guaranteed instead of parse-and-retry. Provider-native JSON schema modes give the same for hosted models. **High value, low effort.** |
| **Guardrails AI** | [guardrails-ai/guardrails](https://github.com/guardrails-ai/guardrails) | Validators (regex, competitor-check, LLM-judge, custom) with on-fail actions (reask, fix, filter, exception) | Our GUARD is a hand-rolled version (validators + reask x3 + fallback). Could adopt its validator interface for testability; not required. |
| **NeMo Guardrails (Colang)** | [NVIDIA/NeMo-Guardrails](https://github.com/NVIDIA/NeMo-Guardrails) | Input/output/dialog rails defined in Colang flows; jailbreak and topical rails | Input-side jailbreak/topic rails are useful; but reported **16% false positives** in an education benchmark ([arXiv 2605.06669](https://arxiv.org/pdf/2605.06669)); our deterministic policy is already a "dialog rail". Use selectively, if at all. |
| **DSPy** | [stanfordnlp/dspy](https://github.com/stanfordnlp/dspy) | Declarative LM programs with typed signatures; optimisers that tune prompts/few-shots against a metric | Strong fit for **optimising the DIAGNOSIS prompt against a labelled set** (metric = step-label accuracy) and the REPLY few-shots against a judge metric. Medium effort. |
| **LangGraph** | [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | Explicit state graphs, persistence/checkpointing, human-in-the-loop interrupts, replay | Our pipeline is already a fixed DAG with a deterministic policy; LangGraph would add checkpointing/replay and HITL interrupts but also dependency weight. Only worth it if we need teacher-approval interrupts or session replay tooling. |

General point: all these frameworks enforce **form** (schema, flow); none enforce **pedagogical content**. The content guarantees in our design come from the authored sheet and information hiding, which no framework provides.

---

## Part B. Synthesis

### B1. Design patterns across the field

1. **Decision before generation** (separate "what to do" from "how to say it"): Bridge's (error, strategy, intention) triple ([arXiv](https://arxiv.org/abs/2310.10648v3)), StratL's intent graph ([arXiv](https://arxiv.org/abs/2410.03781v2)), MWPTutor's FST ([arXiv](https://arxiv.org/abs/2402.09216)), stepwise verify-then-generate ([arXiv](https://arxiv.org/html/2407.09136v1)). Evidence: random decisions -97%, expert decisions +76% (Bridge); targetedness 29% -> 62% (stepwise verification).
2. **Grounding in per-problem authored or retrieved solutions and misconceptions**: AutoTutor EMT, Bastani GPT Tutor ([PDF](https://nmdprojects.net/teaching_resources/bastani_generative_ai_can_harm_learning.pdf)), Harvard physics tutor ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12179260/)), Khanmigo retrieving exercise steps/hints ([blog](https://blog.khanacademy.org/khanmigo-math-computation-and-tutoring-updates/)), Eedi misconceptions ([Eedi](https://www.eedi.com/news/new-exploratory-research-from-eedi-and-google-deepmind-reveals-human-in-the-loop-ai-tutoring-outperforms-human-only-support)).
3. **Graduated hint ladders** (pump/hint/prompt/assertion; bottom-out hints) with known gaming risks ([LearnLab](https://learnlab.org/research/wiki/index.php/Help_abuse); Ruffle&Riley gaming finding [arXiv](https://arxiv.org/html/2404.17460v1)).
4. **Tools for correctness instead of LLM judgement**: calculator (Khanmigo), Lean (LeanTutor), CAS/numeric checks; motivated by poor LLM step-labelling (TutorGym [arXiv](https://arxiv.org/pdf/2505.01563); first-error localisation [arXiv](https://arxiv.org/abs/2509.01395)).
5. **Layered output guards with regeneration**: CodeHelp (best-of-2 + LLM rewrite) ([PDF](https://arxiv.org/pdf/2308.06921)), MWPTutor (resample until checks pass), SocraticLM's Dean agent, PedagogicalRL's leakage judge.
6. **Input-side protection and usage shaping**: CS50 injection guard and hearts ([PDF](https://cs.harvard.edu/malan/publications/V1fp0567-liu.pdf)), SocraticAI query validation ([arXiv](https://arxiv.org/pdf/2512.03501)), CodeHelp sufficiency check.
7. **Simulated students for evaluation and training**: MathDial (LLM student with misconception), SocraticLM, PedagogicalRL, Scarlatos et al., adversarial student agents (ACL 2026).
8. **Rubric-based LLM-judge evaluation, with known ceiling**: LearnLM critics, MRBench 8 dimensions, TutorBench sample-specific rubrics; BEA 2025 best F1 58-72% shows judges are noisy.
9. **Human-in-the-loop at the right layer**: Tutor CoPilot (AI assists humans), Eedi (humans approve AI), CS50 Ed (staff endorsement), Khan dashboards.
10. **Learner modelling across problems**: BKT in CTAT/OATutor, LLMKT for dialogue.

### B2. Where our design is ahead

- **Structural leak prevention by information hiding.** Most systems (Study Mode, Khanmigo, CS50, CodeHelp, SPL, Bastani GPT Tutor) put the full solution in the generator's context and *ask* it not to reveal it; CodeHelp's authors document that models remain "strongly biased towards providing a complete solution" ([PDF](https://arxiv.org/pdf/2308.06921)). Our REPLY never sees later steps, so it cannot leak them; the GUARD only has to catch leaks of the *current* step. Only MWPTutor comes close, with per-state constraints.
- **Deterministic, auditable policy** over an authored step graph, as in MWPTutor/StratL, which are the strongest-controlled published designs; ours adds an authored fallback after 3 failed rewrites, which neither has.
- **Rich per-exercise authoring** (objective/idea/detail per step, common errors with Socratic questions, leak regexes, references to notes) is a superset of Bastani's teacher inputs, which already produced causal evidence of preventing harm.
- **"Find the error" mode with independently verified planted errors** operationalises the erroneous-examples literature ([learning scientists summary](https://www.learningscientists.org/blog/2023/7/27), [Tsovaltzi et al. 2009](https://www-live.dfki.de/fileadmin/user_upload/import/4653_Tsovaltzietal-ErroneousExamples-ECTEL-2009.pdf)) and, crucially, does not trust an LLM to find errors (which it does badly: [arXiv 2509.01395](https://arxiv.org/abs/2509.01395)).
- **University multivariable calculus in Catalan**: almost all benchmarks and datasets are K-12 arithmetic/algebra in English (GSM8K-derived). There is little comparable work at this level and language.

### B3. Where our design is behind (or unproven)

- **No formal correctness checking**: DIAGNOSIS decides "step done" by LLM judgement; TutorGym and EMNLP-2025 results say this is the weakest link.
- **Regex leak checks miss equivalent forms** (EduFair definition), and the LLM judge's accuracy is bounded (BEA 2025).
- **No published-style evaluation harness**: no simulated-student suite, no telling rate / success rate / tutoring score, no stage-level accuracy for DIAGNOSIS, no adversarial suite, no guard false-positive rate.
- **No learner model across exercises** (BKT/KT), so hint level starts at the same place for every student.
- **Anti-gaming**: unclear whether escalation to level 4 requires attempts/time; Ruffle&Riley and Cognitive Tutor data show gaming is the main failure mode of hint ladders.
- **No learning-outcome evidence yet**; the field's best-designed studies (Harvard crossover RCT, Bastani field experiment, Eedi RCT) are the bar.
- **Input-side defences** (prompt-injection classification, PII anonymisation) are not mentioned in our pipeline.

### B4. Ranked top 10 ideas to adopt

| # | Idea | Source(s) | Expected impact | Effort |
|---|---|---|---|---|
| 1 | **CAS-verified step completion.** Add `check:` fields to each sheet step (expected expression(s), equivalence mode); DIAGNOSIS extracts the student's expression; SymPy + random-point numerics decide correctness. LLM only labels steps that are not checkable. | Khanmigo calculator ([blog](https://blog.khanacademy.org/khanmigo-math-computation-and-tutoring-updates/)); LeanTutor ([ICML](https://icml.cc/virtual/2025/52431)); TutorGym ([arXiv](https://arxiv.org/pdf/2505.01563)) | High: removes the weakest link (false "step done" lets policy unlock later content; false "not done" frustrates). | Medium (sheet field + parser + SymPy; LaTeX/Unicode input parsing is the hard part) |
| 2 | **CAS-based semantic leak check in GUARD.** Extract math from candidate replies and test equivalence against every locked step result and the final answer; keep regexes as a fast first pass. | EduFair leakage definition ([arXiv](https://arxiv.org/pdf/2609.12949)); MWPTutor forbidden RHS ([HTML](https://arxiv.org/html/2402.09216v3)) | High: closes the "equivalent form" hole regexes cannot. | Low-medium once #1 exists |
| 3 | **Evaluation harness with simulated students** (one persona per sheet common error, plus "competent", "lost", "answer-seeker"), reporting **success rate, telling rate, tutoring score**, turns to completion, fallback rate, guard false-positive rate. Run on every prompt/sheet change. | MWPTutor metrics; MathDial LLM-student; PedagogicalRL; [arXiv 2605.06669](https://arxiv.org/pdf/2605.06669) for FP rate | High: makes every other change measurable; required for any publication. | Medium |
| 4 | **Adversarial student suite in CI** (persuasion, authority, urgency, role-play, "just confirm X", incremental extraction across turns, language switching Catalan/Spanish/English, LaTeX obfuscation) + input-side injection classifier. | Zhao et al. ACL 2026 ([alphaXiv](https://www.alphaxiv.org/abs/2604.18660)); CS50 guard ([PDF](https://cs.harvard.edu/malan/publications/V1fp0567-liu.pdf)) | High for credibility: our architecture should excel; demonstrating it is a key result. | Low-medium |
| 5 | **Upgrade DIAGNOSIS to verify-then-label**: (a) hidden "minimally corrected student solution" then diff; (b) enumerate plausible paths/errors behind the student's answer before matching to sheet errors; (c) output first-error step + one-line error description; (d) measure accuracy on a labelled set and optimise the prompt (DSPy or manual). | [arXiv 2509.01395](https://arxiv.org/abs/2509.01395); [arXiv 2407.09136](https://arxiv.org/html/2407.09136v1); Khanmigo hidden thinking; [DSPy](https://github.com/stanfordnlp/dspy) | High: Bridge shows wrong decisions are catastrophic (-97%); diagnosis feeds every decision. | Medium |
| 6 | **Anti-gaming hint escalation**: require a student attempt (or explicit self-explanation) before escalating level; time/attempt rate limits; level 4 (bottom-out) only after N verified steps or genuine attempts ("hard reveal"); ask the student to restate the hint in their own words after level 3-4. | Aleven & Koedinger help-seeking ([LearnLab](https://learnlab.org/research/wiki/index.php/Help_abuse)); Ruffle&Riley gaming ([arXiv](https://arxiv.org/html/2404.17460v1)); CS50 hearts; Hostos hard reveal ([HALC](https://halcaiguide.commons.gc.cuny.edu/bots/socratic-math-tutor/)) | Medium-high on learning (the main known failure mode of hint ladders). | Low (pure policy code) |
| 7 | **Explicit decision triple + affective branch in POLICY**: emit (error, strategy, intention) and a teacher-move tag (Focus/Probing/Telling/Generic); map high disorientation/frustration to dedicated affective actions; fast confirmation when the student is right; never withhold after real effort. | Bridge ([arXiv](https://arxiv.org/abs/2310.10648v3)); StratL affective intents; MathDial moves; Khanmigo abandonment reports ([AI Weekly](https://aiweekly.co/alerts/khanmigo-ai-tutor-falls-short-of-khan-academy-hype)) | Medium: better targeted replies, better logs, less frustration-driven abandonment. | Low |
| 8 | **Use the LearnLM critic checklist / MRBench dimensions as the GUARD-judge and offline rubric**; derive **sample-specific rubrics** from each sheet automatically; require **two independent judges to agree** before a pass on borderline cases. | LearnLM ([HTML](https://arxiv.org/html/2407.12687v4)); MRBench ([arXiv](https://arxiv.org/abs/2412.09416)); TutorBench ([arXiv](https://arxiv.org/abs/2510.02663)); PedagogicalRL unanimity ([HTML](https://arxiv.org/html/2505.15607v2)) | Medium: more reliable, explainable judge; aligns evaluation with the literature. | Low-medium |
| 9 | **Teacher-facing review loop**: transcript browser with diagnosis/policy/guard decisions, flags for fallbacks, guard trips and long stuck episodes; a quality dashboard of error/leak/fallback rates across releases. Also anonymise PII before LLM calls. | Khanmigo dashboard; Eedi human-in-the-loop ([Eedi](https://www.eedi.com/news/new-exploratory-research-from-eedi-and-google-deepmind-reveals-human-in-the-loop-ai-tutoring-outperforms-human-only-support)); CS50 anonymisation/endorsement ([PDF](https://cs.harvard.edu/malan/publications/V1fp0567-liu.pdf)); Tutor CoPilot | Medium: catches sheet errors and silent failures; builds instructor trust; GDPR compliance. | Medium |
| 10 | **Semi-automated sheet authoring + learner model**: LLM drafts sheets from course notes and solutions (steps, expectations, common errors, leak patterns, CAS checks), self-consistency verified, then professor edits; tag steps/errors with KCs and run BKT across exercises to set initial hint level and pick next exercise. | Ruffle&Riley script induction ([arXiv](https://arxiv.org/abs/2310.01420)); MWPTutor cached generation with checks; self-consistency in Pardos et al. ([SCALE](https://scale.stanford.edu/publications/chatgpt-generated-help-produces-learning-gains-equivalent-human-tutor-authored-help)); OATutor BKT ([repo](https://github.com/CAHLR/OATutor)); LLMKT ([arXiv](https://arxiv.org/abs/2409.16490v1)) | Medium-high for scale (authoring is the bottleneck for coverage of the course); medium for personalisation. | Medium-high |

Honourable mentions: best-of-2 generation before GUARD to cut rewrite loops (CodeHelp); per-action few-shot "golden" replies in REPLY (LearnLM golden conversations; Calculus I RAG + few-shot 93% Socratic compliance); a sufficiency gate asking the student to show work when the message is too vague (CodeHelp, SocraticAI); a crossover RCT in the course modelled on Kestin et al. ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12179260/)).

### B5. Things to avoid (lessons from the field)

- **Prompt-only control** (Study Mode, Mr. Ranedeer, SPL): easily bypassed ([Willison](https://simonwillison.net/2025/Jul/29/openai-introducing-study-mode)).
- **Fully cached utterances** without dialogue context: redundant hints in about a third of cases (MWPTutor cached variant, [HTML](https://arxiv.org/html/2402.09216v3)).
- **Leniency on partial expectation coverage** (Ruffle&Riley, [HTML](https://arxiv.org/html/2404.17460v1)).
- **Over-aggressive guards**: 16% false positives (NeMo in [arXiv 2605.06669](https://arxiv.org/pdf/2605.06669)) degrade pedagogy; monitor fallback rate.
- **Equating engagement or perceived helpfulness with learning** (Ruffle&Riley no gains vs reading; Khanmigo reports).
- **Trusting LLM judges as ground truth**: best BEA 2025 systems reach only 58-72 macro-F1 ([findings](https://arxiv.org/pdf/2507.10579)).
- **Optimising student success alone**: drives leakage toward the maximum (PedagogicalRL, [HTML](https://arxiv.org/html/2505.15607v2)).
