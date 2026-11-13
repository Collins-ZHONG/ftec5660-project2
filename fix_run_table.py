from docx import Document
from pathlib import Path
p=Path(r'C:\Users\Collins\Python\FTEC5660\ind_proj_2\ftec5660-project2\A-MEM_Reproducibility_Report.docx')
d=Document(p)
t=next(t for t in d.tables if len(t.rows)==21 and len(t.columns)==7)
vals=[0.9434054754674435,0.9540413580834866,0.9322419874370098,0.9447815380990505,0.953898262232542,0.9438297487795353,0.9453752599656582,0.9397729001939297,0.9335256442427635,0.9405632875859737]
for i,v in enumerate(vals, start=11):
    t.rows[i].cells[5].text=f'{v:.4f}'
    for r in t.rows[i].cells[5].paragraphs[0].runs: r.font.size=__import__('docx').shared.Pt(7.8)
d.save(p)
print(p)
