# 컴파일러 Knowledge

> 삼성DS 시스템 전문가 과정 — 컴파일러 (문수묵 교수) | 마지막 업데이트: Ch1~3

---

## ① 수식 모음

| 수식 | 변수 의미 | 적용 조건 | 사용처 |
|------|----------|-----------|--------|
| T = IC × CPI × CT | IC=실행 명령어 수, CPI=명령어당 사이클, CT=1/ClockFreq | CT는 HW 고정. 컴파일러는 IC,CPI만 줄일 수 있음 | 최적화 효과 평가 |
| OUT[b] = GEN[b] ∪ (IN[b] − KILL[b]) | GEN=BB b의 locally generated defs, KILL=같은 변수의 다른 정의들, IN=b 진입 시 도달 정의 | Forward 분석. KILL은 정적 속성(IN에 있는 것만 실제 kill됨) | RD |
| IN[b] = ∪ OUT[p], ∀ pred p | OUT[p]=선행자 p의 출구 도달 정의 | 합류점에서 union (어떤 경로든 도달하면 포함) | RD |
| IN[b] = USE[b] ∪ (OUT[b] − DEF[b]) | USE=locally exposed uses, DEF=BB b에서 정의된 변수, OUT=b 출구 시 live 변수 | Backward 분석. DEF는 BB 내 정의된 모든 변수 | LV |
| OUT[b] = ∪ IN[s], ∀ succ s | IN[s]=후계자 s의 진입 live 변수 | 합류점에서 union (어떤 후속 경로든 사용되면 live) | LV |
| Speedup = T_old / T_new | T_old=최적화 전, T_new=최적화 후 | Speedup>1이면 개선 | 최적화 비교 |

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
| 도메인 | 정의(definition) 집합 | 변수(variable) 집합 |
| 비트벡터 크기 | 함수 내 정의 개수 | 함수 내 변수 개수 |
| 방향 | Forward: OUT=f(IN) | Backward: IN=f(OUT) |
| 전달함수 | GEN∪(x−KILL) | USE∪(x−DEF) |
| GEN/USE | GEN: BB 내 마지막 정의 | USE: locally exposed uses |
| KILL/DEF | KILL: 같은 변수의 다른 정의들 (정적) | DEF: BB에서 정의된 변수 |
| 합류 연산 | IN[b]=∪OUT[pred] | OUT[b]=∪IN[succ] |
| 합류 노드 | 여러 pred 가진 노드 | 여러 succ 가진 노드 |
| 초기화 | OUT[b]={} | IN[b]={} |
| 경계 조건 | OUT[entry]={} | IN[exit]={} |
| 변화 시 전파 | successor 추가 | predecessor 추가 |
| 용도 | live range 구축, 상수 전파 | RA, dead code 제거 |

### 지역 최적화 기법 비교

| 기법 | 패턴 | 변환 | 효과 |
|------|------|------|------|
| Load-to-Copy | store 직후 같은 위치 load | load→copy | 메모리 접근 제거 |
| Local CSE | BB 내 동일 식 중복 | 두 번째 삭제/재사용 | 연산 제거 |
| Constant Folding | 컴파일 타임 계산 가능 | 상수로 교체 | 연산 제거 |
| Dead Code Elim | 결과 미사용 | 명령어 삭제 | 코드 축소 |
| Copy Propagation | copy 소스로 대체 | 사용처를 원본으로 | copy dead화 |

### 루프 최적화 기법 비교

| 기법 | 조건 | 변환 | 효과 |
|------|------|------|------|
| LICM | 루프 불변식 | 루프 밖으로 이동 | 반복 횟수만큼 절감 |
| Strength Reduction | 유도변수 존재 | 곱셈→덧셈 | 비싼 연산 제거 |
| IV Elimination | SR 후 원래 IV 불필요 | 새 IV로 조건 교체, 원래 제거 | 레지스터/코드 절약 |

### Copy Elimination 비교

| 기법 | 원리 | 조건 | 부작용 |
|------|------|------|--------|
| Copy Propagation | 사용처를 원본으로 교체 | 항상 가능 | 없음 |
| Copy Coalescing | 소스/타겟 LR 합쳐 같은 레지스터 | LR이 간섭 안 해야 함 | 간선 증가→컬러링 어려움 |

## ③ 용어 정의

