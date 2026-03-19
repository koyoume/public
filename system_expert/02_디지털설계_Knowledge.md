# 디지털 설계 - 학습 누적 정리

> 이 문서는 수업 후 정리된 내용을 누적하는 Knowledge 문서입니다.
> 각 섹션에 날짜와 함께 내용을 추가해 나갑니다.

---

## 디지털 시스템 설계

### RTL 설계
<!-- RTL 설계 방법론, 데이터패스/제어유닛 분리 -->

### FSM 설계
<!-- 상태 다이어그램, 상태 인코딩, 최적화 -->

### HDL 코딩
<!-- Verilog/VHDL 문법, 코딩 패턴, 합성 가능 코드 -->

### 타이밍 & 최적화
<!-- 클럭 주기, 크리티컬 패스, 파이프라이닝 -->

### FPGA
<!-- FPGA 구조, 설계 흐름, 제약 조건 -->

### 기타

---

## 논리 설계

### 조합 논리
<!-- 불 대수, 카르노 맵, MUX, 디코더, ALU -->

### 순차 논리
<!-- 플립플롭, 레지스터, 카운터, 시프트 레지스터 -->

### 상태 머신
<!-- Mealy vs Moore, 상태 최소화, 인코딩 -->

### 타이밍 분석
<!-- setup time, hold time, clock skew, 메타스태빌리티 -->

### 기타

---

## 디지털 집적회로

> 삼성 DS System Expert Course | 서울대 김재준 교수

---

### Ch1. Digital Circuit Introduction (2026-03-18)

**트랜지스터 (Transistor)**
- "Trans + Resistor" — 전류를 제어하는 소자. 현대 디지털 칩은 대부분 MOSFET 사용
- MOSFET 3단자: Gate(제어), Source(출발), Drain(도착)
- Gate 아래 산화막(SiO₂)은 절연체 → 전기장으로만 채널 제어

**반도체 (Semiconductor)**
- 순수 Si: 자유 전하 없음 → 부도체에 가까움
- 도핑(Doping): 불순물 주입으로 전도성 생성
  - N-type: Donor 주입 → 자유 전자(음전하) 과잉
  - P-type: Acceptor 주입 → 정공(양전하) 과잉
- Shockley 주차장 비유: 2층 주차장에서 차(전자)와 빈자리(정공)의 이동으로 전도 설명

**NMOS vs PMOS**
- NMOS: Gate HIGH → ON (전자 채널), Gate LOW → OFF
- PMOS: Gate LOW → ON (정공 채널), Gate HIGH → OFF
- 두 특성이 상보적(Complementary) → CMOS의 근거
- Vth (Threshold Voltage): ON/OFF 기준 전압

**CMOS 인버터**
- PMOS(위) + NMOS(아래) 구조
- A=0: PMOS ON, NMOS OFF → Y=1 (VDD로 충전)
- A=1: PMOS OFF, NMOS ON → Y=0 (GND로 방전)
- 항상 하나만 ON → 정적 전류 이론상 0 → 저전력의 핵심

**CMOS 일반 구조**
- Pull-up Network (PUN): PMOS, 출력을 VDD로 올림
- Pull-down Network (PDN): NMOS, 출력을 GND로 내림
- PDN 직렬 ↔ PUN 병렬 (항상 쌍)
- CMOS 게이트는 구조상 항상 반전 출력 (NAND, NOR, NOT만 직접 구현)

**NAND / NOR**
- NAND: PDN NMOS 직렬, PUN PMOS 병렬
- NOR: PDN NMOS 병렬, PUN PMOS 직렬

**설계 플로우 (Design Flow)**
- Full-Custom: 회로도 → 시뮬레이션 → 레이아웃 → DRC → LVS → 추출 → Tape-out
- Semi-Custom: 표준 셀 라이브러리 + 자동 배선
- 추상화 3단계: 아키텍처 수준 → 논리 수준 → 기하학(레이아웃) 수준

