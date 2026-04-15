# 컴퓨터구조 Knowledge

> 삼성DS · COD (Computer Organization & Design) RISC-V
> 최종 업데이트: 2026-04-15 · Ch1~Ch4

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
| `TCO = CAPEX + OPEX` | 총 소유 비용 | CAPEX=초기 투자, OPEX=운영 비용 | perf/TCO로 실질 가성비 평가 |
| `perf/TCO` | TCO 단위당 성능 | perf=성능(throughput 등), TCO=총 소유 비용 | 높을수록 가성비 좋음 |
| `FP값 = (-1)^S × (1+Frac) × 2^(Exp-Bias)` | IEEE 754 부동소수점 값 | S=부호, Frac=소수부, Exp=지수, Bias=127(single)/1023(double) | 정규화 기준, hidden bit=1 |
| `Single range: ±1.2×10⁻³⁸ ~ ±3.4×10³⁸` | 단정밀도 범위 | 정밀도 ~6자리 십진수 (2⁻²³) | Exp 8bit, Frac 23bit |
| `Double range: ±2.2×10⁻³⁰⁸ ~ ±1.8×10³⁰⁸` | 배정밀도 범위 | 정밀도 ~16자리 십진수 (2⁻⁵²) | Exp 11bit, Frac 52bit |
| `Speedup_pipeline ≈ Stages` (이상적) | 파이프라인 이상적 속도 향상 | Stages=파이프라인 단계 수 | 균형 잡힌 경우. 불균형 시 더 적음 |
| `IPC = 1/CPI` | 사이클당 명령어 수 | Multiple issue에서 CPI<1일 때 사용 | peak IPC=issue width |

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
| CAPEX vs OPEX | 초기 투자비(서버·장비 구매) | 운영비(전력·냉각·인건비·유지보수) | TCO=CAPEX+OPEX. 데이터센터에서 OPEX(특히 전력)가 TCO의 상당 부분 차지 |
| Single vs Double precision | 32-bit(S1+Exp8+Frac23), Bias=127 | 64-bit(S1+Exp11+Frac52), Bias=1023 | Single:~6자리/Double:~16자리 십진. 범위와 정밀도 트레이드오프 |
| FP 덧셈 vs FP 곱셈 | 지수 정렬→가수 덧셈→정규화→반올림 | 지수 덧셈→가수 곱셈→정규화→반올림→부호결정 | 덧셈: 지수 맞춤이 핵심. 곱셈: 지수끼리 더하고 가수끼리 곱함 |
| Restoring vs Non-restoring div | 음수 나머지 시 divisor 다시 더함 | 다음 단계에서 보정 | Restoring이 더 단순, Non-restoring이 더 빠름 |
| Guard/Round/Sticky bits | 추가 정밀도 비트 | | 정확한 반올림을 위한 IEEE 754 메커니즘 |
| Integer regs vs FP regs | x0~x31 (32×64-bit) | f0~f31 (32×64-bit) | 별도 레지스터 파일. FP 명령어는 FP 레지스터만 사용 |
| Single-cycle vs Pipelined | 한 사이클에 명령어 완료, T_c=최긴 경로 | 5 stage 중첩, T_c=최긴 stage | Pipelined: throughput↑, latency 동일 |
| Forwarding vs Stalling | 결과를 즉시 전달(bypass) | 1+cycle 대기(bubble 삽입) | Forwarding이 성능↑. Load-use는 stall 불가피 |
| Static vs Dynamic branch pred | 컴파일러가 방향 예측(backward taken 등) | HW가 BHT로 런타임 예측(1-bit,2-bit) | Dynamic이 정확도↑, HW 복잡도↑ |
| Static vs Dynamic multiple issue | 컴파일러가 issue slot 패킹(VLIW) | CPU가 런타임에 발행 결정(Superscalar) | Static: 컴파일러 의존. Dynamic: HW 복잡↑, OoO 가능 |
| In-order vs Out-of-order | 프로그램 순서대로 실행 (A53) | 의존성 없으면 먼저 실행 (i7) | OoO: 성능↑ 전력↑ 복잡도↑ |
| Exception vs Interrupt | CPU 내부 발생(opcode,overflow,syscall) | 외부 I/O 컨트롤러 | 처리 메커니즘 유사: SEPC/SCAUSE 저장→handler |
| ARM A53 vs Intel i7 | PMD, 100mW, 8-stage in-order | Server, 130W, 14-stage OoO+speculation | 전력효율 vs 절대성능 |