| 용어 | 정의 |
|------|------|
| AST | 파스 트리에서 불필요한 노드를 제거한 추상 구문 트리 |
| Available Expression | 지점 p에 도달하는 모든 경로에서 계산+피연산자 미재정의인 표현식 |
| Basic Block (BB) | 제어 흐름이 시작에 들어와 끝에 나가며 중간 분기 없는 연속 명령어 |
| CFG | BB를 노드, 제어 흐름을 간선으로 하는 방향 그래프 |
| Copy Coalescing | COPY 소스/타겟 LR이 비간섭이면 합쳐 같은 레지스터, COPY 삭제 |
| CPI | 명령어 하나당 평균 클럭 사이클 수 |
| Dead Code | 결과가 후속 명령어에서 사용되지 않는 명령어 |
| Definition | 변수에 값을 대입하는 명령어 (쓰기) |
| DEF[b] | BB b에서 정의된 변수 집합 |
| Fixed Point | 반복 계산에서 값이 변하지 않는 수렴 상태 |
| GEN[b] | BB b의 locally generated definitions 집합 |
| Induction Variable | 루프 반복마다 일정하게 변하는 변수 |
| Interference Graph | 노드=LR, 간선=동시 live. 그래프 컬러링으로 RA |
| IR | 소스와 타겟 사이의 중간 표현 |
| KILL[b] | BB b 내 정의와 같은 변수의 다른 정의들 (정적 속성) |
| Live Range (Web) | 정의+도달 가능한 사용의 집합. RA 단위 |
| Live Variable | 지점 p에서 어떤 경로에서 재정의 전 사용되는 변수 |
| Locally Exposed Use | BB 내 사용인데 앞에 같은 변수 정의가 BB 내 없는 것 |
| Locally Generated Def | BB 내 변수의 마지막 정의 |
| Memory Live Range | 같은 메모리 위치 접근하는 store/load 집합 |
| φ-function | SSA 합류점에 삽입. 경로에 따라 값 선택 (실행 안 되는 표기법) |
| Pseudo Register | 물리 RA 전 가상 레지스터 |
| Reaching Definition | 정의 d가 p에 도달=d→p 경로 존재+kill 안 됨 |
| Register Promotion | load/store→copy. singleton 변수만 가능 |
| Spilling | RA 시 레지스터 부족→일부 web을 스택으로 |
| SSA | 각 변수가 전체에서 단 한 번만 정의되는 형태 |
| Strength Reduction | 곱셈→덧셈 교체. 유도변수에 적용 |
| Transfer Function | BB 통과 시 데이터 흐름 정보 변화 함수 |
| USE[b] | BB b의 locally exposed uses 집합 |
| Worklist Algorithm | 변화 노드만 재계산. 고정점까지 수렴 |

### RISC 명령어 레퍼런스 (HP PA-RISC 기반)

수업 예제에서 사용되는 명령어. 표기: `CMD src, dst` (소스 먼저, 목적지 나중).

#### 데이터 이동 (Load / Store / Copy)

| 명령어 | 문법 | 동작 |
|--------|------|------|
| LDW | `LDW offset(reg), dst` | 메모리[reg+offset] → dst 레지스터에 로드 (word) |
| LDWS | `LDWS offset(reg), dst` | 메모리[reg+offset] → dst 레지스터에 로드 (word, short displacement) |
| LDWS,MA | `LDWS,MA offset(reg), dst` | 메모리[reg] → dst 로드 후, reg += offset (Modify After: 포인터 자동 증가) |
| LDWX,S | `LDWX,S idx(base), dst` | 메모리[base + idx×4] → dst (인덱스 스케일 로드, ×4 = word 크기) |
| STW | `STW src, offset(reg)` | src 레지스터 → 메모리[reg+offset]에 저장 (word) |
| STWS | `STWS src, offset(reg)` | src 레지스터 → 메모리[reg+offset]에 저장 (word, short displacement) |
| STWM | `STWM src, offset(reg)` | src → 메모리[reg]에 저장 후, reg += offset (Modify: 포인터 자동 증가) |
| LDI | `LDI imm, dst` | 즉시값(immediate) → dst 레지스터에 로드 |
| LDO | `LDO offset(reg), dst` | reg + offset → dst (Load Offset: 레지스터+상수 덧셈, 메모리 접근 아님) |
| COPY | `COPY src, dst` | src 레지스터 → dst 레지스터 복사 |

#### 산술/논리 연산

| 명령어 | 문법 | 동작 |
|--------|------|------|
| ADD | `ADD src1, src2, dst` | src1 + src2 → dst |
| MULTI | `MULTI imm, src, dst` | imm × src → dst (즉시값 곱셈) |
| SUB | `SUB src1, src2, dst` | src1 − src2 → dst |
| SUBI | `SUBI imm, src, dst` | imm − src → dst (즉시값에서 뺄셈) |
| SH2ADD | `SH2ADD src, base, dst` | (src << 2) + base → dst (src×4 + base, 배열 인덱싱용) |

#### 주소 계산 (32비트 상수 로드)

| 명령어 | 문법 | 동작 |
|--------|------|------|
| ADDILG | `ADDILG LR'sym, reg, dst` | reg + symbol의 상위 21비트 → dst (Long displacement 상위) |
| ADDIL | `ADDIL LR'sym, reg, dst` | ADDILG와 동일 (표기 변형) |
| LDO (하위) | `LDO RR'sym(src), dst` | src + symbol의 하위 11비트 → dst (Long displacement 하위) |

ADDILG + LDO 쌍으로 32비트 전역 주소 획득. SPARC의 `sethi+or`, MIPS의 `lui+ori`에 대응.

#### 분기 / 비교

| 명령어 | 문법 | 동작 |
|--------|------|------|
| IF | `IF reg1 < reg2 GOTO label` | reg1 < reg2이면 label로 분기 (의사 명령어) |
| IFNOT | `IFNOT reg1 < reg2 GOTO label` | 조건 불만족 시 label로 분기 (의사 명령어) |
| COMB,<= | `COMB,<=,N src1, src2, label` | src1 ≤ src2이면 label로 분기 (Compare and Branch) |
| COMBF,< | `COMBF,<,N src1, src2, label` | src1 < src2가 **거짓**이면 분기 (Compare and Branch False) |
| COMIB,<= | `COMIB,<=,N imm, reg, label` | imm ≤ reg이면 label로 분기 (즉시값 비교) |
| COMIBF,< | `COMIBF,<,N imm, reg, label` | imm < reg가 거짓이면 분기 |

