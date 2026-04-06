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
| 초기화 | OUT[b] = {} | IN[b] = {} |
| 경계 조건 | OUT[entry] = {} | IN[exit] = {} |
| 합류 노드 | 여러 predecessor를 가진 노드 | 여러 successor를 가진 노드 |
| 용도 | live range 구축, 상수 전파 | 레지스터 할당, dead code 제거 |

### 지역 최적화 기법 비교

| 기법 | 분석 | 변환 | 예시 |
|------|------|------|------|
| Load-to-Copy | store 직후 같은 위치 load | load → copy로 교체 | `stw x, @z; y=ldw @z` → `stw x, @z; y=x` |
| Local CSE | BB 내 동일 식 중복 계산 | 두 번째 이후 삭제 또는 재사용 | `x=y+z; ... w=y+z` → `x=y+z; ... w=x` |
| Constant Folding | 컴파일 타임 계산 가능 | 상수 값으로 교체 | `if(4>3)` → `if(true)` |
| Dead Code Elim | 결과가 사용되지 않음 | 명령어 삭제 | `x=y+1; x=10` → `x=10` |
| Copy Propagation | copy의 소스로 대체 가능 | 사용처를 원본으로 교체 | `x=y; z=x+1` → `z=y+1` |

### 루프 최적화 기법 비교

| 기법 | 설명 | 효과 |
|------|------|------|
| LICM (Loop Invariant Code Motion) | 루프 안에서 매번 같은 결과인 코드를 루프 밖으로 | 반복 횟수만큼 연산 절감 |
| Strength Reduction | 비싼 연산(곱셈)을 싼 연산(덧셈)으로 교체 | 유도변수 × 상수 → 이전 값 + 상수 |
| Induction Variable Elimination | 강도 감소 후 원래 유도변수가 불필요하면 제거 | 레지스터 절약, 코드 축소 |

## ③ 용어 정의

