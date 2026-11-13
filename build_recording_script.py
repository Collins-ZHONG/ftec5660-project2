from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

OUT = Path(__file__).parent / "A-MEM_Recording_Script.docx"
doc = Document()
sec = doc.sections[0]
sec.top_margin = Inches(0.72)
sec.bottom_margin = Inches(0.7)
sec.left_margin = Inches(0.85)
sec.right_margin = Inches(0.85)
normal = doc.styles["Normal"]
normal.font.name = "Aptos"
normal.font.size = Pt(10.5)
normal.font.color.rgb = RGBColor(35, 49, 60)
normal.paragraph_format.space_after = Pt(7)
normal.paragraph_format.line_spacing = 1.12
for nm, sz, col in [("Title", 27, "173A52"), ("Heading 1", 16, "173A52")]:
    st = doc.styles[nm]
    st.font.name = "Aptos Display"
    st.font.size = Pt(sz)
    st.font.bold = True
    st.font.color.rgb = RGBColor.from_string(col)
    st.paragraph_format.space_before = Pt(10)
    st.paragraph_format.space_after = Pt(4)
title_ppr = doc.styles["Title"]._element.get_or_add_pPr()
border = title_ppr.find(qn("w:pBdr"))
if border is not None:
    title_ppr.remove(border)

hp = sec.header.paragraphs[0]
hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
r = hp.add_run("FTEC5660  |  VIDEO PRESENTATION SCRIPT")
r.font.size = Pt(8)
r.font.color.rgb = RGBColor(100, 115, 125)
fp = sec.footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = fp.add_run("A-MEM LoCoMo reproduction  |  ")
r.font.size = Pt(8)
fld = OxmlElement("w:fldSimple")
fld.set(qn("w:instr"), "PAGE")
fp._p.append(fld)

p = doc.add_paragraph(style="Title")
p.add_run("A-MEM Reproducibility Presentation")
p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(12)
r = p.add_run("Recording script and screen cues | approximately 9-11 minutes")
r.font.size = Pt(12)
r.font.color.rgb = RGBColor(82, 104, 118)
p = doc.add_paragraph()
r = p.add_run("Recording note. ")
r.bold = True
r.font.color.rgb = RGBColor(39, 102, 120)
p.add_run("The spoken text is in English. Bracketed screen cues are not read aloud. Keep API keys, credential-bearing environment variables, and private account details off screen.")