---

## ③ 용어 정의

| 용어 | 정의 |
|------|------|
| ABI | ISA + 시스템SW 인터페이스. 같은 ISA라도 OS 다르면 ABI 다를 수 있음 |
| Abstraction | 하위 세부사항을 숨기고 단순 인터페이스만 노출하는 설계 원칙 |
| Amdahl's Law | 부분 개선이 전체 성능에 비례하지 않음. T=T_affected/n + T_unaffected |
| Basic Block | 중간에 분기 없고 분기대상도 처음뿐인 명령어 시퀀스. 최적화 기본 단위 |
| Cache Memory | CPU 내/근처 소형 고속 SRAM. 메인메모리 접근 지연 감소 |
| CAPEX (Capital Expenditure) | 자본적 지출. 서버·장비·인프라 등 초기 구매/구축 비용. 일회성 투자 |
| CISC | 복잡·다양·가변길이 명령어. x86 대표 |
| CPI | 명령어당 평균 클럭 사이클. CPU HW와 명령어 mix에 의해 결정 |
| Datapath | 프로세서 내부 데이터 연산 유닛 (ALU, 레지스터) |
| Denormal Number | Exponent=0일 때 hidden bit=0. 정규화 수보다 더 작은 값 표현. Gradual underflow 허용 |
| Control | 명령어 해석(decode) → Datapath에 제어 신호 |
| Design Principle 1 | Simplicity favors regularity |
| Design Principle 2 | Smaller is faster |
| Design Principle 3 | Good design demands good compromises |
| Dynamic Linking | 호출 시점에만 라이브러리 로드. Lazy Linkage |
| Exception | CPU 내부에서 발생하는 예외(undefined opcode, overflow, syscall). SEPC/SCAUSE에 기록 후 handler로 점프 |
| Forwarding (Bypassing) | 파이프라인에서 결과가 나오면 레지스터 write 전에 바로 다음 명령어 입력으로 전달. Data hazard 해결 |
| Hazard | 파이프라인에서 다음 명령어를 즉시 시작하지 못하게 하는 상황. Structural/Data/Control 3종류 |
| IC (Instruction Count) | 프로그램 실행 시 총 명령어 수 |
| IEEE 754 | 부동소수점 표현 및 연산의 국제 표준. Single(32-bit), Double(64-bit). Bias, hidden bit, 특수값(±0, ±Inf, NaN, Denormal) 정의 |
| Infinity (±∞) | Exp=111...1, Frac=000...0. 오버플로우 시 사용. 후속 계산에 전파 가능 |
| ISA | HW/SW 인터페이스. 프로세서가 이해하는 명령어 집합 정의 |
| ILP (Instruction-Level Parallelism) | 파이프라인/다중 발행으로 여러 명령어를 동시 실행하는 병렬성 |
| IPC (Instructions Per Cycle) | 사이클당 명령어 수. CPI<1일 때(multiple issue) 사용. IPC=1/CPI |
| Little Endian | 최하위 바이트가 가장 낮은 주소. RISC-V 사용 |
| lr.d / sc.d | Load Reserved / Store Conditional. 동기화용 atomic 쌍 |
| lui | 20-bit 상수를 rd[31:12]에 로드, sign extend, [11:0]=0 |
| Moore's Law | IC 트랜지스터 수 약 2년마다 2배. 경험적 관찰(물리법칙 아님) |
| NaN (Not a Number) | Exp=111...1, Frac≠0. 0/0 등 정의되지 않은 결과. 후속 계산에 전파 |
| OPEX (Operating Expenditure) | 운영 지출. 전력·냉각·인건비·유지보수·네트워크 등 지속적 비용. 데이터센터에서 전력이 OPEX의 핵심 |
| Overflow | 연산 결과가 표현 가능 범위 초과. 정수: 부호 반전으로 감지. FP: Infinity로 처리 |
| Power Wall | 전압/발열 한계로 클럭 향상 불가 → 멀티코어 전환 |
| Pipeline | 명령어 실행을 여러 stage로 나누어 중첩 실행. Throughput↑, Latency 동일 |
| Pipeline Register | 각 stage 사이의 레지스터. 이전 cycle 정보 보존 (IF/ID, ID/EX, EX/MEM, MEM/WB) |
| R/I/S/SB/U/UJ-type | RISC-V 6가지 32-bit 고정길이 명령어 포맷 |
| RISC-V | UC Berkeley 개발 오픈 RISC ISA. 이 과목 기준 ISA |
| Saturating Operation | 오버플로우 시 wrap-around 대신 최대/최소값으로 고정. 오디오/비디오 처리에 사용 |
| SIMD | Single Instruction Multiple Data. 하나의 명령어로 여러 데이터를 동시 처리. SSE/AVX가 대표적 |
| Sign Extension | 넓은 비트 확장 시 부호비트 복제. lb(sign), lbu(zero) |
| SPEC | Standard Performance Evaluation Corp. 기하평균 벤치마크 |
| Stored Program | 명령어도 이진수로 메모리 저장. 프로그램이 프로그램 조작 가능 |
| Superscalar | Dynamic multiple issue. CPU가 런타임에 사이클당 여러 명령어 발행. OoO 실행 가능 |
| Speculation | 분기 결과 등을 예측하여 미리 실행. 맞으면 commit, 틀리면 flush+rollback |
| TCO (Total Cost of Ownership) | 총 소유 비용 = CAPEX + OPEX. 시스템의 전체 수명 동안 발생하는 모든 비용. 성능 평가 시 단순 구매가가 아닌 TCO 기준이 실질적 |
| perf/TCO | TCO 단위당 성능. 실질적 가성비 지표. 전력 효율이 좋은 시스템은 OPEX↓→TCO↓→perf/TCO↑ |
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

