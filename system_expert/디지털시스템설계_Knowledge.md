# 디지털 시스템 설계 (Digital Systems Design) — 오픈북 시험 대비 정리

> 삼성DS System Expert Course | 서울대 심재웅 교수 | 최종 업데이트: 2026-04-14

---

## ① 수식 모음

| 분류 | 수식 | 변수 설명 |
|------|------|-----------|
| **[Ch0] 전력** | P ∝ C·V²·F | C: 커패시턴스, V: 전압, F: 주파수 (Dennard Scaling) |
| **[Ch1] SOP** | F = Σ(minterms where Y=1) | minterm의 OR, 정규 곱의 합 |
| **[Ch1] POS** | F = Π(maxterms where Y=0) | maxterm의 AND, 정규 합의 곱 |
| **[Ch1] Combining** | P·A + P·A̅ = P | 변수 A 제거 (K-Map의 핵심 원리) |
| **[Ch1] Covering** | B·(B+C) = B | 흡수법칙 |
| **[Ch1] Consensus** | BC + B̅D + CD = BC + B̅D | 중복 항 제거 |
| **[Ch1] De Morgan** | (B₀·B₁...)̅ = B̅₀+B̅₁... | AND↔OR 반전 교환 |
| **[Ch1] De Morgan (dual)** | (B₀+B₁...)̅ = B̅₀·B̅₁... | |
| **[Ch1] Mux** | Y = D₀·S̅ + D₁·S | 2:1 Mux 수식 |
| **[Ch1] FSM next state (예)** | S'₁ = S₁ ⊕ S₀ | Traffic Light Controller |
| **[Ch1] FSM next state (예)** | S'₀ = S̅₁·S̅₀·T̅_A + S₁·S̅₀·T̅_B | |

---

## ② 핵심 비교표

| 비교 항목 | A | B |
|-----------|---|---|
| **Combinational vs Sequential** | 출력 = f(현재 입력만), 메모리 없음 | 출력 = f(현재+과거 입력), 메모리 있음 |
| **Latch vs Flip-Flop** | Level-sensitive (CLK=1일 때 transparent) | Edge-triggered (rising edge에서만 값 갱신) |
| **SR Latch vs D Latch** | S,R 두 입력 (S=R=1 금지상태 존재) | D,CLK 두 입력 (금지상태 없음, what/when 분리) |
| **Moore vs Mealy FSM** | 출력 = f(state만), 안정적, 한 클럭 늦음 | 출력 = f(state+input), 빠른 반응, glitch 주의 |
| **SOP vs POS** | minterm(Y=1)의 OR | maxterm(Y=0)의 AND |
| **Minterm vs Maxterm** | 모든 변수의 AND (min satisfiability) | 모든 변수의 OR (max satisfiability) |
| **wire vs reg [Ch2]** | continuous assign(assign)의 LHS, 값 저장 불가 | procedural block(always)의 LHS, 반드시 물리 레지스터는 아님 |
| **Structural vs Dataflow vs Behavioral [Ch2]** | 게이트/모듈 인스턴스화 | assign+연산자, 조합논리 | always블록+reg |
| **Continuous vs Procedural Assignment [Ch2]** | assign으로 wire 구동, 항상 활성 | always 블록 내에서 reg에 할당 |
| **Synthesizable vs Non-synthesizable [Ch2]** | module, always, assign, wire, reg | initial, #delay, $display, $monitor, $finish |
| **Moore's Law vs Dennard Scaling [Ch0]** | 트랜지스터 수 ~2배/18-24개월 (둔화 중) | 전력밀도 일정 (이미 종료) |

---

## ③ 용어 정의

