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

> 마지막 업데이트: 2026-03-18 | 완료 챕터: Chap 1.1, 1.2, 2, 3.1, 3.2, 6.1(K-map)

---

### Chap 1.1 — 디지털 추상화 (Digital Abstraction)

**핵심 개념**
- 디지털 추상화 동기: 아날로그 노이즈 누적 문제 → 이진 신호 + 복원 메커니즘으로 해결
- 신호 복원(Signal Restoration): 게이트 통과 시 노이즈 마진 내 노이즈 자동 제거

**전압 파라미터** (2.5V LVCMOS 기준)
- V_OL=0.2V, V_IL=0.7V → V_NML = V_IL - V_OL = 0.5V (Low 노이즈 마진)
- V_OH=2.1V, V_IH=1.7V → V_NMH = V_OH - V_IH = 0.4V (High 노이즈 마진)
- Forbidden Zone: V_IL ~ V_IH (입력 미정의 구간)
- DC Transfer Curve: 입력→출력 전압 관계 곡선, 신호 복원 조건 만족 필수

**정보 표현 원칙**
- 수행할 연산(Operation)에 맞는 인코딩 선택
- 예) 감산 혼색 → OR 연산으로 구현

**회로 분류**
- 조합 논리(Combinational): 출력 = f(현재 입력만), 메모리 없음
- 순차 논리(Sequential): 출력 = f(현재 입력 + 이전 상태), 레지스터 필요

---

### Chap 1.2 — 디지털 논리 함수 (Logic Functions)

**핵심 개념**
- Combinational: 출력 = f(현재 입력), 메모리/클럭 없음, 피드백 없음
- Sequential: 출력 = f(현재 입력 + 이전 상태), 레지스터+클럭 필요, 피드백 있음

**Verilog 기초**
- `wire` + `assign`: 조합 논리 (Continuous Assignment - 입력 바뀌면 즉시 반영)
- `reg` + `always @(posedge clk)`: 순차 논리
- `wire fanOn = expr` ≡ `wire fanOn; assign fanOn = expr` ≡ `assign fanOn = expr` (합성 결과 동일)
- Continuous Assignment: 항상 연결된 wire 표현, 입력 변화 즉시 반영
- Simulation(기능 검증) vs Synthesis(하드웨어 변환) 두 가지 목적

**Verilog Synthesis 단계**
- Transform: RTL → 기술 독립적 게이트 변환 (Elaboration → Generic Synthesis → Technology Mapping)
- Optimize: 제약조건(Timing/Area/Power) 만족하도록 게이트 개선
- Behavioral Description: 동작 기술, 합성 불가 코드 포함 가능, 시뮬레이션용
- RTL Description: 클럭 단위 레지스터 전송 기술, 합성 가능

---

### Chap 2 — 설계 플로우 (Design Flow)

**칩 기본 구조**
- Wafer → Die → Chip 계층
- Devices: Transistors → Logic Gates & Cells → Function Blocks
- Interconnects: Local signals / Global signals / Clock signals / Power·Ground nets
- ASIC(위치 제한 없음, 최대 성능) vs FPGA(위치 한정, 단시간 설계)

**설계 Flow ★**
- Spec → System Design → 아키텍처 Design → RTL/Logic Design → HW Implementation → 통합 평가
- HW/SW partitioning: System 단계에서 결정
- High-level synthesis vs RTL synthesis 차이: clock step scheduling 여부
- Logic 최적화 단계: wire 지연 = 0 가정
- Physical Design: Placement(블록 위치) + Routing(배선 경로)

**Physical Design 배치 순서**
- Floorplanning → PDN 배선 → Placement → CTS(CDN) → Signal Routing → RC Extraction → Verification

**PDN / CDN / Metal Layer**
- Metal Layer: 높은 층 = 두껍고 저항 작음 = 전원/글로벌용, 낮은 층 = 얇고 로컬 신호용
- Via: 층간 수직 연결
- PDN(Power Delivery Network): Grid 구조, IR Drop / Ground Bounce 최소화 목표
- CDN(Clock Distribution Network): H-Tree 구조, Clock Skew 최소화 목표
- Signal Routing: 수평/수직 교대 Metal Layer 배정 (Crosstalk 최소화)

**신호 지연 R, C**
- R, C는 기생 성분(Parasitic) — 의도하지 않았지만 물리적으로 불가피
- R: 금속 배선 고유 저항 → 전압 강하(레벨 문제)
- C: 배선-기판/배선-배선 커패시터 → 충방전 지연(타이밍 문제)
- RC 지연 τ = R × C