sections = [
    ("0:00-0:50 | Opening", "[Show the title slide or the first page of the report.]", "Hello. This presentation describes my small-scale reproduction of A-MEM, an agentic memory system for large language model agents. I ran the authors' public implementation on a selected subset of the LoCoMo conversational memory benchmark, then made one measurable change: I compared retrieval depth k equals ten with k equals five. The goal was to check what part of the workflow I could reproduce, measure the effect of this parameter change, and explain why my results should not be treated as a numerical replication of the full paper."),
    ("0:50-2:00 | Project and target", "[Show the project GitHub repository and the A-MEM framework figure in the report.]", "A-MEM addresses a practical problem: useful information in a long interaction may be spread across many conversation turns. The system converts interactions into structured memory notes, connects related notes, and can update existing memories as new information arrives. For a later question, it retrieves relevant memories and gives them to an LLM agent as context. This approach is inspired by connected note-taking systems such as Zettelkasten.\n\nI used the authors' public code rather than implementing the method from scratch. My reproduction target was the observable workflow: building memories from conversation data, retrieving memory for a question, generating an answer, and evaluating that answer against the provided reference. This is a bounded reproduction of one implementation path, not the full set of experiments in the paper."),
    ("2:00-3:15 | Data and experimental design", "[Show Table 1 and Figure 2 in the report.]", "I selected one conversation, conv-26, from LoCoMo. The pilot condition contains the D2 portion, which has 17 turns. The expanded condition contains D2, D17, and D18, for 67 turns in total. Both conditions use the same 16 original questions from D2. I did not rewrite the questions or reference answers.\n\nFor each condition, I compared the repository's default retrieval setting, k equals ten, with k equals five. I ran each setting five times. Within each memory-length condition, the k settings and repeated evaluations shared the same constructed memory cache. The two data conditions had separate caches. The repeated runs used seeds 42 through 46, although the seed only controls the answer-option ordering for one question category; it does not make the LLM's complete generation deterministic.\n\nBecause this is one conversation with only 16 questions, and the question categories are unevenly represented, I report aggregate results only. I do not draw category-level conclusions."),
    ("3:15-4:25 | Environment and method", "[Show Table 2. If appropriate, briefly show the evaluation command without displaying the terminal history or credentials.]", "The experiments ran on Windows from PowerShell, using Python 3.11.4 in a project virtual environment. The language model backend was DeepSeek's OpenAI-compatible API with the deepseek-chat model. The embedding model was all-MiniLM-L6-v2 from Sentence Transformers. I used the repository's robust evaluation script and memory layer.\n\nFor each memory condition, the system first constructs memory notes and an embedding index. For each question, it generates query keywords, retrieves the top k seed memories, expands the context through linked neighbors, and asks the language model to generate an answer. The evaluation reports Exact Match, Token F1, BERTScore F1, and SBERT similarity. I summarize the five run-level aggregate scores for each setting using a mean and sample standard deviation. These standard deviations describe variation across repeated runs on the same questions; they are not confidence intervals over independent datasets."),
    ("4:25-6:30 | Results", "[Show Table 3 in the report. Pause briefly so the audience can read the four rows.]", "Here are the results. In the 17-turn pilot, k equals ten has a higher mean Token F1 than k equals five: 0.594 compared with 0.561. It also has higher BERTScore F1 and SBERT similarity. Exact Match goes in the other direction, with 0.375 for k equals ten and 0.400 for k equals five. That Exact Match difference is small.\n\nIn the 67-turn condition, k equals ten has higher means on all four reported metrics. The Token F1 means are 0.620 for k equals ten and 0.604 for k equals five. The difference is modest, and the run-to-run variation is meaningful relative to the size of the difference.\n\nSo the result offers limited descriptive support for the local hypothesis that retrieving more seed memories may help answer matching in this subset. It does not establish that k equals ten is generally better. More retrieved memories could increase the chance of including useful evidence, but they could also add irrelevant context. I did not measure evidence recall or context noise, so I cannot verify that mechanism.\n\nThe 67-turn condition has higher means than the 17-turn pilot for both k values. This is an observation, not evidence that adding more conversation turns caused the scores to improve. The two conditions use separately constructed memory caches, and the study is limited to one conversation and one fixed question set."),
    ("6:30-7:45 | Comparison with the paper and modification", "[Show the section comparing the reproduction with the original study.]", "The reproduction is consistent with A-MEM at the workflow level: conversation experience is organized into memories, retrieved for later questions, and used to generate answers. The measurable modification was retrieval depth, comparing k equals ten with k equals five while holding the question set, model backend, embedding model, and evaluation implementation constant within each data condition.\n\nI cannot claim numerical agreement with the paper. The paper evaluates broader benchmark settings using its own models and experimental protocol. My study uses one conversation, 16 questions, DeepSeek, and a robust script from the public repository. I also did not compare A-MEM with other memory systems or disable its linking and evolution components. Therefore, this experiment does not establish the full benchmark performance or test whether linked memory evolution itself causes an improvement."),
    ("7:45-8:40 | Practical issues", "[Show the setup notes or the README. Do not reveal credential values.]", "The main practical setup issue was configuring an OpenAI-compatible client for the DeepSeek endpoint and model ID. The API credential was kept in a local process environment and was not committed to the repository. Package installation and access to the embedding model depended on network connectivity. Some API requests timed out, so incomplete runs had to be rerun; only completed runs were included in the five-run summaries. These issues affected the time needed to run the experiments, but the final comparisons use the completed result files."),
    ("8:40-9:40 | Conclusion and recommendation", "[Return to the conclusion slide or report summary.]", "To conclude, I successfully ran a selected A-MEM public workflow on a LoCoMo subset and measured a retrieval-depth change. Across five repeated runs, k equals ten had higher mean Token F1 in both memory conditions, while the Exact Match comparison was mixed. The evidence supports a small, context-dependent trend, not a general ranking of the two settings.\n\nThis work shows that the selected pipeline can construct memory, retrieve linked context, answer questions, and produce aggregate evaluation metrics using a hosted LLM API. It does not reproduce the paper's full numerical results or verify the causal contribution of A-MEM's memory-linking mechanism. For future users, I recommend starting with a small subset, validating the API endpoint with a minimal request, keeping credentials outside the repository, and saving each completed run separately. Thank you.")
]

for heading, cue, speech in sections:
    doc.add_heading(heading, level=1)
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(cue)
    r.italic = True
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(39, 102, 120)
    for part in speech.split("\n\n"):
        p = doc.add_paragraph(part)
        p.paragraph_format.keep_together = True

doc.core_properties.title = "A-MEM Reproducibility Presentation Script"
doc.core_properties.subject = "English recording script with screen cues for a 15-minute course presentation"
doc.core_properties.author = "FTEC5660"
doc.save(OUT)
print(OUT)
