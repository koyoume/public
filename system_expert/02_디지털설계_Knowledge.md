# 디지털 집적회로 (Digital Integrated Circuits) — 오픈북 시험 대비 정리

> 삼성 DS System Expert Course | 서울대 김재준 교수 | 최종 업데이트: 2026-04-02

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
| **[Ch6] FF 최대 지연 (setup)** | tpd ≤ Tc − tpcq − tsetup | Tc: 클럭 주기, tpcq: CLK→Q 전파 지연 |
| **[Ch6] FF 최대 지연 (skew 포함)** | tpd ≤ Tc − tpcq − tsetup − tskew | tskew: 클럭 스큐 |
| **[Ch6] FF 최소 지연 (hold)** | tcd ≥ thold − tccq | tccq: CLK→Q 오염 지연, tcd: 조합 논리 오염 지연 |
| **[Ch6] FF 최소 지연 (skew 포함)** | tcd + tccq ≥ thold + tskew | |
| **[Ch6] Pulsed Latch 최대 지연** | tpd ≤ Tc − tpcq − tsetup + Tpw | Tpw: 펄스 폭 (Time Borrowing) |
| **[Ch6] Pulsed Latch 최소 지연** | tcd ≥ thold − tccq + Tpw | |
| **[Ch6] Two-Phase 최대 지연** | Tc ≥ tpdq1 + tpd1 + tpdq2 + tpd2 | setup overhead 없음 |
| **[Ch6] Time Borrowing 최대량** | tborrow = Tc/2 − tsetup | |
| **[Ch6] Two-Phase 최소 지연** | tccq + tcd ≥ thold | 매 Tc/2마다 성립해야 함 |
| **[Ch8] DRAM 읽기 전압변화 "1"** | ΔVbl = +Ccell·VDD/2 / (Cbl+Ccell) | Ccell: 셀 커패시턴스, Cbl: 비트라인 커패시턴스 |
| **[Ch8] DRAM 읽기 전압변화 "0"** | ΔVbl = −Ccell·VDD/2 / (Cbl+Ccell) | |
| **[Ch8] 전하 공유 전압** | V(X2) = VDD × C2/(C1+C2) | 내부 노드 프리차지 없을 때 전압 강하 |
| **[Ch9] SRAM 셀 크기 비율** | NR : XR : PR ≈ 2 : 1 : 1 | 읽기 안정성과 쓰기 용이성 균형점 |
| **[Ch9] DRAM 읽기 ΔVbl** | ΔVbl = ±Ccell·VDD/2 / (Cbl+Ccell) | SRAM에도 동일 원리 적용 |

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

### 클로킹 방식 비교 (Ch6)

| 항목 | FF (Edge-Triggered) | Pulsed Latch | Two-Phase Latch |
|------|-------------------|--------------|-----------------|
| 최대 지연 | Tc − tpcq − tsetup | Tc − tpcq − tsetup + Tpw | Tc − tpdq1 − tpdq2 |
| Setup overhead | 있음 | 있음 (Tpw로 완화) | 없음 (Time Borrowing으로 대체) |
| 최소 지연 조건 | tcd ≥ thold − tccq | tcd ≥ thold − tccq + Tpw | tccq+tcd ≥ thold (매 Tc/2) |
| Time Borrowing | 없음 | Tpw만큼 | Tc/2 − tsetup만큼 |
| 구현 복잡도 | 단순 | 보통 | 복잡 (2개 클럭) |
| 사용 빈도 | 가장 많음 | 고성능 설계 | 특수 설계 |

### D-Latch vs D Flip-Flop (Ch6)

| 항목 | D-Latch | D Flip-Flop |
|------|---------|-------------|
| 트리거 방식 | 레벨 감지 (Level-Sensitive) | 엣지 트리거 (Edge-Triggered) |
| CLK=1 | 투명 (D→Q 통과) | 이전 값 유지 (Slave 불투명) |
| CLK=0 | 불투명 (Q 유지) | 샘플링 준비 (Master 투명) |
| 데이터 캡처 | CLK=1인 동안 계속 | 상승 에지 순간만 |
| 구성 | 단일 래치 | 마스터(CLK_bar)+슬레이브(CLK) 직렬 |
| 더블 샘플링 위험 | 있음 | 없음 |

### 다이나믹 회로 비교 (Ch7)

