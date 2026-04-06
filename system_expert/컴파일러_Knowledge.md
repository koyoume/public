# 컴파일러 Knowledge

> 삼성DS 시스템 전문가 과정 — 컴파일러 (문수묵 교수) | 마지막 업데이트: Ch1~3

---

## ① 수식 모음

| 수식 | 의미 | 사용처 |
|------|------|--------|
| 실행시간 = IC × CPI × CycleTime | IC: 명령어 수, CPI: 명령어당 사이클, CycleTime: 클럭 주기. 컴파일러는 IC와 CPI를 줄인다 | 최적화 효과 평가 |
| OUT[b] = GEN[b] ∪ (IN[b] − KILL[b]) | Reaching Definitions 전달함수. GEN: BB에서 생성된 정의, KILL: BB에서 kill되는 정의 | RD 분석 |
| IN[b] = ∪ OUT[p] (모든 predecessor p) | RD의 합류 연산. 어떤 경로든 도달하면 포함 (union) | RD 분석 |
| IN[b] = USE[b] ∪ (OUT[b] − DEF[b]) | Live Variables 전달함수. USE: locally exposed uses, DEF: BB에서 정의된 변수 | LV 분석 |
| OUT[b] = ∪ IN[s] (모든 successor s) | LV의 합류 연산. 어떤 후속 경로든 사용되면 live (union) | LV 분석 |

## ② 핵심 비교표

### 프로그램 실행 방식 비교

| 항목 | 컴파일러 | 인터프리터 (VM) | 하이브리드 |
|------|---------|---------------|-----------|
| 대표 언어 | C/C++ | Python, JS | Java |
| 실행 흐름 | 소스→기계어→HW 실행 | 소스→SW가 직접 해석 실행 | 소스→바이트코드→VM(인터프리터/JIT) |
| 성능 | 가장 빠름 | 느림 | 중간 (JIT으로 개선) |
| 이식성 | 낮음 (타겟 종속) | 높음 | 높음 (VM만 있으면 됨) |
| compile/runtime | 분리 | runtime만 | 2단계 (compile+runtime) |

### Reaching Definitions vs Live Variables

| 항목 | Reaching Definitions | Live Variables |
|------|---------------------|----------------|
| 도메인 | 정의(definition)들의 집합 | 변수(variable)들의 집합 |
| 비트벡터 크기 | 함수 내 정의 개수 | 함수 내 변수 개수 |
| 방향 | Forward: OUT = f(IN) | Backward: IN = f(OUT) |
| 전달함수 | GEN ∪ (x − KILL) | USE ∪ (x − DEF) |
| GEN/USE | GEN: BB 내 마지막 정의 | USE: locally exposed uses |
| KILL/DEF | KILL: 같은 변수의 다른 정의들 | DEF: BB에서 정의된 변수 |
| 합류 연산 | IN[b] = ∪ OUT[pred] | OUT[b] = ∪ IN[succ] |
| 합류 노드 | 여러 predecessor를 가진 노드 | 여러 successor를 가진 노드 |
| 초기화 | OUT[b] = {} | IN[b] = {} |
| 경계 조건 | OUT[entry] = {} | IN[exit] = {} |
| 변화 시 전파 | successor에 추가 | predecessor에 추가 |
| 용도 | live range 구축, 상수 전파 | 레지스터 할당, dead code 제거 |

### 지역 최적화 기법 비교

| 기법 | 분석 | 변환 | 예시 |
|------|------|------|------|
| Load-to-Copy | store 직후 같은 위치 load | load → copy로 교체 | `stw x, @z; y=ldw @z` → `stw x, @z; y=x` |
| Local CSE | BB 내 동일 식 중복 계산 | 두 번째 이후 삭제/재사용 | `x=y+z; ... w=y+z` → `x=y+z; ... w=x` |
| Constant Folding | 컴파일 타임 계산 가능 | 상수 값으로 교체 | `if(4>3)` → `if(true)` |
| Dead Code Elim | 결과가 사용되지 않음 | 명령어 삭제 | `x=y+1; x=10` → `x=10` |
| Copy Propagation | copy의 소스로 대체 가능 | 사용처를 원본으로 교체 | `x=y; z=x+1` → `z=y+1` |

### 루프 최적화 기법 비교

| 기법 | 설명 | 효과 | 적용 조건 |
|------|------|------|-----------|
| LICM | 루프 안에서 매번 같은 결과인 코드를 루프 밖으로 | 반복 횟수만큼 연산 절감 | 루프 불변식(loop invariant) |
| Strength Reduction | 비싼 연산(곱셈)을 싼 연산(덧셈)으로 교체 | 유도변수 × 상수 → 이전값 + 상수 | 유도변수(induction variable) 존재 |
| IV Elimination | 강도 감소 후 원래 유도변수 불필요하면 제거 | 레지스터 절약, 코드 축소 | 새 유도변수로 조건 대체 가능 |