| 용어 | 정의 |
|------|------|
| always block | sensitivity list의 이벤트 발생 시 실행되는 procedural block [Ch2] |
| assign | continuous assignment 키워드, wire에 값을 지속적으로 구동 [Ch2] |
| Bistable element | 두 안정 상태를 가진 메모리의 기본 빌딩 블록 [Ch1] |
| Combinational circuit | 출력이 현재 입력의 조합에만 의존하는 회로 [Ch1] |
| Concatenation | 비트를 이어붙이는 연산 {a, b}. 예: {c_out, sum} [Ch2] |
| Continuous assignment | assign 키워드로 net에 값을 지속 구동하는 할당 방식 [Ch2] |
| D Flip-Flop | master+slave D Latch 조합, rising edge에서만 값 갱신 [Ch1] |
| D Latch | D(data)와 CLK으로 구성, CLK=1 시 transparent [Ch1] |
| Decoder | N입력 2^N 출력, 입력 조합에 따라 하나의 출력만 assert [Ch1] |
| Dennard Scaling | 트랜지스터 축소 시 전력밀도 일정 법칙 (P∝CV²F, 2000년대 종료) [Ch0] |
| FSM | Finite State Machine, next state logic + register + output logic [Ch1] |
| Gray Code | 연속 값이 1비트만 차이나는 코드 (K-Map에서 사용) [Ch1] |
| HDL | Hardware Description Language, 하드웨어를 텍스트로 기술 [Ch2] |
| Implicant | 하나 이상 리터럴의 AND [Ch1] |
| K-Map | Karnaugh Map, 불리언 수식 그래픽 간소화 도구 [Ch1] |
| Literal | 변수 또는 그 보수 (A, A̅) [Ch1] |
| Logical completeness | AND, OR, NOT만으로 모든 회로 구현 가능한 성질 [Ch1] |
| Maxterm | 함수의 모든 변수를 포함하는 합 (OR) [Ch1] |
| Mealy machine | 출력이 현재 상태+입력에 의존하는 FSM [Ch1] |
| Minterm | 함수의 모든 변수를 포함하는 곱 (AND) [Ch1] |
| Module | Verilog의 기본 빌딩 블록, 입출력 포트를 가진 하드웨어 단위 [Ch2] |
| Moore machine | 출력이 현재 상태에만 의존하는 FSM [Ch1] |
| Moore's Law | 칩 트랜지스터 수 약 18-24개월마다 2배 증가 법칙 [Ch0] |
| Multiplexer (Mux) | 선택 신호로 여러 입력 중 하나를 출력으로 선택 [Ch1] |
| NAND | NOT-AND, NAND만으로 모든 논리 구현 가능 [Ch1] |
| Netlist | 합성 결과물, 게이트와 와이어의 연결 목록 [Ch2] |
| POS | Product of Sums, maxterm의 AND [Ch1] |
| Prime implicant | 다른 implicant와 더 합쳐질 수 없는 implicant [Ch1] |
| Procedural assignment | always/initial 블록 내에서 reg에 값 할당 [Ch2] |
| reg | Verilog variable 타입, procedural block에서 할당, 반드시 물리 레지스터는 아님 [Ch2] |
| Register | 공통 CLK을 공유하는 N개 flip-flop의 뱅크 [Ch1] |
| RTL | Register-Transfer Level = synthesizable behavioral + dataflow [Ch2] |
| Sensitivity list | always 블록이 반응하는 신호 목록 [Ch2] |
| Sequential circuit | 출력이 입력 시퀀스(현재+과거)에 의존, 메모리 있음 [Ch1] |
| SOP | Sum of Products, minterm의 OR [Ch1] |
| SR Latch | Set-Reset Latch, 교차 결합 NOR 게이트, S=R=1 금지 [Ch1] |
| Structural modeling | 게이트/모듈 인스턴스화로 회로를 기술하는 방식 [Ch2] |
| Synthesis | HDL 코드를 게이트/와이어(netlist)로 변환하는 과정 [Ch2] |
| Testbench | 설계 모듈을 검증하기 위한 시뮬레이션 코드 (합성 불가) [Ch2] |
| Timescale | `timescale 시간단위/정밀도, 시뮬레이션 시간 기준 설정 [Ch2] |
| TPU | Tensor Processing Unit, Google의 DNN 가속기 [Ch0] |
| wire | Verilog net 타입, 하드웨어 연결점, 값 저장 불가 [Ch2] |
| X (unknown) | 알 수 없는 논리 값, 시뮬레이터 초기화 전 상태 [Ch1,Ch2] |
| Z (high-impedance) | 구동되지 않는 floating 상태 [Ch1,Ch2] |

---

## ④ 주제별 상세

### [Ch0] Introduction & Trend in Computer Systems

**Dennard Scaling과 전력 문제:**
전력 P ∝ C·V²·F. 트랜지스터 축소 → C 감소, V 감소 가능 → F 증가해도 전력 유지. 하지만 2000년대 중반 이후 V를 더 낮출 수 없게 되어 Dennard Scaling 종료 → 주파수 경쟁 중단 → 멀티코어/가속기 시대로 전환.

**성능 향상 원천 (AMD Lisa Su 발표):**
공정기술 40%, 마이크로아키텍처 17%, 전력관리 15%, 다이크기 12%, TDP 8%, 컴파일러 8%.

**특수 가속기 스펙:**

```
  칩         │ 공정   │ 다이   │ 성능           │ 전력
