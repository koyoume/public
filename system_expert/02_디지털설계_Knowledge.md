# 디지털 집적회로 (Digital Integrated Circuits) — 오픈북 시험 대비 정리

> 삼성 DS System Expert Course | 서울대 김재준 교수 | 최종 업데이트: 2026-03-23

---

## ① 수식 모음

| 분류 | 수식 | 변수 설명 |
|------|------|-----------|
| **[Ch2] 캐리어 농도** | np = ni² | n: 전자 농도, p: 정공 농도, ni: 진성 캐리어 농도 |
| **[Ch2] N형 캐리어** | n ≈ Nd, p = ni²/Nd | Nd: 도너 농도 |
| **[Ch2] P형 캐리어** | p ≈ Na, n = ni²/Na | Na: 억셉터 농도 |
| **[Ch2] 공핍층 두께** | Wd = √(2εsi·φs / qNA) | εsi: Si 유전율, φs: 표면전위, NA: 기판 도핑 |
| **[Ch2] 반전 전하** | Qinv = Cox(Vg − VTH) | Cox: 단위면적 산화막 커패시턴스 |
| **[Ch2] 문턱 전압** | VTH = VFB + 2φF + √(2εsi·qNA·2φF) / Cox | VFB: 플랫밴드 전압, φF: 페르미 전위 |
| **[Ch2] 다이오드 I-V** | I = I₀(e^(qV/kT) − 1) | I₀: 역포화 전류, kT/q ≈ 26mV (상온) |
| **[Ch2] 선형 영역 Ids** | Ids = μnCox(W/L)[(Vgs−Vt)Vds − Vds²/2] | μn: 전자 이동도, W/L: 폭/채널길이 비 |
| **[Ch2] 포화 영역 Ids** | Ids = ½μnCox(W/L)(Vgs−Vt)² | 조건: Vds > Vgs−Vt |
| **[Ch2] 채널길이 변조** | Ids = ½μnCox(W/L)(Vgs−Vt)²(1+λVds) | λ: 채널길이 변조 계수 |
| **[Ch2] 서브스레숄드 스윙** | S = (kT/q)·ln(10)·n ≥ 60 mV/dec | 이론적 최솟값 60 mV/decade (300K) |
| **[Ch3] 노이즈 마진 H** | NMH = VOH − VIH | VOH: 출력 HIGH 최솟값, VIH: 입력 HIGH 최솟값 |
| **[Ch3] 노이즈 마진 L** | NML = VIL − VOL | VIL: 입력 LOW 최댓값, VOL: 출력 LOW 최댓값 |
| **[Ch3] 동적 전력** | P = CL·VDD²·f | CL: 부하 커패시턴스, f: 동작 주파수 |
| **[Ch3] 정적 전력** | Pleak = Ileak·VDD | Ileak: 누설 전류 |
| **[Ch3] 전파 지연** | tp = 0.69·CL·(Rp+Rn)/2 | Rp: PMOS ON 저항, Rn: NMOS ON 저항 |
| **[Ch3] Pull-up 지연** | tpLH = 0.69·Rp·CL | 출력 0→1 |
| **[Ch3] Pull-down 지연** | tpHL = 0.69·Rn·CL | 출력 1→0 |
| **[Ch4] 게이트 지연** | td = td0·(p + LE×f) | p: 기생 지연, LE: 논리적 노력, f: 전기적 팬아웃 |
| **[Ch4] 팬아웃** | f = Cout/Cin | 출력 커패시턴스 / 입력 커패시턴스 |
| **[Ch4] Path Effort** | PE = G × B × EF | G: Path LE 곱, B: 분기 노력, EF: Cout/Cin |
| **[Ch4] Path 최소 지연** | D = N·td0·PE^(1/N) + P | N: 단수, P: 총 기생 지연 |
| **[Ch4] 최적 단수** | N = log₄(PE) | 단당 최적 effort ≈ 4 (γ=1 시 ≈ 3.6) |
| **[Ch4] 최적 단당 effort** | f̂ = PE^(1/N) | |
| **[Ch4] 분기 노력** | b = (Con-path + Coff-path) / Con-path | |
| **[Ch5] 배선 저항** | R = R□ × (L/W) | R□ = ρ/H: 면저항 (Ω/□) |
| **[Ch5] 평행판 커패시턴스** | C = εdi·WL/T | εdi: 유전체 유전율, T: 절연층 두께 |
| **[Ch5] Elmore 지연** | TDi = Σk Rki·Ck | Rki: 소스→i와 소스→k 공통 경로 저항 |
| **[Ch5] 분산 RC 지연** | t = RC/2 | R: 총 배선 저항, C: 총 배선 커패시턴스 |
| **[Ch5] 배선 지연 의존성** | twire ∝ L² | L: 배선 길이 (Rw∝L, Cw∝L) |
| **[Ch5] 최적 리피터 크기** | Wopt = √(Rinv·Cw / Rw·Cinv) | |
| **[Ch5] 최적 리피터 수** | Nopt = √(Rw·Cw / 2Rinv·Cinv) | |