**무어의 법칙 (Moore's Law)**
- 트랜지스터 수 2년마다 2배
- 한계: 전력 밀도 폭증(Power Crisis), 누설 전류 증가, 전압 스케일링 어려움
- 극복 시도: FinFET(3D 트랜지스터), 칩렛(Chiplet), 3D 집적
- More Moore vs More than Moore

---

### Ch2. MOSFET Device Characteristics (2026-03-18)

**에너지 밴드 (Energy Band)**
- 전도 밴드(Conduction Band, Ec): 자유 전자 존재 가능
- 가전자 밴드(Valence Band, Ev): 원자에 묶인 전자
- 밴드갭(Band Gap, Eg): 전자가 존재할 수 없는 금지 구역. Si에서 ≈ 1.12eV

**페르미 레벨 (Fermi Level, Ef)**
- 전자가 존재할 확률이 정확히 50%인 에너지 레벨
- Fermi-Dirac 분포: f(E) = 1 / (1 + e^((E-Ef)/kT))
- 두 물질이 접촉하면 Ef가 같아질 때까지 전하 이동 → 평형

**캐리어 농도 (Carrier Concentration)**
- np = ni² (질량 작용 법칙) — 항상 일정
- N-type: n ≈ Nd, p = ni²/Nd
- P-type: p ≈ Na, n = ni²/Na

**PN 접합 (PN Junction)**
- N-P 접촉 시 확산(Diffusion)으로 캐리어 이동 → 공핍 영역(Depletion Region) 형성
- 내장 전위(Built-in Potential, Vbi): 공핍층에 생기는 자연 전위차
- 순방향 바이어스: 장벽 낮아짐 → 전류 지수함수적 증가 I = I₀(e^(qV/kT) - 1)
- 역방향 바이어스: 장벽 높아짐 → 전류 거의 없음, 공핍층 넓어짐
- MOSFET에서 Source/Drain-기판 접합은 항상 역방향 유지 필요

**MOS 커패시터 (MOS Capacitor)**
- Flat Band (VFB): 에너지 밴드가 평평한 기준 상태
- Depletion (Vg > VFB): 정공 밀려남 → 공핍층 형성, Wd = √(2εsi·φs / qNA)
- Inversion (Vg > VTH): 표면에 반전층(N채널) 형성 → 전류 통로 생성
- 반전 전하: Qinv = Cox(Vg - VTH)

**문턱 전압 (Threshold Voltage, VTH)**
- 반전층이 형성되기 시작하는 최소 Gate 전압
- VTH = VFB + 2φF + √(2εsi·qNA·2φF) / Cox

**I-V 특성 — 선형 영역 (Linear Region)**
- 조건: Vgs - Vt > Vds
- Ids = μnCox(W/L)[(Vgs-Vt)Vds - Vds²/2]
- 트랜지스터가 저항처럼 동작

**I-V 특성 — 포화 영역 (Saturation Region)**
- 조건: Vds > Vgs - Vt (핀치오프 발생)
- Ids = (1/2)μnCox(W/L)(Vgs-Vt)²
- Ids가 Vds와 무관 → Gate 전압으로만 전류 제어

**채널 길이 변조 (Channel Length Modulation)**
- 포화 시 Vds 증가 → 핀치오프 점 이동 → 유효 L 감소 → Ids 미세 증가
- Ids = (1/2)μnCox(W/L)(Vgs-Vt)²(1 + λVds)

**속도 포화 (Velocity Saturation)**
- 단채널에서 전기장 강해짐 → 전자 속도 포화(vsat)에 도달
- 장채널: Ids ∝ (Vgs-Vt)² / 단채널: Ids ∝ (Vgs-Vt) (선형에 가까워짐)

**단채널 효과 (Short Channel Effects, SCE)**
- VTH roll-off: 채널 짧아질수록 VTH 감소
- DIBL (Drain-Induced Barrier Lowering): Vds 증가 → VTH 추가 감소

**서브스레숄드 전류 (Subthreshold Current)**
- Vgs < VTH에서도 지수함수적 누설 전류 존재
- 서브스레숄드 스윙 S: 전류 10배 변화에 필요한 Vgs 변화량
- S의 이론적 최솟값 = 60 mV/decade (상온, 300K) ← 현재 CMOS의 근본 한계

**MOSFET 커패시턴스**
- Gate 커패시턴스(CGC): OFF → Cox와 Cd 직렬 / ON → Cox
- Source/Drain 접합 커패시턴스: 바닥면 + 측벽, 역방향 전압에 따라 변화

---

### Ch3. CMOS Circuit Basics (2026-03-18)

**노이즈 마진 (Noise Margin)**
- 노이즈 원인: 유도성 결합, 용량성 결합, 전원/접지 노이즈
- 4개 기준 전압: VOH, VOL (출력), VIH, VIL (입력)
- NMH = VOH - VIH (HIGH 신호 허용 노이즈)
- NML = VIL - VOL (LOW 신호 허용 노이즈)
- 이상적 인버터: NMH = NML = VDD/2

**전압 전달 특성 (VTC, Voltage Transfer Characteristic)**
- Vin을 0→VDD로 올리며 Vout 변화를 그린 DC 특성 곡선
- VIL, VIH: VTC 기울기가 정확히 -1인 두 점
- 5개 구간: A(NMOS off) → B(NMOS 약) → C(전환, 기울기 최대) → D(PMOS 약) → E(PMOS off)

**재생 특성 (Regenerative Characteristics)**
- Vin < VIL: 버퍼 반복 통과 시 VOL로 수렴 (신호 복원)
- Vin > VIH: VOH로 수렴 (신호 복원)
- VIL < Vin < VIH: 불확정, 수렴 방향 보장 안 됨
- 좋은 게이트: VTC 기울기 절댓값 >> 1 → 불확정 영역 좁음

**동적 전력 (Dynamic Power)**
- P = CL × VDD² × f
- 전환 시 에너지: 충전 시 CL·VDD² (절반은 PMOS에서 열소모, 절반은 CL 저장)
- VDD 낮추기가 가장 효과적 저전력 방법 (제곱 비례)

**정적 누설 전력 (Static Leakage Power)**
- P_leak = I_leak × VDD
- 원인: 서브스레숄드 전류 (Ch2 연결)
- 현대 고성능 프로세서에서 무시 못 할 비중 차지

**전파 지연 (Propagation Delay)**
- RC 모델: MOSFET ON 상태 = 저항 R
- tpLH = 0.69 × Rp × CL (Pull-up, 0→1)
- tpHL = 0.69 × Rn × CL (Pull-down, 1→0)
- tp = 0.69 × CL × (Rp + Rn)/2

**인버터 사이징 (Inverter Sizing)**
- PMOS W = 2 × NMOS W: μp ≈ μn/2 이므로 저항 같게 하려면 2배 필요
- 직렬 N개 트랜지스터 → 각 W를 N배로 → 인버터와 동일 속도
- NAND 2입력: NMOS W=2, PMOS W=2

**인버터 체인 최적 사이징**
- 등비수열로 크기 증가가 최적 (각 단 비율 동일)
- α = (CL/Cin)^(1/N) (N: 단수)
- 최적 비율 α ≈ e ≈ 2.7, 실용적 최적 단수 ≈ 3~4단

---

### CMOS 기초
<!-- 위 Ch1~Ch3 내용으로 대체됨 -->

### 논리 게이트 설계
<!-- Ch1 NAND/NOR, Ch3 사이징 참조 -->

### 전력 분석
<!-- Ch3 동적/정적 전력 참조 -->

### 배선 & 지연
<!-- Ch3 RC 모델, 인버터 체인 참조 -->

### 메모리 회로
<!-- SRAM 셀, DRAM, 센스 앰프 — 미학습 -->

### 저전력 설계
<!-- 전압 스케일링, 클럭 게이팅, 파워 게이팅 — 미학습 -->

### 기타

---

## 과목 간 연결 포인트
<!-- 추상화 수준별 연결: 트랜지스터 → 게이트 → 시스템 -->

---

## 시험 대비 핵심 요약

---

## 오답 & 취약 영역