**Power / Signal Integrity**
- Power Integrity: IR Drop, Power Grid Noise, Ground Bounce → 전원 안정 공급 문제
- Signal Integrity: RC 지연, Crosstalk, Reflection, EMI → 신호 파형 왜곡 문제
- 해결: 버퍼 삽입, Decoupling Capacitor, 배선 강화, Low-k 유전체

**DFT / Testing / Verification**
- Verification: 제조 전 설계 오류 찾기 (Simulation, Formal Verification, Emulation)
- Testing: 제조 후 불량 칩 선별
- DFT(Design For Testability): Controllability + Observability 높이는 설계 방법론
- Scan: FF들을 체인으로 연결 → 내부 상태 직렬 읽기/쓰기
- BIST(Built-In Self Test): LFSR(패턴 생성) + MISR(결과 압축) → 자가진단

**PPA & Timing**
- PPA: Power / Performance / Area — 항상 트레이드오프
- Slack = t_cy - (t_dCQ + t_dMax + t_s), Slack > 0이면 타이밍 통과
- Worst Gate Slack: 칩 전체에서 가장 작은 Slack
- f_effective = 1 / (T_target - Worst_Slack)
- Setup: t_cy > t_dCQ + t_dMax + t_s
- Hold: t_h < t_cCQ + t_cMin (클럭 주기와 무관, 어떤 속도에서도 위험)

**RTL 설계**
- RTL = Register Transfer Level: 클럭 단위로 레지스터 간 데이터 전송 기술
- Datapath 방식: 상태를 테이블 대신 수식으로 표현 (next = rst ? 0 : state + 1)
- Counter: next = rst ? 0 : state + 1
- Shift Register: next = rst ? 0 : {state[n-2:0], sin}
- Control/Datapath 분리: FSM(제어) + Datapath(연산) 역할 분담
- Status Signals: Datapath → Control, Control Signals: Control → Datapath

**Inverter × N (Drive Strength)**
- N배 크기 인버터: 트랜지스터 폭 N배 → 전류 N배, 출력저항 1/N배
- 입력 C도 N배 증가 → 앞단에 부담
- Buffer Chain: 단계적으로 크기 키우기 (3~4배씩) → 최적 지연
- 사용처: 큰 Fanout, 긴 배선 구동, Clock 분배

---

### Chap 3.1 — 불 대수 공리와 정리 (Boolean Algebra: Axioms & Theorems)