### Copy Elimination 비교

| 기법 | 원리 | 예시 | 부작용 |
|------|------|------|--------|
| Copy Propagation | copy 사용처를 원본으로 교체 → copy dead | `y=x; z=y+1` → `z=x+1` | 없음 |
| Copy Coalescing | 소스/타겟 LR 간섭 없으면 합쳐 같은 레지스터 | `COPY r1,r2` → 삭제 | 합친 노드 간선 증가 → 컬러링 어려움 |

## ③ 용어 정의

| 용어 | 정의 |
|------|------|
| AST | 파스 트리에서 불필요한 노드를 제거한 추상 구문 트리. IR의 한 형태 |
| Available Expression | 지점 p에 도달하는 모든 경로에서 계산되었고 피연산자 미재정의인 표현식 |
| Basic Block (BB) | 제어 흐름이 처음에 들어와 끝에서 나가며 중간에 분기 없는 연속 명령어 시퀀스 |
| CFG | 기본 블록을 노드, 제어 흐름을 간선으로 하는 방향 그래프 |
| Copy Coalescing | COPY 소스/타겟 LR이 간섭 안 하면 합쳐 같은 레지스터 할당, COPY 삭제 |
| CPI | 명령어 하나당 평균 소요 클럭 사이클 수 |
| Dead Code | 결과가 어떤 후속 명령어에서도 사용되지 않는 명령어 |
| Definition | 변수에 값을 대입하는 명령어. 쓰기(write) |
| DEF[b] | BB b에서 정의된 변수들의 집합 |
| Extended Basic Block | 들어오는 분기 없이 나가는 분기만 있는 연속 BB 체인 |
| Fixed Point | 반복 계산에서 더 이상 값이 변하지 않는 수렴 상태 |
| GEN[b] | BB b에서 생성된 정의들의 집합 (= locally generated definitions) |
| Induction Variable | 루프 반복마다 일정하게 증가/감소하는 변수 |
| Interference Graph | 노드: LR(web), 간선: 동시 live 관계. 그래프 컬러링으로 RA |
| IR | 소스와 타겟 사이의 중간 표현 |
| KILL[b] | BB b 내의 정의와 같은 변수를 정의하는 함수 내 다른 정의들의 집합 (정적 속성) |
| Live Range (Web) | 정의와 그 정의에 도달하는 모든 사용의 집합. RA의 단위 |
| Live Variable | 지점 p에서 시작하는 어떤 경로에서 값이 재정의 전에 사용되는 변수 |
| LLVM | Low Level Virtual Machine. 모듈화된 오픈소스 컴파일러 인프라 |
| Locally Exposed Use | BB 내 사용인데 그 전에 같은 변수 정의가 BB 내에 없는 것 |
| Locally Generated Def | BB 내 어떤 변수의 마지막 정의 |
| Memory Live Range | 같은 메모리 위치에 접근하는 store/load 집합 |
| Meet Operator | 여러 경로의 정보를 합치는 연산. RD/LV 모두 union |
| φ-function | SSA에서 합류점에 삽입. 경로에 따라 값 선택하는 표기법 |
| Pseudo Register | 물리 RA 전 가상 레지스터. 무한 개 가정 |
| Reaching Definition | 정의 d가 p에 도달 = d→p 경로 존재 + kill 안 됨 |
| Register Promotion | load/store→copy. singleton 변수 조건 |
| Spilling | RA 시 레지스터 부족 → 일부 web을 스택으로 |
| SSA | 각 변수가 프로그램 전체에서 단 한 번만 정의되는 형태 |
| Strength Reduction | 곱셈→덧셈 교체. 유도변수에 적용 |
| Transfer Function | BB 통과 시 데이터 흐름 정보 변화를 기술하는 함수 |
| USE[b] | BB b의 locally exposed uses 집합 |
| Worklist Algorithm | 변화 노드만 재계산하는 반복 알고리즘 |

## ④ 주제별 상세

---

### Ch1. 컴파일러 구조와 최적화 개요

#### 컴파일러 3단계 구조

```
              FRONT-END (Analysis)
C++ src ──┐
Fortran ──┤→ Scanner(Lexer) ↔ Symbol Tables ↔ Parser → Code Generator
C src   ──┘                                              ↓
                         MIDDLE-END                Intermediate Code
                                                        ↓
                                                   Optimization
                                                        ↓
              BACK-END (Synthesis)              Code Generator
                                                        ↓
                                               Low-Level IR → Optimizer
                                                        ↓
                                              Relocatable Object Code
              RUN-TIME                                  ↓
                                    Linker (+ libc.a) → a.out → Loader → HW
```