| 용어 | 정의 |
|------|------|
| AST (Abstract Syntax Tree) | 파스 트리에서 불필요한 노드를 제거한 추상 구문 트리. IR의 한 형태 |
| Available Expression | 지점 p에 도달하는 모든 경로에서 계산되었고, 마지막 계산 이후 피연산자가 재정의되지 않은 표현식 |
| Basic Block (BB) | 제어 흐름이 처음에 들어와 끝에서 나가며, 중간에 분기가 없는 연속 명령어 시퀀스 |
| CFG (Control Flow Graph) | 기본 블록을 노드, 제어 흐름을 간선으로 하는 방향 그래프 |
| Copy Coalescing | COPY의 소스와 타겟 live range가 간섭하지 않으면 합쳐 같은 레지스터 할당, COPY 삭제 |
| Copy Propagation | x=y 이후 x 사용을 y로 교체하여 copy를 죽은 코드로 만드는 기법 |
| CPI (Cycles Per Instruction) | 명령어 하나당 평균 소요 클럭 사이클 수 |
| Dead Code | 결과가 어떤 후속 명령어에서도 사용되지 않는 명령어 |
| Definition (정의) | 변수에 값을 대입하는(또는 대입할 수 있는) 명령어. 쓰기(write) |
| DEF[b] | BB b에서 정의된 변수들의 집합 (Live Variables 분석용) |
| Extended Basic Block | 들어오는 분기 없이 나가는 분기만 있는 연속 BB 체인. BB와 동일한 최적화 적용 가능 |
| Fixed Point (고정점) | 반복 계산에서 더 이상 값이 변하지 않는 수렴 상태. 데이터 흐름 방정식의 해 |
| GEN[b] | BB b에서 생성된 정의들의 집합 (= locally generated definitions) |
| Induction Variable | 루프 반복마다 일정하게 증가/감소하는 변수. 강도 감소의 대상 |
| Interference Graph | 노드: live range(web), 간선: 동시에 살아있는 관계. 그래프 컬러링으로 레지스터 할당 |
| IR (Intermediate Representation) | 소스와 타겟 사이의 중간 표현. AST, 스택머신코드, 레지스터기반코드 등 |
| KILL[b] | BB b 내의 정의와 같은 변수를 정의하는 함수 내 다른 정의들의 집합. b를 통과하면 무효화 |
| LICM | Loop Invariant Code Motion. 루프 불변 코드를 루프 헤더(밖)로 이동 |
| Live Range (Web) | 하나의 정의와 그 정의에 도달하는 모든 사용의 집합. 레지스터 할당의 단위 |
| Live Variable | 지점 p에서 시작하는 어떤 경로를 따라 값이 (재정의 전에) 사용되는 변수 |
| LLVM | Low Level Virtual Machine. 모듈화된 오픈소스 컴파일러 인프라. Frontend-Optimizer-Backend 구조 |
| Locally Exposed Use | BB 내에서 사용되지만, 그 사용 전에 같은 변수의 정의가 BB 내에 없는 사용 |
| Locally Generated Definition | BB 내에서 어떤 변수에 대한 마지막 정의. GEN 집합의 원소 |
| Memory Live Range | 같은 메모리 위치에 접근하는 store/load들의 집합 |
| Meet Operator (합류 연산자) | 여러 경로의 데이터 흐름 정보를 합치는 연산. RD/LV 모두 union 사용 |
| φ-function (파이 함수) | SSA에서 제어 합류점에 삽입. 어느 경로로 왔느냐에 따라 값을 선택하는 표기법 |
| Pseudo Register | 물리 레지스터 할당 전 사용하는 가상 레지스터. 무한 개 가정 |
| Reaching Definition | 정의 d가 지점 p에 도달 = d→p 경로가 존재하고, 그 경로에서 d가 kill되지 않음 |
| Register Promotion | 메모리 접근(load/store)을 레지스터 연산(copy)으로 승격. 단일 변수 조건 |
| RISC | Reduced Instruction Set Computer. 균일한 명령어, load/store 아키텍처, 범용 레지스터 |
| Spilling | 레지스터 부족 시 일부 live range를 스택 메모리로 내보내는 것 |
| SSA (Static Single Assignment) | 각 변수가 프로그램 전체에서 단 한 번만 정의되는 표현 형태. 합류점에 φ-function 삽입 |
| Strength Reduction (강도 감소) | 비싼 연산(곱셈)을 싼 연산(덧셈)으로 교체. 유도변수에 적용 |
| Transfer Function (전달함수) | BB를 통과하면서 데이터 흐름 정보가 어떻게 변하는지를 기술하는 함수 |
| USE[b] | BB b의 locally exposed uses 집합 (Live Variables 분석용) |
| Use (사용) | 변수의 값을 읽는 명령어. 읽기(read) |
| Worklist Algorithm | 변화가 있는 노드만 재계산하는 반복 알고리즘. 고정점까지 수렴 |

## ④ 주제별 상세

### Ch1. Introduction — 컴파일러 개론

**컴파일러 = 번역기**: 소스 언어 → 타겟 언어. 이 과목은 백엔드(코드 생성 + 최적화)에 집중.

**컴파일러 구조 (3단계)**:
```
Source Code
    ↓
FRONT-END (Analysis)
  Lexer → Parser → Semantic Analysis
    ↓
MIDDLE-END
  IR 생성 → Machine-independent Optimization
    ↓
BACK-END (Synthesis)
  Machine Code Generation → Machine-dependent Optimization
    ↓
RUNTIME: Linker → Loader → 실행
```

**LLVM 구조**:
```
C      → Clang FE  ─┐                    ┌→ X86 BE  → X86
Fortran→ llvm-gcc FE┼→ LLVM Optimizer ──→┼→ ARM BE  → ARM
Haskell→ GHC FE    ─┘   (LLVM IR)        └→ PPC BE  → PowerPC
```

**Front-end 요약**:
- Lexer: 정규식 → 유한 오토마타. 도구: lex/flex
- Parser: CFG → 파스 트리. Top-down vs Bottom-up(더 강력). 도구: yacc/bison
- Semantic Analysis: 심볼 테이블 기반. 자동 생성 불가, 직접 구현
- IR: AST, 스택머신코드(`push a; push b; add; store c`), 레지스터 기반 코드