─────────────┼────────┼────────┼────────────────┼──────
 TPU v1      │ 28nm   │ 331mm² │ 92 TOPs (INT8) │ 40W
 TPU v2      │ -      │ -      │ 45 TFLOPs      │ -
 TPU v3      │ -      │ -      │ 105 TFLOPs     │ -
 Tesla FSD   │ 14nm   │ 260mm² │ 73.72 TOPs     │ 36W
 AWS Inferentia│ -     │ -      │ 128 TOPS       │ -
 Intel Loihi │ 14nm   │ 60mm²  │ SNN 전용       │ -
```

---

### [Ch1] Review: Logic Design

**Logic Gates 진리표:**

```
 A B │ AND OR XOR NAND NOR XNOR
─────┼──────────────────────────
 0 0 │  0   0   0    1    1    1
 0 1 │  0   1   1    1    0    0
 1 0 │  0   1   1    1    0    0
 1 1 │  1   1   0    0    0    1
```

**Boolean Algebra — Axioms:**

```
 A1: B=0 if B≠1     A1': B=1 if B≠0       (Binary)
 A2: 0̅=1            A2': 1̅=0              (NOT)
 A3: 0·0=0          A3': 1+1=1            (AND/OR)
 A4: 1·1=1          A4': 0+0=0            (AND/OR)
 A5: 0·1=0          A5': 1+0=1            (AND/OR)
```

**Boolean Algebra — Theorems (One Variable):**

```
 T1: B·1=B          T1': B+0=B            (Identity)
 T2: B·0=0          T2': B+1=1            (Null)
 T3: B·B=B          T3': B+B=B            (Idempotency)
 T4: B̿=B                                  (Involution)
 T5: B·B̅=0          T5': B+B̅=1            (Complements)