#### LLVM 구조

```
C       → Clang FE  ─┐                         ┌→ LLVM X86 BE  → x86
Fortran → llvm-gcc FE ┼→ LLVM Optimizer(LLVM IR)┼→ LLVM PPC BE  → PowerPC
Haskell → GHC FE     ─┘                         └→ LLVM ARM BE  → ARM
```

#### 최적화 컴파일러 페이즈 파이프라인

```
Graph Repr. of IR
  ↓ (1)  Basic Block Optimization
  ↓ (2)  Dataflow Analysis + Interval Analysis
  ↓ (3)  Global CSE
  ↓ (4)  Promotion of Memory Operations
  ↓ (5)  LICM
  ↓ (6)  Induction Variable Analysis
  ↓ (7)  Register Reassociation
  ↓ (8)  Register Web (Live Range) Builder
  ↓ (9)  Instruction Scheduling       ← pre-RA
  ↓ (10) Register Allocation           ←
  ↓ (11) Peephole Optimization
  ↓ (12) Instruction Scheduling       ← post-RA
Graph Repr. of Optimized Code
```

#### 메모리 계층 지연시간

```
L1 cache         0.5 ns ─┐
Branch mispredict  5 ns   │ CPU 내부
L2 cache          10 ns ─┘
Main memory      100 ns    ← L1 대비 200배
Disk seek  10,000,000 ns   ← L1 대비 2천만배
```

#### 복합 명령어 예: `for(i=0;i<N;i++) A[i]=0;` 최적화 후

```
ADDIB,< 1,%r23,$003     ; i++, i<N이면 루프 (증가+비교+분기)
STWM   %r0,100(%r31)    ; 0→A[i], ptr+=100   (저장+포인터증가)
```
→ 루프 본체 **2개 명령어**. 컴파일러 최적화를 전제로 설계된 ISA.

#### Ch1 응용문제 A: 컴파일러 구조 역할 식별

**[문제]** 다음 각 작업이 컴파일러의 어떤 단계(Front-end/Middle-end/Back-end/Runtime)에서 수행되는지 답하라.

| # | 작업 | 답 |
|---|------|-----|
| 1 | 입력 문자열을 토큰으로 분리 | Front-end (Lexer) |
| 2 | 변수 사용 전 선언 여부 검사 | Front-end (Semantic Analysis) |
| 3 | 파스 트리에서 AST/바이트코드 생성 | Middle-end (IR Generation) |
| 4 | 공통 부분식 제거 (CSE) | Middle-end (Machine-indep. Opt) |
| 5 | 레지스터 할당 | Back-end |
| 6 | 명령어 스케줄링 | Back-end |
| 7 | 여러 .o 파일을 합쳐 실행 파일 생성 | Runtime (Linker) |
| 8 | LLVM IR → ARM 기계어 변환 | Back-end (Code Generator) |

#### Ch1 응용문제 B: 실행 시간 개선 분석

**[문제]** 프로그램의 IC=10^9, CPI=1.5, Clock=2GHz일 때:
(a) 실행 시간을 구하라.
(b) 컴파일러 최적화로 IC를 30% 줄이고 CPI를 1.2로 개선했다면 새 실행 시간과 속도 향상(speedup)을 구하라.

**[풀이]**:
```
(a) 실행시간 = IC × CPI × CycleTime = 10^9 × 1.5 × (1/2×10^9)
            = 10^9 × 1.5 × 0.5ns = 0.75초

(b) 새 IC = 10^9 × 0.7 = 7×10^8
    새 실행시간 = 7×10^8 × 1.2 × 0.5ns = 0.42초
    Speedup = 0.75 / 0.42 = 1.79배
```

#### Ch1 응용문제 C: 스택머신코드 → RISC 코드 변환

**[문제]** `z = x + y` (z: 전역 GP+8, x: 전역 GP+0, y: 지역 SP-4)의 스택머신코드를 RISC 의사코드로 변환하라. 현재 스택 깊이=0.

**[풀이]**:
```
스택머신코드               RISC 변환 (스택깊이 추적)
push_const GP+8     →    loadi GP+8, s0        ; z의 주소 (depth: 0→1)
push_const GP+0     →    loadi GP+0, s1        ; x의 주소 (depth: 1→2)
fetch               →    load  s1(0), s1       ; x의 값    (depth: 2→2)
push_reg SP              copy  SP, s2           ; (depth: 2→3)
push_const 4        →    loadi 4, s3            ; (depth: 3→4)
sub                 →    sub   s2, s3, s2       ; SP-4      (depth: 4→3)
fetch               →    load  s2(0), s2       ; y의 값    (depth: 3→3)
add                 →    add   s1, s2, s1       ; x + y     (depth: 3→2)
assign              →    store s0(0), s1        ; z = x+y   (depth: 2→0)
```

