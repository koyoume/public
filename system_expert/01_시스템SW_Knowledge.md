# 시스템 SW - 학습 누적 정리

> 이 문서는 수업 후 정리된 내용을 누적하는 Knowledge 문서입니다.
> ★ = 시험 출제 가능성 높음 / 마지막 업데이트: 2026-03-18

---

## 시스템 프로그래밍

### Ch1. Introduction — Five Great Realities
- **Reality #1** Int ≠ Integer, Float ≠ Real → 유한 비트 표현 → 오버플로우, 결합법칙 위반
- **Reality #2** 어셈블리 이해 필수 → 버그 분석, 컴파일러 최적화, 역공학
- **Reality #3** 메모리는 유한 자원 → 공간적/시간적 참조 오류 → C는 보호 없음
- **Reality #4** 성능 ≠ 점근 복잡도만 → 메모리 접근 패턴이 결정 (copyij 4.3ms vs copyji 81.8ms)
- **Reality #5** I/O·네트워크도 시스템의 일부
- 과목 관점: Programmer-Centric (추상화 아래 현실을 이해)

---

### Ch2. Machine-Level Programming

#### Part I: Basics
- **ISA** (Instruction Set Architecture) = 프로그래머 가시 상태 정의
- **Microarchitecture** = ISA 구현체 (캐시, 파이프라인 — 프로그래머에게 비가시)
- **Programmer-Visible State**: PC(%rip), 레지스터 파일, Condition Codes, Memory
- **x86-64 레지스터**: %rax(반환), %rdi~%r9(인자), %rsp(스택), %rbp(프레임), %rbx/%r12~%r14(callee-saved)
- **Operand 타입 3가지**: Immediate($), Register(%), Memory(())
- ★ **Mem→Mem 직접 이동 불가** (단일 명령어)
- **주소 지정**: D(Rb, Ri, S) → Mem[Reg[Rb] + S×Reg[Ri] + D]
- **leaq**: 메모리 읽지 않고 주소값 계산 → 포인터 연산 & 곱셈 최적화
- **AT&T 문법**: op Src, Dest (Intel과 반대)
- **컴파일 파이프라인**: .c → (Compiler) → .s → (Assembler) → .o → (Linker) → 실행파일

#### Part II: Control
- **Condition Codes (4개)**: CF(unsigned overflow), ZF(결과=0), SF(결과<0), OF(signed overflow)
- **설정 방법**: 산술연산(암묵적) / cmpq(a-b, 저장 안함) / testq(a&b, 저장 안함)
- ★ **cmpq 순서**: cmpq Src2, Src1 → Src1-Src2
- **조건 점프**: signed(jg/jl/jge/jle) vs unsigned(ja/jb)
- ★ **루프 변환 패턴**:
  - do-while: body → if(Test) goto loop
  - while: goto test → body → if(Test) goto loop (Jump-to-Middle)
  - for: Init + while 패턴
- 컴파일러는 모든 루프를 goto + 조건 점프로 변환

#### Part III: Procedures
- **스택**: 높은→낮은 주소 방향 성장 / pushq=%rsp-=8 / popq=%rsp+=8
- ★ **call**: 복귀주소 push + 점프 / **ret**: 복귀주소 pop + 점프
- ★ **인자 전달**: %rdi, %rsi, %rdx, %rcx, %r8, %r9 (7번째~: 스택) / 반환: %rax
- ★ **레지스터 저장 규칙**:
  - Caller-saved: %rax, %rcx, %rdx, %rsi, %rdi, %r8~%r11 (callee가 자유롭게 사용)
  - Callee-saved: %rbx, %r12~%r14, %rbp (사용 전 push, 반환 전 pop)
- **스택 프레임 구조** (위→아래): 반환주소 / saved registers / 지역변수 / 인자 빌드 공간

---