**최적화 컴파일러 페이즈 구조**:
```
Graph Repr. of IR
  ↓ Basic Block Optimization
  ↓ Dataflow Analysis + Interval Analysis
  ↓ Global Common Subexpression Elimination
  ↓ Promotion of Memory Operations
  ↓ Loop Invariant Code Motion
  ↓ Induction Variable Analysis
  ↓ Register Reassociation
  ↓ Register Web (Live Range) Builder
  ↓ Instruction Scheduling (pre-RA)
  ↓ Register Allocation
  ↓ Peephole Optimization
  ↓ Instruction Scheduling (post-RA)
Graph Repr. of Optimized Code
```

최적화 레벨: -O1(기본), -O2(안정), -O3+(공격적, 불안정 가능)

---

### Ch2. Code Optimization Example — 단계별 최적화 실전

**예제 프로그램과 최적화 전 코드**:
```c
int a[25][25];
main() {
    int i;
    for (i=0; i<25; i++)
        a[i][0] = 0;
}
```

RISC 비최적화 코드 (루프 본체, 의사 레지스터):
```
$03: LDW  -40(30),206       ; i를 메모리에서 로드
     ADDILG LR'a,27,213     ; &a 상위비트
     LDO  RR'a(213),208     ; &a 하위비트
     MULTI 100,206,214      ; i*100 (행 오프셋)
     ADD  208,214,215       ; &a[i][0]
     STWS 0,0(215)          ; a[i][0] = 0
     LDW  -40(30),206       ; i 다시 로드 (중복!)
     LDO  1(206),216        ; i+1
     STW  216,-40(30)       ; i=i+1 저장
     LDW  -40(30),206       ; i 또 로드 (중복!)
     LDI  25,212            ; 25 또 로드 (중복!)
     IF   206<212 GOTO $03
     NOP
```
→ 13개 명령어, 중복 다수, 매번 곱셈

**단계별 최적화 적용과 결과**:

| 단계 | 최적화 | 핵심 변화 |
|------|--------|----------|
| 1 | BB 내 지역 최적화 | Load→Copy, 지역 CSE로 중복 LDW 일부 제거 |
| 2 | Global CSE | BB 경계 넘어 중복 LDW, LDI 추가 제거 |
| 3 | Register Promotion | 변수 i를 메모리→레지스터로 승격. STW/LDW 전부 제거 |
| 4 | Loop Opt (LICM+SR+IVE) | 주소계산 루프 밖으로, 곱셈→덧셈, 원래 i 제거 |
| 5 | Live Range + Dead Code | 죽은 코드(COPY 0,206 등) 삭제, 웹 번호 부여 |
| 6 | Instruction Scheduling | 독립 명령어 재배치로 2-ALU 병렬 실행 |
| 7 | Register Alloc + Copy Elim | 물리 레지스터 할당, COPY 제거(propagation+coalescing) |

**최종 최적화 코드** (루프 본체 4개 명령어):
```
$03: ADD  65,69,68       ; &a + offset
     STWS 0,0(68)        ; a[i][0] = 0
     LDO  100(69),69     ; offset += 100
     IF   69<71 GOTO $03 ; offset < 2500?
```

**Strength Reduction 핵심 원리 (예시 풀이)**:

원래: `i`가 0,1,2,...,24로 변할 때 `i*100`을 매번 곱셈으로 계산
```
MULTI 100, i, offset    ; 곱셈 (비싼 연산)
```
변환: 새 유도변수 `offset`을 0에서 시작, 매번 100 더함
```
초기: offset = 0
루프: offset = offset + 100  ; 덧셈 (싼 연산)
조건: offset < 2500          ; 25*100 (원래 i<25 대체)
```
→ 원래 유도변수 i가 불필요해져 제거됨 (Induction Variable Elimination)

**Register Promotion 조건**:
- 대상: 같은 메모리 위치에 접근하는 store/load 쌍 (Memory Live Range)
- 조건: singleton 변수여야 함 (배열, 포인터, 구조체 불가)
- 변환: store → copy, load → 삭제

