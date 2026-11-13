from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from pathlib import Path

path = Path(r'C:\Users\Collins\Python\FTEC5660\ind_proj_2\ftec5660-project2\A-MEM_Reproducibility_Report.docx')
doc = Document(path)
# avoid duplicate insertion
if any('Run-level aggregate scores' in p.text for p in doc.paragraphs):
    raise SystemExit('Run-level table already present')

rows = [
('Pilot, 17 turns','10','1',0.3750,0.570256,0.940957,0.727270),
('Pilot, 17 turns','10','2',0.3750,0.606959,0.945044,0.725946),
('Pilot, 17 turns','10','3',0.3750,0.586476,0.943156,0.724485),
('Pilot, 17 turns','10','4',0.3750,0.606959,0.944821,0.725611),
('Pilot, 17 turns','10','5',0.3750,0.600384,0.942823,0.732575),
('Pilot, 17 turns','5','1',0.3750,0.525092,0.934319,0.669878),
('Pilot, 17 turns','5','2',0.3750,0.552272,0.937965,0.692800),
('Pilot, 17 turns','5','3',0.5000,0.649497,0.950842,0.783445),
('Pilot, 17 turns','5','4',0.3750,0.545697,0.935890,0.679905),
('Pilot, 17 turns','5','5',0.3750,0.531789,0.934733,0.670112),
('Expanded, 67 turns','10','1',0.5000,0.628159,0.945534,0.739866),
('Expanded, 67 turns','10','2',0.5625,0.690659,0.953618,0.794145),
('Expanded, 67 turns','10','3',0.3750,0.471647,0.932104,0.595750),
('Expanded, 67 turns','10','4',0.4375,0.619735,0.946835,0.751258),
('Expanded, 67 turns','10','5',0.5625,0.691263,0.950274,0.797238),
('Expanded, 67 turns','5','1',0.5000,0.618842,0.946900,0.726367),
('Expanded, 67 turns','5','2',0.4375,0.632235,0.946300,0.752697),
('Expanded, 67 turns','5','3',0.5000,0.574588,0.938900,0.696820),
('Expanded, 67 turns','5','4',0.4375,0.576947,0.936500,0.672078),
('Expanded, 67 turns','5','5',0.4375,0.618613,0.945400,0.741652),
]

def shade(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = tcPr.find(qn('w:shd'))
    if shd is None:
        shd = OxmlElement('w:shd'); tcPr.append(shd)
    shd.set(qn('w:fill'), fill)

def borders(table):
    tblPr = table._tbl.tblPr
    b = tblPr.first_child_found_in('w:tblBorders')
    if b is None:
        b=OxmlElement('w:tblBorders'); tblPr.append(b)
    for edge in ('top','left','bottom','right','insideH','insideV'):
        el=b.find(qn('w:'+edge))
        if el is None: el=OxmlElement('w:'+edge); b.append(el)
        el.set(qn('w:val'),'single'); el.set(qn('w:sz'),'4'); el.set(qn('w:space'),'0'); el.set(qn('w:color'),'D9D9D9')

def set_cell_text(cell, text, bold=False, size=8.2, color=None, align=WD_ALIGN_PARAGRAPH.CENTER):
    cell.text=''
    p=cell.paragraphs[0]; p.alignment=align; p.paragraph_format.space_after=Pt(0); p.paragraph_format.space_before=Pt(0)
    r=p.add_run(str(text)); r.bold=bold; r.font.size=Pt(size)
    if color: r.font.color.rgb=RGBColor(*color)
    cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
    tcPr=cell._tc.get_or_add_tcPr()
    mar=tcPr.first_child_found_in('w:tcMar')
    if mar is None: mar=OxmlElement('w:tcMar'); tcPr.append(mar)
    for side in ('top','start','bottom','end'):
        e=mar.find(qn('w:'+side))
        if e is None: e=OxmlElement('w:'+side); mar.append(e)
        e.set(qn('w:w'),'70'); e.set(qn('w:type'),'dxa')

# insert after Table 3 caption paragraph
anchor = next(p for p in doc.paragraphs if p.text.startswith('Table 3. Mean'))
caption = OxmlElement('w:p')
anchor._p.addnext(caption)
cap_para = anchor._parent.add_paragraph()  # temporary paragraph object
# use the inserted element via Paragraph wrapper
from docx.text.paragraph import Paragraph
cap = Paragraph(caption, anchor._parent)
cap.style = doc.styles['Normal']
cap.paragraph_format.space_before = Pt(8); cap.paragraph_format.space_after = Pt(4)
run=cap.add_run('Table 4. Individual run-level aggregate scores for all 20 completed evaluations.'); run.bold=True; run.font.size=Pt(9)

# create table and move after caption
# create at end then relocate
table=doc.add_table(rows=1, cols=7)
table.alignment=WD_TABLE_ALIGNMENT.CENTER
table.autofit=False
headers=['Condition','k','Run','EM','Token F1','BERTScore F1','SBERT']
widths=[Inches(1.35),Inches(.38),Inches(.42),Inches(.75),Inches(.88),Inches(1.05),Inches(.78)]
for i,h in enumerate(headers):
    table.columns[i].width=widths[i]; set_cell_text(table.rows[0].cells[i], h, True, 8.0, (255,255,255)); shade(table.rows[0].cells[i],'365F91')
# repeat header
trPr=table.rows[0]._tr.get_or_add_trPr(); rep=OxmlElement('w:tblHeader'); rep.set(qn('w:val'),'true'); trPr.append(rep)
for idx,row in enumerate(rows, start=1):
    cells=table.add_row().cells
    vals=[row[0],row[1],row[2],f'{row[3]:.4f}',f'{row[4]:.4f}',f'{row[5]:.4f}',f'{row[6]:.4f}']
    for i,v in enumerate(vals):
        set_cell_text(cells[i],v,size=7.8,align=WD_ALIGN_PARAGRAPH.LEFT if i==0 else WD_ALIGN_PARAGRAPH.CENTER)
        if idx%2==0: shade(cells[i],'F2F6FA')
    for i,w in enumerate(widths): cells[i].width=w
borders(table)
# relocate table after caption
cap._p.addnext(table._tbl)
# Add explanatory note after table
note = OxmlElement('w:p'); table._tbl.addnext(note); np=Paragraph(note, anchor._parent); np.style=doc.styles['Normal']; np.paragraph_format.space_before=Pt(4); np.paragraph_format.space_after=Pt(6)
r=np.add_run('The table reports the aggregate score produced by each run. These rows expose the small-sample basis of the mean ± standard deviation summary; they are not independent conversation samples.'); r.italic=True; r.font.size=Pt(8)

doc.save(path)
print(path)
