from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# 한글 폰트 등록
font_paths = [
    '/usr/share/fonts/truetype/nanum/NanumGothic.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
]
font_name = 'DejaVuSans'
for fp in font_paths:
    if os.path.exists(fp):
        fname = os.path.basename(fp).replace('.ttf','')
        pdfmetrics.registerFont(TTFont(fname, fp))
        font_name = fname
        break

styles = getSampleStyleSheet()
title_style = ParagraphStyle('Title', fontName=font_name, fontSize=16, spaceAfter=6, textColor=colors.HexColor('#1a237e'), leading=20)
h1_style = ParagraphStyle('H1', fontName=font_name, fontSize=13, spaceAfter=4, textColor=colors.HexColor('#283593'), leading=16)
h2_style = ParagraphStyle('H2', fontName=font_name, fontSize=11, spaceAfter=3, textColor=colors.HexColor('#1565c0'), leading=14)
normal_style = ParagraphStyle('Normal', fontName=font_name, fontSize=9, spaceAfter=3, leading=13)
correct_style = ParagraphStyle('Correct', fontName=font_name, fontSize=9, spaceAfter=3, leading=13, textColor=colors.HexColor('#2e7d32'))
wrong_style = ParagraphStyle('Wrong', fontName=font_name, fontSize=9, spaceAfter=3, leading=13, textColor=colors.HexColor('#c62828'))
note_style = ParagraphStyle('Note', fontName=font_name, fontSize=9, spaceAfter=3, leading=13, textColor=colors.HexColor('#e65100'), backColor=colors.HexColor('#fff3e0'))

entries = [
    {
        'q_num': 'Q6',
        'chapter': 'Ch2 — 단채널 효과',
        'question': '채널 길이 L을 절반으로 줄였을 때 DIBL, 속도 포화, 서브스레숄드 스윙 S의 변화',
        'result': '부분 정답',
        'my_answer': 'DIBL: Vth 감소 (Drain 영향이 Source까지 미침). 속도 포화: 단채널에서 Ids가 (Vgs-Vt)에 선형 비례. S 변화: 미답',
        'correct_answer': (
            '1. DIBL: L 감소 -> Drain 공핍층이 Source 장벽에 영향 -> Vth 감소\n'
            '2. 속도 포화: 단채널에서 전기장 강해짐 -> vsat 도달 -> Ids가 (Vgs-Vt)^2에서 (Vgs-Vt)로 선형화. '
            'Vgs 대비 전류 효율 저하 (최대 Ids 절대값 감소가 아닌 증가율 둔화)\n'
            '3. S 변화: DIBL로 n 증가 -> S = (kT/q)ln(10)*n 증가 -> 누설 전류 제어 어려워짐'
        ),
        'key_concept': 'S = (kT/q) * ln(10) * n >= 60mV/dec. 채널 단축시 n 증가로 S 악화',
    },
    {
        'q_num': 'Q7',
        'chapter': 'Ch4 — Logical Effort Path 계산',
        'question': 'NAND2 -> NOR2 -> INV 경로에서 PE, 최적 단수 N, f-hat, 각 단 Cin 계산 (Wi -> 27Wi)',
        'result': '정답',
        'my_answer': 'PE = 59.94, N = 3단, f-hat = 3.86. Cin_inv = 6.99, Cin_nor = 3.02, Cin_nand = 1.04',
        'correct_answer': (
            'G = 1 x 4/3 x 5/3 x 1 = 20/9 = 2.22\n'
            'EF = 27/1 = 27, B = 1\n'
            'PE = 2.22 x 27 = 59.94\n'
            'N = log4(59.94) = 2.95 -> 3단\n'
            'f-hat = 59.94^(1/3) = 3.86\n'
            '뒤에서 앞으로: Cin_inv = 27/3.86 = 6.99, Cin_nor = (6.99 x 5/3)/3.86 = 3.02, '
            'Cin_nand = (3.02 x 4/3)/3.86 = 1.04 ≈ Wi (입력과 일치 확인)'
        ),
        'key_concept': '뒤에서 앞으로 Cin 계산: Cin_i = (Cout_i x LE_i) / f-hat. 최종값이 Wi와 일치하는지 검증 필수',
    },
    {
        'q_num': 'Q8',
        'chapter': 'Ch6 — Pulsed Latch Time Borrowing',
        'question': 'Tc=10ns, tsetup=0.5ns, Tpw=2ns. 최대 tpd 증가량, Hold 조건 강화, Tpw 무한대 불가 이유',
        'result': '부분 정답',
        'my_answer': '1. 2ns. 2. tcd > thold - tccq + Tpw. 3. Hold time 위반 위험만 언급',
        'correct_answer': (
            '1. Tpw = 2ns만큼 tpd 허용량 증가\n'
            '2. tcd >= thold - tccq + Tpw (Hold 조건 강화)\n'
            '3. Tpw 무한대 불가 이유:\n'
            '   - Hold 조건이 극도로 강화되어 tcd를 무한히 크게 할 수 없음\n'
            '   - 투명 구간이 길어지면 더블 샘플링 문제 재발\n'
            '   - tborrow 물리적 상한: tborrow_max = Tc/2 - tsetup = 4.5ns'
        ),
        'key_concept': 'Tpw가 클수록 느린 경로에 유리하지만 빠른 경로 Hold 위반 위험 증가. 상한 = Tc/2 - tsetup',
    },
    {
        'q_num': 'Q9',
        'chapter': 'Ch7 — 다이나믹 회로 전하 공유',
        'question': 'C2=100fF(VDD), C1=50fF(0V). 전하 공유 후 출력 전압 계산 및 해결책',
        'result': '정답',
        'my_answer': 'V(출력) = 100/(100+50) * VDD = 0.667 * 1.8 = 1.2V. 해결책: C1도 프리차지',
        'correct_answer': (
            'V(X2) = VDD * C2/(C1+C2) = 1.8 * 100/150 = 1.2V\n'
            '전압 강하 = 0.6V. 인버터 트립 전압(≈VDD/2 = 0.9V) 이상이므로 오동작 없음.\n'
            '단 더 큰 C1이거나 VDD가 낮으면 트립 전압 아래로 떨어져 오동작.\n'
            '해결책: 프리차지 구간(CLK=0)에 C1 노드에도 약한 PMOS 연결 -> VDD로 충전\n'
            '-> 평가시 C1=C2=VDD이므로 전압 변화 없음'
        ),
        'key_concept': '전하 공유 수식: V(X2) = VDD * C2/(C1+C2). 내부 노드 프리차지로 해결',
    },
    {
        'q_num': 'Q10',
        'chapter': 'Ch8 — DRAM vs eDRAM Gain Cell',
        'question': '조건A(CPU 다이, 읽기 빈번) vs 조건B(독립칩, 최대 용량) 메모리 선택',
        'result': '정답',
        'my_answer': 'A: eDRAM Gain Cell (비파괴 읽기, 복원 불필요). B: DRAM (트랜지스터 적어 면적 유리)',
        'correct_answer': (
            'A -> eDRAM Gain Cell:\n'
            '   - 읽기/쓰기 경로 분리 -> 비파괴 읽기 -> 복원 불필요 -> 읽기 지연 감소\n'
            '   - PMOS 게이트 누설 < NMOS 기판 누설 -> 리프레시 주기 연장\n'
            '   - CPU와 같은 다이 -> 통신 지연 최소화\n'
            'B -> DRAM(1T-1C):\n'
            '   - 셀당 1T+1C -> 최소 면적 -> 최대 집적도\n'
            '   - Gain Cell(3T)은 동일 면적에 1/3 용량'
        ),
        'key_concept': 'Gain Cell 장점: 비파괴 읽기, 낮은 누설. DRAM 장점: 최소 면적(1T-1C)',
    },
]