| 항목 | Unfooted | Footed | 정적 CMOS |
|------|---------|--------|-----------|
| PDN 구성 | NMOS만 | NMOS + 풋 NMOS | NMOS + PMOS PUN |
| 프리차지 입력 조건 | 반드시 0 | 제약 없음 | 해당 없음 |
| LE (논리 노력) | 작음 (빠름) | 큼 (느림) | 중간 |
| 충돌 가능성 | 있음 | 없음 | 없음 |
| 출력 단조성 | 0→1만 가능 | 0→1만 가능 | 양방향 |

### 메모리 종류 비교 (Ch8)

| 항목 | SRAM | DRAM | Flash (NAND) | Flash (NOR) |
|------|------|------|--------------|-------------|
| 셀 구성 | 6T | 1T-1C | 1T (FG) | 1T (FG) |
| 휘발성 | 휘발성 | 휘발성 | 비휘발성 | 비휘발성 |
| 리프레시 | 불필요 | 필요 (~64ms) | 불필요 | 불필요 |
| 읽기 방식 | 비파괴 | 파괴적 (복원 필요) | 비파괴 | 비파괴 |
| 셀 면적 | 큼 | 작음 | 매우 작음 | 작음 |
| 속도 | 빠름 | 보통 | 느림 | 보통 |
| 사용처 | 캐시 | 메인 메모리 | SSD·스토리지 | 펌웨어·부팅 |

### DRAM vs eDRAM Gain Cell (Ch8)

| 항목 | 표준 DRAM (1T-1C) | Gain Cell (3T) |
|------|-----------------|----------------|
| 셀 구조 | 트랜지스터 1 + 커패시터 | 트랜지스터 3개 |
| 읽기 방식 | 파괴적 (복원 필요) | 비파괴적 |
| 데이터 저장소 | 별도 커패시터 | 트랜지스터 게이트 커패시턴스 |
| 누설 특성 | NMOS 기판 누설 | PMOS 게이트 누설 (더 작음) |
| 집적도 | 높음 | 낮음 |

### 6T SRAM Art of Balancing (Ch9)

| 트랜지스터 | 크게 하면 (장점) | 크게 하면 (부작용) | 권장 비율 |
|-----------|----------------|-------------------|----------|
| NR (드라이브 NMOS) | 읽기 전류↑ → 읽기 속도↑ | 인버터 트립 전압↓ → 읽기 중 셀 불안정 | 2 |
| XR (접근 트랜지스터) | 읽기/쓰기 속도↑ | 읽기 중 Q 노드 전압↑ → 데이터 뒤집힘 | 1 |
| PR (로드 PMOS) | 피드백 강화 → SNM↑ 안정성↑ | 쓰기 시 XL이 PL 이기기 어려움 → 쓰기 실패 | 1 |

### SRAM 센스 앰프 비교 (Ch9)

| 항목 | 차동 쌍 (Differential Pair) | 클럭드 (Clocked) |
|------|---------------------------|----------------|
| 클럭 필요 | 불필요 (비동기) | 필요 (sense_clk) |
| 정적 전력 | 큼 (바이어스 전류 상시) | 작음 |
| 속도 | 보통 | 빠름 (재생 피드백) |
| 격리 트랜지스터 | 불필요 | 필요 (BL 커패시턴스 분리) |
| 현재 사용 | 제한적 | 주류 |

### SRAM 안정성 개선 방법 비교 (Ch9)

| 방법 | SNM 개선 | 쓰기 용이성 | 면적 | 복잡도 |
|------|---------|------------|------|--------|
| PMOS 강화 | ↑ | ↓ | 소폭↑ | 낮음 |
| 셀 VDD 높이기 | ↑ | ↑ (BL 낮춤) | 동일 | 높음 (이중 전원) |
| 8T SRAM | Read=Standby SNM | 무관 | ↑↑ (면적 33%↑) | 보통 |

### 6T vs 8T vs 10T SRAM (Ch9)