---

## ② 핵심 비교표

### NMOS vs PMOS

| 항목 | NMOS | PMOS |
|------|------|------|
| 기판 | P형 | N형 |
| 주 캐리어 | 전자 (Electron) | 정공 (Hole) |
| 채널 형성 조건 | Vgs > VTH (Gate HIGH) | Vgs < VTH (Gate LOW) |
| ON 조건 (디지털) | Gate = 1 | Gate = 0 |
| 이동도 | μn (높음) | μp ≈ μn/2 (낮음) |
| 회로 역할 | Pull-down Network | Pull-up Network |
| 기호 | 동그라미 없음 | Gate에 동그라미 |

### CMOS 게이트 Logical Effort 비교

| 게이트 | 입력 커패시턴스 Cin | LE (입력당) | 기생 지연 p |
|--------|-------------------|-------------|------------|
| 인버터 | 3Cg (PMOS 2W + NMOS W) | 1 | 1 |
| NAND2 | 4Cg (PMOS 2W + NMOS 2W) | 4/3 ≈ 1.33 | 2 |
| NOR2 | 5Cg (PMOS 4W + NMOS W) | 5/3 ≈ 1.67 | 2 |
| NAND3 | 5Cg | 5/3 | 3 |
| NOR3 | 7Cg | 7/3 | 3 |

### 배선 RC 모델 비교

| 모델 | 구조 | Elmore 지연 | 평가 |
|------|------|------------|------|
| 분산 RC (실제) | N개 직렬 분할 | RC/2 | 기준 |
| L형 | R → C | RC | ❌ 2배 과대평가, 사용 금지 |
| π형 | C/2 → R → C/2 | RC/2 | ✅ |
| T형 | R/2 → C → R/2 | RC/2 | ✅ |

### NMOS 동작 영역 비교

| 영역 | 조건 | 전류 수식 | 특징 |
|------|------|-----------|------|
| 차단 (Off) | Vgs < Vt | Ids ≈ 0 (누설만) | 스위치 OFF |
| 선형 (Linear) | Vgs−Vt > Vds | μnCox(W/L)[(Vgs−Vt)Vds − Vds²/2] | 저항처럼 동작 |
| 포화 (Saturation) | Vds > Vgs−Vt | ½μnCox(W/L)(Vgs−Vt)² | Vds와 무관 |

### 단채널 효과 비교

| 효과 | 원인 | 결과 | 심해지는 조건 |
|------|------|------|--------------|
| VTH roll-off | Source/Drain 공핍층이 채널 분담 | VTH 감소 | L↓ |
| DIBL | Drain 전위가 Source 장벽에 영향 | VDS 증가 시 VTH 추가 감소 | L↓, VDS↑ |
| 속도 포화 | 전기장 강해져 전자속도 vsat 도달 | Ids ∝ (Vgs−Vt) 선형화 | L↓ |
| 서브스레숄드 누설 | OFF여도 지수함수적 전류 | 정적 전력 증가 | Vt↓, T↑ |

### 배선 종류 비교