**기본 연산자**
- AND(·): 둘 다 1일 때만 1
- OR(+): 하나라도 1이면 1
- NOT('): 반전, 연산자 우선순위: NOT > AND > OR

**공리 (Axioms) — 증명 없이 참**
- Identity: 1·x=x, 0+x=x
- Annihilation: 0·x=0, 1+x=1
- Negation: 0'=1, 1'=0

**주요 성질 (Properties) ★**

| 이름 | AND 버전 | OR 버전 |
|------|---------|---------|
| Complementation | x·x'=0 | x+x'=1 |
| Idempotence | x·x=x | x+x=x |
| Absorption | x·(x+y)=x | x+(x·y)=x |
| Combining ★ | (x·y)+(x·y')=x | (x+y)·(x+y')=x |
| DeMorgan ★★ | (x·y)'=x'+y' | (x+y)'=x'·y' |
| Consensus | (x·y)+(x'·z)+(y·z)=(x·y)+(x'·z) | |
| Distributive (특수) | x+(y·z)=(x+y)·(x+z) | ← 일반 수학과 다름! |

**Duality (쌍대)**
- AND↔OR, 0↔1 교환 시 모든 정리 성립
- 정리 증명 수를 절반으로 줄임

**로직 함수 표현 5가지 & 유일성**
- English: 모호, 비유일
- Boolean Expression: 수학적, 비유일
- Truth Table: 완전, **유일 ✅**, 크기 2^n
- Schematic: 구현용, 비유일
- BDD(Binary Decision Diagram): **유일 ✅**(변수 순서 고정 시), 효율적
- ROBDD = Reduced Ordered BDD: 등가 검증에 핵심 자료구조

---

### Chap 3.2 — Normal Forms, Logic Diagram, Verilog

**Normal Form (정규형)**
- SoP(Sum of Products): AND항들을 OR로 연결
- Canonical SoP: 모든 항이 모든 변수 포함 → **유일 ✅**
- Minterm(mₙ): 모든 변수가 정확히 한 번 등장하는 AND항
- f = Σm(출력=1인 행 번호) 표기법
- 번호 규칙: 입력값을 이진수로 읽은 것 (a=1,b=0,c=1 → 101₂ = 5 → m₅)

**Shannon Expansion**
- f(a,b,c) = a'·f(0,b,c) + a·f(1,b,c)
- 반복 적용 → Canonical SoP 자동 생성

**수식 → 게이트 변환**
- SoP → 2단 AND-OR 회로 (1단: AND 게이트, 2단: OR 게이트)
- AND-OR → NAND-NAND: 드모르간 적용, 기능 동일, 트랜지스터 효율적
- Bubble Rule: 버블(○) 두 개 만나면 상쇄 (이중 반전 = 반전 없음)
- NAND-NAND = AND-OR (버블 규칙으로 증명)

**XOR**
- a⊕b = a'b + ab' (둘이 다를 때 1)
- a⊕1 = a' → 제어 가능 인버터
- a⊕0 = a, a⊕a = 0, a⊕a' = 1
- NAND 4개로 구현 가능

**AOI / OAI (Complex Gates)**
- AOI(AND-OR-Inverter): f = (AND그룹들의 OR)' → Pull-Down: AND직렬·그룹병렬
- OAI(OR-AND-Inverter): f = (OR그룹들의 AND)' → Pull-Down: OR병렬·그룹직렬
- 명명법: AOI22 = AND(2)·OR·AND(2)·INV, OAI13 = OR(1)·AND·OR(3)·INV
- 최적화 효과: 트랜지스터 ~50% 감소, 게이트 단수 3단→1단

**Verilog**
- &(AND), |(OR), ~(NOT), ^(XOR), ~^(XNOR)
- assign f = 불표현식 → 합성기 자동 최적화

---

### Chap 6.1 — 카르노 맵 (Karnaugh Map)

**K-map 원리**
- Combining 정리 시각화 도구: 인접 Minterm 묶기 = 변수 제거
- Gray Code 배열: 인접 칸은 항상 1비트만 다름 → Combining 적용 가능
- 가장자리 Wrap-around: 상하/좌우 연결 (토로이드 구조)

**Implicant & Cube**
- Implicant: 출력=1을 만드는 입력 조합 집합
- k-cube: 2^k개 Minterm 묶음, 변수 k개 제거됨
- X 표기: 제거된 변수 (Don't care)
- 묶음 클수록 → 항 단순 → 게이트 입력 수 감소

**묶음 규칙**
- 크기: 반드시 2의 거듭제곱 (1, 2, 4, 8, ...)
- 모양: 직사각형
- 전략: 가능한 한 크게 묶기

**Prime Implicant (PI) & Essential PI**
- PI: 더 이상 크게 묶을 수 없는 최대 크기 Implicant
- Essential PI: 특정 Minterm을 오직 하나의 PI로만 커버 → 반드시 선택
- 최소 SoP 절차: PI 찾기 → Essential PI 선택 → 나머지 최소 커버

**Canonical SoP → Simplified SoP 관계**
- Canonical: 모든 Minterm 나열, 유일하지만 복잡
- K-map: 인접 Minterm 합쳐서 항 수·리터럴 수 최소화
- 결과: Simplified SoP → 최소 게이트 구현
- CAD 도구는 멀티레벨 회로까지 고려해 더 잘 최적화

---

### 조합 논리
<!-- MUX, 디코더, 인코더, ALU - 추후 업데이트 -->

### 순차 논리

#### Chap 10 — Latch & Flip-flop

**진화 흐름 ★**
- RS Latch → Gated Latch → Master-Slave FF → D Flip-flop
- 각 단계마다 이전 소자의 문제를 해결

**RS Latch**
- 피드백 구조(NOR×2)로 기억 가능
- S=1→Q=1(Set), R=1→Q=0(Reset), SR=00→Hold, SR=11→불안정(사용 금지)

**Gated Latch (Level-Sensitive Latch)**
- Enable=1인 동안만 S, R 동작
- Level-Sensitive: Enable High 레벨 동안 입력 변화가 즉시 출력에 반영
- 문제: Transparency — Enable=1 동안 입력이 출력에 계속 투명하게 보임

**Master-Slave Flip-flop**
- Master(CLK=1에 열림) + Slave(CLK=0에 열림) 직렬 구성
- Transparency 해결: 한 번에 하나씩만 열림
- Falling-edge triggered (하강 엣지 트리거)
- 문제: 1's Catching — CLK=1 동안 글리치(0-1-0)가 Master에 포착됨

**D Flip-flop ★★ (현재 표준)**
- S=D, R=D' 강제 → SR=11 불가 → 1's Catching 해결
- Rising-edge triggered (상승 엣지 트리거)
- 동작: 클럭 상승 엣지 직전의 D값이 Q로 저장
- Positive/Negative edge-triggered FF 트랜지스터 수 동일 (CLK↔CLK' 교환)

**타이밍 파라미터 3가지 ★★★**
- Tsu (Setup Time): 클럭 엣지 전 D가 안정되어야 하는 최소 시간 (예: 1.8ns)
- Th (Hold Time): 클럭 엣지 후 D가 유지되어야 하는 최소 시간 (예: 0.5ns)
- Tc2q (Clock-to-Q): 클럭 엣지 후 Q 출력 안정까지 지연 (예: 1.1ns)
- 위반 시 → Metastability 발생 가능

**Latch vs Flip-flop 핵심 차이 ★**
- Latch: Level-sensitive, Enable=1 동안 투명(계속 반응)
- FF: Edge-triggered, 엣지 순간만 캡처 (투명성 없음)

**FF 전력 소모가 큰 이유**
- 클럭 자체 스위칭 전력 (칩 전체 전력의 20~40%)
- 매 클럭마다 FF 내부 노드 충전/방전 (값 안 바뀌어도 동작)

### 상태 머신
<!-- Mealy vs Moore, 상태 최소화, 인코딩 - 추후 업데이트 -->

### 타이밍 분석

#### Chap 15 — Timing Constraints

**두 가지 지연 개념 ★**
- Propagation Delay (t_d): 입력 완전 안정 → 출력 완전 안정 (최악, Critical Path)
- Contamination Delay (t_c): 입력 첫 변화 → 출력 첫 변화 (최선, 가장 빠른 경로)
- 항상 t_c ≤ t_d
- t_d: "언제부터 출력을 믿을 수 있나?" → Setup에 사용
- t_c: "언제부터 출력이 이전 값이 아닌가?" → Hold에 사용

**D FF의 지연 구분**
- t_dCQ: Clock-to-Q Propagation Delay (최악)
- t_cCQ: Clock-to-Q Contamination Delay (최선)

**Setup Time Constraint ★★★**
- t_cy > t_dCQ + t_dMax + t_s
- Slack = t_cy - (t_dCQ + t_dMax + t_s)
- Slack > 0 → 통과, Slack < 0 → 위반
- 위반 시 해결: 클럭 주기 늘리기 or Critical Path 최적화

**Hold Time Constraint ★★★**
- t_h < t_cCQ + t_cMin
- "Unsafe at any speed" — 클럭 주기와 무관!
- 위반 시 해결: 버퍼 삽입으로 t_cMin 증가
- FF를 직접 연결하면 Hold 위반 위험 (t_cMin = 0)

**Clock Skew (t_k) 포함 수식**
- Setup: t_cy > t_dCQ + t_dMax + t_s - t_k  (FF2가 늦게 받으면 Setup에 유리)
- Hold:  t_h < t_cCQ + t_cMin + t_k         (같은 경우 Hold에 불리)
- Skew 양면성: Setup ↔ Hold 트레이드오프

**최소 클럭 주기 / 최대 주파수**
- t_cy_min = t_dCQ + t_dMax + t_s - t_k
- f_max = 1 / t_cy_min

**합성 리포트 읽기**
- Area Report: Combinational area, Noncombinational area, Total cell area
- Timing Report: Startpoint→Endpoint, Incr(게이트 지연), Path(누적 지연), data arrival time
- Levels of Logic: 크리티컬 패스 게이트 단수
- Logic 지연 vs Route 지연: 둘의 비율로 최적화 방향 결정

### 기타

---

## 디지털 집적회로

### CMOS 기초
<!-- NMOS/PMOS 동작, CMOS 인버터, 전달 특성 -->

### 논리 게이트 설계
<!-- CMOS 게이트, 복합 게이트, 사이징 -->

### 전력 분석
<!-- 동적 전력, 정적 전력, 누설 전류 -->

### 배선 & 지연
<!-- RC 모델, Elmore 지연, 인터커넥트 -->

### 메모리 회로
<!-- SRAM 셀, DRAM, 센스 앰프 -->

### 저전력 설계
<!-- 전압 스케일링, 클럭 게이팅, 파워 게이팅 -->

### 기타

---

## 과목 간 연결 포인트
<!-- 추상화 수준별 연결: 트랜지스터 → 게이트 → 시스템 -->

---

## 시험 대비 핵심 요약

---

## 오답 & 취약 영역