| 항목 | 6T | 8T | 10T |
|------|----|----|-----|
| 트랜지스터 수 | 6 | 8 | 10 |
| 읽기/쓰기 포트 | 공유 | 분리 (단방향 읽기) | 분리 (차동 읽기) |
| Read SNM | < Standby SNM | = Standby SNM | = Standby SNM |
| 읽기 속도 | 보통 | 빠름 | 빠름 |
| 셀 면적 | 기준 | 크게 증가 | 매우 크게 증가 |
| 사용처 | 일반 SRAM | 고안정성 캐시 | 특수 설계 |

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
| 게인 셀 | Gain Cell | 읽기 경로가 저장 노드와 분리된 eDRAM 셀. 비파괴 읽기 가능 |
| 단조성 | Monotonicity | 다이나믹 회로에서 평가 중 출력이 0→1로만 변할 수 있는 특성 |
| 더블 샘플링 | Double Sampling | 래치 투명 구간에 데이터가 두 번 통과하는 오류 |
| 도미노 로직 | Domino Logic | 다이나믹 게이트 + 정적 인버터. 단조성 문제 해결 |
| 리프레시 | Refresh | DRAM에서 누설로 사라지는 전하를 주기적으로 재충전하는 동작 (~64ms) |
| 분산 RC | Distributed RC | 배선을 무한히 작은 R·C 단위의 연속 구조로 모델링 |
| 비파괴 읽기 | Non-destructive Read | 읽기 후 저장 데이터가 손상되지 않는 읽기 방식 |
| 셋업 타임 | Setup Time (tsetup) | 클럭 에지 이전 데이터가 안정되어야 하는 최소 시간 |
| 시간 빌리기 | Time Borrowing | 래치 투명 구간을 이용해 다음 단계의 시간을 빌려 쓰는 기법 |
| 오염 지연 | Contamination Delay (tcd) | 입력 변화 후 출력이 처음 흔들리기 시작하는 최소 시간 |
| 전하 공유 | Charge Sharing | 다이나믹 회로 내부 노드 간 전하 재분배로 출력 전압 강하 |
| 전파 지연 (CLK→Q) | Clock-to-Q Delay (tpcq) | 클럭 에지 후 FF 출력이 최종값에 도달하는 시간 |
| 컨트롤 게이트 | Control Gate | Flash 셀에서 외부 전압을 인가하는 게이트 |
| 클럭 스큐 | Clock Skew (tskew) | 인접 FF 간 클럭 도달 시간 차이 |
| 키퍼 | Keeper | 다이나믹 회로에서 누설 전류를 막는 약한 PMOS |
| 투명 모드 | Transparent Mode | D-Latch에서 CLK=1일 때 D가 Q로 그대로 통과하는 상태 |
| 파울러-노르트하임 터널링 | Fowler-Nordheim Tunneling | Flash 소거 시 전자가 얇은 산화막을 양자 터널링으로 통과하는 현상 |
| 파괴적 읽기 | Destructive Read | 읽기 동작이 저장 데이터를 손상시켜 복원이 필요한 방식 (DRAM) |
| 핫 전자 주입 | Hot Electron Injection | Flash 프로그래밍 시 높은 에너지 전자가 터널 산화막을 넘어 FG에 주입 |
| 홀드 타임 | Hold Time (thold) | 클럭 에지 이후 데이터가 안정되어야 하는 최소 시간 |
| 플로팅 게이트 | Floating Gate | Flash 셀에서 전하를 저장하는 완전 절연된 도체 게이트 |
| CLK-to-Q 오염 지연 | CCQ (tccq) | 클럭 에지 후 FF 출력이 처음 흔들리기 시작하는 최소 시간 |
| DSL/SSL | Drain/Source Select Line | NAND Flash에서 스트링의 드레인/소스 선택 트랜지스터 제어선 |
| FN 터널링 | FN Tunneling | → 파울러-노르트하임 터널링 참조 |
| Vpass | — | NAND Flash 읽기 시 비선택 셀을 강제로 켜는 통과 전압 (~4-5V) |
| Vread | — | NAND Flash 읽기 시 선택 셀에 인가하는 읽기 판별 전압 (~0V) |
| WL / BL | Word Line / Bit Line | 메모리에서 행 선택선(WL)과 열 데이터선(BL) |
| 계층적 비트라인 | Hierarchical Bit Line | 로컬·글로벌 BL 분리로 BL 커패시턴스 감소 |
| 격리 트랜지스터 | Isolation Transistor | 센싱 시작 시 BL과 센스 앰프를 분리하는 트랜지스터 |
| 비트라인 이퀄라이저 | Bit Line Equalizer | BL과 BLb를 같은 전압으로 맞추는 회로 |
| 쌍안정 | Bi-stable | 두 개의 안정 상태(Q=1/Qb=0, Q=0/Qb=1)를 가지는 특성 |
| 읽기 파괴 | Read Disturb | 읽기 동작 중 접근 트랜지스터로 인해 저장 노드 전압이 교란되는 현상 |
| 정적 노이즈 마진 | SNM (Static Noise Margin) | SRAM 셀 안정성 지표. 두 VTC 곡선의 눈(Eye) 안 최대 내접 정사각형 한 변 길이 |
| 접근 트랜지스터 | Access Transistor (XL/XR) | WL 신호로 제어되어 셀과 BL을 연결하는 트랜지스터 |
| 컬럼 멀티플렉싱 | Column Multiplexing | 다수 비트라인 중 일부만 선택해 데이터 입출력 |
| 프리디코딩 | Predecoding | 주소를 미리 부분 디코딩해 최종 단 게이트 수를 줄이는 기법 |
| 피치 매칭 | Pitch Matching | WL 드라이버 높이를 SRAM 셀 행 높이에 맞추는 설계 제약 |
| Random Vt 변동 | Random Vt Fluctuation | 공정 미세화로 인한 트랜지스터 간 Vth 불균일 현상. SRAM 불안정 주요 원인 |
| 재생 피드백 | Regenerative Feedback | 센스 앰프에서 작은 차이를 레일-투-레일로 증폭하는 양성 피드백 루프 |

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