#### 복합 명령어 (Compound Instructions)

| 명령어 | 문법 | 동작 |
|--------|------|------|
| ADDIB,< | `ADDIB,< imm, reg, label` | reg += imm → 결과 < 0이면 label로 분기 (증가+비교+분기) |
| ADDIBF,< | `ADDIBF,< imm, reg, label` | reg += imm → 결과 < 0이 **거짓**이면 분기 |
| LDWS,MA | `LDWS,MA offset(reg), dst` | 로드 + 포인터 자동 증가 (위 데이터 이동 참조) |
| STWM | `STWM src, offset(reg)` | 저장 + 포인터 자동 증가 (위 데이터 이동 참조) |

#### 기타

| 명령어 | 문법 | 동작 |
|--------|------|------|
| NOP | `NOP` | 아무 동작 안 함 (분기 delay slot 채우기 등에 사용) |
| LDWCOPY | `LDWCOPY src, dst` | 최적화 표기: load-to-copy 변환 후의 copy (수업 예제 전용) |

#### 특수 레지스터

| 레지스터 | 역할 |
|----------|------|
| r0 | 항상 0 (상수 레지스터) |
| r27 (GP) | Global Pointer — 전역 데이터 영역 기준 주소 |
| r30 (SP) | Stack Pointer — 스택 영역 기준 주소 |
| r31 | 범용 (예제에서 임시 레지스터로 사용) |
| 200+ | 의사 레지스터 (pseudo register, 물리 할당 전) |

#### N 접미사 (Nullification)

`,N` 접미사가 붙은 분기 명령어: 분기가 **실행되지 않을 때** 다음 명령어(delay slot)를 무효화(nullify). 분기가 실행되면 delay slot도 정상 실행. 파이프라인 최적화용.

## ④ 주제별 상세

---

### Ch1. 컴파일러 구조와 최적화 개요

#### 1-1. 프로그램 실행 3가지 방식

```
(A) 컴파일러:
  [Source] → Compiler → [Executable] → HW → Output
  compile time ─────┘                  └─ runtime

(B) 인터프리터:
  [Source] → Interpreter(SW) → Output
                └─── runtime ───┘

(C) 하이브리드:
  [Source] → Compiler → [Bytecode IR] → VM(Interp/JIT) → Output
  compile time ─────┘                   └──── runtime ────┘
```

**[예시문제]** Java 프로그램의 실행 과정을 단계별로 설명하라.

**[풀이]**: ① javac가 .java를 .class(바이트코드)로 컴파일 (compile time) → ② JVM이 바이트코드를 로드 → ③ 인터프리터로 실행하거나, 자주 실행되는 부분은 JIT 컴파일러가 기계어로 변환 후 HW에서 직접 실행 (runtime). 이식성: JVM만 있으면 어떤 CPU에서든 실행 가능.

#### 1-2. 컴파일러 3단계 구조

```
              FRONT-END (Analysis)
C++ src ──┐
Fortran ──┤→ Lexer → Parser → Semantic Analyzer → IR Generator
C src   ──┘        ↕ Symbol Table                     ↓
                         MIDDLE-END                    IR
                                                       ↓
                                                  Optimizer (machine-indep)
                                                       ↓
              BACK-END (Synthesis)              Code Generator
                                                       ↓
                                               Low-Level IR → Optimizer (machine-dep)
                                                       ↓
                                              Relocatable Object Code (.o)
              RUN-TIME                                 ↓
                                    Linker (+libc) → a.out → Loader → HW
```

**[예시문제]** "변수 x의 타입이 int인지 확인"은 어느 단계인가?

**[풀이]**: Front-end의 Semantic Analysis. 심볼 테이블에서 x의 선언을 찾아 타입을 확인. CFG로 표현 불가 → 자동 생성 불가, 직접 구현 필요.

#### 1-3. LLVM 구조

```
C       → Clang FE  ─┐                         ┌→ LLVM X86 BE  → x86
Fortran → llvm-gcc FE ┼→ LLVM Optimizer(LLVM IR)┼→ LLVM PPC BE  → PowerPC
Haskell → GHC FE     ─┘                         └→ LLVM ARM BE  → ARM
```

**[예시문제]** LLVM에 M개 언어와 N개 아키텍처가 있을 때, 모듈 수는?

**[풀이]**: M(프론트엔드) + 1(공통 옵티마이저) + N(백엔드) = **M+N+1**개. 만약 단일 구조였으면 M×N개 필요. LLVM IR이 공통 인터페이스 역할.

#### 1-4. Front-end: Lexer → Parser → Semantic Analyzer

```
입력: "int foo = 100;"

Lexer (정규식→유한오토마타):
  → [KW:int] [ID:foo] [OP:=] [NUM:100] [SYM:;]

Parser (CFG→파스트리):
  var_decl
  ├── type: "int"
  ├── ID: "foo"
  └── init: NUM(100)

Semantic Analyzer (심볼테이블):
  SymTable: {foo: type=int, scope=local, offset=SP-4}
  check: 100은 int와 호환? → OK
```