#### 1-추가. perf/TCO — 실질적 가성비 지표

컴퓨터 시스템의 가치를 평가할 때, 단순히 "성능(perf)"이나 "구매 가격"만 보면 안 된다. 실질적 가성비는 **perf/TCO**(총 소유 비용 대비 성능)로 평가한다.

**TCO (Total Cost of Ownership) = CAPEX + OPEX**

- **CAPEX (Capital Expenditure, 자본적 지출)**: 시스템을 도입할 때 발생하는 초기 투자 비용. 서버 구매비, 장비비, 인프라 구축비, 라이선스 비용 등. 일회성.

- **OPEX (Operating Expenditure, 운영 지출)**: 시스템을 운영하는 동안 지속적으로 발생하는 비용. 전력 비용, 냉각 비용, 인건비(관리/유지보수), 네트워크 비용, 소프트웨어 유지보수 등.

**왜 perf/TCO가 중요한가?**

데이터센터에서는 서버 구매비(CAPEX)보다 **전력+냉각(OPEX)**이 TCO의 상당 부분을 차지한다. 따라서:
- 저전력 프로세서는 OPEX↓ → TCO↓ → perf/TCO↑ (가성비 향상)
- 비싼 고성능 서버라도 전력 효율이 좋으면 perf/TCO가 더 높을 수 있음
- Google이 10-50% 부하에서 주로 운영 → idle 전력이 OPEX에 큰 영향 → Energy Proportionality 문제와 직결

이것이 Ch1의 Power Wall, SPECpower 벤치마크, Energy Proportionality 논의와 직결된다.

```
perf/TCO ↑ 전략:
  ├─ perf ↑: 더 빠른 프로세서, 병렬화, 캐시 최적화
  └─ TCO ↓:
      ├─ CAPEX ↓: 저렴한 HW, 효율적 설계
      └─ OPEX ↓: 저전력(P=CV²f↓), 효율적 냉각, 자동화
```

### Chapter 2: Instructions — Language of the Computer

(이전 채팅에서 상세 정리 완료 — 95 slides 전체 반영)