### Ch3. Stack Buffer Overflow
- **메모리 레이아웃** (낮은→높은): Text → Data → Heap(↑) → Shared Libs → Stack(↓)
- **Buffer Overflow**: 배열 경계 초과 쓰기 → 인접 메모리 오염
- ★ **스택 구조**: char name[32] = rbp-0x20 → name+32=saved rbp → name+40=RET ADDR
- ★ **공격 방법 3가지**:
  1. Return Address Overwrite: RET ADDR → 원하는 함수 주소
  2. Code Injection: 버퍼에 악성 코드 + RET ADDR → 버퍼 주소
  3. ROP: 기존 코드의 Gadget(ret으로 끝나는 명령 시퀀스) 조합
- ★ **방어 기법**:
  1. 안전한 코딩: gets→fgets, strcpy→strncpy
  2. ASLR: 스택/힙/라이브러리 주소 랜덤화
  3. NX Bit: 스택 non-executable → Code Injection 무력화
  4. Stack Canary(-fstack-protector): 버퍼~RET ADDR 사이 랜덤값 → 변조 감지
- **공격-방어**: Code Injection→NX / NX우회→ROP / ROP→ASLR / 실무: 3가지 동시 적용

---

### Ch4. Memory Hierarchy
- **CPU-Memory Gap**: CPU 속도 >> 메모리 속도 → 격차 심화
- ★ **지역성 (Locality)**:
  - 시간적(Temporal): 최근 참조 → 곧 다시 참조 (예: 루프 변수)
  - 공간적(Spatial): 인접 주소 → 곧 참조 (예: 배열 순차 접근)
- **Row-Major Order**: C 2D 배열은 행 우선 저장 → 행 우선 접근이 공간적 지역성↑
- ★ **열 우선 접근(sum_array_cols)**은 지역성 나쁨 → 성능 저하 (19배 차이)
- **메모리 계층** (L0→L6): 레지스터→L1/L2/L3 캐시(SRAM)→DRAM→SSD→HDD→원격
  - 빠를수록 비싸고 작음 / 레벨 k는 레벨 k+1의 캐시 / Cache Line = 64bytes
- **Cache Hit**: 즉시 반환 / **Cache Miss**: 하위 레벨에서 블록 fetch → Placement/Replacement Policy
- **Replacement Policy**: LRU, FIFO, Random
- **캐시 관리**: 레지스터(컴파일러) / L1~L3(하드웨어) / VM 페이지(OS+HW) / TLB(MMU)

---

### Ch5. Code Optimization & Linking

#### 컴파일러 최적화
- **목표**: 명령어 수 최소화 / 메모리 접근 최소화 / 분기 최소화
- **Local 최적화** (단일 블록): Constant Folding, Strength Reduction, Dead Code, CSE
- **Global 최적화** (함수 전체): Code Motion, Loop Unrolling, Inlining
- ★ **주요 기법**:
  - Constant Folding: `0xFF << 8` → `0xFF00`
  - Strength Reduction: `b*5` → `(b<<2)+b`
  - Dead Code Elimination: 실행 불가/불필요 코드 제거
  - CSE: 공통 부분식 한 번만 계산
  - Code Motion: 루프 불변 계산을 루프 밖으로
  - Loop Unrolling: 루프 조건 체크 횟수 감소
  - Inlining: 함수 본문을 호출 지점에 복사 (코드 크기↑ 주의)
- ★ **최적화 한계**:
  - Side Effect 함수(strlen) → 이동 불가 → O(n²) 위험
  - Signed integer overflow = Undefined Behavior → 컴파일러 임의 처리
  - 함수 단위 분석 (inter-procedure 불가)

#### 링킹
- ★ **링킹 3단계**:
  1. 심볼 테이블 구성: Global(외부 참조 가능) / Local(static) / External Reference
  2. 심볼 해석: 참조 → 정의 연결
  3. 재배치: .o 상대 주소 → 실행파일 절대 주소
- **Static Library (.a)**: ar로 묶음 / 실행파일에 코드 복사 / 재컴파일 필요
- **Dynamic Library (.so)**: 실행 시 공유 메모리 링크 / 업데이트 용이
- `ldd`: 동적 라이브러리 의존성 확인