### Ch6. Clocking Elements

- **D-Latch**: CLK=1 → 투명(D=Q), CLK=0 → 불투명(Q 유지). 레벨 감지 래치
- **D Flip-Flop**: 마스터(CLK_bar)+슬레이브(CLK) 두 래치 직렬. 상승 에지 순간만 캡처
- **FF가 래치보다 선호되는 이유**: 더블 샘플링 문제 방지. 명확한 동기화
- **Setup Time**: 클럭 에지 이전 tsetup 동안 D 안정 필요. 측정: tclk-q가 10% 증가하는 시점
- **Hold Time**: 클럭 에지 이후 thold 동안 D 안정 필요. 측정: tclk-q가 10% 증가하는 시점
- **tpd vs tcd**: tpd = 최악 지연(출력 최종 안정), tcd = 최선 지연(출력 처음 흔들림). tcd ≤ tpd
- **클럭 스큐 영향**: Setup 위반 최악 = 수신 FF 클럭이 먼저 도달. Hold 위반 최악 = 수신 FF 클럭이 늦게 도달
- **Pulsed Latch**: Tpw만큼 최대 tpd 연장(Time Borrowing). 동시에 최소 tcd 조건 강화
- **Two-Phase Latch**: Setup overhead 없음. Time Borrowing = Tc/2 − tsetup. 매 Tc/2마다 Hold 조건 검사
- **Time Borrowing 의미**: 래치 투명 구간 동안 늦게 도착한 데이터도 통과 가능 → 느린 경로 허용

### Ch7. Dynamic Circuits

- **다이나믹 기본 동작**: CLK=0 → 프리차지(Y=VDD), CLK=1 → 평가(PDN 동작, 조건부 방전)
- **장점**: PMOS PUN 제거 → LE 감소, 트랜지스터 수 감소, 빠른 방전
- **단조성**: 평가 중 출력은 0→1만 가능. 1→0은 불가 (프리차지로만 1 복원)
- **단조성 문제**: 이전 단 출력이 평가 시작 순간 잠깐 1 → 다음 단 오평가
- **도미노 해결**: 다이나믹 + 인버터 → 출력 항상 0에서 시작 → 0→1만 전파. 비반전 로직
- **Unfooted**: 빠름, 프리차지 중 입력 0 필수. Footed: 안전, LE 나쁨
- **FF 뒤 첫 단**: 반드시 Footed (Q=1 상태에서 프리차지 시작 가능)
- **Keeper**: 약한 PMOS. 누설 전류 > Keeper > 이기면 안 됨 (평가 방해 금지)
- **전하 공유**: 내부 노드 부동 → 전하 재분배 → Vout 강하. 해결: 내부 노드도 프리차지
- **파이프라인**: CL1/CL2 반대 위상 클럭으로 교번 → 전체 클럭 주기 활용
- **차동 도미노**: F와 F' 동시 계산 → 비반전 제약 해소. 트랜지스터 2배
- **현재 위치**: 정적 CMOS에 밀림. 메모리 읽기/쓰기 경로(와이드 OR 구조)에 주로 사용
- **전력 문제**: 매 사이클 프리차지 스위칭 → 정적 CMOS보다 스위칭 활동 높음