| 구분 | 로컬 배선 (Local) | 글로벌 배선 (Global) |
|------|-----------------|---------------------|
| 용도 | 블록 내부 게이트 연결 | 멀리 떨어진 블록 연결 |
| 공정 스케일링 | 함께 작아짐 ✅ | 길이 유지 ❌ |
| 지연 추세 | 공정 발전 시 개선 | 저항 증가로 악화 가능 |
| 리피터 필요성 | 불필요 | 주요 대상 ★ |

---

## ③ 용어 정의 (가나다순)

| 용어 | 영문 | 정의 |
|------|------|------|
| 가전자 밴드 | Valence Band | 원자에 묶인 전자가 있는 에너지 밴드. 최상단 = Ev |
| 공핍 영역 | Depletion Region | PN 접합에서 캐리어가 사라지고 이온만 남은 영역 |
| 공핍층 커패시턴스 | Depletion Capacitance (Cd) | 공핍층 폭에 의해 결정되는 커패시턴스 |
| 기생 지연 | Parasitic Delay (p) | 부하가 0이어도 존재하는 고유 지연. 접합 커패시턴스 기인 |
| 기생 커패시턴스 | Parasitic Capacitance | 트랜지스터 Source/Drain 접합 커패시턴스. 지연 증가 원인 |
| 내장 전위 | Built-in Potential (Vbi) | PN 접합 평형 시 자연 형성되는 전위차 |
| 논리적 노력 | Logical Effort (LE) | 게이트 입력 커패시턴스 / 동일 전류 인버터 입력 커패시턴스 |
| 노이즈 마진 | Noise Margin (NM) | 신호가 얼마나 오염되어도 정상 동작하는지 나타내는 여유 전압 |
| 단채널 효과 | Short Channel Effects (SCE) | 채널이 짧아질 때 나타나는 VTH 감소, DIBL, 속도포화 등 |
| 도핑 | Doping | 반도체에 불순물을 주입해 전도성을 높이는 공정 |
| 동적 전력 | Dynamic Power | 스위칭 시 커패시턴스 충방전으로 소모되는 전력. P=CL·VDD²·f |
| 디지털 추상화 | Digital Abstraction | 연속 아날로그 신호를 0/1로 이진화하는 개념 |
| 리피터 | Repeater | 긴 배선 중간에 삽입하는 인버터. 지연 L²→L로 개선 |
| 면저항 | Sheet Resistance (R□) | ρ/H. 배선 모양(L/W)과 곱해 실제 저항 계산 |
| 문턱 전압 | Threshold Voltage (VTH) | 채널(반전층)이 형성되기 시작하는 최소 Gate 전압 |
| 밀러 효과 | Miller Effect | 커플링 커패시턴스가 역상 스위칭 시 2배로 느껴지는 효과 |
| 반전 조건 | Inversion | Vg > VTH 시 게이트 아래 반전층(채널) 형성 상태 |
| 반전층 | Inversion Layer | Gate 전압으로 형성된 전류 통로. MOSFET 동작의 핵심 |
| 분기 노력 | Branching Effort (B) | 경로에서 분기로 인해 증가하는 구동 부담. b=(Con+Coff)/Con |
| 비저항 | Resistivity (ρ) | 재료 고유의 전기 저항 특성. 단위 Ω·m |
| 서브스레숄드 스윙 | Subthreshold Swing (S) | 전류 10배 변화에 필요한 Vgs 변화. 이론 최솟값 60 mV/dec |
| 서브스레숄드 전류 | Subthreshold Current | Vgs < VTH에서도 흐르는 누설 전류 |
| 속도 포화 | Velocity Saturation | 강한 전기장에서 전자 속도가 vsat에 수렴하는 현상 |
| 전도 밴드 | Conduction Band | 자유 전자가 존재하는 에너지 밴드. 최하단 = Ec |
| 전압 전달 특성 | VTC (Voltage Transfer Characteristic) | 인버터 Vin-Vout DC 특성 곡선 |
| 전파 지연 | Propagation Delay (tp) | 입력이 50%를 넘어 출력이 50%에 도달할 때까지의 시간 |
| 질량 작용 법칙 | Mass Action Law | np = ni². 도핑에 무관하게 항상 성립 |
| 정공 | Hole | P형 반도체의 양전하 캐리어. 전자가 빠진 빈자리 |
| 채널 길이 변조 | Channel Length Modulation | Vds 증가 시 유효 채널 길이 감소로 Ids 미세 증가. 계수 λ |
| 커플링 커패시턴스 | Coupling Capacitance (Cc) | 인접 배선 사이에 형성되는 커패시턴스. 노이즈 원인 |
| 페르미 레벨 | Fermi Level (Ef) | 전자 점유 확률이 50%인 에너지 레벨 |
| 페르미-디랙 분포 | Fermi-Dirac Distribution | f(E) = 1/(1+e^((E-Ef)/kT)). 에너지 상태 점유 확률 |
| 팬아웃 | Fanout (f) | Cout/Cin. 내가 구동하는 부하의 상대적 크기 |
| 플랫밴드 전압 | Flat Band Voltage (VFB) | 에너지 밴드가 평평한 상태의 게이트 전압. 기준점 |
| DIBL | Drain-Induced Barrier Lowering | Drain 전압이 Source 쪽 장벽을 낮춰 VTH 감소시키는 효과 |
| Elmore 지연 | Elmore Delay | RC 트리에서 TDi = Σ Rki·Ck. 임펄스 응답 1차 모멘트 |
| MOS 커패시터 | MOS Capacitor | Gate-산화막-반도체 구조. MOSFET 동작의 핵심 구조 |
| Pull-down Network | PDN | NMOS로 구성. 출력을 GND로 내리는 네트워크 |
| Pull-up Network | PUN | PMOS로 구성. 출력을 VDD로 올리는 네트워크 |
| VIH | — | 입력으로 HIGH를 인식하는 최소 전압. VTC 기울기 −1 점 |
| VIL | — | 입력으로 LOW를 인식하는 최대 전압. VTC 기울기 −1 점 |
| VOH | — | 출력 HIGH 최솟값 |
| VOL | — | 출력 LOW 최댓값 |