#### Ch1 응용문제 D: LLVM 구조의 장점

**[문제]** LLVM에 새로운 프로그래밍 언어 Rust와 새로운 아키텍처 RISC-V를 추가하려 한다. 각각 어떤 부분만 구현하면 되는가? 기존에 지원하는 C/ARM과의 조합도 자동으로 지원되는가?

**[풀이]**:
```
Rust 추가: Rust Frontend만 구현 (소스→LLVM IR 변환)
  → 기존 LLVM Optimizer + 모든 Backend(X86,ARM,PPC...) 자동 활용
  → Rust→X86, Rust→ARM, Rust→PPC 모두 자동 지원

RISC-V 추가: RISC-V Backend만 구현 (LLVM IR→RISC-V 기계어)
  → 기존 모든 Frontend(Clang,GHC...) + Optimizer 자동 활용
  → C→RISC-V, Fortran→RISC-V, Haskell→RISC-V 모두 자동 지원

M개 언어 + N개 아키텍처 = M+N개 모듈만 구현 (M×N이 아님!)
```

---

### Ch2. 단계별 최적화 실전 예제

#### 예제와 비최적화 코드

```c
int a[25][25]; // 전역, GP 기반. 행크기=25*4=100byte
main() { int i; for(i=0;i<25;i++) a[i][0]=0; }
```

```
     STW   0,-40(30)             ; i=0 (스택)
     LDW   -40(30),206           ; r206=i
     LDI   25,212                ; r212=25
     IFNOT 206<212 GOTO $02
$03: LDW   -40(30),206           ; 중복#1
     ADDILG LR'a,27,213          ; &a 상위21bit
     LDO   RR'a(213),208         ; &a 하위11bit
     MULTI 100,206,214           ; i*100 (곱셈!)
     ADD   208,214,215           ; &a[i][0]
     STWS  0,0(215)              ; a[i][0]=0
     LDW   -40(30),206           ; 중복#2
     LDO   1(206),216            ; i+1
     STW   216,-40(30)           ; i=i+1
     LDW   -40(30),206           ; 중복#3
     LDI   25,212                ; 중복 상수
     IF    206<212 GOTO $03
$02:
```
루프 본체 13개 명령어.

#### CFG

```
  ┌── BB0 ──┐  STW, LDW, LDI, IFNOT
  └────┬─────┘
       ↓       ↗ loop back
  ┌── BB1 ──┐  LDW, ADDILG, LDO, MULTI, ADD, STWS,
  │          │  LDW, LDO, STW, LDW, LDI, IF
  └────┬─────┘
       ↓
  ┌── BB2 ──┐  Exit
  └──────────┘
```

#### 7단계 최적화 코드 변화 추적

```
[원본]     루프본체 13개: LDW×4, LDI×2, MULTI, ADDILG+LDO 매반복
    ↓ BB Opt (load-copy, CSE, const folding)
[단계1]    중복 LDW 일부 제거, IFNOT 제거
    ↓ Global CSE
[단계2]    BB경계 넘어 LDW, LDI 추가 삭제
    ↓ Register Promotion (singleton i → 레지스터)
[단계3]    모든 STW/LDW 사라짐. COPY로 대체.
    ↓ Loop Opt (LICM + Strength Reduction + IV Elim)
[단계4]    ADDILG/LDO 루프밖. 곱셈→덧셈. 원래 i 불필요.
    ↓ Live Range + Dead Code
[단계5]    COPY 0,206과 LDI 25,212 삭제 (dead). 웹번호 부여.
    ↓ Instruction Scheduling (2-ALU)
[단계6]    독립 명령어 재배치 (LDO↔ADD 등)
    ↓ Register Allocation + Copy Elimination
[단계7]    COPY 삭제 (propagation+coalescing). 최종 4개 명령어:

$03: ADD   65,69,68        ; &a + offset
     STWS  0,0(68)         ; a[i][0] = 0
     LDO   100(69),69      ; offset += 100
     IF    69<71 GOTO $03  ; offset < 2500?
```

#### Strength Reduction 상세

```
원래: i=0,1,...,24 → offset = i×100 = 0,100,...,2400 (곱셈 매번)
변환: offset=0 → offset=offset+100 (덧셈 매번)
      조건: i<25 → offset<2500 (=25×100)
      → 원래 i 제거 (IV Elimination)
```

#### Register Promotion 조건