**[예시문제]** `x = y + "hello";`에서 Lexer, Parser, Semantic Analyzer 중 에러를 잡는 곳은?

**[풀이]**: **Semantic Analyzer**. Lexer는 토큰 분리만 (x, =, y, +, "hello", ; 모두 유효한 토큰). Parser는 `expr = expr + expr` 구조로 문법상 유효. Semantic Analysis에서 int와 string의 + 연산 타입 불일치를 검출.

#### 1-5. 실행 시간 공식과 최적화

```
T = IC × CPI × CT

  IC  ← 컴파일러가 줄임 (CSE, DCE, 루프 최적화 등)
  CPI ← 컴파일러가 줄임 (명령어 스케줄링, 레지스터 할당 등)
  CT  ← HW 결정 (컴파일러 관여 불가)
```

메모리 계층 지연:
```
L1 cache         0.5 ns    ← 레지스터 할당으로 활용 극대화
Main memory      100 ns    ← L1 대비 200배
Disk seek  10,000,000 ns   ← L1 대비 2천만배
```

**[예시문제]** IC=10^9, CPI=1.5, Clock=2GHz. 최적화 후 IC 30%↓, CPI→1.2. Speedup은?

**[풀이]**:
```
CT = 1/(2×10^9) = 0.5ns
T_old = 10^9 × 1.5 × 0.5ns = 0.75초
T_new = 0.7×10^9 × 1.2 × 0.5ns = 0.42초
Speedup = 0.75/0.42 = 1.79배
```

#### 1-6. 최적화 컴파일러 페이즈 파이프라인

```
(1)  Basic Block Optimization        ← BB 내 지역 최적화
(2)  Dataflow Analysis               ← RD, LV 등 정보 계산
(3)  Global CSE                      ← BB 경계 넘어 중복 제거
(4)  Promotion of Memory Ops         ← load/store → 레지스터
(5)  LICM                            ← 루프 불변 코드 이동
(6)  Induction Variable Analysis     ← 강도 감소 + IV 제거
(7)  Register Reassociation
(8)  Register Web Builder            ← Live Range 구축
(9)  Instruction Scheduling          ← pre-RA (병렬 실행)
(10) Register Allocation             ← 그래프 컬러링
(11) Peephole Optimization           ← 패턴 기반 소규모 개선
(12) Instruction Scheduling          ← post-RA (RA가 순서 변경하므로)
```

**[예시문제]** Instruction Scheduling이 RA 전후 2번 수행되는 이유는?

**[풀이]**: pre-RA 스케줄링은 의사 레지스터(무한) 가정으로 자유롭게 재배치. RA가 물리 레지스터를 할당하면서 spill 코드 삽입/명령어 순서 변경이 발생할 수 있음. 따라서 post-RA에서 실제 레지스터 제약을 반영한 재스케줄링 필요.

#### 1-7. 복합 명령어와 ISA 설계

```c
for (i=0; i<N; i++) A[i] = 0;
```
최적화 후:
```
ADDIB,< 1,%r23,$003     ; i++ + (i<N?) + branch → 3동작 1명령어
STWM   %r0,100(%r31)    ; store 0 + ptr+=100    → 2동작 1명령어
```

**[예시문제]** ADDIB,<가 수행하는 3가지 동작을 나열하라.

**[풀이]**: ① r23에 1 더함 (i++) ② 결과가 0보다 작은지 비교 (i<N, 카운터가 음수→양수) ③ 조건 만족 시 $003으로 분기. 컴파일러 최적화가 이 패턴을 인식해 생성.

---

### Ch2. 단계별 최적화 실전 예제

#### 2-1. RISC 코드 생성: 스택머신 → RISC 변환

```
스택머신 IR (high-level):     RISC 의사코드 (low-level IR):
  push → load/loadi             각 스택 슬롯에 의사 레지스터 부여
  fetch → load                  (s0, s1, s2, ...)
  assign → store                스택 깊이(depth)를 추적하며 변환
  add/sub/... → add/sub/...
```

**[예시문제]** `x = y` (x: 전역 GP+4, y: 지역 SP-4)의 스택코드를 RISC로 변환하라.

**[풀이]** (현재 스택 깊이=0으로 시작):
```
push_const GP+4   → loadi GP+4, s0      ; x주소 (depth:0→1)
push_reg SP       → copy  SP, s1        ; SP     (depth:1→2)
push_const 4      → loadi 4, s2         ; 4      (depth:2→3)
sub               → sub   s1, s2, s1    ; SP-4   (depth:3→2)
fetch             → load  s1(0), s1     ; y값    (depth:2→2)
assign            → store s0(0), s1     ; x=y    (depth:2→0)
```

#### 2-2. 예제 프로그램과 비최적화 코드

```c
int a[25][25]; // 전역. 행크기=25*4=100byte
main() { int i; for(i=0;i<25;i++) a[i][0]=0; }
```