---

## ④ 주제별 상세

### Ch1. Digital Circuit Introduction

- **트랜지스터**: "Trans+Resistor". 현대 칩은 MOSFET 사용. 3단자: Gate(제어), Source(출발), Drain(도착)
- **Gate 아래 SiO₂**: 절연체 → 전기장으로만 채널 제어. 직접 전류 흐르지 않음
- **반도체 도핑**: N-type(Donor→전자 과잉), P-type(Acceptor→정공 과잉)
- **NMOS**: Gate HIGH → ON. P형 기판 위 N형 S/D
- **PMOS**: Gate LOW → ON. N형 기판 위 P형 S/D. 이동도 낮아 NMOS의 2배 W 필요
- **CMOS 인버터**: PMOS(위)+NMOS(아래). 항상 하나만 ON → 정적 전력 이론상 0
- **PUN/PDN 법칙**: PDN 직렬 ↔ PUN 병렬 (항상 쌍). NAND: PDN 직렬/PUN 병렬. NOR: PDN 병렬/PUN 직렬
- **Full-Custom 흐름**: 회로도→시뮬→레이아웃→DRC→LVS→추출→Tape-out
- **무어의 법칙**: 2년마다 트랜지스터 2배. 한계: 전력 위기, 누설 전류, 전압 스케일링 어려움
- **FinFET**: 3D 트랜지스터 구조로 누설 전류 감소. 22nm 공정부터 도입

### Ch2. MOSFET Device Characteristics