- Memory Live Range 구축 (같은 메모리 위치 store/load 집합)
- 조건: **singleton 변수** (배열, 포인터, 구조체 불가)
- 변환: store → copy, load → 삭제
- 주소 유도(address derivation)로 같은 위치 판별: `STW 0,-40(30)` → addr = SP-40

#### SSA Form

```
일반형:              SSA형:                합류점:
a = x+y             a0 = x+y             b1 = M[x0]
b = a-1             b0 = a0-1            a1 = 0
a = y+b             a1 = y+b0            if b1<4: a2=b1
b = x*4             b1 = x*4             a3 = φ(a2,a1)
a = a+b             a2 = a1+b1           c1 = a3+b1
```

φ-function = 표기법(실제 실행 안 됨). 경로에 따라 값 선택.
이점: 변수 이름만으로 어느 정의인지 즉시 식별 → 분석/최적화 극적 단순화.

#### Ch2 응용문제 A: 지역 최적화 적용

**[문제]** 아래 BB에 가능한 모든 지역 최적화를 적용하고 결과 코드를 보여라.

```
a = load @x          ; (1)
b = a + 1            ; (2)
store b, @y           ; (3)
c = load @y           ; (4)
d = a + 1            ; (5)
e = 3 * 4            ; (6)
store e, @z           ; (7)
f = load @z           ; (8)
```

**[풀이]**:
```
(1) a = load @x           ; 유지
(2) b = a + 1             ; 유지
(3) store b, @y            ; 유지
(4) c = b                  ; Load-to-Copy: (3)에서 b를 @y에 저장 직후 load → copy
(5) d = b                  ; Local CSE: a+1은 (2)에서 이미 계산, 결과=b → d=b
                             (또는 copy propagation: d=a+1과 b=a+1이 동일)
(6) e = 12                 ; Constant Folding: 3*4=12를 컴파일 타임에 계산
(7) store 12, @z           ; Constant Propagation: e=12이므로 12 직접 사용
(8) f = 12                 ; Load-to-Copy + Constant Propagation: @z에 12 저장 직후

만약 c, d, f가 이후 사용되지 않으면 → Dead Code Elimination으로 삭제 가능
```

#### Ch2 응용문제 B: 최적화 단계 역추적

**[문제]** 아래 변환 전/후 코드를 보고, 어떤 최적화 단계들이 적용되었는지 순서대로 나열하라.

```
변환 전 (루프 본체):          변환 후 (루프 본체):
  LDW   SP-8, r10   ; i       ADD  r20, r11, r12
  MULTI 16, r10, r11 ; i*16    STWS r0, 0(r12)
  ADD   r20, r11, r12 ; &A+i*16  LDO 16(r11), r11
  STWS  r0, 0(r12)   ; A[i]=0   IF r11 < r21 GOTO loop
  LDW   SP-8, r10   ; i (중복)
  LDO   1(r10), r13  ; i+1
  STW   r13, SP-8    ; i=i+1
  IF    r10 < r14 GOTO loop
```

**[풀이]**:
```
① Local CSE: 중복 LDW SP-8,r10 제거
② Register Promotion: i를 스택(SP-8)에서 레지스터로 승격 → STW/LDW 제거
③ Strength Reduction: MULTI 16,i → LDO 16(r11),r11 (곱셈→덧셈)
④ Induction Variable Elimination: 원래 i 제거, r11 기반 조건으로 교체 (r11<r21)
⑤ Dead Code Elimination: 원래 i 관련 코드 삭제
```

#### Ch2 응용문제 C: Register Promotion 적용 가능성 판단

**[문제]** 아래 각 경우에 Register Promotion이 가능한지, 불가능하면 이유를 답하라.

| # | 코드 | 가능? | 이유 |
|---|------|-------|------|
| 1 | `STW r5, SP-16; ... LDW SP-16, r8` | 가능 | singleton 지역변수 |
| 2 | `STW r5, GP+100; ... LDW GP+100, r8` | 가능 | singleton 전역변수 |
| 3 | `ADD r1,r2,r3; STW r5,0(r3); ... LDW 0(r3),r8` | 불가 | 포인터 기반 접근 — r3이 가리키는 곳이 가변 |
| 4 | `STW r5, GP+arr+r2*4; ... LDW GP+arr+r2*4` | 불가 | 배열 접근 — 인덱스에 따라 다른 위치 |
| 5 | `for 루프 내 STW/LDW SP-20` (구조체 필드) | 불가 | 구조체의 일부 — singleton 아님 |

핵심: **singleton 변수** (단순 스칼라, 고정 주소)만 승격 가능. 배열, 포인터, 구조체 불가.

#### Ch2 응용문제 D: Strength Reduction + IV Elimination 적용