핵심 토픽: Instruction Set 개념, RISC-V 소개, 산술 연산(3-오퍼랜드), DP1/2/3, 레지스터(32×64b), 메모리 오퍼랜드(ld/sd, Little Endian, byte addressing), 즉시값(addi), 부호(2's complement, sign extension), 6가지 명령어 포맷(R/I/S/SB/U/UJ), 논리연산(sll/srl/and/or/xor), 분기(beq/bne/blt/bge/bltu/bgeu), 프로시저(jal/jalr, 스택, leaf/non-leaf, 재귀 fact), Memory Layout, 문자 데이터(ASCII/Unicode, lb/lbu/sb), 32-bit 상수(lui+addi), Branch/Jump addressing(PC-relative), 동기화(lr.d/sc.d), 번역 과정(Compiler→Assembler→Linker→Loader), Dynamic Linking, Sort 종합예시, Array vs Pointer, x86 비교, RISC-V Extensions(I/M/A/F/D/C), Fallacies & Pitfalls, SPEC2006 명령어 빈도

**R-type 인코딩 예시**: add x9,x20,x21 → 0000000|10101|10100|000|01001|0110011 = 0x015A04B3

**if-else 예시**: bne x22,x23,Else / add x19,x20,x21 / beq x0,x0,Exit / Else: sub / Exit:

**Factorial 예시**: sp-=16, sd x1/x10, base→return 1, recursive→jal fact, mul x10,x10,x6

### Chapter 3: Arithmetic for Computers

(이전 채팅에서 상세 정리 완료 — 52 slides 전체 반영)

핵심 토픽: 정수 덧셈/뺄셈 오버플로우 조건, 곱셈 하드웨어(long multiplication, optimized, faster multiplier), 나눗셈(restoring division, SRT), RISC-V mul/mulh/div/rem 명령어, IEEE 754 부동소수점(Single/Double, Bias, hidden bit, Denormal, ±Inf, NaN), FP 덧셈 4단계(정렬→덧셈→정규화→반올림), FP 곱셈 5단계(지수 덧셈→가수 곱셈→정규화→반올림→부호), FP Adder HW(4-stage pipeline), RISC-V FP 레지스터(f0~f31) 및 명령어(fadd.d/fmul.d/fld/fsd/feq.d 등), Guard/Round/Sticky bits, SIMD/Subword Parallelism, SSE2/AVX, Saturating operation, FP Associativity 불성립

**FP 변환 예시**: -0.75 = (-1)¹ × 1.1₂ × 2⁻¹ → S=1, Frac=100...0, Exp=-1+127=126=01111110₂

**오버플로우 조건**: 양수+양수→결과 음수, 음수+음수→결과 양수이면 overflow. 부호가 다른 피연산자끼리는 overflow 불가

**FP 덧셈**: Step1 지수정렬 → Step2 가수덧셈 → Step3 정규화 → Step4 반올림
**FP 곱셈**: Step1 지수덧셈 → Step2 가수곱셈 → Step3 정규화 → Step4 반올림 → Step5 부호결정

### Chapter 4: The Processor

(이전 채팅에서 상세 정리 완료 — 129 slides 전체 반영)

핵심 토픽: Logic Design(조합/순차, clocking methodology), Single-cycle Datapath(IF→ID→EX→MEM→WB, critical path=ld), ALU Control(ALUOp+funct→ALU control), 5-Stage Pipeline(IF/ID/EX/MEM/WB, throughput↑ latency 동일, Speedup≈stages), Pipeline Registers(IF/ID, ID/EX, EX/MEM, MEM/WB), Hazards 3종(Structural→메모리분리, Data→Forwarding/Stall, Control→Branch Prediction), Forwarding 감지 조건(EX/MEM.Rd=ID/EX.Rs1등), Load-Use Hazard(stall+bubble, code scheduling으로 회피), Branch Prediction(static/dynamic, 1-bit/2-bit, BTB), Exception/Interrupt(SEPC/SCAUSE, flush, handler), ILP(Deeper pipeline, Multiple issue), Static issue(VLIW, dual-issue), Dynamic issue(Superscalar, OoO, Reservation Station, Reorder Buffer), Speculation(branch/load), Loop Unrolling+Register Renaming, ARM A53(in-order 100mW) vs i7(OoO 130W)

**Pipeline performance**: Single-cycle T_c=800ps vs Pipelined T_c=200ps → 4× speedup

**Forwarding 조건**: EX hazard: EX/MEM.Rd = ID/EX.Rs1 or Rs2 (Rd≠0, RegWrite=1). MEM hazard: MEM/WB.Rd = ID/EX.Rs1 or Rs2 (EX hazard 아닐 때만)

**Load-Use stall**: ID/EX.MemRead AND (ID/EX.Rd = IF/ID.Rs1 or Rs2) → bubble

**Code scheduling 예시**: ld 사이에 독립 명령어 끼워 stall 제거 (13→11 cycles)

**Dual-issue scheduling**: IPC=5/4=1.25. Loop unrolling(4×) 후 IPC=14/8=1.75

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
### Ch3 계산
- [ ] 십진/이진 수를 IEEE 754 single/double로 변환 (S, Exp, Frac)
- [ ] IEEE 754 비트 패턴을 십진수로 역변환
- [ ] FP 덧셈 4단계 수동 계산 (정렬→덧셈→정규화→반올림)
- [ ] FP 곱셈 5단계 수동 계산
- [ ] 정수 오버플로우 판별 (부호 조합별)
- [ ] 이진 long multiplication 수동 계산
- [ ] mulh로 64-bit 오버플로우 검출 방법

### Ch3 개념
- [ ] IEEE 754 포맷: S, Exponent, Fraction, Bias, hidden bit
- [ ] Single vs Double 범위/정밀도 차이
- [ ] Denormal, ±Infinity, NaN의 의미와 비트 패턴
- [ ] 정수 오버플로우 조건 (양+양→음, 음+음→양)
- [ ] 곱셈 HW: 기본→optimized→faster 구조
- [ ] 나눗셈이 곱셈보다 병렬화 어려운 이유 (conditional subtraction)
- [ ] FP 덧셈 vs FP 곱셈 절차 차이
- [ ] Guard/Round/Sticky bits의 역할
- [ ] SIMD/Subword parallelism 개념
- [ ] FP associativity 불성립과 병렬 프로그램 영향
- [ ] RISC-V FP 레지스터(f0~f31)와 정수 레지스터 분리
- [ ] Arithmetic right shift ≠ signed division (음수에서 차이)

### Ch4 계산
- [ ] Single-cycle vs Pipelined 성능 비교 (T_c, throughput, speedup)
- [ ] 파이프라인 타이밍 다이어그램 그리기 (multi-cycle diagram)
- [ ] Forwarding 필요 여부 판별 (EX/MEM, MEM/WB hazard 조건)
- [ ] Load-use hazard 감지 및 stall 후 cycle 수 계산
- [ ] Code scheduling으로 stall 제거 (명령어 재배치)
- [ ] Dual-issue 스케줄링 및 IPC 계산
- [ ] Loop unrolling 후 IPC 계산
- [ ] Branch misprediction penalty 계산

### Ch4 개념
- [ ] 5-stage pipeline 각 단계(IF/ID/EX/MEM/WB) 역할
- [ ] Pipeline이 throughput↑이지 latency↓가 아닌 이유
- [ ] 3가지 Hazard(Structural/Data/Control) 정의와 해결책
- [ ] Forwarding(Bypassing) 원리와 한계(load-use)
- [ ] Load-use stall 감지 조건과 bubble 삽입 메커니즘
- [ ] Branch prediction: static vs dynamic, 1-bit vs 2-bit, BTB
- [ ] Exception vs Interrupt, SEPC/SCAUSE, precise exception
- [ ] Static multiple issue(VLIW) vs Dynamic(Superscalar)
- [ ] Out-of-order execution: Reservation Station, Reorder Buffer
- [ ] Speculation 원리와 rollback
- [ ] RISC-V ISA가 파이프라인에 유리한 이유 (32-bit 고정, 규칙적 포맷)
- [ ] Critical path가 clock period를 결정하는 원리