```
     STW   0,-40(30)             ; i=0 (스택)
     LDW   -40(30),206           ; r206=i
     LDI   25,212                ; r212=25
     IFNOT 206<212 GOTO $02
$03: LDW   -40(30),206           ; 중복#1
     ADDILG LR'a,27,213          ; &a 상위21bit+GP
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
루프 본체 13개 명령어. CFG:
```
  BB0 ──→ BB1 ←─┐ loop back
          │  ───┘
          ↓
          BB2 (exit)
```

#### 2-3. 지역 최적화 (BB 내) — 각 기법별 다이어그램과 예시

**Load-to-Copy**:
```
변환 전:                    변환 후:
  STW  r5, @mem   ─┐        STW  r5, @mem
  LDW  @mem, r8   ←┘        COPY r5, r8      ← 메모리 접근 제거
```

**[예시문제]** `STW 0,-40(30)` 직후 `LDW -40(30),206`에 적용하라.

**[풀이]**: 같은 주소 -40(SP)에 0을 저장 직후 로드 → `COPY 0, 206`. r0=0이므로 r206=0.

**Local CSE**:
```
변환 전:                    변환 후:
  x = y + z     (1번째)      x = y + z
  ...                        ...
  w = y + z     (2번째)      w = x         ← 재사용
```

**[예시문제]** BB 내에서 `LDW -40(30),206`이 2번 나타나고 중간에 -40(30)이나 r206이 변경되지 않았다면?

**[풀이]**: 두 번째 `LDW -40(30),206` 삭제. 첫 번째 결과(r206)가 여전히 유효.

**Constant Folding + Propagation**:
```
변환 전:           변환 후:
  x = 3 * 4        x = 12          ← Constant Folding
  y = x + 1        y = 13          ← Constant Propagation + Folding
```

**Dead Code Elimination**:
```
변환 전:           변환 후:
  x = y + 1        (삭제)          ← x가 아래에서 덮어쓰여짐
  ...               ...
  x = 10            x = 10
```

**Copy Propagation**:
```
변환 전:           변환 후:
  x = y             (x=y dead→삭제 가능)
  z = x + 100       z = y + 100    ← x 대신 y 사용
```

**[예시문제]** 아래 BB에 가능한 모든 지역 최적화를 적용하라.
```
a = load @x       ; (1)
b = a + 1         ; (2)
store b, @y       ; (3)
c = load @y       ; (4)
d = a + 1         ; (5)
e = 3 * 4         ; (6)
```

**[풀이]**:
```
(1) a = load @x         → 유지
(2) b = a + 1           → 유지
(3) store b, @y         → 유지
(4) c = b               → Load-to-Copy: (3)직후 load
(5) d = b               → Local CSE: a+1 = (2)의 결과 b
(6) e = 12              → Constant Folding: 3*4=12
```

#### 2-4. Global CSE — Available Expression

```
Available Expression 조건:
  지점 p에 도달하는 "모든 경로"에서 식 e가 계산됨
  + 마지막 계산 이후 e의 피연산자가 재정의되지 않음
  → p에서 e가 다시 나타나면 중복 → 삭제
```

**[예시문제]** BB0에서 `r212=25`를 계산. BB1 시작점에서 r212가 available한가?

**[풀이]**: BB1에 도달하는 경로: ①BB0→BB1 (첫 진입), ②BB1→BB1 (루프백). 루프 끝에서 r212가 재정의되지 않았다면 두 경로 모두에서 r212=25가 유효 → **available** → BB1 내 `LDI 25,212` 삭제 가능.

#### 2-5. Register Promotion

```
조건:
  ① Memory Live Range 구축 (같은 주소의 store/load 집합)
  ② singleton 변수 (배열/포인터/구조체 불가)
  ③ 주소 유도(address derivation)로 같은 위치 판별

변환:
  store → copy
  load  → 삭제 (이미 레지스터에 있음)
```

**[예시문제]** 다음 중 Register Promotion 가능한 것은?

| # | 코드 | 가능? | 이유 |
|---|------|-------|------|
| 1 | `STW r5, SP-16; LDW SP-16, r8` | O | singleton 지역변수 |
| 2 | `STW r5, 0(r3)` (r3=포인터) | X | 포인터 — 주소 가변 |
| 3 | `STW r5, GP+arr+r2*4` | X | 배열 — 인덱스 가변 |

#### 2-6. 루프 최적화: LICM + Strength Reduction + IV Elimination

```
LICM:
  변환 전:                변환 후:
  loop:                   p = &A;         ← 루프 밖으로
    p = &A;   ← 불변     loop:
    ... use p ...            ... use p ...

Strength Reduction:
  i=0,1,...,N-1 → i*K = 0,K,2K,...
  MULTI K,i,t  →  초기 t=0; 루프 내 t=t+K  (곱셈→덧셈)

IV Elimination:
  SR 후 원래 i가 조건에만 사용 → 조건을 t 기반으로 교체 → i 제거
```

**[예시문제]** 아래 루프에 SR + IV Elimination을 적용하라.
```c
for (j=0; j<50; j++)
    C[j*12] = D[j*6+3];
```

**[풀이]**:
```
Step 1 — SR: 새 유도변수 도입
  t1=0 (j*12 대체), t2=3 (j*6+3 대체)
  loop: C[t1]=D[t2]; t1+=12; t2+=6;