**Copy Elimination 두 가지 방법**:
- Copy Propagation: `y=x; z=y+1` → `z=x+1` (copy를 dead code로)
- Copy Coalescing: 소스/타겟 live range가 간섭 안 하면 합쳐서 같은 레지스터 할당 → `COPY rx,rx` 삭제
  - 트레이드오프: 합친 노드의 간선 증가 → 컬러링 어려워짐

**SSA Form 핵심**:
```
일반 형태:           SSA 형태:
a = x+y             a0 = x+y
b = a-1             b0 = a0-1
a = y+b             a1 = y+b0    ← 다른 이름
b = x*4             b1 = x*4
a = a+b             a2 = a1+b1
```
합류점: φ-function 삽입. `a3 = φ(a1, a2)` = 경로에 따라 선택 (실제 실행 아닌 표기법)

이점: 변수 이름만으로 어느 정의인지 즉시 식별 → 분석/최적화 극적 단순화

---

### Ch3. Data Flow Analysis — 데이터 흐름 분석

**목적**: 함수의 각 명령어 경계마다 데이터 조작에 관한 전역 정보를 계산. 최적화의 기반.

**2단계 분석 전략**:
```
1단계: Global Analysis — CFG 위에서 BB 단위, 각 BB 경계의 정보 계산
2단계: Local Analysis — BB 내부, 각 명령어 경계의 정보 계산
```

**명령어의 효과** (`a = b + c`의 경우):
- USE: b, c를 읽음
- KILL: a의 이전 정의를 무효화
- GEN: a에 대한 새 정의 생성

**BB의 효과 — 핵심 3개념**:
- Locally Exposed Use: BB 안에서 사용되지만, 그 전에 같은 변수 정의가 BB 내에 없는 것
- Kill: BB 내 정의가 같은 변수의 BB 외부 정의를 무효화
- Locally Generated Definition: BB 내 어떤 변수의 마지막 정의

**KILL의 의미 (주의)**: KILL은 BB의 정적 속성. "만약 이 정의가 여기 도달하면 죽인다"는 잠재적 능력. 실제 효과는 `IN − KILL` 계산 시 IN에 포함된 것만 영향받음. 예: B1이 함수 시작이면 IN={}이므로 KILL이 무엇이든 효과 없음.

#### Reaching Definitions 분석

**정의**: 정의 d가 지점 p에 도달 = d→p 경로 존재 + 경로에서 d가 kill되지 않음

**방정식**: Forward 분석
```
OUT[b] = GEN[b] ∪ (IN[b] − KILL[b])
IN[b]  = ∪ OUT[p]  (모든 predecessor p)
경계: OUT[entry] = {}, 초기: OUT[b] = {}
```

**GEN/KILL 계산법**:
- GEN[b]: BB 내에서 각 변수의 마지막 정의 모음
- KILL[b]: BB 내에서 정의된 각 변수에 대해, 함수 전체에서 같은 변수를 정의하는 **다른** 명령어들의 집합

**예시 문제 풀이**:
```
entry → B1 → B2 ←─┐
                ↓    │ (B3→B2 루프백)
               B3 ──┘
                ↓
               B4 → exit

B1: d1: i=m-1,  d2: j=n,    d3: a=u1
B2: d4: i=i+1,  d5: j=j-1
B3: d6: a=u2
B4: d7: i=u3
```

Step 1 — GEN/KILL 계산:
```
B1: GEN={1,2,3}  KILL={4,5,6,7}  (i→kill d4,d7 / j→kill d5 / a→kill d6)
B2: GEN={4,5}    KILL={1,2,7}    (i→kill d1,d7 / j→kill d2)
B3: GEN={6}      KILL={3}        (a→kill d3)
B4: GEN={7}      KILL={1,4}      (i→kill d1,d4)
```

Step 2 — 반복 계산:

1회차:
```
B1: IN={} → OUT = {1,2,3}∪({}-{4,5,6,7}) = {1,2,3}
B2: IN = OUT[B1]∪OUT[B3] = {1,2,3}∪{} = {1,2,3}
    OUT = {4,5}∪({1,2,3}-{1,2,7}) = {4,5}∪{3} = {3,4,5}
B3: IN = OUT[B2] = {3,4,5}
    OUT = {6}∪({3,4,5}-{3}) = {4,5,6}
B4: IN = OUT[B2] = {3,4,5}
    OUT = {7}∪({3,4,5}-{1,4}) = {3,5,7}
```

2회차 (B2 변화 → 전파):
```
B2: IN = {1,2,3}∪{4,5,6} = {1,2,3,4,5,6}  ← 변화!
    OUT = {4,5}∪({1,2,3,4,5,6}-{1,2,7}) = {4,5}∪{3,4,5,6} = {3,4,5,6}
B3: IN = {3,4,5,6}, OUT = {6}∪{4,5,6} = {4,5,6}  ← 변화 없음
B4: IN = {3,4,5,6}, OUT = {7}∪{3,5,6} = {3,5,6,7}  ← 변화
```

3회차: B2 재확인 → IN, OUT 변화 없음 → 수렴 (고정점)

최종:
```
     IN              OUT
B1:  {}              {1,2,3}
B2:  {1,2,3,4,5,6}  {3,4,5,6}
B3:  {3,4,5,6}      {4,5,6}
B4:  {3,4,5,6}      {3,5,6,7}
```

#### Live Variables 분석

**정의**: 변수 v가 지점 p에서 live = p에서 시작하는 어떤 경로에서 v가 (재정의 전에) 사용됨

**방정식**: Backward 분석
```
IN[b]  = USE[b] ∪ (OUT[b] − DEF[b])
OUT[b] = ∪ IN[s]  (모든 successor s)
경계: IN[exit] = {}, 초기: IN[b] = {}
```

**USE/DEF 계산법**:
- USE[b]: BB 내에서 사용되지만, 그 사용 전에 같은 변수의 정의가 BB 내에 없는 변수들
- DEF[b]: BB 내에서 정의된 변수들의 집합

**Worklist 알고리즘 (Backward)**:
```
초기화: IN[exit]={}, 모든 IN[i]={}
while ChangeNodes ≠ {}:
  remove i from ChangeNodes
  OUT[i] = ∪ IN[s]  (모든 successor s)
  oldin = IN[i]
  IN[i] = USE[i] ∪ (OUT[i] − DEF[i])
  if oldin ≠ IN[i]:
    모든 predecessor p를 ChangeNodes에 추가  ← RD와 반대!
```

**RD vs LV 방향 비교 다이어그램**:
```
Reaching Definitions (Forward):
  OUT[p1] ─┐
  OUT[p2] ─┼→ IN[b] → [BB b: transfer function] → OUT[b]
  OUT[p3] ─┘
           union

Live Variables (Backward):
  IN[b] ← [BB b: transfer function] ← OUT[b] ←┬─ IN[s1]
                                                ├─ IN[s2]
                                                └─ IN[s3]
                                               union
```

## ⑤ 시험 대비 체크리스트

### 계산 문제 유형
- [ ] GEN/KILL 테이블 계산 (주어진 CFG + 정의에서)
- [ ] Reaching Definitions 반복 계산 (IN/OUT 테이블 완성)
- [ ] USE/DEF 테이블 계산
- [ ] Live Variables 반복 계산 (IN/OUT 테이블 완성)
- [ ] Strength Reduction 적용: 곱셈→덧셈 변환 + 새 유도변수 도입
- [ ] 최적화 전후 코드 비교: 어떤 최적화가 적용되었는지 식별

### 개념 문제 유형
- [ ] Forward vs Backward 분석의 차이와 각각의 예
- [ ] KILL의 의미: 정적 속성 vs 실제 효과 (IN에 있어야 kill됨)
- [ ] 보수적 근사(conservative approximation)의 의미와 필요성
- [ ] 합류 연산자로 union을 쓰는 이유
- [ ] 컴파일러 구조 3단계(FE/ME/BE)의 역할 구분
- [ ] SSA의 장점과 φ-function의 역할
- [ ] Register Promotion의 조건과 제약
- [ ] Copy Propagation vs Copy Coalescing의 차이