doc = SimpleDocTemplate(
    '/home/claude/오답노트.pdf',
    pagesize=A4,
    leftMargin=15*mm, rightMargin=15*mm,
    topMargin=15*mm, bottomMargin=15*mm
)

story = []
story.append(Paragraph('디지털 집적회로 — 오답노트', title_style))
story.append(Paragraph('삼성 DS System Expert Course | 서울대 김재준 교수', normal_style))
story.append(HRFlowable(width='100%', thickness=2, color=colors.HexColor('#1a237e')))
story.append(Spacer(1, 4*mm))

for e in entries:
    # 문제 헤더
    result_color = '#2e7d32' if e['result'] == '정답' else '#e65100' if e['result'] == '부분 정답' else '#c62828'
    story.append(Paragraph(
        f"<font color='{result_color}'>[{e['result']}]</font>  {e['q_num']} — {e['chapter']}",
        h1_style
    ))
    story.append(Paragraph(f"<b>문제:</b> {e['question']}", normal_style))
    story.append(Spacer(1, 2*mm))

    # 내 답변
    story.append(Paragraph('<b>내 답변:</b>', h2_style))
    story.append(Paragraph(e['my_answer'], normal_style))
    story.append(Spacer(1, 1*mm))

    # 정답/보완
    story.append(Paragraph('<b>정답 및 보완:</b>', h2_style))
    for line in e['correct_answer'].split('\n'):
        story.append(Paragraph(line if line else ' ', normal_style))
    story.append(Spacer(1, 1*mm))

    # 핵심 개념
    story.append(Paragraph(f"<b>핵심 개념:</b> {e['key_concept']}", note_style))
    story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#90caf9')))
    story.append(Spacer(1, 3*mm))

doc.build(story)
print('PDF 생성 완료')