Step 2 — IV Elim: j<50 → t1<600 (=50*12)
  while(t1<600) { C[t1]=D[t2]; t1+=12; t2+=6; }
  → j 제거. 곱셈 2개→덧셈 2개.
```

#### 2-7. Register Allocation — 그래프 컬러링

```
Interference Graph:
  노드 = web (live range)
  간선 = 동시에 live인 web 쌍 (같은 레지스터 불가)

  x ──── y     x,y 동시 live → 다른 색 필요
  |    / |
  |  /   |     K개 물리 레지스터로 K-coloring
  z      w     NP-complete → 휴리스틱

Spilling: 레지스터 부족 → web을 스택으로
  def 직후 store 추가, use 직전 load 추가
```

**[예시문제]** 3개 물리 레지스터(R1,R2,R3)로 아래 간섭 그래프를 컬러링하라.
```
a ── b
|  / |
| /  |
c    d
```

**[풀이]**: a-b 간섭, a-c 간섭, b-c 간섭, b-d 간섭. a→R1, b→R2, c→R3, d→R1(또는 R3). a-d 간섭 없으므로 같은 색 가능. 4개 web을 3색으로 배정 가능 → spilling 불필요.

#### 2-8. Copy Elimination

**[예시문제]** 아래에 (a) copy propagation, (b) copy coalescing을 적용하라.
```
COPY r1, r2
ADD  r2, r3, r4
MUL  r2, r5, r6
```

**[풀이 (a)]**: r2 사용을 r1으로 교체 → COPY dead → 삭제:
```
ADD  r1, r3, r4
MUL  r1, r5, r6
```

**[풀이 (b)]**: r1과 r2의 LR이 간섭 안 하면 합쳐서 같은 물리 레지스터 → `COPY rX,rX` → 삭제. 주의: r1이 COPY 이후에도 live하면 간섭 → coalescing 불가.

#### 2-9. SSA Form

```
변환 규칙:
  ① 같은 변수 재정의 → 새 이름 부여 (a→a0,a1,a2,...)
  ② 제어 합류점 → φ-function 삽입
     a_merged = φ(a_then, a_else)
  ③ φ는 실제 실행 안 되는 표기법

이점: 변수 이름만으로 어느 정의인지 즉시 식별
     → 상수 전파 등 분석/최적화 극적 단순화
```

**[예시문제]** 아래를 SSA로 변환하고 상수 전파를 적용하라.
```
x = 5; y = x+1; if(y>3) x = y*2; z = x+y;
```

**[풀이]**:
```
SSA 변환:
  x0=5; y0=x0+1; if(y0>3) x1=y0*2;
  x2=φ(x1,x0); z0=x2+y0;

상수 전파:
  x0=5, y0=6, 6>3=true → then만 실행
  x1=12, x2=φ(12,5)=12, z0=12+6=18
```

#### 2-10. 전체 최적화 추적 요약

```
[원본]  루프 13개 명령어 (LDW×4, LDI×2, MULTI, ADDILG+LDO 매반복)
  ↓ (1) BB Opt: load-copy, CSE → 중복 LDW 일부 제거
  ↓ (2) Global CSE: BB 넘어 LDW, LDI 추가 삭제
  ↓ (3) Reg Promotion: i의 모든 STW/LDW → COPY/삭제
  ↓ (4) Loop Opt: ADDILG/LDO 루프밖(LICM), MULTI→LDO(SR), i제거(IVE)
  ↓ (5) Live Range: dead code 삭제 (COPY 0,206 + LDI 25,212)
  ↓ (6) Scheduling: 독립 명령어 재배치 (2-ALU)
  ↓ (7) RA + Copy Elim: COPY propagation/coalescing → 삭제
[최종]  루프 4개 명령어:
  ADD 65,69,68 / STWS 0,0(68) / LDO 100(69),69 / IF 69<71 GOTO
```

---

### Ch3. Data Flow Analysis

#### 3-1. 데이터 흐름 분석의 목적과 2단계 전략

```
목적: 함수의 각 지점에서 데이터 조작 정보 제공
     → 최적화의 기반 (분석 없이 최적화 불가)

1단계 Global: CFG의 BB 단위 → BB 경계 정보
  BB 효과를 요약(GEN/KILL 등) → 반복 계산 → 고정점
2단계 Local: BB 내부 → 명령어 경계 정보
  전역 결과를 출발점으로 명령어 효과 순차 적용
```

**[예시문제]** 왜 BB 단위로 나눠 분석하는가?

**[풀이]**: BB 내부에는 분기가 없어 선형 분석으로 충분. 복잡한 제어 흐름(분기/합류/루프)은 전역 분석에서 BB 단위로 처리. 2단계 분리로 효율적.

#### 3-2. 명령어와 BB의 효과

```
명령어 a = b + c:
  USE: {b, c}     (읽기)
  KILL: a의 이전 정의  (덮어쓰기)
  GEN: a의 새 정의   (생성)

BB 효과 (명령어 합성):
  Locally Exposed Use: 사용인데 앞에 같은 변수 정의가 BB 내 없음
  Locally Gen Def: 변수의 BB 내 마지막 정의
  Kill: BB 내 정의가 같은 변수의 BB 외부 정의를 무효화
