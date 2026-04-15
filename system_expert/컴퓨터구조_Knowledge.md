# 컴퓨터구조 Knowledge

> 삼성DS · COD (Computer Organization & Design) RISC-V
> 최종 업데이트: 2026-04-15 · Ch1~Ch2

---

## ① 수식 모음

| 수식 | 의미 | 변수 설명 | 조건/비고 |
|------|------|----------|----------|
| `CPU Time = IC × CPI × T_c` | CPU 실행 시간 | IC=명령어 수, CPI=명령어당 사이클, T_c=클럭 주기 | 성능 비교의 기본 수식 |
| `CPU Time = Clock Cycles / Clock Rate` | 위와 동치 | Clock Cycles = IC × CPI, Clock Rate = 1/T_c | |
| `Performance = 1 / Execution Time` | 성능 정의 | | 높을수록 빠름 |
| `Speedup = Perf_X/Perf_Y = Time_Y/Time_X` | X가 Y보다 몇 배 빠른가 | | |
| `CPI = Σ(CPI_i × IC_i) / IC_total` | 가중 평균 CPI | CPI_i=클래스별 CPI, IC_i=클래스별 명령어 수 | 명령어 mix 반영 |
| `Power = C × V² × f` | CMOS 동적 전력 | C=capacitive load, V=전압, f=주파수 | |
| `T_improved = T_affected/n + T_unaffected` | Amdahl's Law | n=개선 배율 | 전체 성능 상한 결정 |
| `Cost/die = Cost_wafer / (Dies/wafer × Yield)` | 다이 비용 | 다이 면적↑ → 비용 비선형↑ | |
| `Yield ≈ 1/(1 + Defects×Die_area/2)²` | 수율 근사 | | 경험적 모델 |
| `SPEC ratio = Ref_time / Target_time` | SPEC 점수 | 높을수록 빠름 | |
| `Overall SPEC = (Π ratio_i)^(1/n)` | SPEC 기하 평균 | n=벤치마크 수 | |
| `Moore's Law: 현재 × 2^(n/2)` | n년 후 트랜지스터 수 | | 경험적 관찰 |
| `slli by i = ×2^i` | 좌 시프트 = 곱셈 | | |
| `srli by i = ÷2^i` | 우 논리 시프트 = 나눗셈 | | unsigned only |
| `Byte offset = index × 8` | doubleword 배열 주소 | A[i] → offset = i×8 | |

---

## ② 핵심 비교표

| 비교 항목 | A | B | 차이점 |
|----------|---|---|--------|
| ISA vs ABI | HW/SW 인터페이스(명령어 집합) | ISA + 시스템SW 인터페이스 | ISA 같아도 OS 다르면 ABI 다름 |
| ISA vs Implementation | 명세("무엇을") | 마이크로아키텍처("어떻게") | Intel/AMD 같은 x86 다르게 구현 |
| RISC vs CISC | 단순·규칙·고정길이 | 복잡·가변길이 | RISC: HW 간결→파이프라이닝 용이 |
| Response Time vs Throughput | 작업 완료 시간 | 단위시간당 총 작업량 | 빠른CPU→둘다↑, CPU추가→주로Throughput↑ |
| Elapsed vs CPU Time | 전체응답(I/O,OS포함) | 순수 연산만 | CPU Time으로 CPU 성능 비교 |
| Volatile vs Non-volatile | DRAM(전원off시 소실) | HDD,SSD,Flash(보존) | |
| SRAM vs DRAM | 빠르고 비쌈(캐시) | 느리고 저렴(메인메모리) | 메모리 계층 핵심 |
| Saved vs Temporary regs | x8-9,x18-27(callee보존) | x5-7,x28-31(비보존) | 함수호출 저장/복원 규약 |
| Leaf vs Non-leaf | 다른 함수 호출 안 함 | 다른 함수 호출함 | Non-leaf: ra(x1)도 스택 저장 필수 |
| lb vs lbu | Sign extend | Zero extend | 부호 있는/없는 바이트 로드 |
| blt/bge vs bltu/bgeu | Signed 비교 | Unsigned 비교 | 같은 비트도 해석 다름 |
| Static vs Dynamic linking | 컴파일시 라이브러리 포함 | 실행시 필요할때 로드 | Dynamic: 경량화, 자동 버전 업데이트 |
| Array vs Pointer | 매번 index×size+base | 주소 직접 증가 | 컴파일러가 동일 최적화 가능→배열 권장 |
| PC-relative vs Absolute | PC+offset(분기) | 전체주소(lui+jalr) | PC-relative: 위치독립, 짧은 인코딩 |