**[문제]** 아래 루프에 강도 감소와 유도 변수 제거를 적용하라.
```c
for (j = 0; j < 50; j++)
    C[j*12] = D[j*6 + 3];
```

**[풀이]**:

```
유도변수: j (0→49)
파생식: j*12 (0,12,24,...,588), j*6+3 (3,9,15,...,297)

Step 1 — Strength Reduction:
  t1 = 0;   // j*12 대체
  t2 = 3;   // j*6+3 대체
  for (j=0; j<50; j++) {
      C[t1] = D[t2];
      t1 += 12;        // 곱셈→덧셈
      t2 += 6;         // 곱셈→덧셈
  }

Step 2 — IV Elimination (j를 t1 기반으로 조건 교체):
  t1 = 0; t2 = 3;
  while (t1 < 600) {   // j<50 → t1 < 50*12 = 600
      C[t1] = D[t2];
      t1 += 12;
      t2 += 6;
  }
  → j 완전 제거. 곱셈 2개→덧셈 2개.
```

#### Ch2 응용문제 E: SSA 변환 + φ-function 삽입

**[문제]** 아래 코드를 SSA로 변환하라.

```
    a = 1
    b = 2
    if (a < b)
        a = a + b
        b = a - 1
    else
        b = a * 3
    c = a + b
```

**[풀이]**:

```
    a0 = 1
    b0 = 2
    if (a0 < b0)
      then:
        a1 = a0 + b0      ; a1 = 1+2 = 3
        b1 = a1 - 1       ; b1 = 3-1 = 2
      else:
        b2 = a0 * 3       ; b2 = 1*3 = 3
    합류점:
        a2 = φ(a1, a0)    ; then→a1=3, else→a0=1
        b3 = φ(b1, b2)    ; then→b1=2, else→b2=3
    c0 = a2 + b3

φ-function 삽입 기준:
  - a: then에서 재정의(a1), else에서 미변경(a0) → φ 필요
  - b: then에서 재정의(b1), else에서도 재정의(b2) → φ 필요
  - c: 합류 후에만 정의 → φ 불필요
```

#### Ch2 응용문제 F: Copy Elimination 두 방법 비교

**[문제]** 아래 코드에서 (a) copy propagation, (b) copy coalescing을 각각 적용한 결과를 보여라.

```
COPY r1, r2          ; r2 = r1
ADD  r2, r3, r4      ; r4 = r2 + r3
MUL  r2, r5, r6      ; r6 = r2 * r5
```

**[풀이]**:

**(a) Copy Propagation**: r2 사용을 r1으로 교체
```
COPY r1, r2          ; (이제 dead → 삭제 가능)
ADD  r1, r3, r4      ; r2 → r1
MUL  r1, r5, r6      ; r2 → r1
```
r2가 더 이상 사용 안 됨 → COPY 삭제 (Dead Code Elim) → 결과:
```
ADD  r1, r3, r4
MUL  r1, r5, r6
```

**(b) Copy Coalescing**: r1과 r2의 live range가 간섭하지 않으면 합쳐서 같은 물리 레지스터 할당
- 조건: r1의 LR과 r2의 LR이 동시에 live인 구간이 없어야 함
- r1이 COPY 이후에도 live하다면 (다른 곳에서 r1 사용) → **간섭 → coalescing 불가**
- r1이 COPY 이후 dead라면 → 간섭 없음 → r1=r2로 통합 → COPY 삭제

---

### Ch3. Data Flow Analysis

#### 분석 전략 2단계

```
1단계 Global: CFG의 BB 단위 → 각 BB 경계 정보
2단계 Local:  BB 내부 → 각 명령어 경계 정보 (전역 결과를 출발점)
```

#### BB의 효과 분석 예

```
BB:
  r4 = r1+r2   ; USE: r1✓,r2✓(exposed). DEF: r4
  r2 = r4+1    ; USE: r4(not exposed). DEF: r2
  r5 = r3+r1   ; USE: r3✓(exposed). DEF: r5
  r1 = r5      ; DEF: r1
  r4 = r2*r4   ; DEF: r4
  r2 = r5      ; DEF: r2

Exposed Uses = {r1,r2,r3}
Gen Defs = r1(최종), r4(최종), r2(최종)
```

#### RD vs LV 방향

```
RD (Forward):  OUT[pred] → union → IN[b] → [GEN∪(IN−KILL)] → OUT[b]
LV (Backward): IN[b] ← [USE∪(OUT−DEF)] ← OUT[b] ← union ← IN[succ]
```

#### KILL의 의미 (주의!)