- **에너지 밴드**: 전도 밴드(Ec, 자유 전자) ↔ 가전자 밴드(Ev, 묶인 전자). 사이 = 금지 구역(Eg=1.12eV for Si)
- **페르미 레벨**: 전자 점유 확률 50% 에너지. 두 물질 접촉 시 Ef 같아질 때까지 전하 이동
- **MOS 커패시터 3단계**: Flat Band(VFB) → Depletion(공핍층 형성) → Inversion(반전층, 채널 생성)
- **VTH 결정 요소**: VFB, 기판 도핑(NA), 산화막 두께(tox→Cox), 페르미 전위(φF)
- **선형 vs 포화 경계**: Vds = Vgs − Vt (핀치오프 발생 지점)
- **포화 전류**: Vds와 무관 → Gate만으로 전류 제어. 디지털 회로의 핵심 동작점
- **채널 길이 변조**: λ 클수록(짧은 채널일수록) 포화 전류가 Vds에 더 민감
- **속도 포화**: 단채널에서 Ids가 (Vgs−Vt)² → (Vgs−Vt) 선형으로 변화
- **서브스레숄드 한계**: 60 mV/decade는 CMOS의 근본 장벽. 돌파 시도: 터널 FET, NC-FET
- **접합 커패시턴스**: 역방향 바이어스 유지 필수. 바닥면+측벽으로 구성

### Ch3. CMOS Circuit Basics

- **노이즈 원인 3가지**: 유도성 결합, 용량성 결합, 전원/접지 노이즈
- **VTC 5구간**: A(NMOS off)→B(NMOS 약)→C(전환, 기울기 최대)→D(PMOS 약)→E(PMOS off)
- **VIL/VIH**: VTC에서 기울기가 정확히 −1인 두 점
- **재생 특성**: Vin < VIL이면 게이트 체인 통과 시 VOL로 수렴. VIL~VIH 사이면 불확정
- **동적 전력 핵심**: VDD 낮추기가 가장 효과적(제곱 비례). VDD를 1/2로 → 전력 1/4
- **정적 전력**: 서브스레숄드 누설 전류 × VDD. 수백억 트랜지스터 합산 시 무시 불가
- **이상적 인버터**: NMH = NML = VDD/2, VOH=VDD, VOL=0
- **PMOS W = 2×NMOS W**: μp ≈ μn/2이므로 같은 저항을 위해 2배 폭 필요
- **직렬 N개 → W를 N배**: NAND N입력의 PDN이 직렬 N개이므로 각 NMOS W를 N배로
- **인버터 체인 최적 비율**: 각 단 크기 등비수열. 최적 α ≈ e ≈ 2.7, 실용적 단수 3~4

### Ch4. Logical Effort

- **기생 커패시턴스 포함 지연**: td = td0·(γ + f). γ = Cpar/Cin ≈ 1 (인버터). γ가 최소 고유 지연
- **LE 직관**: 같은 출력 전류를 위해 인버터 대비 몇 배 입력 커패시턴스를 요구하는가
- **LE 계산**: 각 입력의 (PMOS W + NMOS W) / 인버터 등가 Cin(=3Cg)
- **NOR > NAND LE**: PMOS 직렬(NOR) → PMOS 이동도 낮아 더 크게 키워야 함 → 입력 C 증가
- **Path LE 절차 6단계**: ①PE=G·B·EF → ②N=log₄(PE) → ③N단 스케치 → ④D=N·PE^(1/N)+P → ⑤f̂=PE^(1/N) → ⑥뒤에서 앞으로 크기 결정
- **최적 단당 effort**: ≈ 4 (γ=0), ≈ 3.6 (γ=1)
- **분기 노력 B**: 분기가 있으면 off-path 부하도 구동 → PE 증가 → 지연 증가
- **LE 한계**: 인터커넥트 무시, 지연만 최적화(전력·면적 제외), 균일 분기 가정, 입력 슬루 무시

### Ch5. Interconnect Wire