---

## ③ 용어 정의

| 용어 | 정의 |
|------|------|
| ABI | ISA + 시스템SW 인터페이스. 같은 ISA라도 OS 다르면 ABI 다를 수 있음 |
| Abstraction | 하위 세부사항을 숨기고 단순 인터페이스만 노출하는 설계 원칙 |
| Amdahl's Law | 부분 개선이 전체 성능에 비례하지 않음. T=T_affected/n + T_unaffected |
| Basic Block | 중간에 분기 없고 분기대상도 처음뿐인 명령어 시퀀스. 최적화 기본 단위 |
| Cache Memory | CPU 내/근처 소형 고속 SRAM. 메인메모리 접근 지연 감소 |
| CISC | 복잡·다양·가변길이 명령어. x86 대표 |
| CPI | 명령어당 평균 클럭 사이클. CPU HW와 명령어 mix에 의해 결정 |
| Datapath | 프로세서 내부 데이터 연산 유닛 (ALU, 레지스터) |
| Control | 명령어 해석(decode) → Datapath에 제어 신호 |
| Design Principle 1 | Simplicity favors regularity |
| Design Principle 2 | Smaller is faster |
| Design Principle 3 | Good design demands good compromises |
| Dynamic Linking | 호출 시점에만 라이브러리 로드. Lazy Linkage |
| IC (Instruction Count) | 프로그램 실행 시 총 명령어 수 |
| ISA | HW/SW 인터페이스. 프로세서가 이해하는 명령어 집합 정의 |
| Little Endian | 최하위 바이트가 가장 낮은 주소. RISC-V 사용 |
| lr.d / sc.d | Load Reserved / Store Conditional. 동기화용 atomic 쌍 |
| lui | 20-bit 상수를 rd[31:12]에 로드, sign extend, [11:0]=0 |
| Moore's Law | IC 트랜지스터 수 약 2년마다 2배. 경험적 관찰(물리법칙 아님) |
| Power Wall | 전압/발열 한계로 클럭 향상 불가 → 멀티코어 전환 |
| R/I/S/SB/U/UJ-type | RISC-V 6가지 32-bit 고정길이 명령어 포맷 |
| RISC-V | UC Berkeley 개발 오픈 RISC ISA. 이 과목 기준 ISA |
| Sign Extension | 넓은 비트 확장 시 부호비트 복제. lb(sign), lbu(zero) |
| SPEC | Standard Performance Evaluation Corp. 기하평균 벤치마크 |
| Stored Program | 명령어도 이진수로 메모리 저장. 프로그램이 프로그램 조작 가능 |
| Yield | 웨이퍼당 정상 다이 비율. 면적↑→수율↓→비용 비선형↑ |

---

## ④ 주제별 상세

### Chapter 1: Computer Abstractions and Technology

(이전 채팅에서 상세 정리 완료 — 60 slides 전체 반영)

핵심 토픽: 무어의 법칙, 컴퓨터 분류(PC/Server/Super/Embedded/PMD/Cloud), 8 Great Ideas, SW 계층(App/System/HW), HW 5대 구성(Input/Output/Processor/Memory/Cache), ISA/ABI/Implementation, IC 제조와 비용(Yield, Cost/die), 성능 수식(CPU Time=IC×CPI×Tc), CPI mix, Power Wall(P=CV²f), Amdahl's Law, SPEC 벤치마크, 멀티프로세서 전환