---

### Ch6. Virtual Memory

#### VM의 3가지 역할 ★
1. **Caching**: DRAM이 디스크의 캐시 / Page(4KB) 단위 / Page Table로 관리
2. **Memory Management**: 프로세스마다 독립적 가상 주소 공간 / 공유 라이브러리 공유
3. **Memory Protection**: PTE 권한 비트(R/W, U/S, XD) / MMU가 매 접근마다 검사

#### Page Table & 주소 변환
- **PTE 필드**: P(Present), R/W, U/S(SUP), D(Dirty), A(Reference), XD(NX bit)
- **VA 구조**: VPN(Virtual Page Number) + VPO(Virtual Page Offset)
- **PA**: PPN + PPO (PPO = VPO)
- ★ **Page Hit**: PTE valid=1 → MMU가 PA 변환 후 즉시 반환
- ★ **Page Fault 처리 흐름**: 예외 → 커널 핸들러 → victim 선택 → 디스크 로드 → PTE 갱신 → iret → 재실행
- **Thrashing**: Working Set > 물리 메모리 → 페이지 교체 폭주

#### TLB & Multi-Level Page Table
- **TLB**: MMU 내부 PTE 캐시 / Hit=메모리 1회 / Miss=2회
- TLB Miss 드문 이유: 시간적 지역성
- ★ **Multi-Level PT**: 48-bit VA, 4KB 페이지 → 단일 PT=512GB 필요
  - Core i7: 4단계(VPN1~4 각 9bit + VPO 12bit) / CR3=L1 PT 물리주소

#### Memory Mapping & COW
- **mmap**: 파일/익명 메모리를 VA에 매핑 (MAP_SHARED/MAP_PRIVATE/MAP_ANON)
- **COW(Copy-on-Write)**: 쓰기 전까지 물리 페이지 공유 → Protection Fault → 새 페이지 복사
  - fork() 최적화의 핵심

---

### Ch7. Dynamic Memory Allocation

#### 기본 개념
- **Heap**: brk 포인터 / sbrk()로 확장
- **malloc**: 16-byte 정렬(x86-64) / 실패 시 NULL + errno
- **Explicit vs Implicit**: malloc/free vs GC
- ★ **단편화**:
  - Internal: 블록 > 페이로드 (정렬 패딩, 헤더)
  - External: 가용 합계 충분 but 연속 블록 부족
- **성능 목표**: 처리량↑ vs 메모리 활용률(Oₖ = maxPᵢ/Hₖ)↑ — 상충

#### 가용 블록 추적 ★
- **블록 헤더**: size | alloc_bit (최하위 비트 재활용)
- **Method 1 Implicit List**: 헤더 size로 순회 / O(전체 블록) / 구현 단순
- **Method 2 Explicit List**: free 블록에 prev/next / O(가용 블록) / 삽입: LIFO/FIFO/주소순
- **Method 3 Segregated List**: 크기 클래스별 리스트 / 처리량↑ 단편화↓ / first-fit ≈ best-fit

#### 핵심 정책
- **Placement**: First-fit / Next-fit / Best-fit
- **Splitting**: 가용 블록 분할 후 남은 부분 새 가용 블록
- **Coalescing**: free 시 인접 가용 블록 병합 / 미병합 → False Fragmentation

#### GC 알고리즘
- **Reference Counting**: count=0이면 해제 / 순환 참조 처리 불가
- **Mark & Sweep**: Root DFS → 마크 → 미마크 회수 / 순환 처리 가능 / Stop-the-world

#### 보안 취약점 ★
- **Heap Overflow**: 인접 메타데이터 오염 → prev/next 덮어쓰기 → Arbitrary Write
- **Use-After-Free**: Dangling pointer + Heap Spray → vtable 조작 → 제어 흐름 탈취
- **Double-Free**: 가용 리스트 오염 → 동일 블록 이중 반환

---