KILL = **정적 속성**. "만약 이 정의가 도달하면 죽인다"는 잠재적 능력.
실제 효과: `IN − KILL`에서 IN에 포함된 것만 영향.
B1이 함수 시작 → IN={} → KILL 효과 없음 ({} − anything = {}).

#### Worklist Algorithm 비교

```
RD (Forward):                        LV (Backward):
초기: OUT[entry]={}, OUT[i]={}       초기: IN[exit]={}, IN[i]={}
while ChangeNodes≠{}:                while ChangeNodes≠{}:
  remove i                            remove i
  IN[i] = ∪OUT[pred]                  OUT[i] = ∪IN[succ]
  oldout = OUT[i]                      oldin = IN[i]
  OUT[i] = GEN∪(IN−KILL)              IN[i] = USE∪(OUT−DEF)
  if changed:                          if changed:
    add successors                       add predecessors
```

---

### 응용문제 1: Reaching Definitions 전체 풀이

**[문제]** 아래 CFG의 GEN/KILL 계산 후 RD의 IN/OUT을 구하라.

```
entry → B1 → B2 ←─B3    B2 → B3, B2 → B4 → exit
B1: d1:i=m-1, d2:j=n, d3:a=u1
B2: d4:i=i+1, d5:j=j-1
B3: d6:a=u2  (→B2 루프백)
B4: d7:i=u3  (→exit)
```

**[Step 1] 변수별 정의 위치**:
```
i: d1(B1), d4(B2), d7(B4)
j: d2(B1), d5(B2)
a: d3(B1), d6(B3)
```

**GEN/KILL**:

| BB | GEN | KILL 계산 | KILL |
|----|-----|-----------|------|
| B1 | {1,2,3} | i→{4,7}, j→{5}, a→{6} | {4,5,6,7} |
| B2 | {4,5} | i→{1,7}, j→{2} | {1,2,7} |
| B3 | {6} | a→{3} | {3} |
| B4 | {7} | i→{1,4} | {1,4} |

**[Step 2] 반복 계산** (초기: 모든 OUT={}):

| 회차 | BB | IN | OUT | 변화? |
|------|----|----|-----|-------|
| 1 | B1 | {} | {1,2,3} | Y |
| 1 | B2 | {1,2,3}∪{}={1,2,3} | {4,5}∪{3}={3,4,5} | Y |
| 1 | B3 | {3,4,5} | {6}∪{4,5}={4,5,6} | Y |
| 1 | B4 | {3,4,5} | {7}∪{3,5}={3,5,7} | Y |
| 2 | B2 | {1,2,3}∪{4,5,6}=**{1,2,3,4,5,6}** | {4,5}∪{3,4,5,6}=**{3,4,5,6}** | Y |
| 2 | B3 | {3,4,5,6} | {4,5,6} | N |
| 2 | B4 | {3,4,5,6} | {3,5,6,7} | Y |
| 3 | B2 | {1,2,3}∪{4,5,6}={1,2,3,4,5,6} | {3,4,5,6} | **N→수렴** |

**[최종 답]**:

| BB | IN | OUT |
|----|----|-----|
| B1 | {} | {1,2,3} |
| B2 | {1,2,3,4,5,6} | {3,4,5,6} |
| B3 | {3,4,5,6} | {4,5,6} |
| B4 | {3,4,5,6} | {3,5,6,7} |

---

### 응용문제 2: Live Variables 전체 풀이

**[문제]** 같은 CFG에서 USE/DEF 계산 후 LV의 IN/OUT을 구하라.

**[Step 1] USE/DEF**:

| BB | 코드 | USE (exposed uses) | DEF |
|----|------|--------------------|-----|
| B1 | i=m-1, j=n, a=u1 | {m,n,u1} | {i,j,a} |
| B2 | i=i+1, j=j-1 | {i,j} (정의 전에 사용) | {i,j} |
| B3 | a=u2 | {u2} | {a} |
| B4 | i=u3 | {u3} | {i} |

**[Step 2] 반복 계산 (Backward)** (초기: 모든 IN={}):

| 회차 | BB | OUT | IN | 변화? |
|------|----|----|-----|-------|
| 1 | B4 | IN[exit]={} | {u3}∪({}−{i})={u3} | Y |
| 1 | B3 | IN[B2]={} | {u2}∪({}−{a})={u2} | Y |
| 1 | B2 | IN[B3]∪IN[B4]={u2}∪{u3}={u2,u3} | {i,j}∪({u2,u3}−{i,j})={i,j,u2,u3} | Y |
| 1 | B1 | IN[B2]={i,j,u2,u3} | {m,n,u1}∪({i,j,u2,u3}−{i,j,a})={m,n,u1,u2,u3} | Y |
| 2 | B3 | IN[B2]={i,j,u2,u3} | {u2}∪({i,j,u2,u3}−{a})=**{i,j,u2,u3}** | Y |
| 2 | B2 | {i,j,u2,u3}∪{u3}={i,j,u2,u3} | {i,j}∪({i,j,u2,u3}−{i,j})={i,j,u2,u3} | **N→수렴** |