- **배선 문제 3가지**: 저항(R)·커패시턴스(C)→지연·전력 증가. 인덕턴스(L)는 온칩에서 보통 무시
- **AR(Aspect Ratio)**: H/W. 공정 발전 → AR 증가 추세 (저항 관리 목적)
- **면저항(R□)**: ρ/H. 정사각형 수(L/W)와 곱해 총 저항 계산. 형태(모양)만으로 결정됨
- **Low-k 유전체**: 배선 커패시턴스 감소 목적. Gate 유전체(High-k)와 반대 요구
- **커플링 밀러 효과**: 역상 스위칭 시 Ceff = Cself + 2Cc (2배 증폭)
- **쉴드 삽입**: 크리티컬 신호선 양쪽에 GND/VDD 배선 → 커플링 차단. 면적 트레이드오프
- **Elmore 지연 핵심**: 소스에 가까운 저항이 더 많은 C를 충전 → 지연 기여 더 큼
- **L형 모델 금지**: Elmore 지연 = RC (실제 RC/2의 2배). π형·T형은 RC/2로 정확
- **L² 문제**: Rw∝L, Cw∝L → twire∝L². 배선 2배 길면 지연 4배
- **리피터 효과**: N 구간 분할 → 지연 L²→L로 개선. 단, 전력 증가 트레이드오프
- **글로벌 배선**: 공정 스케일링으로 길이 안 줄어듦 + 저항 증가 → 지연 악화. 리피터 삽입 주요 대상

---

## ⑤ 시험 대비 체크리스트

### 계산 문제 유형

- [ ] **VTH 계산**: VFB, φF, NA, Cox 주어졌을 때 VTH 구하기
- [ ] **Ids 계산**: Vgs, Vds, Vt, μnCox, W/L 주어졌을 때 선형/포화 판별 후 Ids 계산
- [ ] **노이즈 마진 계산**: VOH, VOL, VIH, VIL에서 NMH, NML 계산
- [ ] **동적 전력 계산**: CL, VDD, f 주어졌을 때 P 계산. VDD 변경 시 전력 변화율
- [ ] **전파 지연 계산**: Rn, Rp, CL 주어졌을 때 tpHL, tpLH, tp 계산
- [ ] **인버터 체인 사이징**: 입출력 커패시턴스 비율, 단수 N 주어졌을 때 각 단 크기 계산
- [ ] **LE 계산**: 게이트 회로도 보고 Cin, LE 계산
- [ ] **Path Effort 계산**: 여러 단 게이트 경로에서 G, B, EF, PE 계산
- [ ] **최적 단수 계산**: PE 주어졌을 때 N = log₄(PE)
- [ ] **최적 게이트 크기**: f̂ 주어졌을 때 뒤에서 앞으로 Cin 계산
- [ ] **배선 저항 계산**: ρ, L, W, H 주어졌을 때 R 계산. 정사각형 수(L/W)로도 계산
- [ ] **Elmore 지연 계산**: RC 트리 그림 보고 특정 노드의 Elmore 지연 계산
- [ ] **리피터 최적화**: Rw, Cw, Rinv, Cinv 주어졌을 때 Nopt, Wopt 계산

### 개념 문제 유형

- [ ] NMOS/PMOS ON 조건과 차이 설명
- [ ] CMOS가 정적 전력이 이론상 0인 이유 (항상 하나만 ON)
- [ ] VIL/VIH가 VTC의 기울기 −1인 점으로 정의되는 이유
- [ ] 재생 특성(Regenerative Characteristic)이 의미하는 바
- [ ] 동적 전력에서 VDD를 낮추는 것이 왜 가장 효과적인가 (제곱 비례)
- [ ] 서브스레숄드 스윙 60 mV/decade가 이론적 한계인 이유
- [ ] NAND가 NOR보다 LE가 작은 이유 (PMOS 이동도와 연결)
- [ ] 분기 노력(Branching Effort)이 필요한 이유
- [ ] 배선 지연이 L²에 비례하는 이유 (Rw∝L, Cw∝L)
- [ ] L형 RC 모델이 잘못된 이유 (RC vs RC/2)
- [ ] 리피터 삽입이 지연을 L²→L로 바꾸는 원리
- [ ] 글로벌 배선이 공정 스케일링으로 개선되지 않는 이유
- [ ] 커플링 커패시턴스의 밀러 효과 설명 (역상 vs 동상)
- [ ] Low-k 유전체와 High-k 유전체가 각각 어디에 왜 쓰이는가
- [ ] 채널 길이 변조(λ)가 짧은 채널에서 더 심한 이유