### Ch8. Exceptions (예외 처리)
- **Exception**: 이벤트 발생 시 User → OS Kernel로 제어권 이전
- **복귀 방식**: I_current 재실행 / I_next 진행 / Abort
- **Exception Table**: OS가 구성 / 예외 번호 k → 핸들러 주소 매핑

#### ★ 예외 분류 4가지
| 종류 | 원인 | 의도 | 복귀 |
|------|------|------|------|
| Interrupt | 외부 장치(비동기) | - | I_next |
| Trap | 명령어(동기) | 의도적 | I_next |
| Fault | 명령어(동기) | 비의도 | I_current or Abort |
| Abort | 명령어(동기) | 비의도 | Abort |

#### System Call (Trap의 핵심) ★
- **%rax**: syscall 번호 / **%rdi~%r9**: 인자 / **%rax**: 반환값 (음수=오류)
- 주요 번호: read(0), write(1), open(2), fork(57), execve(59), exit(60), kill(62)

---

### Ch9. Processes (프로세스)
- **정의**: 실행 중인 프로그램의 인스턴스
- **추상화**: Logical Control Flow + Private Address Space
- **Context Switch**: ① 레지스터→메모리 저장 ② 다음 프로세스 스케줄 ③ 레지스터 복원 + 주소공간 전환
- **생명주기**: Ready → Running → Waiting → Terminated

#### ★ 핵심 API
- **fork()**: 1번 호출 2번 반환 / 부모→자식PID, 자식→0 / COW로 주소공간 공유
- **exit(status)**: 0=정상, 非0=오류
- **wait(&status)**: 자식 종료 대기 + zombie 회수
- **execve(file, argv, envp)**: PID 유지, 메모리 교체 / 반환 없음
- **zombie**: 종료됐지만 wait() 안됨 → `<defunct>` / **orphan**: 부모 먼저 종료 → init(PID=1)

---

### Ch10. Signals (시그널)
- **정의**: 커널→프로세스 이벤트 알림 / ID 1~30 / 정보: ID + 도착 사실뿐

#### ★ 주요 시그널
| ID | 이름 | 기본동작 | 원인 |
|----|------|----------|------|
| 2 | SIGINT | 종료 | Ctrl-C |
| 9 | SIGKILL | 종료 | 강제종료 (재정의 불가) |
| 11 | SIGSEGV | 종료 | segfault |
| 17 | SIGCHLD | 무시 | 자식 종료 |
| 20 | SIGTSTP | 정지 | Ctrl-Z |

#### ★ 상태 & 처리
- `pnb = pending & ~blocked` → 실제 처리 / 시그널 큐 없음 → 같은 타입 최대 1개 pending
- 동일 시그널: implicit blocking / 다른 시그널: 핸들러 중첩 가능
- **안전한 핸들러**: G0(단순/플래그만) / G1(async-signal-safe: write/kill✓, printf/malloc✗) / G4(volatile) / G5(volatile sig_atomic_t)
- Shell + SIGCHLD 패턴: 백그라운드 자식 종료 → SIGCHLD → waitpid() → zombie 회수

---

### Ch11. Threads (스레드)
- **전용**: 레지스터(PC), TID, 스택 (보호 없음!) / **공유**: 코드, 전역데이터, 힙, 파일 디스크립터
- **비용**: 프로세스 ~20K cycles vs 스레드 ~10K cycles / 피어(peer) 풀 구조

#### Pthreads API ★
- `pthread_create(&tid, attr, func, arg)` / `pthread_join(tid, &retval)`
- `pthread_self()` / `pthread_exit(retval)` / `exit()` = 모든 스레드 종료

#### 3대 문제: Race / Deadlock / Starvation

---

### Ch12. Synchronization (동기화)

#### 공유 변수 & Race ★
- 전역변수/지역static: 공유 / 지역변수: 비공유
- `cnt++` = L-U-S 3단계 → 인터리빙 시 Race
- Critical Section / Unsafe Region / Progress Graph

#### Mutex & Semaphore ★
- **Mutex**: lock/unlock / test_and_set으로 구현 (원자적)
- **Semaphore**: wait(P: s--) + post(V: s++) / s≥0 불변 / binary(초기=1)=mutex

