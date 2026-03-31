# 논리설계 — 오픈북 시험 참고 문서

> 마지막 업데이트: 2026-03-20 | 완료 챕터: Chap 1.1, 1.2, 2, 3.1, 3.2, 6.1, 8, 10, 11, 14.2, 14.3, 15, 20, 28, 29, Low Power Design
> 구성: 수식 모음 → 핵심 비교표 → 용어 정의 → 주제별 상세

---

## ① 수식 모음 (시험 중 빠른 참조)

### 노이즈 마진
| 수식 | 의미 |
|------|------|
| V_NML = V_IL - V_OL | Low 노이즈 마진 |
| V_NMH = V_OH - V_IH | High 노이즈 마진 |

### Number Systems
| 수식 | 의미 |
|------|------|
| 2's Comp(N) = 비트반전 + 1 | 2의 보수 변환 |
| 범위 (n비트 2's Comp) = -2^(n-1) ~ +2^(n-1)-1 | 표현 범위 |
| Overflow = Cin(MSB) XOR Cout(MSB) | 오버플로우 검출 |
| Fixed-point 변환: 실수 × 2^f → 반올림 → 이진수 | 고정소수점 변환 |
| Floating-point: M × 2^(E-Bias) | 부동소수점 값 |
| 절대 오차 (f비트 Fixed) = 2^(-(f+1)) | 고정소수점 최대 오차 |

### 타이밍 제약 (Timing Constraints)
| 수식 | 조건 | 비고 |
|------|------|------|
| t_cy > t_dCQ + t_dMax + t_s | Setup (Skew 없음) | 위반 시 클럭 늘리기 |
| t_h < t_cCQ + t_cMin | Hold (Skew 없음) | "Unsafe at any speed" |
| t_cy > t_dCQ + t_dMax + t_s - t_k | Setup (Skew 포함) | t_k↑ → Setup 유리 |
| t_h < t_cCQ + t_cMin + t_k | Hold (Skew 포함) | t_k↑ → Hold 불리 |
| Slack = t_cy - (t_dCQ + t_dMax + t_s) | Setup Slack | >0이면 통과 |
| t_cy_min = t_dCQ + t_dMax + t_s - t_k | 최소 클럭 주기 | |
| f_max = 1 / t_cy_min | 최대 동작 주파수 | |

### Metastability / Synchronizer
| 수식 | 의미 |
|------|------|
| DV(t) = DV(0) × e^(t/τ) | 메타스태블 상태 해소 동역학 |
| P_E = (t_s + t_h) / t_cy | 메타스태블 진입 확률 |
| P_S = exp(-t_w / τ) | 탈출 못할 확률 |
| P_F = P_E × P_S | 단일 이벤트 오류 확률 |
| f_F = f_a × P_F | 단위 시간당 오류 빈도 |
| MTTF = 1 / f_F | 평균 고장 간격 |
| t_w = t_cy - t_s - t_dCQ | FF 2개 기준 대기 시간 |

### 저전력 설계
| 수식 | 의미 |
|------|------|
| P_dynamic = ½ × S × C × V² × F | 동적 전력 |
| I_sub = K₁×W×e^(-Vth/nV₀) | Subthreshold Leakage |
| I_ox = K₂×W×(V/T_ox)²×e^(-aT_ox) | Gate-oxide Leakage |

---

## ② 핵심 비교표

### Combinational vs Sequential
| 구분 | Combinational | Sequential |
|------|--------------|------------|
| 출력 | f(현재 입력) | f(현재 입력 + 이전 상태) |
| 메모리 | 없음 | 있음 (레지스터) |
| 클럭 | 불필요 | 필요 |
| 피드백 | 없음 | 있음 |
| Verilog | assign / always @(*) | always @(posedge clk) |

### Latch vs Flip-flop
| 구분 | Latch | Flip-flop |
|------|-------|-----------|
| 트리거 방식 | Level-sensitive | Edge-triggered |
| 언제 바뀌나 | Enable=1인 동안 계속 | 클럭 엣지 순간만 |
| 투명성 | 있음 (Transparent) | 없음 |
| 용도 | 특수 상황 | 일반 순차 논리 (표준) |

### Setup vs Hold Violation
| 구분 | Setup Violation | Hold Violation |
|------|----------------|----------------|
| 원인 | 데이터가 너무 늦게 도착 | 데이터가 너무 빨리 도착 |
| 클럭으로 해결? | ✅ 클럭 주기 늘리기 | ❌ "Unsafe at any speed" |
| 해결책 | t_cy↑, Critical Path 최적화 | 버퍼 삽입 (t_cMin↑) |
| 관련 지연 | t_dMax (최악 지연) | t_cMin (최선 지연) |

### Propagation vs Contamination Delay
| 구분 | Propagation Delay (t_d) | Contamination Delay (t_c) |
|------|------------------------|--------------------------|
| 정의 | 입력 안정 → 출력 안정 | 입력 첫 변화 → 출력 첫 변화 |
| 경우 | 최악 (Worst case) | 최선 (Best case) |
| 용도 | Setup Constraint | Hold Constraint |
| 대소 | t_d ≥ t_c | t_c ≤ t_d |

### Static vs Dynamic Power
| 구분 | Static Power | Dynamic Power |
|------|-------------|---------------|
| 발생 시점 | 항상 (동작 무관) | 회로 동작 시 |
| 주요 원인 | Leakage 전류 | 커패시턴스 충방전 |
| 민감 요소 | Vth, T_ox | V², F |
| 공정 미세화 영향 | 기하급수적 증가 | 증가 |
| 해결 기법 | Power Gating, High-k | Clock Gating, DVS |

### Clock Gating 비교
| 구분 | ILD (Idle Logic Driven) | DTD (Data Toggling Driven) |
|------|------------------------|---------------------------|
| 기반 | en 신호 | XOR (din ≠ dout 검출) |
| 적용 범위 | en 있는 FF만 | 모든 FF (범용) |
| 면적 overhead | 작음 | 40%↑ |
| 클럭 절감 | ~37% | ~33% |

### 로직 표현 5가지 유일성
| 표현 | 유일성 | 주요 용도 |
|------|--------|---------|
| English | ❌ | 스펙 작성 |
| Boolean Expression | ❌ | 수학적 분석 |
| Truth Table | ✅ | 완전한 함수 정의, 검증 |
| Schematic | ❌ | 실제 구현 |
| BDD (순서 고정 시) | ✅ | EDA 툴, 등가 검증 |

### Binary vs One-Hot State Assignment
| 구분 | Binary 인코딩 | One-Hot 인코딩 |
|------|--------------|----------------|
| 비트 수 | ⌈log₂n⌉ 비트 | n 비트 |
| FF 수 | 적음 (최소) | 많음 (상태 수만큼) |
| 조합 논리 | 복잡 | 단순 |
| 속도 | 보통 | 빠름 |
| 면적 | 작음 | 큼 |
| next state 수식 | 카르노맵 필요 | 전이도에서 직접 읽음 |
| 주요 사용처 | 상태 많은 FSM, ASIC | 상태 적은 FSM, FPGA |

### Moore vs Mealy FSM
| 구분 | Moore Machine | Mealy Machine |
|------|--------------|---------------|
| 출력 결정 | f(state) | f(state, input) |
| 출력 표기 위치 | 상태 원 안 | 전이 화살표 위 |
| 출력 변화 시점 | 클럭 엣지 후 | 입력 변화 즉시 |
| 안정성 | 글리치 없음 ✅ | 입력 글리치 전파 가능 |
| 반응 속도 | 1클럭 지연 | 즉각 반응 |
| 상태 수 | 상대적으로 많음 | 상대적으로 적음 |
| Verilog 출력 위치 | 별도 assign | next state와 같은 always |
| 사용 빈도 | 많음 (안정적) | 속도 중요 시 |

### Verilog 핵심 구분
| 구분 | wire | reg |
|------|------|-----|
| 의미 | 물리적 연결선 | 값 저장 변수 |
| 사용 위치 | assign, 포트 연결 | always 블록 내부 |
| 회로 대응 | 조합 논리 | FF or 조합 |

### Verification vs Test vs Characterization
| 구분 | Verification | Test | Characterization |
|------|-------------|------|-----------------|
| 목적 | 설계가 스펙 만족? | 제조가 올바른가? | 성능 파라미터 측정 |
| 시점 | 제조 전 | 제조 후 | 제조 후 |
| 대상 | 설계 자체 | 모든 칩 (전수) | 샘플만 |
| 주요 도구 | Simulation, STA, Formal | ATPG, Scan, BIST | V-I 측정, 가속 수명 |

### 정수 표현 방식 비교 (n=4비트 기준)
| 구분 | Sign-Magnitude | 1's Complement | 2's Complement |
|------|---------------|----------------|----------------|
| 음수 변환 | MSB=1, 절대값 | 비트 전체 반전 | 비트 반전 + 1 |
| 0의 개수 | 2개 (+0, -0) | 2개 (+0, -0) | 1개 ✅ |
| 표현 범위 | -7 ~ +7 | -7 ~ +7 | -8 ~ +7 ✅ |
| 덧셈 복잡도 | 복잡 | 중간 (End-around carry) | 단순 ✅ |
| 현재 사용 | 거의 없음 | 없음 | 현대 표준 ✅ |

### Fixed-Point vs Floating-Point
| 구분 | Fixed-Point | Floating-Point |
|------|------------|----------------|
| 소수점 위치 | 고정 | 동적 (이동 가능) |
| 표현 범위 | 좁음 | 매우 넓음 |
| 오차 종류 | 절대 오차 | 상대 오차 |
| 연산 복잡도 | 단순 | 복잡 (FPU 필요) |
| 음수 방식 | 2의 보수 | 부호-절대값 (MSB) |
| 표기법 | i.f, si.f | M × 2^(E-Bias) |
| 주요 용도 | DSP, 임베디드 | 과학 계산, 그래픽 |

### Combinational Building Blocks 비교
| 블록 | 입력 | 출력 | 기능 | Verilog 핵심 |
|------|------|------|------|-------------|
| Decoder | n비트 이진 | 2^n 비트 One-hot | 이진→One-hot | `1 << a` |
| Encoder | 2^n 비트 One-hot | n비트 이진 | One-hot→이진 | OR 패턴 |
| MUX | n개 k비트 입력 + select | k비트 | 입력 선택 | `({k{s[i]}} & ai)` OR |
| Arbiter | n비트 request | n비트 grant | 첫 번째 1 선택 | carry chain |
| Priority Encoder | n비트 | log₂n 비트 | 첫 1의 위치 이진수 | Arbiter+Encoder |
| Eq Comparator | a, b (n비트) | 1비트 eq | a==b? | `a==b` |
| Mag Comparator | a, b (n비트) | 1비트 gt | a>b? | `a>b` |

### ROM vs RAM vs PLA
| 구분 | ROM | RAM | PLA |
|------|-----|-----|-----|
| 쓰기 가능 | ❌ | ✅ | ❌ (설계 시 고정) |
| 구조 | Decoder + 연결망 | Decoder + R/W | AND배열 + OR배열 |
| AND항 수 | 2^n (모든 Minterm) | 2^n | 필요한 것만 |
| 주요 용도 | 룩업 테이블, 로직 | 데이터 저장 | 복수 SoP 함수 |

### Stuck-at Fault 검출 조건
| 조건 | 설명 |
|------|------|
| Sensitization | 해당 노드가 결함값과 반대 값이 되도록 입력 인가 |
| Propagation | 해당 노드의 값이 외부 출력까지 전달되도록 설정 |
| Fault Coverage | 검출된 Fault 수 / 전체 Fault 수 (목표: 95~99%) |

---

## ③ 용어 정의 (가나다순)

**2's Complement (2의 보수)**: 현대 컴퓨터 정수 표현 표준. 비트 반전+1. 0 하나, 덧셈 단순. n비트 범위: -2^(n-1) ~ 2^(n-1)-1.

**Arbiter (중재기)**: n비트 request 중 첫 번째 1을 찾아 grant. carry chain 구조. Priority Encoder = Arbiter + Encoder.

**ATPG (Automatic Test Pattern Generation)**: 특정 Fault를 검출하는 테스트 패턴을 자동 생성. Sensitization + Propagation 조건 만족.

**BDD (Binary Decision Diagram)**: 변수 순서 고정 후 결정 트리를 압축한 논리 함수 표현. ROBDD는 유일성 보장.

**BIST (Built-In Self Test)**: 칩 내부에 테스트 회로 내장. LFSR(패턴 생성) + MISR(결과 압축)으로 자가진단.

**Canonical SoP**: 모든 항이 모든 변수를 포함하는 SoP. 진리표와 1:1 대응, 유일성 보장.

**CDN (Clock Distribution Network)**: 클럭을 전체 FF에 동시 공급하는 배선망. H-Tree 구조, Clock Skew 최소화 목표.

**Clock Skew (t_k)**: FF2 클럭 도착 시간 - FF1 클럭 도착 시간. Setup에는 유리, Hold에는 불리 (양수일 때).

**Contamination Delay (t_c)**: 입력이 처음 변한 순간 → 출력이 처음 흔들리기 시작하는 시간. Hold에 사용.

**Arbiter (중재기)**: n비트 request 중 첫 번째 1을 찾아 grant. carry chain 구조. Priority Encoder = Arbiter + Encoder.

**Critical Path**: 칩에서 가장 지연이 긴 신호 경로. 최대 동작 주파수를 결정.

**Characterization (특성화)**: 샘플 칩의 동작 범위·파라미터·노화 특성 측정. NBTI, HCI, 온도 영향 포함.

**Decoder (디코더)**: n비트 이진 → 2^n 비트 One-hot 변환. b=1<<a. 분할 정복으로 대형 디코더 구성.

**DFT (Design For Testability)**: 테스트 용이성을 위한 설계 방법론. Controllability + Observability 향상.

**DVS (Dynamic Voltage Scaling)**: 부하에 따라 전압/주파수를 동적으로 조절. DC-DC Converter 필요.

**Encoder (인코더)**: One-hot → 이진 코드 변환. Decoder 역방향. 대형: 2단 구성 + any-input-true 출력.

**Essential PI**: 특정 Minterm을 오직 하나의 PI로만 커버할 수 있는 Prime Implicant. 반드시 선택.

**Fault Coverage**: 검출된 Stuck-at Fault 수 / 전체 Fault 수. 테스트 품질 지표. 목표 95~99%.

**FIFO Synchronizer**: 멀티비트 신호를 클럭 도메인 간 안전하게 전달. 포인터만 Gray Code + Brute-Force Sync.

**Fixed-Point (고정소수점)**: si.f 형식. 소수점 위치 고정. 절대 오차 = 2^(-(f+1)). 변환: 실수×2^f → 반올림 → 이진수.

**Floating-Point (부동소수점)**: M × 2^(E-Bias). Mantissa(가수) + Exponent(지수). Implied 1 (정규화 시 맨 앞 1 저장 생략). 상대 오차.

**Formal Verification**: 수학적 증명으로 기능 정확성 확인. 테스트 패턴 불필요. 소규모 블록에 적합.

**MUX (Multiplexer)**: n개의 k비트 입력 중 select로 하나 선택. One-hot select: s[i]로 마스킹 후 OR. Binary MUX = Decoder + One-hot MUX.

**Overflow (오버플로우)**: 2의 보수 연산 결과가 표현 범위 초과. 검출: Carry-in(MSB) XOR Carry-out(MSB) = 1이면 오버플로우.

**PLA (Programmable Logic Array)**: AND 배열 + OR 배열. ROM보다 적은 AND항으로 복수 SoP 함수 구현.

**Gray Code**: 인접 값 사이에 1비트만 변화하는 인코딩. 멀티비트 동기화에 사용.

**Hold Time (t_h)**: 클럭 엣지 이후 D 입력이 안정적으로 유지되어야 하는 최소 시간.

**Implicant**: 출력=1을 만드는 입력 조합 집합. k-cube = 2^k개 Minterm 묶음.

**IR Drop**: 전원 배선의 저항으로 인한 전압 강하. Power Integrity 문제.

**Mealy Machine**: 출력 = f(state, input). 전이 화살표에 출력 표기. 즉각 반응, 상태 수 적음. 글리치 가능.

**Metastability**: Setup/Hold 위반 시 FF가 0도 1도 아닌 불법 중간 상태에 빠지는 현상. 제거 불가, 확률만 줄일 수 있음.

**Moore Machine**: 출력 = f(state). 상태 원 안에 출력 표기. 클럭 동기 출력, 글리치 없음. 신호등 FSM이 대표 예.

**Minterm (mₙ)**: 모든 변수가 정확히 한 번 등장하는 AND항. n번 Minterm = 이진수 n에 해당하는 입력 조합.

**PDN (Power Delivery Network)**: 전원을 칩 전체에 공급하는 배선망. Grid 구조, IR Drop 최소화.

**PPA**: Power / Performance / Area. 설계의 3대 지표, 항상 트레이드오프.

**Prime Implicant (PI)**: 더 이상 크게 묶을 수 없는 최대 크기 Implicant.

**Propagation Delay (t_d)**: 입력이 완전히 안정된 후 → 출력이 완전히 안정될 때까지의 시간. Setup에 사용.

**RTL (Register Transfer Level)**: 클럭 단위로 레지스터 간 데이터 전송을 기술하는 설계 수준.

**Scan**: FF들을 직렬 체인으로 연결. 내부 상태를 외부에서 읽고 쓸 수 있게 함.

**Setup Time (t_s)**: 클럭 엣지 이전에 D 입력이 안정적이어야 하는 최소 시간.

**Shannon Expansion**: f(a,b,c) = a'·f(0,b,c) + a·f(1,b,c). 변수를 기준으로 함수를 두 개로 분리.

**Slack**: 타이밍 여유. = t_cy - (t_dCQ + t_dMax + t_s). 양수면 통과, 음수면 위반.

**One-Hot 인코딩**: n개 상태에 n비트를 사용. 한 번에 1비트만 1. next state 수식을 전이도에서 직접 읽을 수 있음. FPGA에 적합.

**State Assignment**: FSM의 각 상태에 이진수 코드를 부여하는 과정. Binary 또는 One-Hot 방식. 선택에 따라 회로 크기/속도 달라짐.

**SoP (Sum of Products)**: AND항들을 OR로 연결한 불 표현식 형태.

**τ (시정수)**: FF의 메타스태빌리티 해소 속도. 작을수록 빨리 안정됨.

**Transparency**: Latch의 특성. Enable=1 동안 입력 변화가 즉시 출력에 반영됨.

---

## ④ 주제별 상세

### 디지털 추상화 (Chap 1.1)
- 노이즈 마진 내 노이즈 → 게이트 통과 시 자동 복원
- 전압 파라미터 (2.5V LVCMOS): V_OL=0.2V, V_IL=0.7V, V_IH=1.7V, V_OH=2.1V
- Forbidden Zone: V_IL ~ V_IH (입력 미정의 구간)
- DC Transfer Curve: 입력→출력 전압 관계, 신호 복원 조건 만족 필수

### Verilog 핵심 (Chap 1.2)
- `wire` + `assign` = Continuous Assignment = 조합 논리 (입력 바뀌면 즉시 반영)
- `reg` + `always @(posedge clk)` = 순차 논리
- `wire f = expr` ≡ `wire f; assign f = expr` ≡ `assign f = expr` (합성 동일)
- Synthesis: Transform (RTL→게이트) → Optimize (제약 만족)
- 합성 가능: assign, always @(*), always @(posedge clk)
- 합성 불가: #(시간 지연), initial, $display

### 설계 플로우 (Chap 2)
```
Spec → System → Architecture → RTL/Logic → HW Implementation → 통합 평가
```
- HW/SW partitioning: System 단계
- High-level vs RTL synthesis 차이: clock step scheduling 여부
- Logic 최적화 단계: wire 지연 = 0 가정
- Physical Design 순서: Floorplan → PDN → Placement → CTS → Signal Routing → RC Extraction

### 불 대수 핵심 정리 (Chap 3.1)

**공리**: Identity(1·x=x, 0+x=x), Annihilation(0·x=0, 1+x=1), Negation(0'=1, 1'=0)

**자주 쓰는 정리**:
- Absorption: x+(x·y)=x, x·(x+y)=x
- Combining: (x·y)+(x·y')=x ← K-map의 핵심
- DeMorgan: (x·y)'=x'+y', (x+y)'=x'·y' ← NAND/NOR 변환 핵심
- 특수 Distributive: x+(y·z)=(x+y)·(x+z) ← 일반 수학과 다름!
- Duality: AND↔OR, 0↔1 교환 시 모든 정리 성립

### Normal Form & 게이트 변환 (Chap 3.2)
- Canonical SoP = Σm(출력=1인 행 번호) → 유일성 보장
- SoP → 2단 AND-OR → NAND-NAND (드모르간, 기능 동일)
- Bubble Rule: ○○ 쌍은 상쇄 (이중 반전)
- AOI(AND그룹 OR 후 반전), OAI(OR그룹 AND 후 반전) → 트랜지스터 ~50% 감소
- XOR: a⊕b = a'b+ab', a⊕1=a'(제어 반전), a⊕0=a

### 카르노 맵 (Chap 6.1)
- Gray Code 배열 → 인접 칸 1비트만 다름 → Combining 정리 시각화
- 묶음 규칙: 2의 거듭제곱, 직사각형, 최대한 크게, 가장자리 연결
- PI 찾기 → Essential PI 선택 → 나머지 최소 커버 = 최소 SoP

### Latch & Flip-flop 진화 (Chap 10)
```
RS Latch → Gated Latch → Master-Slave FF → D Flip-flop
  SR=11금지  Transparency   1's Catching    현재 표준
```
- D FF 타이밍 파라미터: Tsu(1.8ns), Th(0.5ns), Tc2q(1.1ns)
- FF 전력 큰 이유: ①클럭 스위칭(전체 20~40%) ②내부 노드 매 클럭 충방전

### Timing Constraints (Chap 15)
- t_d ≥ t_c (Propagation ≥ Contamination)
- t_dCQ: Clock-to-Q 최악 / t_cCQ: Clock-to-Q 최선
- Setup 위반 → 클럭 주기 늘리기 / Hold 위반 → 버퍼 삽입
- Hold 위반은 클럭 주기와 무관! ("Unsafe at any speed")

### Metastability (Chap 28)
- Setup/Hold 위반 시 → 0도 1도 아닌 불법 상태
- DV(t) = DV(0)×e^(t/τ) → 지수적 해소 but 시간 불확실
- P_failure = f_a × f_cy × (t_s+t_h) × exp(-t_w/τ)
- 제거 불가, 확률만 줄이는 것

### Synchronizer Design (Chap 29)
- Brute-Force: FF 직렬 연결로 t_w 확보 → P_S 기하급수적 감소
- 멀티비트: Gray Code (1비트만 변화) → Brute-Force 적용 가능
- 임의 멀티비트: FIFO Synchronizer (포인터만 Gray Code + Sync)
- 사용처: 비동기 외부 입력, 클럭 도메인 경계

### State Assignment (Chap 14.2)
- FSM 상태에 이진수 코드를 부여하는 과정. 선택에 따라 회로 크기/속도 달라짐
- Binary: ⌈log₂n⌉ 비트, FF 적음, 조합 복잡. Gray Code 순서로 배정 권장
- One-Hot: n비트, FF = 상태 수, 조합 단순. next_X = OR(X로 전이되는 모든 조건)
- Verilog FSM 3단 구조: ①FF(State Reg) ②always@(*)+casex(Next State) ③assign(Output)
- `define으로 상태 코드 정의 (가독성, 변경 용이)
- One-Hot 사용처: FPGA(FF 풍부), 속도 중요, 상태 적은 FSM

### Moore vs Mealy FSM
- Moore: 출력 = f(state), 상태 원 안에 출력 표기, 클럭 동기 안정 출력
- Mealy: 출력 = f(state, input), 전이 화살표에 입력/출력 표기, 즉각 반응
- Moore 장점: 글리치 없음, 디버깅 쉬움 → 더 많이 사용
- Mealy 장점: 1클럭 빠른 반응, 상태 수 적음
- Verilog: Moore는 출력을 별도 assign, Mealy는 next state와 같은 always 블록
- 신호등 FSM = Moore (출력이 상태만으로 고정, carew는 next state에만 영향)

### FSM 설계 전체 흐름 (Chap 14.3)
```
① 동작 서술 → ② State Diagram → ③ State Table(추상)
→ ④ State Assignment(이진코드) → ⑤ Encoded State Table
→ ⑥ K-map(next state 비트별) → ⑦ Logic Equations → ⑧ 회로도
```
- State Table: 현재상태 | next(!input) | next(input) | 출력
- Encoded Table: 추상 상태명을 이진수로 교체
- K-map: next state 비트(ns1, ns0) 각각, 출력 비트 각각 따로 작성
- Moore 출력 K-map: state 비트만 변수 (입력 열 없음)
- 신호등 Binary(Gray Code) 예시:
  - ns1 = s0
  - ns0 = (s0 | carew) & !s1
  - lgns=!s1&!s0, lyns=s0&!s1, lrns=s1, lgew=s0&s1, lyew=!s0&s1, lrew=!s1
- Gray Code State Assignment 이유: K-map 인접 묶기 쉬움, 글리치 최소화
- Verilog 스타일 가이드: DFF 명시적 인스턴스, Inferred Latch 금지, reset 필수, `define 사용

### Low Power Design
- Dynamic Power: P = ½SCV²F → V² 민감 (전압 낮추기 최우선)
- Static Power: Leakage → 공정 미세화로 비중 급증
- Clock Gating: 클럭 차단(Dynamic↓), ILD(en 기반)/DTD(XOR 기반)
- Power Gating: 전원 차단(Static+Dynamic↓), SRFF로 상태 보존
- DVS: 전압/주파수 동적 조절, DC-DC Converter 필요

### Combinational Building Blocks (Chap 8)
**설계 철학: Divide and Conquer — 블록 조립**
- Decoder: 이진→One-hot. `b = 1<<a`. 분할: n비트를 k비트씩 나눠 Decoder + AND 조합
- Encoder: One-hot→이진. Decoder 역방향. 대형: 2단(Low bits + High bits), any-input-true(c=|a) 필요
- MUX: select 신호로 입력 중 하나 선택. One-hot select: `({k{s[i]}} & ai)` OR. Binary MUX = Decoder + One-hot MUX
- Arbiter: 첫 번째 1 찾아 grant. carry chain: `c = {..., 1'b1}; g = r & c`
- Priority Encoder = Arbiter + Encoder (첫 1의 위치를 이진수로 출력)
- Eq Comparator: `assign eq = (a==b)`. Mag Comparator: `assign gt = (a>b)`
- Maximum Unit: Magnitude Comparator + 2:1 MUX 결합
- Barrel Shifter: 순환 시프트. 밀려난 비트가 반대쪽으로 재투입
- ROM: Decoder + 연결망. 2D 배열로 구현. 임의 논리 함수 구현 가능
- RAM: ROM + 쓰기 기능. 단일포트/듀얼포트
- PLA: AND 배열 + OR 배열. 필요한 곱항만 생성 → ROM보다 효율적

**MUX/Decoder로 임의 논리 함수 구현**
- Decoder: 원하는 Minterm들을 OR → `wire f = b[1]|b[3]|b[5]|b[7]`
- MUX: Binary select MUX, 데이터 입력에 진리표 상수 직접 입력

### Number Systems (Chap 11)
**정수 음수 표현 3가지**
- Sign-Magnitude: MSB=부호(0양수/1음수), 나머지=절대값. 0 두 개, 덧셈 복잡 → 미사용
- 1's Complement: 전체 비트 반전. 0 두 개, End-around carry → 미사용
- 2's Complement: 비트 반전 + 1. 0 하나, 덧셈 단순 → 현대 표준

**2의 보수 핵심**
- 변환: 비트 반전 후 +1 (역변환도 동일)
- 뺄셈 = 덧셈: A - B = A + (B의 2의 보수)
- 올림수(Carry out) 발생 시 무시 (정상 동작)
- Overflow 검출: Carry-in(부호비트) XOR Carry-out(부호비트) = 1
- Overflow 발생 조건: 양수+양수=음수 OR 음수+음수=양수

**Fixed-Point (si.f 형식)**
- i = 정수 비트 수, f = 소수 비트 수, s = 부호 (2의 보수)
- 변환: 실수 × 2^f → 반올림 → 이진수
- 절대 오차(최대) = 2^(-(f+1))
- 예: 1.389 → ×8=11.112 → 반올림=11 → 1011₂ = 1.375

**Floating-Point (M × 2^(E-Bias))**
- Mantissa(가수): 정규화 = 1.xxx 형태, Implied 1 (맨 앞 1 저장 생략)
- Exponent(지수): 실제 지수 = 저장값 - Bias
- 부호: 부호-절대값 방식 (MSB)
- 상대 오차: 값의 크기에 비례, 넓은 범위에서 균일한 정밀도
- IEEE 754 (32비트): 부호 1 + 지수 8 + 가수 23, Bias=127

### Verification and Test (Chap 20)
- Spec Coverage: 스펙 기능 100% 검증 필수
- Impl Coverage: 코드 모든 줄 + FSM 모든 엣지 실행
- Directed Test: 경계 케이스 수동 작성 (23:59:59→00:00:00 등)
- Random Test: 무작위 입력, 상위 모델(C++)과 출력 비교
- STA (Static Timing Analysis): 패턴 없이 모든 경로 타이밍 수학적 분석. False Path 오보고 한계
- Formal Verification: 수학적 증명, 패턴 불필요, 소규모 블록 적합

**Test (제조 테스트) — 제조 후 전수**
- Stuck-at Fault: SA0(항상 0 고착)/SA1(항상 1 고착) → 실제 제조 결함과 유사
- Fault 검출 조건: Sensitization(결함값 반대 인가) + Propagation(출력까지 전달)
- ATPG: Fault 검출 테스트 패턴 자동 생성. Fault Coverage = 검출/전체
- Redundant Logic: 제거해도 기능 동일 → Undetectable Fault 발생 가능
- Scan: FF 직렬 체인 → 순차 논리를 조합 논리처럼 테스트
- RAM BIST: March Algorithm (0 쓰기→읽기→1 쓰기→읽기 순환)
- LBIST: LFSR(패턴 생성) + Scan + MISR(서명 압축) → 자가진단

**Characterization (특성화) — 제조 후 샘플만**
- 동작 범위: 전원 전압 범위, 클럭 주파수 범위
- Critical Parameters: V-I 곡선, 전력, 지연, 동작 코너
- 가속 수명 시험: NBTI(PMOS 역바이어스 열화), HCI(고전계 전자 포획), 온도

---

## ⑤ 시험 대비 핵심 체크리스트

### 자주 나오는 계산 문제
- [ ] 노이즈 마진 계산: V_NML = V_IL - V_OL
- [ ] Setup Slack 계산: t_cy - (t_dCQ + t_dMax + t_s)
- [ ] Hold 조건 확인: t_h < t_cCQ + t_cMin
- [ ] Clock Skew 포함 최소 클럭 주기
- [ ] MTTF 계산: 1 / (f_a × P_E × P_S)
- [ ] 동적 전력 감소율: V 절반 → 전력 1/4

### 자주 나오는 개념 문제
- [ ] Latch vs FF 차이 (Level-sensitive vs Edge-triggered)
- [ ] Setup vs Hold 위반 해결 방법 차이
- [ ] Metastability 제거 불가 이유
- [ ] Gray Code가 동기화에 필요한 이유
- [ ] Clock Gating ILD vs DTD 장단점
- [ ] Power Gating 시 SRFF가 필요한 이유

---

## ⑥ 미학습 챕터 (추후 업데이트)
- Chap 4: CMOS Logic Circuits (Switch Model, Gates, Tristate)
- Chap 6.2: PoS, Hazards
- Chap 7: Verilog Combinational (case, casex, Testbench)
- Chap 8: Building Blocks (Decoder, MUX, Arbiter, Comparator, ROM/RAM)
- Chap 9: Combinational Examples
- Chap 11: Number Systems
- Chap 12: Adders (FA-based, PG-based)
- Chap 13: Multipliers
- Chap 14: Sequential Logic (FSM 설계, State Assignment)
- Chap 16: Datapath Sequential Logic (Counter, Shift Register)
- Chap 19: Sequential Examples
- Chap 20: Verification & Test