**CPU Time 예시**: A(2GHz,10s) → Cycles=20G. B 목표 6s, 1.2×cycles → Rate_B=24G/6=4GHz

**CPI mix 예시**: Class A(CPI=1), B(2), C(3). Seq1(2,1,2)→10cycles/5IC=CPI2.0. Seq2(4,1,1)→9cycles/6IC=CPI1.5 → IC 적다고 항상 빠른 것 아님

**Amdahl 예시**: 100s 중 80s 개선. 5× 전체? → 80/n+20=20 → 불가능!

**Power 예시**: 85% C, 85% V, 85% f → P_new/P_old = 0.85×0.85²×0.85 = 0.85⁴ ≈ 0.52

### Chapter 2: Instructions — Language of the Computer

(이전 채팅에서 상세 정리 완료 — 95 slides 전체 반영)

핵심 토픽: Instruction Set 개념, RISC-V 소개, 산술 연산(3-오퍼랜드), DP1/2/3, 레지스터(32×64b), 메모리 오퍼랜드(ld/sd, Little Endian, byte addressing), 즉시값(addi), 부호(2's complement, sign extension), 6가지 명령어 포맷(R/I/S/SB/U/UJ), 논리연산(sll/srl/and/or/xor), 분기(beq/bne/blt/bge/bltu/bgeu), 프로시저(jal/jalr, 스택, leaf/non-leaf, 재귀 fact), Memory Layout, 문자 데이터(ASCII/Unicode, lb/lbu/sb), 32-bit 상수(lui+addi), Branch/Jump addressing(PC-relative), 동기화(lr.d/sc.d), 번역 과정(Compiler→Assembler→Linker→Loader), Dynamic Linking, Sort 종합예시, Array vs Pointer, x86 비교, RISC-V Extensions(I/M/A/F/D/C), Fallacies & Pitfalls, SPEC2006 명령어 빈도

**R-type 인코딩 예시**: add x9,x20,x21 → 0000000|10101|10100|000|01001|0110011 = 0x015A04B3

**if-else 예시**: bne x22,x23,Else / add x19,x20,x21 / beq x0,x0,Exit / Else: sub / Exit:

**Factorial 예시**: sp-=16, sd x1/x10, base→return 1, recursive→jal fact, mul x10,x10,x6

---

## ⑤ 시험 대비 체크리스트

### Ch1 계산
- [ ] CPU Time = IC × CPI × T_c
- [ ] 두 컴퓨터 speedup 계산
- [ ] Weighted average CPI (명령어 mix)
- [ ] Amdahl's Law (개선 후 시간, 달성 가능 여부)
- [ ] Power = C×V²×f (전력 절감 비율)
- [ ] Moore's Law: n년 후 트랜지스터 수
- [ ] SPEC ratio / 기하 평균
- [ ] IC Cost: yield, cost/die

### Ch1 개념
- [ ] 8 Great Ideas 나열 및 1줄 설명
- [ ] ISA vs ABI vs Implementation
- [ ] Response Time vs Throughput
- [ ] Power Wall과 멀티코어 전환 이유
- [ ] MIPS 지표의 한계

### Ch2 계산
- [ ] C → RISC-V 변환 (산술, if/else, while, 함수)
- [ ] R-type 32-bit 이진/16진 인코딩
- [ ] 배열 주소 계산 (index×8+base)
- [ ] 2's complement 부정(반전+1), sign extension
- [ ] 스택 프레임 크기와 sp 변화 추적

### Ch2 개념
- [ ] DP 1, 2, 3 의미와 적용 예
- [ ] 6가지 명령어 포맷 (R/I/S/SB/U/UJ) 용도와 필드
- [ ] Saved vs Temporary 레지스터 규약
- [ ] Leaf vs Non-leaf (ra 저장 여부)
- [ ] Memory Layout (Text/Static/Heap/Stack)
- [ ] lr.d/sc.d 동기화 원리
- [ ] Static vs Dynamic linking
- [ ] Stored Program Concept
- [ ] Little Endian
- [ ] lb vs lbu, blt vs bltu