```

**[예시문제]** 아래 BB의 exposed uses와 generated defs를 구하라.
```
r4 = r1 + r2
r2 = r4 + 1
r5 = r3 + r1
r1 = r5
r4 = r2 * r4
r2 = r5
```

**[풀이]** (각 줄에서 exposed/not exposed 판별):
```
r4 = r1 + r2   ; r1✓exposed, r2✓exposed (둘 다 BB 내 첫 사용)
r2 = r4 + 1    ; r4: NOT exposed (위에서 정의)
r5 = r3 + r1   ; r3✓exposed, r1: exposed (위에서 정의 안 됨→여전히 exposed)
r1 = r5        ; r5: NOT exposed
r4 = r2 * r4   ; r2, r4: NOT exposed
r2 = r5        ; r5: NOT exposed

Exposed Uses = {r1, r2, r3}
Gen Defs = {r1(=r5 최종), r4(=r2*r4 최종), r2(=r5 최종)}
```

#### 3-3. Reaching Definitions — 전달함수와 알고리즘

```
전달함수 (Forward):
  OUT[b] = GEN[b] ∪ (IN[b] − KILL[b])
      ↑        ↑           ↑
    나가는    BB에서      들어온 것 중
    정의     생성된 정의   kill 안 된 것

합류: IN[b] = ∪ OUT[pred]  (union: 어떤 경로든 도달하면 포함)
경계: OUT[entry] = {}
초기: OUT[b] = {}
```

**KILL의 의미 (주의!)**:
```
KILL = 정적 속성 (static property)
  "같은 변수를 정의하는 함수 내 다른 명령어 목록"
  실제 kill 효과: IN에 포함된 것만 영향받음
  예: IN={} → {}-KILL = {} → KILL 효과 없음
```

**GEN/KILL 계산 절차**:
```
Step 1: 함수 전체의 변수별 정의 위치를 정리
  변수 x: d1(B1), d4(B2), d7(B4)
  변수 y: d2(B1), d5(B2)

Step 2: 각 BB에 대해
  GEN[b] = BB 내 각 변수의 마지막 정의 번호 수집
  KILL[b] = BB 내 정의된 각 변수에 대해,
            함수 전체에서 같은 변수를 정의하는 "다른" 명령어 번호 수집
```

**[예시문제]** 아래 CFG의 RD를 구하라.

```
entry → B1 → B2 ←─ B3(루프백)
              ↓  ↘
              B3   B4 → exit

B1: d1:i=m-1, d2:j=n, d3:a=u1
B2: d4:i=i+1, d5:j=j-1
B3: d6:a=u2
B4: d7:i=u3
```

**[풀이 Step 1]** 변수별 정의: i→{d1,d4,d7}, j→{d2,d5}, a→{d3,d6}

| BB | GEN | KILL |
|----|-----|------|
| B1 | {1,2,3} | i→{4,7},j→{5},a→{6} = {4,5,6,7} |
| B2 | {4,5} | i→{1,7},j→{2} = {1,2,7} |
| B3 | {6} | a→{3} = {3} |
| B4 | {7} | i→{1,4} = {1,4} |

**[풀이 Step 2]** 반복 (초기 OUT={}):

| 회 | BB | IN | OUT | 변화 |
|----|----|----|-----|------|
| 1 | B1 | {} | {1,2,3} | Y |
| 1 | B2 | {1,2,3}∪{}={1,2,3} | {4,5}∪{3}={3,4,5} | Y |
| 1 | B3 | {3,4,5} | {6}∪{4,5}={4,5,6} | Y |
| 1 | B4 | {3,4,5} | {7}∪{3,5}={3,5,7} | Y |
| 2 | B2 | {1,2,3}∪{4,5,6}={1..6} | {4,5}∪{3,4,5,6}={3,4,5,6} | Y |
| 2 | B3 | {3,4,5,6} | {4,5,6} | N |
| 2 | B4 | {3,4,5,6} | {3,5,6,7} | Y |
| 3 | B2 | {1,2,3}∪{4,5,6}={1..6} | {3,4,5,6} | N→수렴 |

**[최종]**: B1:IN={},OUT={1,2,3} / B2:IN={1..6},OUT={3,4,5,6} / B3:IN={3,4,5,6},OUT={4,5,6} / B4:IN={3,4,5,6},OUT={3,5,6,7}

#### 3-4. Live Variables — 전달함수와 알고리즘

```
전달함수 (Backward):
  IN[b] = USE[b] ∪ (OUT[b] − DEF[b])
      ↑        ↑            ↑
    진입 시   BB에서        나간 live 변수 중
    live     사용된 변수    BB에서 재정의 안 된 것

합류: OUT[b] = ∪ IN[succ]  (union: 후속 경로 중 하나라도 사용하면 live)
경계: IN[exit] = {}
초기: IN[b] = {}
변화 시: predecessor를 ChangeNodes에 추가 (← RD와 반대!)
```

**USE/DEF 계산 절차**:
```
USE[b]: BB를 위에서 아래로 읽으며, 각 변수의 첫 접근이
        사용(read)이면 USE에 추가.
        정의(write)가 먼저 나오면 USE에 포함 안 됨.