**[최종 답]**:

| BB | OUT | IN |
|----|-----|-----|
| B1 | {i,j,u2,u3} | {m,n,u1,u2,u3} |
| B2 | {i,j,u2,u3} | {i,j,u2,u3} |
| B3 | {i,j,u2,u3} | {i,j,u2,u3} |
| B4 | {} | {u3} |

해석: B2에서 i,j는 B2 내 사용. u2,u3는 B3,B4에서 사용 → B2 통과 시 live 유지.

---

### 응용문제 3: 최적화 기법 식별

**[문제]** 변환을 보고 적용된 최적화를 답하라.

| # | 변환 전 | 변환 후 | 답 |
|---|---------|---------|-----|
| a | `STW x,@z; y=LDW @z` | `STW x,@z; y=x` | Load-to-Copy |
| b | `x=y+z; ... w=y+z` | `x=y+z; ... w=x` | Local CSE |
| c | `for(...){p=&A; ...}` | `p=&A; for(...){...}` | LICM |
| d | `for(i=0;i<N;i++) f(i*7)` | `t=0; for(...){f(t);t+=7}` | Strength Reduction |
| e | `x=y; z=x+1` | `z=y+1` | Copy Propagation + DCE |
| f | `COPY r5,r3` (비간섭) | `r3=r5 할당 후 삭제` | Copy Coalescing |

---

### 응용문제 4: Strength Reduction 적용

**[문제]** 아래 루프에 강도 감소를 적용하라.
```c
for (i=0; i<100; i++)
    B[i*8] = A[i*4];
```

**[풀이]**:
```
유도변수: i (0→99)
파생식: i*4 (0,4,...,396), i*8 (0,8,...,792)

변환:
  t1=0; t2=0;
  for (t1<400) {       // i<100 → t1<100*4=400 (IV Elim)
      B[t2] = A[t1];
      t1 += 4;          // i*4 → 덧셈
      t2 += 8;          // i*8 → 덧셈
  }
```
곱셈 2개 → 덧셈 2개로 교체. 원래 i 제거.

---

### 응용문제 5: SSA 변환 + 상수 전파

**[문제]** 아래를 SSA로 변환하고 상수 전파를 적용하라.
```
    x = 5
    y = x + 1
    if (y > 3)
        x = y * 2
    z = x + y
```

**[풀이 — SSA 변환]**:
```
    x0 = 5
    y0 = x0 + 1
    if (y0 > 3)
        x1 = y0 * 2
    x2 = φ(x1, x0)     ← 합류점
    z0 = x2 + y0
```

**[상수 전파]**: x0=5, y0=5+1=6, 6>3=true → then만 실행 → x1=6*2=12, x2=φ(12,5)=12 (then만), z0=12+6=18.

SSA에서는 변수 이름(x0, x1, x2)만으로 어느 정의인지 즉시 확인 → 별도 reaching def 분석 불필요.

## ⑤ 시험 대비 체크리스트

### 계산 문제 유형
- [ ] GEN/KILL 테이블 계산 (변수별 정의 위치 정리 → 다른 정의 수집)
- [ ] Reaching Definitions 반복 계산 (IN/OUT 테이블, 수렴까지)
- [ ] USE/DEF 테이블 계산 (locally exposed use 식별 주의)
- [ ] Live Variables 반복 계산 (Backward 방향 주의)
- [ ] Strength Reduction: 곱셈→덧셈 + 새 유도변수 + 조건 교체 + IV 제거
- [ ] SSA 변환: 변수 리네이밍 + φ-function 삽입 위치
- [ ] 최적화 전후 코드 비교: 적용된 기법 식별
- [ ] Register Promotion: Memory LR 식별 → store→copy, load 삭제

### 개념 문제 유형
- [ ] Forward(RD) vs Backward(LV) 분석의 차이
- [ ] KILL의 정적 속성 의미 (IN에 있어야 실제 kill)
- [ ] 보수적 근사(conservative approximation)의 필요성
- [ ] 합류에서 union을 쓰는 이유 (안전성)
- [ ] FE/ME/BE의 역할 구분
- [ ] SSA의 장점과 φ-function 역할
- [ ] Register Promotion 조건 (singleton) 및 제약 (배열/포인터/구조체 불가)
- [ ] Copy Propagation vs Coalescing 차이와 트레이드오프
- [ ] Instruction Scheduling이 RA 전후 2번인 이유