### Ch8. Memory Cell Operations

- **DRAM 구조**: 1T-1C. WL=1로 NMOS 켜서 BL↔C_cell 연결. C_cell 전하가 데이터
- **DRAM Dynamic 의미**: 전하 누설 → 시간 지나면 데이터 소실 → 64ms마다 리프레시 필수
- **DRAM 쓰기**: BL=VDD(쓰기1) 또는 BL=GND(쓰기0), WL=1 → C_cell 충방전
- **DRAM 읽기**: BL 플로팅 → WL=1 → C_cell과 C_BL 전하 공유 → ΔV_BL 발생 (수십~수백 mV)
- **파괴적 읽기**: 읽기 후 C_cell 전하 손상 → 센스 앰프가 증폭 후 반드시 복원
- **ΔV_BL이 작은 이유**: C_BL >> C_cell → 공유 후 전압 변화 미미 → 센스 앰프 필수
- **eDRAM Gain Cell**: 읽기/쓰기 경로 분리 → 비파괴 읽기. PMOS 사용(게이트 누설↓)
- **3T Gain Cell 데이터 유지**: "1" 유지 시간 > "0" 유지 시간 (자기 역방향 바이어스 효과)
- **Flash 구조**: 플로팅 게이트(FG) + 컨트롤 게이트. FG 전하량 → Vth 변화 → 데이터 표현
- **프로그래밍 (쓰기 "0")**: 핫 전자 주입. 컨트롤 게이트+드레인 고전압 → 뜨거운 전자가 FG로 주입
- **소거 ("1")**: FN 터널링. 소스 고전압 → 전자가 터널 산화막 통과해 FG 탈출. 블록 단위
- **Flash 내구성 제한**: 고전압 반복으로 터널 산화막 열화 → 통상 10,000~100,000회
- **NAND 구조**: 셀 직렬 연결 → 고밀도. 선택 셀=Vread(0V), 비선택 셀=Vpass(4-5V 강제 통과)
- **NOR 구조**: 셀 병렬 연결 → 임의 접근, XIP 가능. 펌웨어·부팅 코드 저장

### Ch9. SRAM Design

- **6T 셀 구조**: NL+PL(왼쪽 인버터) + NR+PR(오른쪽 인버터) + XL+XR(접근 트랜지스터). 교차 피드백으로 쌍안정 유지
- **Hold 동작**: WL=0 → XL/XR 꺼짐 → 셀 고립 → 피드백 루프로 데이터 영구 유지. 리프레시 불필요
- **읽기 동작**: BL=BLb=VDD 프리차지 → WL=1 → Q=0 쪽 BL 방전 → ΔV 발생 → 센스 앰프 증폭
- **읽기 파괴 위험**: XR 통해 BL(VDD)→Q 노드 전류 → Q 전압 상승 → 인버터 트립 전압 초과 시 데이터 뒤집힘
- **쓰기 동작**: BL=0, BLb=1, WL=1 → XL vs PL 전투 → XL이 PL보다 강해야 쓰기 성공
- **Art of Balancing (NR:XR:PR ≈ 2:1:1)**:
  - NR 크게: 읽기 전류↑ 속도↑ / 과하면 트립 전압↓ → 읽기 중 셀 불안정
  - XR 크게: 읽기·쓰기 속도↑ / 과하면 Q 노드 전압↑ → 데이터 뒤집힘
  - PR 크게: SNM↑ 안정성↑ / 과하면 XL이 PL 이기기 어려움 → 쓰기 실패
