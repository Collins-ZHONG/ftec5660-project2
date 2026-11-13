from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).parent
OUT = ROOT / "A-MEM_Reproducibility_Report.docx"
FIG = ROOT / "Figure" / "framework.jpg"
FLOW = ROOT / "experiment_workflow.png"

def draw_flow():
    w, h = 1800, 430
    im = Image.new("RGB", (w, h), "white")
    d = ImageDraw.Draw(im)
    try:
        font = ImageFont.truetype("arial.ttf", 24)
        small = ImageFont.truetype("arial.ttf", 19)
    except OSError:
        font = ImageFont.load_default()
        small = font
    items = [
        ("Dataset selection", "conv-26\nD2 / D2+D17+D18"),
        ("Memory construction", "A-MEM notes +\nembedding index"),
        ("Question answering", "16 fixed D2 questions\nretrieve k=10 or 5"),
        ("Five repeated runs", "Seeds 42-46\nshared cache per length"),
        ("Evaluation", "EM, Token F1,\nBERTScore, SBERT"),
    ]
    x0, bw, gap, by, bh = 35, 320, 37, 125, 180
    colors = ["#EAF2F8", "#E8F4F1", "#FFF4E5", "#F1ECF8", "#EAF4EA"]
    for i, (title, body) in enumerate(items):
        x = x0 + i * (bw + gap)
        d.rounded_rectangle((x, by, x + bw, by + bh), radius=12, fill=colors[i], outline="#536878", width=3)
        d.text((x + 18, by + 22), title, fill="#172B3A", font=font)
        d.multiline_text((x + 18, by + 79), body, fill="#334E5C", font=small, spacing=7)
        if i < len(items) - 1:
            ax = x + bw + 5
            d.line((ax, by + bh // 2, ax + gap - 10, by + bh // 2), fill="#526777", width=4)
            d.polygon([(ax + gap - 10, by + bh // 2), (ax + gap - 22, by + bh // 2 - 9), (ax + gap - 22, by + bh // 2 + 9)], fill="#526777")
    d.text((40, 355), "Two memory-length conditions are evaluated independently; k settings share the cache within each condition.", fill="#526777", font=small)
    im.save(FLOW, quality=95)

def shade(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tcPr.append(shd)

def set_repeat_table_header(row):
    trPr = row._tr.get_or_add_trPr()
    tblHeader = OxmlElement("w:tblHeader")
    tblHeader.set(qn("w:val"), "true")
    trPr.append(tblHeader)

def set_cell_text(cell, text, bold=False, color="20364A", size=9):
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(str(text))
    r.bold = bold
    r.font.name = "Aptos"
    r.font.size = Pt(size)
    r.font.color.rgb = RGBColor.from_string(color)
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER

def add_table(doc, headers, rows, widths=None, size=9):
    t = doc.add_table(rows=1, cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.style = "Table Grid"
    set_repeat_table_header(t.rows[0])
    for i, h in enumerate(headers):
        set_cell_text(t.rows[0].cells[i], h, True, "FFFFFF", size)
        shade(t.rows[0].cells[i], "204E68")
    for ri, row in enumerate(rows):
        cells = t.add_row().cells
        for i, value in enumerate(row):
            set_cell_text(cells[i], value, False, "20364A", size)
            if ri % 2 == 1:
                shade(cells[i], "F1F5F7")
    if widths:
        for row in t.rows:
            for i, width in enumerate(widths):
                row.cells[i].width = Inches(width)
    return t

def caption(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(9)
    r = p.add_run(text)
    r.italic = True
    r.font.size = Pt(8)
    r.font.color.rgb = RGBColor(85, 100, 110)

def body(doc, text, style=None):
    p = doc.add_paragraph(style=style)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.08
    p.add_run(text)
    return p

draw_flow()
doc = Document()
sec = doc.sections[0]
sec.top_margin = Inches(0.62)
sec.bottom_margin = Inches(0.62)
sec.left_margin = Inches(0.72)
sec.right_margin = Inches(0.72)

styles = doc.styles
normal = styles["Normal"]
normal.font.name = "Aptos"
normal.font.size = Pt(9.5)
normal.font.color.rgb = RGBColor(36, 51, 63)
normal.paragraph_format.space_after = Pt(5)
for name, size, color in [("Title", 27, "173A52"), ("Heading 1", 17, "173A52"), ("Heading 2", 12, "276678")]:
    s = styles[name]
    s.font.name = "Aptos Display"
    s.font.size = Pt(size)
    s.font.bold = True
    s.font.color.rgb = RGBColor.from_string(color)
    s.paragraph_format.space_before = Pt(11 if name != "Title" else 0)
    s.paragraph_format.space_after = Pt(5)
title_ppr = styles["Title"]._element.get_or_add_pPr()
title_border = title_ppr.find(qn("w:pBdr"))
if title_border is not None:
    title_ppr.remove(title_border)

# restrained running header and page number
hp = sec.header.paragraphs[0]
hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
hr = hp.add_run("FTEC5660  |  REPRODUCIBILITY REPORT")
hr.font.name = "Aptos"
hr.font.size = Pt(8)
hr.font.color.rgb = RGBColor(95, 112, 122)
fp = sec.footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
fr = fp.add_run("A-MEM LoCoMo subset study  •  ")
fr.font.size = Pt(8)
fld = OxmlElement("w:fldSimple")
fld.set(qn("w:instr"), "PAGE")
fp._p.append(fld)

p = doc.add_paragraph(style="Title")
p.add_run("A-MEM Reproducibility Study")
p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(15)
r = p.add_run("A small-scale LoCoMo evaluation with a retrieval-depth modification")
r.font.size = Pt(12)
r.font.color.rgb = RGBColor(82, 104, 118)

body(doc, "This report documents a bounded reproduction of A-MEM's public memory-based question-answering workflow and a controlled comparison of two retrieval settings. On one LoCoMo conversation and 16 fixed questions, retrieving k=10 seed memories produced slightly higher mean Token F1 in both memory-length conditions, while Exact Match was mixed in the shorter pilot. The findings are descriptive and do not establish a general advantage or reproduce the paper's full benchmark results.")

doc.add_heading("1. Project and Research Background", level=1)
body(doc, "Long conversations can scatter useful facts across many turns. A-MEM (Agentic Memory for LLM Agents) addresses this problem by turning experience into structured memory notes and organizing notes through links that can evolve as new information arrives. At query time, the system retrieves relevant notes and supplies them to an LLM agent. The design is inspired by Zettelkasten-style connected note taking (Xu et al., 2025).")
body(doc, "The reproduced workflow uses the authors' public implementation rather than rebuilding the method. It covers conversation ingestion, memory-note construction, embedding-based retrieval, linked-context expansion, answer generation, and answer scoring. The scope is intentionally limited to one conversation and a small fixed question set.")
doc.add_picture(str(FIG), width=Inches(6.8))
caption(doc, "Figure 1. A-MEM framework reproduced from the authors' public repository (Xu et al., 2025, Figure/framework.jpg). The original figure depicts note construction, link generation, memory evolution, and retrieval.")

heading2 = doc.add_heading("2. Reproduction Scope and Experimental Design", level=1)
heading2.paragraph_format.page_break_before = True
body(doc, "The target behavior was the successful execution of A-MEM's public LoCoMo memory-question-answering pipeline and its overall answer-matching behavior on a selected subset. The local modification was retrieval depth: the repository default retrieve_k=10 was compared with retrieve_k=5. The working hypothesis was that more retrieved seed memories might improve coverage of answer evidence, while also potentially introducing irrelevant context.")
body(doc, "This is a small-scale reproduction using one LoCoMo conversation (conv-26) and 16 original D2 questions. Because the question count is small and category counts are uneven, the analysis uses aggregate metrics only and makes no category-level comparisons. The study is not designed to test A-MEM's linked-memory mechanism against an ablation or competing memory system.")
add_table(doc, ["Condition", "Conversation turns", "Questions", "Memory cache"], [
    ["Pilot", "D2 (17)", "Same 16 original D2 questions", "One cache; shared across k and repeats"],
    ["Expanded", "D2 + D17 + D18 (67)", "Same 16 original D2 questions", "One separate cache; shared across k and repeats"],
], [1.0, 1.55, 2.05, 2.2], 8.5)
caption(doc, "Table 1. Data conditions and cache use.")

doc.add_picture(str(FLOW), width=Inches(6.8))
caption(doc, "Figure 2. Experimental workflow used in this study. Each condition was run with k=10 and k=5, with five repeated evaluations per setting.")

doc.add_heading("3. Experimental Environment and Procedure", level=1)
add_table(doc, ["Component", "Configuration"], [
    ["Code", "GitHub fork of ftec5660-project2; recorded revision f9a173dec325d84fcc97e7828775c7b241c33466"],
    ["Runtime", "Windows PowerShell; Python 3.11.4 in project-local virtual environment"],
    ["LLM", "DeepSeek API, OpenAI-compatible client; model deepseek-chat; base URL https://api.deepseek.com"],
    ["Embeddings", "Sentence Transformers all-MiniLM-L6-v2"],
    ["Evaluation", "Repository test_advanced_robust.py and robust memory layer; ratio=1.0"],
    ["Runs", "Five paired repetitions per condition and k; seeds 42-46. The seed affects category-5 option ordering only."],
    ["Decoding", "Category 5 temperature 0.5; other answer categories use script setting 0.7."],
    ["Key packages", "openai 3.46.0; sentence-transformers 6.2.0; torch 2.15.0; numpy 2.4.6; scikit-learn 1.9.1; bert-score 0.3.13"],
], [1.2, 5.6], 8.2)
caption(doc, "Table 2. Recorded local environment. The repository requirements are not version-pinned; the list is the inspected environment, not a complete lockfile.")
body(doc, "For each condition, the script builds memory notes and a sentence-embedding index. For each question it generates query keywords, retrieves the top-k seed notes, expands context through linked neighbors, and generates an answer. Exact Match (EM), Token F1, BERTScore F1, and SBERT similarity are then evaluated against the supplied reference answers. The five run-level aggregate scores for each metric and setting are summarized using the mean and sample standard deviation.")

doc.add_heading("4. Results", level=1)
add_table(doc, ["Memory condition", "k", "Exact Match", "Token F1", "BERTScore F1", "SBERT similarity"], [
    ["Pilot, 17 turns", "10", "0.3750 ± 0.0000", "0.5942 ± 0.0158", "0.9434 ± 0.0017", "0.7272 ± 0.0032"],
    ["Pilot, 17 turns", "5", "0.4000 ± 0.0559", "0.5609 ± 0.0507", "0.9387 ± 0.0069", "0.6992 ± 0.0480"],
    ["Expanded, 67 turns", "10", "0.4875 ± 0.0815", "0.6203 ± 0.0896", "0.9457 ± 0.0090", "0.7357 ± 0.0822"],
    ["Expanded, 67 turns", "5", "0.4625 ± 0.0342", "0.6042 ± 0.0266", "0.9406 ± 0.0046", "0.7179 ± 0.0331"],
], [1.25, 0.38, 1.05, 1.05, 1.25, 1.25], 8.0)
caption(doc, "Table 3. Mean ± sample standard deviation across five repeated runs. Standard deviations describe run-to-run variability in aggregate scores, not variation across independent questions or datasets.")
body(doc, "In the 17-turn pilot, k=10 had higher mean Token F1, BERTScore F1, and SBERT similarity, while k=5 had a slightly higher mean Exact Match. In the 67-turn condition, k=10 had higher means on all four metrics. The Token F1 difference was small in both conditions (0.033 in the pilot and 0.016 in the expanded condition), and run-to-run variability is material relative to these differences. This provides limited descriptive support for the local hypothesis that retrieving more seed memories may help overall answer matching in this subset; it does not show that k=10 is generally better.")
body(doc, "All four means were higher in the 67-turn condition than in the 17-turn condition at both k values. This is an observed contrast between two separately constructed caches. Since the study has one conversation, a fixed question set, and one cache per condition, it cannot attribute the difference to the added turns or claim that more text caused better performance.")
body(doc, "Aggregate metrics are used because the 16 questions are unevenly distributed across categories, with some categories represented by only one or two items and one category absent. A single response could dominate a small category score. Repeating model calls does not create new questions or independent conversations, so category-level findings would be unstable and are not reported.")

doc.add_heading("5. Comparison with the Original Study", level=1)
body(doc, "The reproduction is consistent with the paper at the workflow level: conversational experience is organized into memory notes, retrieved for a later question, and used to produce an answer. It also follows the public implementation's memory, retrieval, and evaluation path for the selected subset. The local parameter comparison is compatible with the paper's practical observation that retrieval settings matter, but it is not a direct test of the paper's central method claim.")
body(doc, "Numerical agreement with the paper cannot be assessed. The original study evaluates broader benchmark settings with its own models and experimental protocol; this report uses a single conversation, 16 questions, DeepSeek deepseek-chat, and a robust repository script. It also compares k values within A-MEM rather than comparing A-MEM with alternative memory systems. Therefore, the numbers should not be presented as either a successful or failed numerical reproduction of the paper's headline results.")
body(doc, "The k=10/k=5 comparison is the study's measurable modification. It is isolated within each memory condition, while data, questions, model provider, embedding model, prompts, and evaluation implementation are held constant. The modification changes retrieval depth only; it does not remove or alter A-MEM's memory-linking or evolution components.")

doc.add_heading("6. Main Practical Issues", level=1)
body(doc, "The API backend required an OpenAI-compatible configuration with the DeepSeek endpoint and model ID. Credentials were kept in a process environment variable and are not included in this report or repository. Package and embedding-model access depended on network connectivity; transient request delays also required rerunning an incomplete evaluation. Successful result files were retained for the five-run summaries. These issues affected execution time but do not change the definition of the completed comparisons.")

doc.add_heading("7. Conclusions", level=1)
body(doc, "This study ran a selected A-MEM public workflow on a LoCoMo subset and measured the effect of changing the retrieval count from k=10 to k=5. Across five repeated runs on one conversation and 16 fixed questions, k=10 had higher mean Token F1 in both memory conditions; the Exact Match direction differed in the pilot and expanded conditions. The evidence suggests a small, context-dependent retrieval-depth effect, not a universal ranking.")
body(doc, "The higher means in the expanded condition are descriptive and do not establish that adding conversation turns improves memory performance. The reproduction confirms that the selected public pipeline can construct memory, retrieve linked context, answer questions, and produce aggregate evaluation outputs under a DeepSeek backend. It does not establish the original paper's full benchmark results or verify the causal contribution of linked memory evolution, because no ablation or competing memory baseline was run.")

doc.add_heading("References", level=1)
refp = body(doc, "Xu, W., Liang, Z., Mei, K., Gao, H., Tan, J., & Zhang, Y. (2025). A-Mem: Agentic Memory for LLM Agents. Advances in Neural Information Processing Systems. https://github.com/WujiangXu/A-mem  |  Maharana, A., et al. (2024). Evaluating very long-term conversational memory of LLM agents. Proceedings of ACL. https://github.com/snap-research/locomo")
refp.paragraph_format.space_after = Pt(0)
for run in refp.runs:
    run.font.size = Pt(8)

doc.add_heading("8. Discussion and Reflection", level=1)
body(doc, "")
doc.add_paragraph().paragraph_format.space_after = Pt(0)

doc.core_properties.title = "A-MEM Reproducibility Study"
doc.core_properties.subject = "Small-scale LoCoMo reproduction and retrieval-depth comparison"
doc.core_properties.author = "FTEC5660"
doc.save(OUT)
print(OUT)