DEF[b]: BB 내에서 정의된 모든 변수.
```

**[예시문제]** 같은 CFG에서 LV를 구하라.

**[풀이 Step 1]** USE/DEF:

| BB | 코드 | USE | DEF |
|----|------|-----|-----|
| B1 | i=m-1,j=n,a=u1 | {m,n,u1} | {i,j,a} |
| B2 | i=i+1,j=j-1 | {i,j} (정의 전 사용) | {i,j} |
| B3 | a=u2 | {u2} | {a} |
| B4 | i=u3 | {u3} | {i} |

**[풀이 Step 2]** 반복 Backward (초기 IN={}):

| 회 | BB | OUT | IN | 변화 |
|----|----|----|-----|------|
| 1 | B4 | {} | {u3} | Y |
| 1 | B3 | IN[B2]={} | {u2} | Y |
| 1 | B2 | IN[B3]∪IN[B4]={u2,u3} | {i,j}∪{u2,u3}={i,j,u2,u3} | Y |
| 1 | B1 | IN[B2]={i,j,u2,u3} | {m,n,u1}∪{u2,u3}={m,n,u1,u2,u3} | Y |
| 2 | B3 | IN[B2]={i,j,u2,u3} | {u2}∪{i,j,u2,u3}={i,j,u2,u3} | Y |
| 2 | B2 | {i,j,u2,u3}∪{u3}={i,j,u2,u3} | {i,j,u2,u3} | N→수렴 |

**[최종]**: B1:OUT={i,j,u2,u3},IN={m,n,u1,u2,u3} / B2:OUT={i,j,u2,u3},IN={i,j,u2,u3} / B3:OUT={i,j,u2,u3},IN={i,j,u2,u3} / B4:OUT={},IN={u3}

#### 3-5. Local Analysis (BB 내부 명령어 경계)

```
전역 분석 결과(BB 시작 정보)로부터 명령어 하나씩 효과 적용:

  IN(BB) = {d1, d2}        ← 전역 분석에서 제공
    ↓
  x = 1 (d3) → kill d1 → {d2, d3}
    ↓
  y = 1 (d4) → kill d2 → {d3, d4}
    ↓
  z = x+y (d5) →         {d3, d4, d5}
```

**[예시문제]** BB 진입 시 RD IN={d1(x=0), d2(y=0), d5(z=?)}. 아래 각 명령어 후 도달 정의를 구하라.
```
x = 1     (d3)
y = x+1   (d4)
```

**[풀이]**:
```
시작:           {d1, d2, d5}
d3: x=1   → kill d1(x의 이전 정의) → gen d3 → {d2, d3, d5}
d4: y=x+1 → kill d2(y의 이전 정의) → gen d4 → {d3, d4, d5}
```

#### 3-6. 보수적 근사 (Conservative Approximation)

```
원칙: 정확한 정보 계산 불가 시 → 안전한 방향으로 근사
  RD: 실제보다 더 많은 정의가 도달한다고 가정 (union)
      → 최적화 기회를 놓칠 수 있지만 잘못된 최적화는 방지
  LV: 실제보다 더 많은 변수가 live라고 가정 (union)
      → 레지스터를 더 쓸 수 있지만 live 변수를 죽이지는 않음

union을 쓰는 이유: "어떤 경로든 가능하면 포함" → 안전
intersection을 쓰면: "모든 경로에서" → Available Expression에 사용
```

**[예시문제]** RD에서 합류에 intersection을 쓰면 어떤 문제가 생기나?

**[풀이]**: 정의 d가 경로 A로만 도달하고 경로 B로는 도달하지 않으면, intersection은 d를 제외. 하지만 런타임에 경로 A가 실행되면 d가 실제로 도달 → d를 무시하면 잘못된 최적화 (예: d가 도달 안 한다고 가정하고 다른 값을 사용). union이 안전.

## ⑤ 시험 대비 체크리스트

### 계산 문제 유형
- [ ] 실행 시간 계산 (IC × CPI × CT) 및 Speedup
- [ ] 스택머신 → RISC 코드 변환 (스택 깊이 추적)
- [ ] GEN/KILL 테이블 계산 (변수별 정의 위치 → 다른 정의 수집)
- [ ] RD 반복 계산 (IN/OUT, 수렴까지)
- [ ] USE/DEF 테이블 계산 (exposed use 판별)
- [ ] LV 반복 계산 (Backward, predecessor 전파)
- [ ] Local Analysis (BB 내 명령어별 도달 정의)
- [ ] Strength Reduction + IV Elimination 적용
- [ ] SSA 변환 (리네이밍 + φ-function)
- [ ] 간섭 그래프 컬러링 (K개 레지스터)
- [ ] BB 내 지역 최적화 일괄 적용

### 개념 문제 유형
- [ ] Forward(RD) vs Backward(LV) 차이
- [ ] KILL의 정적 속성 의미
- [ ] union vs intersection 선택 이유 (보수적 근사)
- [ ] FE/ME/BE 역할 구분
- [ ] SSA 장점과 φ-function 역할
- [ ] Register Promotion 조건 (singleton)
- [ ] Copy Propagation vs Coalescing 트레이드오프
- [ ] Instruction Scheduling이 RA 전후 2번인 이유
- [ ] LLVM M+N 구조의 장점
- [ ] 복합 명령어와 컴파일러의 관계