- **읽기/쓰기 근본 딜레마**: X 크면 쓰기↑·읽기↓, X 작으면 읽기↑·쓰기↓ → 단일 비율로 해결 불가, 8T로 근본 해결
- **센스 앰프**: 클럭드 방식 주류. sense_clk 타이밍 핵심(너무 이르면 오독, 너무 늦으면 느림). 격리 트랜지스터로 BL 커패시턴스 분리
- **비트라인 프리컨디셔닝**: 프리차지(BL=BLb=VDD) + 이퀄라이저(BL=BLb 동일 전압). 이전 읽기 잔류 차이 제거
- **프리디코딩**: 주소를 1-of-4 그룹으로 미리 디코딩 → 최종 단 2입력 게이트만 → 면적·속도 개선
- **계층적 비트라인**: 로컬 BL(소수 셀) + 글로벌 BL 분리 → BL 커패시턴스↓ → ΔV↑ → 읽기 속도·안정성 향상
- **SNM**: 두 VTC의 눈(Eye) 안 최대 내접 정사각형 한 변 길이. 클수록 안정
- **Read SNM < Standby SNM**: 읽기 시 XR이 Q 노드 교란 → VTC 비대칭 → 눈 좁아짐 → 읽기가 안정성 병목
- **Random Vt Fluctuation**: 공정 미세화 → Vt 불균일 심화 → 극단적 경우 셀이 단안정(Mono-stable)으로 전락
- **8T SRAM**: 읽기 포트(RWL/RBL) 분리 → 읽기 시 저장 노드 교란 없음 → Read SNM = Standby SNM. 면적↑ 대가

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
- [ ] **FF 최대 tpd 계산**: Tc, tpcq, tsetup, tskew 주어졌을 때 허용 최대 tpd 계산
- [ ] **FF 최소 tcd 계산**: thold, tccq, tskew 주어졌을 때 필요 최소 tcd 계산
- [ ] **Pulsed Latch 지연**: Tpw 주어졌을 때 FF 대비 최대 tpd 개선량 계산
- [ ] **Two-Phase Time Borrowing**: Tc, tsetup 주어졌을 때 최대 tborrow 계산
- [ ] **DRAM ΔVbl 계산**: Ccell, Cbl, VDD 주어졌을 때 읽기 전압 변화 계산
- [ ] **전하 공유 전압 계산**: C1, C2, VDD 주어졌을 때 전하 공유 후 V(X2) 계산
- [ ] **SNM 크기 비교**: 읽기/대기 조건 중 어느 쪽이 작은지, 그 이유 설명
- [ ] **SRAM 쓰기 조건**: NR:XR:PR 비율 주어졌을 때 쓰기 성공 여부 판단

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
- [ ] D-Latch와 D FF의 차이, FF이 선호되는 이유 (더블 샘플링)
- [ ] Setup Time과 Hold Time의 정의와 측정 방법 (tclk-q 10% 증가 기준)
- [ ] 클럭 스큐가 Setup/Hold Time에 미치는 영향 (각각 최악 조건)
- [ ] Pulsed Latch의 Time Borrowing 원리와 Hold Time 조건이 강화되는 이유
- [ ] Two-Phase Latch에서 Setup overhead가 사라지는 이유
- [ ] 다이나믹 회로에서 단조성 문제가 발생하는 원인과 도미노 로직의 해결 원리
- [ ] Keeper의 크기 설계 딜레마 (너무 강하면 vs 너무 약하면)
- [ ] 전하 공유 문제의 원인과 내부 노드 프리차지 해결책
- [ ] DRAM 읽기가 파괴적인 이유와 복원이 필요한 이유
- [ ] DRAM ΔVbl이 작은 이유 (Cbl >> Ccell)와 센스 앰프가 필요한 이유
- [ ] Flash 플로팅 게이트가 데이터를 저장하는 원리 (Vth 변화)
- [ ] Flash 프로그래밍(핫 전자 주입)과 소거(FN 터널링)의 차이
- [ ] NAND Flash 읽기에서 Vpass와 Vread의 역할
- [ ] NAND Flash와 NOR Flash의 구조적 차이와 각각의 사용처
- [ ] SRAM이 Static인 이유 (피드백 루프)와 DRAM과의 차이
- [ ] SRAM 읽기 파괴(Read Disturb) 발생 원인과 NR:XR:PR 비율의 의미
- [ ] SRAM 읽기/쓰기 딜레마 — 접근 트랜지스터 크기의 상충 관계
- [ ] Art of Balancing: NR/XR/PR 각각을 크게 했을 때 장점과 부작용
- [ ] SNM의 정의와 Read SNM이 Standby SNM보다 항상 나쁜 이유
- [ ] Vt 불균일(Random Vt Fluctuation)이 SRAM 안정성에 미치는 영향
- [ ] 8T SRAM이 6T보다 안정적인 이유와 그 대가
- [ ] 클럭드 센스 앰프의 sense_clk 타이밍 딜레마 (너무 이르면/늦으면)
- [ ] 격리 트랜지스터의 역할 (BL 커패시턴스 분리)
- [ ] 프리디코딩이 면적과 속도를 동시에 개선하는 원리
- [ ] 계층적 비트라인이 읽기 안정성을 높이는 원리