```

**Boolean Algebra — Theorems (Several Variables):**

```
 T6:  B·C = C·B                  (Commutativity)
 T7:  (B·C)·D = B·(C·D)          (Associativity)
 T8:  B·C + B·D = B·(C+D)        (Distributivity)
 T9:  B·(B+C) = B                (Covering/Absorption)
 T10: B·C + B·C̅ = B              (Combining) ★★★
 T11: BC + B̅D + CD = BC + B̅D    (Consensus)
 T12: (B₀·B₁...)̅ = B̅₀+B̅₁...    (De Morgan's) ★★★
```

**K-Map 규칙:**
1. 1을 모두 덮는 최소 수의 직사각형
2. 각 직사각형은 1만 포함
3. 크기는 2의 거듭제곱 (1,2,4,8...)
4. 가능한 한 크게
5. 가장자리 wrap-around 가능
6. 하나의 1이 여러 원에 포함 가능

**K-Map 간소화 예제:**
```
F = A̅B̅C + A̅BC + AB̅C
  = A̅C(B̅+B) + AB̅C     (T10 적용)
  = A̅C + AB̅C
  = C(A̅ + AB̅)
  = C(A̅+A)(A̅+B̅)       (T8' 분배)
  = C(A̅+B̅)
```

**SR Latch:**

```
 R──→┤NOR├──o──→ Q          S  R │ Q      Q̅
     │ N1│    ╲              ─────┼──────────────
     └───┘     ╲             0  0 │ Qprev  Q̅prev
         ╲      │            0  1 │ 0      1
 S──→┤NOR├──o──→ Q̅          1  0 │ 1      0
     │ N2│                   1  1 │ 0      0 (금지!)
     └───┘
```

**D Flip-Flop (Master-Slave):**

```
            CLK           CLK
  D ──→┤D  Q├─N1─→┤D  Q├──→ Q
       │L1 Q̅├     │L2 Q̅├──→ Q̅
       └────┘      └────┘
       master       slave

  CLK=0: master transparent, slave opaque (D→N1)
  CLK=1: master opaque, slave transparent (N1→Q)
  → Rising edge에서만 D가 Q로 복사됨
```

**FSM 설계 절차:**
1. State Transition Diagram 작성
2. State Transition Table 작성
3. State Encoding (이진 코드 부여)
4. Boolean Equations 유도 (Next State + Output)
5. Schematic 작성

**FSM 예제 — Traffic Light Controller:**

```
  State│Encoding│ LA    │ LB
  ─────┼────────┼───────┼──────
   S0  │  00    │ green │ red
   S1  │  01    │ yellow│ red
   S2  │  10    │ red   │ green
   S3  │  11    │ red   │ yellow

  Next State:
    S'₁ = S₁ ⊕ S₀
    S'₀ = S̅₁·S̅₀·T̅_A + S₁·S̅₀·T̅_B

  Output:
    L_A1 = S₁,  L_A0 = S̅₁·S₀
    L_B1 = S̅₁,  L_B0 = S₁·S₀

  → Moore Machine (출력이 상태에만 의존)
```

---

### [Ch2] Introduction to Verilog

**Module 기본 구조:**

```verilog
module module_name (input  a,
                    input  b,
                    output y);
  // 회로 기술
endmodule
```
- ANSI-C 스타일 포트 선언 사용 (Verilog-2001)
- module 선언 끝에 세미콜론(;) 필수, endmodule 뒤에는 없음

**wire vs reg 사용 규칙:**

```
  wire: assign문의 LHS, module의 input/inout port
  reg:  always/initial 블록의 LHS, output port 가능 (output reg)

  주의: reg ≠ 물리적 레지스터! 합성 시 조합논리가 될 수도 있음
```

**세 가지 Assignment:**

```
 (1) Continuous: assign temp = a | b;     → wire에 사용, 조합논리
 (2) Procedural: always @(*) y = a & b;   → reg에 사용, always 블록 내
 (3) Procedural Continuous: assign/deassign → 특수 용도, 잘 안 씀
```

**세 가지 모델링 레벨 코드 비교 (Full Adder):**

```verilog
// (1) Structural — 게이트 인스턴스화
module full_adder_structural(input x, y, c_in,
                             output sum, c_out);
  wire s1, c1, c2;
  half_adder ha_1(x, y, s1, c1);
  half_adder ha_2(c_in, s1, sum, c2);
  or(c_out, c1, c2);
endmodule

// (2) Dataflow — assign + 연산자
module full_adder_dataflow(input x, y, c_in,
                           output sum, c_out);
  assign {c_out, sum} = x + y + c_in;
endmodule

// (3) Behavioral — always 블록
module full_adder_behavioral(input x, y, c_in,
                             output reg sum, c_out);
  always @(x, y, c_in)
    {c_out, sum} = x + y + c_in;
endmodule
```

**RTL = synthesizable behavioral + dataflow (업계 표준)**

**숫자 표현 형식:**

```
  형식: <size>'<base>value
  예: 16'b0101_1100_0000_1101
      8'hAA  →  10101010
      'hF    →  32비트 0...01111

  크기<값: MSB truncation (4'b11110010 → 0010)
  크기>값: MSB padding (0으로, 또는 x/z로)
  음수: -4'b1001 → 2의 보수
  _: 가독성만, ?: z와 동일
```

**Port Connection:**

```verilog
// Named association (추천!)
half_adder ha_2(.x(cin), .y(s1), .s(s), .c(c2));

// Positional association (비추천)
half_adder ha_1(x, y, s1, c1);
```

**연산자 우선순위 (높→낮):**

```
  ~  >  *,/,%  >  +,-  >  <<,>>  >  <<<,>>>
  >  <,<=,>,>=  >  ==,!=  >  &,~&  >  ^,~^
  >  |,~|  >  ?:
```

**Simulation 핵심:**

```verilog
`timescale 1ns / 100ps      // 시간단위 / 정밀도
$display("...", vars);       // 한 번 출력
$monitor("...", vars);       // 값 변화시마다 자동 출력
$finish;                     // 시뮬레이션 종료
always #5 clk = ~clk;       // 주기 10ns 클럭 생성
```

---

## ⑤ 시험 대비 체크리스트

### 계산 문제 유형
- [ ] 진리표 → SOP/POS 수식 유도
- [ ] K-Map으로 불리언 수식 간소화 (3변수, 4변수)
- [ ] FSM 설계: state diagram → encoding → next state/output equations
- [ ] Boolean Algebra 정리 적용하여 수식 간소화
- [ ] Verilog 숫자 표현 해석 (크기 불일치, 음수, x/z 패딩)

### 개념 문제 유형
- [ ] wire vs reg 차이, 언제 어떤 것을 사용하는가
- [ ] Combinational vs Sequential 회로 구분
- [ ] Latch vs Flip-Flop 차이 (level vs edge)
- [ ] Moore vs Mealy FSM 차이, 주어진 FSM이 어느 것인지 판별
- [ ] Structural vs Dataflow vs Behavioral modeling의 차이와 각각의 코드 패턴
- [ ] Continuous vs Procedural assignment 차이
- [ ] Synthesizable vs Non-synthesizable 구분
- [ ] De Morgan's theorem과 Logical completeness
- [ ] Dennard Scaling이 끝난 이유와 그 결과