#### Producer-Consumer ★
- 1-elem: empty(초기=1) + full(초기=0)
- n-elem: mutex + empty_slots(초기=n) + full_slots(초기=0) + 원형 버퍼

#### Readers-Writers ★
- readcnt + mutex + w / 첫 독자→writer 차단, 마지막→해제 / Writer Starvation 가능

#### Deadlock ★
- 4조건: Mutual Exclusion + Hold&Wait + No Preemption + Circular Wait
- 회피: 모든 스레드 동일 순서로 락 획득

#### Thread Safety ★
- Class1: 공유변수 비보호 / Class2: static 상태(→인자로 전달) / Class3: unsafe 호출
- Reentrant ⊂ Thread-safe

#### Memory Consistency
- Sequential Consistency > TSO(x86, store buffer) > Weak Ordering(ARM)

---

### Ch13. System-Level I/O
- 모든 것은 파일 / 파일 타입: Regular / Directory / Socket

#### Unix I/O ★
- `open/close/read/write/lseek` / 기본 fd: 0(stdin), 1(stdout), 2(stderr)
- **Short count**: EOF / 터미널 / 소켓 → 정상! 항상 처리할 것
- double-close = double-free처럼 위험

#### 커널 파일 구조 ★
- Descriptor Table → Open File Table(file pos + refcnt) → v-node Table
- fork() 후: refcnt+1, 부모/자식이 동일 file pos 공유

#### I/O 리다이렉션 ★
- `dup2(oldfd, newfd)`: newfd를 oldfd 복사본으로 교체
- `ls > foo.txt`: fork → open=3 → dup2(3,1) → close(3) → execve(ls)

#### I/O 계층 선택 ★
| 상황 | 권장 |
|------|------|
| 디스크/터미널 | Standard I/O |
| 시그널 핸들러 | Unix I/O (async-signal-safe) |
| 네트워크 소켓 | RIO |
- Standard I/O 버퍼 flush: `\n` / `fflush()` / `exit()` / main() return

---

## 과목 간 연결 포인트
- Virtual Memory ↔ Process: fork()=COW / execve()=새 페이지 테이블
- Exception ↔ Signal: Page Fault(Fault) → SIGSEGV(Signal)
- Stack Overflow ↔ VM: NX Bit = PTE의 XD 비트
- malloc ↔ VM: sbrk()로 Heap 확장 = brk 포인터 이동
- I/O Redirection ↔ fd 테이블: dup2()로 엔트리 교체
- Thread Safety ↔ Signal: async-signal-safe ⊂ reentrant
- Deadlock 회피 ↔ Circular Wait 조건: 동일 락 순서

---

## 시험 대비 핵심 요약

### ★★ 최우선 암기 항목
1. 예외 분류 4가지 (Interrupt/Trap/Fault/Abort) + 복귀 위치
2. System Call 레지스터 규약 (%rax 번호, %rdi~%r9 인자)
3. fork() 반환값 (부모=자식PID, 자식=0) + COW
4. 인자 전달 레지스터 순서 (rdi/rsi/rdx/rcx/r8/r9)
5. Caller/Callee-saved 레지스터 구분
6. Semaphore wait/post 동작 + 불변 조건(s≥0)
7. Deadlock 4조건 + 회피 방법
8. Page Fault 처리 흐름 7단계
9. Stack Canary / ASLR / NX Bit 역할 구분
10. Segregated Free List 동작 원리

### ★ 자주 출제되는 분석 문제
- fork() 후 출력 순서 분석 (Process Graph)
- cnt++ Race Condition 분석 (L-U-S 인터리빙)
- 스택 프레임 레이아웃 그리기
- dup2() 후 파일 디스크립터 상태 분석
- 세마포어 Producer-Consumer 흐름 추적

---

## 오답 & 취약 영역
<!-- 모의 시험에서 틀린 문제, 약한 개념 추적 -->
