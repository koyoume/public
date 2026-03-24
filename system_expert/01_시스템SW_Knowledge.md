# 시스템 프로그래밍 — 오픈북 시험 최적화 정리

> 마지막 업데이트: 2026-03-24 | Ch1~Ch15 수록 | ★ = 시험 출제 가능성 높음

---

## ① 수식 모음

| 수식 | 의미 | 사용 챕터 |
|------|------|-----------|
| `pnb = pending & ~blocked` | 실제 수신할 시그널 집합 | Ch10 Signal |
| `Oₖ = max(Pᵢ, i≤k) / Hₖ` | 메모리 오버헤드 (1에 가까울수록 좋음) | Ch7 malloc |
| `D(Rb, Ri, S)` → `Mem[Reg[Rb] + S×Reg[Ri] + D]` | 메모리 주소 지정 일반형 | Ch2 Basics |
| `VA = VPN + VPO` → `PA = PPN + PPO` (PPO=VPO) | 가상→물리 주소 변환 | Ch6 VM |
| `2⁴⁸ × 2⁻¹² × 2³ = 2³⁹ bytes = 512GB` | 단일 페이지 테이블 크기 (48-bit VA, 4KB page, 8B PTE) | Ch6 VM |
| `pushq` = `%rsp -= 8` → store | 스택 push 동작 | Ch2 Procedures |
| `popq` = load → `%rsp += 8` | 스택 pop 동작 | Ch2 Procedures |

---

## ② 핵심 비교표

### 예외 분류 4가지 ★

| 종류 | 발생 원인 | 동기/비동기 | 의도성 | 복귀 위치 | 예시 |
|------|-----------|-------------|--------|-----------|------|
| **Interrupt** | 외부 장치 | 비동기 | - | I_next | 타이머, Ctrl-C, NIC |
| **Trap** | 명령어 실행 | 동기 | 의도적 | I_next | syscall, gdb breakpoint |
| **Fault** | 명령어 실행 | 동기 | 비의도 | I_current or Abort | Page Fault, Protection Fault |
| **Abort** | 명령어 실행 | 동기 | 비의도 | Abort | 불법 명령어, Parity Error |

### 레지스터 저장 규칙 ★

| 구분 | 레지스터 | 저장 책임 | 의미 |
|------|----------|-----------|------|
| **Caller-saved** | %rax, %rcx, %rdx, %rsi, %rdi, %r8~%r11 | 호출자(Caller) | Callee가 자유롭게 덮어씀 |
| **Callee-saved** | %rbx, %r12~%r14, %rbp | 피호출자(Callee) | 사용 전 push, 반환 전 pop 필수 |
| **특수** | %rsp | 별도 규칙 | 항상 스택 top |

### 인자 전달 레지스터 순서 ★

| 순서 | 1 | 2 | 3 | 4 | 5 | 6 | 7번째~ |
|------|---|---|---|---|---|---|--------|
| **레지스터** | %rdi | %rsi | %rdx | %rcx | %r8 | %r9 | 스택 |
| **반환값** | %rax | | | | | | |

### 프로세스 vs 스레드 ★

| 항목 | 프로세스 | 스레드 |
|------|----------|--------|
| 주소 공간 | 독립 | 공유 |
| 생성 비용 | ~20K cycles | ~10K cycles |
| 통신 방법 | IPC (파이프/소켓) | 공유 메모리 직접 접근 |
| 스택 보호 | VM으로 격리 | 보호 없음 (다른 스레드 접근 가능) |
| 계층 구조 | 트리 (parent-child) | 피어(peer) 풀 |
| 스택/레지스터 | 독립 | 독립 (스레드별 전용) |
| 코드/데이터/힙 | 독립 | 공유 |

### I/O 함수 계층 선택 가이드 ★

| 상황 | 권장 함수 | 이유 |
|------|-----------|------|
| 디스크/터미널 파일 | Standard I/O (fopen/fprintf 등) | 버퍼링, Short count 자동 처리 |
| 시그널 핸들러 내부 | Unix I/O (read/write) | async-signal-safe |
| 네트워크 소켓 | RIO | Short count 처리 + 소켓 호환 |
| 최고 성능 필요 | Unix I/O | 최소 오버헤드 |
| Standard I/O를 소켓에 | ❌ 사용 금지 | 소켓과 스트림 제약 충돌 |

### malloc 가용 블록 추적 방법 비교 ★

| 방법 | 구조 | 할당 시간 | 장점 | 단점 |
|------|------|-----------|------|------|
| Implicit List | 헤더 size로 순회 | O(전체 블록) | 구현 단순 | 느림 |
| Explicit List | free 블록에 prev/next | O(가용 블록) | 빠름 | 최소 블록 크기↑ |
| Segregated List | 크기 클래스별 리스트 | O(1) 근사 | 처리량↑ 단편화↓ | 복잡 |

### Stack Buffer Overflow 공격-방어 대응 ★

| 공격 기법 | 방어 기법 | 원리 |
|-----------|-----------|------|
| Code Injection | NX Bit | 스택을 non-executable로 마킹 |
| NX 우회 | ROP | 기존 코드 Gadget 조합 |
| ROP | ASLR | 주소 랜덤화로 예측 불가 |
| 모든 오버플로우 | Stack Canary | 변조 감지 후 중단 |

### GC 알고리즘 비교

| 항목 | Reference Counting | Mark & Sweep |
|------|--------------------|--------------|
| 해제 시점 | count = 0 즉시 | Stop-the-world 후 일괄 |
| 순환 참조 | ❌ 처리 불가 | ✓ 처리 가능 |
| 시간 오버헤드 | 중간 (count 관리) | 높음 (전체 탐색) |
| 사용 | Chrome/Firefox C++ | Java, Python, Go |

### Memory Consistency Model 비교

| 모델 | 채택 | 특징 | 재정렬 허용 |
|------|------|------|-------------|
| Sequential Consistency | (이론) | 가장 강력, 직관적 | 없음 |
| TSO (Total Store Ordering) | x86 | store buffer 허용 | Store→Load |
| Weak Ordering | ARM | 거의 모든 재정렬 허용 | 대부분 |


### Security Attacks 비교 ★

| 공격 | 대상 | 원리 | 특징 | 대응책 |
|------|------|------|------|--------|
| **Cold Boot** | DRAM 암호화 키 | 냉각으로 데이터 소멸 지연 | 물리 접근 필요 | TRESOR(레지스터에만 키) |
| **Timing Side-Channel** | 비밀 정보 | 실행 시간 차이 측정 | 소프트웨어 취약점 | Constant-time 구현 |
| **Cache Side-Channel** | 메모리 접근 패턴 | Flush+Reload 시간 측정 | 원격 가능 | 캐시 파티셔닝 |
| **Meltdown** | 커널 메모리 | Speculative Exec + 캐시 채널 | 하드웨어 설계 결함 | KPTI |
| **Rowhammer** | DRAM 비트 | 인접 Row 반복 접근 | 버그 없이 공격 가능 | ECC DRAM, TRR |

### Meltdown vs Rowhammer ★

| 항목 | Meltdown | Rowhammer |
|------|----------|-----------|
| 공격 레이어 | CPU (투기적 실행) | DRAM (물리적 비트 플립) |
| 필요 조건 | 코드 실행 권한 | 메모리 할당 권한 |
| 정보 유출 | 커널 메모리 읽기 | PTE 변조 → 권한 상승 |
| 소프트웨어 버그 | 불필요 (HW 설계 결함) | 불필요 (HW 물리 결함) |
| 대응 | KPTI (SW 패치) | ECC DRAM (HW 교체) |

### Breakpoint 3종류 비교 ★

| 종류 | 구현 방식 | 개수 제한 | 코드 수정 | 용도 |
|------|-----------|-----------|-----------|------|
| **Software** | `int 3` (0xcc) 삽입 → SIGTRAP | 무제한 | 필요 | 실행 흐름 중단 |
| **Hardware** | CPU DR0~DR3 레지스터 | 최대 4개 | 불필요 | 실행 흐름 중단 |
| **Memory** | 페이지 권한 변경 → Protection Fault | 제한적 | 불필요 | 메모리 접근 감지 |


### 주요 시그널 ★

| ID | 이름 | 기본 동작 | 발생 원인 | 재정의 가능 |
|----|------|-----------|-----------|-------------|
| 2 | SIGINT | 종료 | Ctrl-C | ✓ |
| 9 | SIGKILL | 종료 | 강제 종료 | ❌ |
| 11 | SIGSEGV | 종료 | Segmentation Fault | ✓ |
| 14 | SIGALRM | 종료 | 타이머 만료 | ✓ |
| 17 | SIGCHLD | 무시 | 자식 프로세스 종료 | ✓ |
| 20 | SIGTSTP | 정지 | Ctrl-Z | ✓ |

### System Call 주요 번호 ★

| 번호 | 이름 | 설명 |
|------|------|------|
| 0 | read | 파일 읽기 |
| 1 | write | 파일 쓰기 |
| 2 | open | 파일 열기 |
| 3 | close | 파일 닫기 |
| 57 | fork | 프로세스 생성 |
| 59 | execve | 프로그램 실행 |
| 60 | _exit | 프로세스 종료 |
| 62 | kill | 시그널 전송 |

---

## ③ 용어 정의

| 용어 | 정의 |
|------|------|
| **ASLR** (Address Space Layout Randomization) | 프로그램 실행마다 스택/힙/라이브러리 주소를 랜덤화하여 공격자의 주소 예측을 방해하는 보안 기법 |
| **async-signal-safe** | 시그널 핸들러 내에서 안전하게 호출 가능한 함수. 재진입 가능(reentrant)하거나 시그널에 의해 중단되지 않는 함수 (예: write, kill, _exit) |
| **Blocked (시그널)** | 커널이 프로세스에 전달하지 않도록 억제된 시그널 상태. sigprocmask로 설정 |
| **brk 포인터** | 힙(Heap)의 끝을 가리키는 포인터. sbrk()로 증가시켜 힙을 확장 |
| **Cache Line** | 캐시와 메모리 사이 데이터 이동 단위. x86-64에서 64bytes |
| **Callee-saved 레지스터** | 피호출 함수가 사용 전 저장하고 반환 전 복원해야 하는 레지스터 (%rbx, %r12~%r14, %rbp) |
| **Caller-saved 레지스터** | 호출자가 필요 시 저장해야 하는 레지스터. Callee가 자유롭게 덮어씀 |
| **Coalescing** | 해제된 인접 가용 블록들을 하나로 합치는 동작. 외부 단편화 방지 |
| **COW (Copy-on-Write)** | 쓰기가 발생하기 전까지 물리 페이지를 공유하고, 쓰기 시점에 새 페이지를 복사하는 최적화 기법 |
| **CR3 레지스터** | x86-64에서 현재 프로세스의 L1 페이지 테이블 물리 주소를 저장하는 레지스터 |
| **Critical Section** | 공유 자원에 접근하는 코드 구간. 한 번에 하나의 스레드만 실행되어야 함 |
| **CSE (Common Subexpression Elimination)** | 동일한 부분식을 한 번만 계산하는 컴파일러 최적화 기법 |
| **Dangling Pointer** | 이미 해제된 메모리를 가리키는 포인터. Use-After-Free의 원인 |
| **Deadlock** | 둘 이상의 프로세스/스레드가 서로 상대방이 보유한 자원을 무한히 기다리는 상태 |
| **Demand Paging** | 실제 접근이 발생할 때까지 물리 메모리 할당을 지연하는 방식 |
| **Descriptor Table** | 각 프로세스가 보유한 파일 디스크립터 → Open File Table 매핑 테이블 |
| **Double-Free** | 이미 해제된 메모리를 다시 free()하는 버그. 가용 리스트 오염을 유발 |
| **dup2(oldfd, newfd)** | newfd를 oldfd의 복사본으로 만드는 시스템 콜. I/O 리다이렉션 구현에 사용 |
| **Exception Table** | 예외 번호(k)를 인덱스로 핸들러 주소를 저장하는 OS 구성 테이블 (인터럽트 벡터) |
| **execve()** | 현재 프로세스에 새 프로그램을 로드하여 실행. PID는 유지, 메모리는 교체. 성공 시 반환 없음 |
| **External Fragmentation** | 가용 메모리 합계는 충분하지만 연속된 단일 블록이 부족한 단편화 |
| **File Descriptor (fd)** | 열린 파일을 식별하는 작은 정수. 기본값: 0(stdin), 1(stdout), 2(stderr) |
| **fork()** | 부모 프로세스의 복사본인 자식 프로세스를 생성하는 시스템 콜. 1번 호출, 2번 반환 |
| **Gadget (ROP)** | ret 명령어로 끝나는 기존 코드의 명령어 시퀀스. ROP 공격의 빌딩 블록 |
| **Heap Overflow** | 힙 버퍼의 경계를 넘어 인접 메타데이터를 덮어쓰는 취약점 |
| **Heap Spray** | 힙의 특정 위치에 원하는 데이터를 채워넣는 공격 기법. UAF 익스플로잇에 사용 |
| **Implicit Blocking** | 시그널 핸들러 실행 중 동일 타입 시그널이 자동으로 차단되는 메커니즘 |
| **Internal Fragmentation** | 블록 크기가 실제 페이로드보다 커서 낭비되는 내부 공간 |
| **ISA (Instruction Set Architecture)** | 프로세서가 실행할 수 있는 명령어 집합과 프로그래머에게 보이는 상태를 정의하는 명세 |
| **leaq** | Load Effective Address. 메모리를 읽지 않고 주소값 자체를 레지스터에 저장 |
| **Locality (지역성)** | 프로그램이 최근 또는 인접한 주소를 다시 접근하는 경향. 시간적/공간적 지역성으로 구분 |
| **Mark & Sweep** | GC 알고리즘. Root에서 DFS로 도달 가능한 블록을 마크 후, 미마크 블록을 회수 |
| **MMU (Memory Management Unit)** | 가상 주소를 물리 주소로 변환하는 하드웨어 유닛 |
| **mmap()** | 파일이나 익명 메모리를 프로세스의 가상 주소 공간에 매핑하는 시스템 콜 |
| **Mutex (Mutual Exclusion)** | 임계 구역에 대한 상호 배제를 보장하는 동기화 도구. test_and_set 원자적 연산으로 구현 |
| **NX Bit (No-Execute)** | 메모리 영역에 실행 권한을 제거하여 코드 삽입 공격을 방어하는 하드웨어 기능. PTE의 XD 비트 |
| **Open File Table** | 모든 프로세스가 공유하는 테이블. 파일 위치(file pos)와 참조 횟수(refcnt) 저장 |
| **Orphan Process** | 부모가 먼저 종료된 자식 프로세스. init(PID=1)이 입양하여 reaping |
| **Page Fault** | 접근한 가상 페이지가 물리 메모리에 없을 때 발생하는 Fault. 커널이 디스크에서 로드 |
| **Page Table** | 가상 페이지 번호(VPN)를 물리 페이지 번호(PPN)로 매핑하는 커널 자료구조 |
| **Pending (시그널)** | 전송됐지만 아직 수신되지 않은 시그널 상태 |
| **Process** | 실행 중인 프로그램의 인스턴스. Logical Control Flow + Private Address Space 제공 |
| **Progress Graph** | 두 스레드의 실행 상태 공간을 2D로 표현한 그래프. Race Condition 분석 도구 |
| **PTE (Page Table Entry)** | 페이지 테이블의 각 항목. VPN→PPN 매핑 + 권한 비트(P, R/W, U/S, D, A, XD) 포함 |
| **Race Condition** | 둘 이상의 스레드/프로세스가 공유 자원에 비원자적으로 접근하여 결과가 실행 순서에 따라 달라지는 버그 |
| **Reentrant Function** | 공유 변수를 사용하지 않아 동기화 없이 여러 스레드에서 동시 호출 가능한 함수 |
| **ROP (Return-Oriented Programming)** | 기존 코드의 Gadget을 조합하여 NX Bit를 우회하는 공격 기법 |
| **Semaphore** | 음수가 될 수 없는 정수형 동기화 변수. wait(P: s--)와 post(V: s++) 연산으로 조작 |
| **Short Count** | read/write 시 요청한 바이트보다 적게 처리되는 정상적 현상. EOF/터미널/소켓에서 발생 |
| **Signal** | 커널이 프로세스에게 이벤트 발생을 알리는 작은 메시지. 1~30번 정수 ID로 식별 |
| **Splitting** | 가용 블록을 요청 크기만큼 잘라 할당하고 나머지를 새 가용 블록으로 만드는 동작 |
| **Stack Canary** | 버퍼와 반환 주소 사이에 배치되는 랜덤 값. 반환 전 검사하여 스택 오버플로우 탐지 |
| **Starvation** | 특정 프로세스/스레드가 필요한 자원을 무한히 얻지 못하는 상태 |
| **Strength Reduction** | 비용이 큰 연산(곱셈)을 저렴한 연산(시프트+덧셈)으로 대체하는 컴파일러 최적화 |
| **TLB (Translation Lookaside Buffer)** | MMU 내부의 소형 PTE 캐시. 주소 변환 속도를 높이기 위해 사용 |
| **Thread Safety** | 여러 스레드가 동시에 호출해도 항상 올바른 결과를 반환하는 함수의 속성 |
| **Thrashing** | 프로세스의 Working Set이 물리 메모리를 초과하여 페이지 교체가 폭주하는 현상 |
| **Breakpoint** | 프로그램 실행을 특정 지점에서 중단시키는 디버깅 메커니즘. Software/Hardware/Memory 3종류 존재 |
| **DR0~DR3** | x86-64 CPU의 하드웨어 디버그 레지스터. 최대 4개의 Hardware Breakpoint 주소 저장 |
| **int 3 (0xcc)** | x86 소프트웨어 브레이크포인트 명령어. 실행 시 SIGTRAP 발생 |
| **ptrace** | tracer 프로세스가 tracee 프로세스의 메모리/레지스터를 관찰·제어하는 시스템 콜. GDB·strace의 핵심 |
| **strace** | ptrace(PTRACE_SYSCALL)를 활용하여 프로세스의 시스템 콜을 추적하는 도구 |
| **Tracer / Tracee** | ptrace에서 제어하는 프로세스(tracer)와 제어받는 프로세스(tracee) |
| **Cache Side-Channel** | 캐시 hit/miss의 접근 시간 차이를 이용해 피해자의 메모리 접근 패턴을 추론하는 공격 |
| **clflush** | x86 캐시 라인 강제 비우기 명령어. Rowhammer와 Flush+Reload 공격에 활용 |
| **Cold Boot Attack** | DRAM을 냉각하여 데이터 소멸을 지연시킨 후 암호화 키를 추출하는 물리 공격 |
| **ECC DRAM** | 오류 수정 코드를 내장한 DRAM. Rowhammer로 인한 단일 비트 플립을 감지·수정 |
| **Flush+Reload** | 공유 메모리 캐시를 비운 뒤 피해자 접근 후 재접근 시간을 측정하는 cache side-channel 기법 |
| **KPTI** (Kernel Page Table Isolation) | Meltdown 대응책. 커널과 유저 모드의 페이지 테이블을 완전 분리. 5~20% 성능 저하 |
| **Meltdown** | CPU의 투기적 실행(Speculative Execution)과 캐시 부채널을 결합하여 커널 메모리를 유출하는 공격 |
| **Rowhammer** | DRAM의 인접 행(Row)을 반복 접근하여 전하 누설로 비트를 뒤집는 하드웨어 공격 |
| **Side-Channel Attack** | 알고리즘 자체가 아닌 구현의 부수 정보(타이밍, 전력, 음향, 전자기)를 이용한 공격 |
| **Speculative Execution** | CPU가 성능 향상을 위해 결과가 확정되기 전에 미리 명령어를 실행하는 기법. Meltdown의 근본 원인 |
| **TRESOR** | 암호화 키와 AES 연산을 CPU 레지스터에만 유지하여 Cold Boot Attack을 방어하는 Linux 커널 패치 |
| **Transient Instruction** | 투기적 실행으로 실행되었다가 커밋되지 않고 되돌려지는 명령어 |
| **Use-After-Free (UAF)** | 해제된 메모리를 재사용할 때 발생하는 취약점. Dangling Pointer가 원인 |
| **v-node Table** | 파일의 실제 메타데이터(크기, 타입, 접근 권한 등 stat 구조체 내용)를 저장하는 테이블 |
| **Virtual Memory** | 물리 메모리보다 큰 주소 공간을 제공하고 프로세스 격리를 구현하는 추상화 메커니즘 |
| **VPN / VPO** | 가상 주소의 상위 비트(페이지 번호)와 하위 비트(페이지 내 오프셋) |
| **Zombie Process** | 종료됐지만 부모가 wait()를 호출하지 않아 시스템 자원을 점유 중인 프로세스. ps에서 `<defunct>` |

---

## ④ 주제별 상세

### Ch1. Introduction
- Reality #1: Int ≠ Integer, Float ≠ Real → 유한 비트 표현 → 오버플로우, 결합법칙 위반
- Reality #2: 어셈블리 이해 필수 → 버그 분석, 컴파일러 최적화, 역공학
- Reality #3: 메모리는 유한 자원 → C는 메모리 보호 없음
- Reality #4: 성능 ≠ 점근 복잡도 → 메모리 접근 패턴 결정적 (copyij 4.3ms vs copyji 81.8ms, 19배 차이)
- Reality #5: I/O·네트워크도 시스템의 일부
- 과목 관점: Programmer-Centric (추상화 아래 현실 이해)

### Ch2. Machine-Level Programming — Basics
- **Programmer-Visible State**: PC(%rip), 레지스터 파일, Condition Codes, Memory
- **비가시(Microarchitecture)**: 파이프라인, 캐시, 분기 예측기, TLB
- **Operand 3종**: Immediate($), Register(%), Memory(()) → ★ Mem→Mem 직접 이동 불가
- **주소 지정 일반형**: `D(Rb, Ri, S)` → `Mem[Reg[Rb] + S×Reg[Ri] + D]`
- **leaq**: 메모리 읽지 않고 주소값 계산 → `b*3` → `leaq (%rdi,%rdi,2), %rax`
- **AT&T 문법**: `op Src, Dest` (Intel과 반대)

### Ch2. Machine-Level Programming — Control
- **Condition Codes**: CF(unsigned overflow), ZF(=0), SF(<0), OF(signed overflow)
- **설정**: 산술연산(암묵적) / `cmpq Src2,Src1`(Src1-Src2) / `testq`(AND)
- **루프 변환**: 모든 루프 → goto + 조건 점프
  - do-while: `body → if(Test) goto loop`
  - while: `goto test → body → if(Test) goto loop` (Jump-to-Middle)

### Ch2. Machine-Level Programming — Procedures
- **스택 성장 방향**: 높은→낮은 주소 / push: %rsp-=8 / pop: %rsp+=8
- **call**: 복귀주소 push + 목적지 점프 / **ret**: 복귀주소 pop + 점프
- **스택 프레임 구조** (위→아래): 반환주소 → saved callee registers → 지역변수 → 인자 빌드 공간 ← %rsp

### Ch3. Stack Buffer Overflow
- **취약점 구조**: `name[32]`에서 name+32=saved rbp, name+40=RET ADDR
- **ROP**: ret으로 끝나는 Gadget 체인 → NX 우회 / `ret` = 1바이트 `0xc3`
- **Stack Canary**: `%fs:0x28`에 전역 랜덤값 저장 → 함수 진입 시 스택에 복사 → 반환 전 비교

### Ch4. Memory Hierarchy
- **지역성 원칙**: 프로그램은 최근/인접 주소를 재사용하는 경향 → 캐시 효율의 근거
- **Row-Major**: C 2D 배열 행 우선 저장 → 행 순서 접근(sum_array_rows)이 열 순서(sum_array_cols)보다 19배 빠름
- **캐시 계층**: L0(레지스터) → L1/L2/L3(SRAM) → L4(DRAM) → L5(SSD/HDD) → L6(원격)
- **Miss 처리**: Placement Policy(어디에 넣을지) + Replacement Policy(LRU/FIFO/Random)

### Ch5. Code Optimization & Linking
- **Side Effect 주의**: `strlen(s)` = 매 반복 재계산 → O(n²) / 컴파일러가 Code Motion 적용 불가
- **Undefined Behavior**: signed overflow → 컴파일러가 임의로 코드 제거 가능 (Linux 커널 버그 사례)
- **링킹 심볼 3종**: Global(non-static 함수/전역변수) / Local(static) / External Reference
- **재배치**: .o의 0x0 플레이스홀더 → 최종 절대 주소로 교체 (`objdump -r -d` 로 확인)

### Ch6. Virtual Memory
- **물리 주소 방식**: 단순 시스템(임베디드) / 가상 주소 방식: 모든 현대 OS
- **페이지 테이블**: 프로세스마다 독립 / 커널이 DRAM에 유지 / fork() 시 복사 후 COW 적용
- **PTE 비트**: P(존재), R/W(읽기/쓰기), U/S(유저/슈퍼바이저), D(Dirty), A(Accessed), XD(실행금지)
- **Multi-Level PT 이점**: 사용하지 않는 주소 범위의 L1 PTE를 null로 → 메모리 절약
- **Linux 프로세스 VA 레이아웃** (낮은→높은): .text → .data → .bss → Heap(↑) → 공유 라이브러리 → Stack(↓) → Kernel

### Ch7. Dynamic Memory Allocation
- **블록 헤더 트릭**: 정렬로 인해 size 하위 비트 = 항상 0 → alloc bit 재활용
- **False Fragmentation**: free() 후 병합하지 않으면 인접 가용 블록들이 분리된 채로 남음
- **Segregated List**: 크기 클래스별 리스트 → first-fit이 전체 best-fit에 근사
- **Heap Overflow → Arbitrary Write**: `node->prev->next = node->next` 실행 시 덮어쓴 포인터로 임의 주소에 값 쓰기 가능

### Ch8. Exceptions
- **Exception = ECF(Exceptional Control Flow)**: 일반 점프/호출로 처리할 수 없는 이벤트 처리
- **Kernel Preemption**: 타이머 인터럽트로 커널이 유저 프로그램에서 제어권 회수
- **iret**: 인터럽트/폴트 반환 명령어. ret와 유사하나 권한 레벨도 복원

### Ch9. Processes
- **fork() COW 흐름**: 페이지 테이블 복사 → 모든 페이지 Read-Only 표시 → 쓰기 시 Protection Fault → 새 물리 페이지 복사
- **execve() 동작**: 새 프로그램 페이지 테이블 초기화 → .text/.data/.bss/스택 영역 설정 → PC를 진입점으로 설정
- **Process Graph**: 각 정점=statement / a→b=선행 관계 / Topological sort=가능한 실행 순서
- **Zombie 발생 이유**: 자식 종료 시 exit status 보존 필요 → 부모가 wait() 호출 전까지 일부 자원 유지

### Ch10. Signals
- **Shell의 문제**: 백그라운드 job이 종료돼도 shell이 wait() 안 함 → zombie 누적 → 메모리 누수
- **SIGCHLD 해결**: 자식 종료 시 커널이 부모에게 SIGCHLD → 핸들러에서 `waitpid(-1, &status, WNOHANG)` 루프
- **시그널 전송 방법**: `/bin/kill` 명령어 / 키보드(Ctrl-C/Z) / `kill()` 함수 / 커널 자동(Page Fault→SIGSEGV)
- **프로세스 그룹**: Ctrl-C → 포그라운드 프로세스 그룹 전체에 SIGINT 전송

### Ch11. Threads
- **스레드 스택 주의**: VM으로 보호 안 됨 → 다른 스레드가 포인터로 접근 가능 → 버그 원인
- **스레드 인자 전달 패턴**:
  - ✓ `malloc` 개별 할당 후 전달 (스레드 내에서 free)
  - ✓ 정수값 직접 캐스팅 `(void *)i`
  - ✗ `&i` 루프 변수 주소 전달 → Race Condition!

### Ch12. Synchronization
- **cnt++ Race 원인**: L(load)→U(update)→S(store) 3단계가 원자적이지 않음 → 인터리빙 발생
- **Mutex 동작**: `test_and_set` = `[old=*p; *p=LOCKED; return old;]` 원자적 실행
- **Semaphore 불변**: s ≥ 0 항상 유지 / wait에서 s=0이면 블로킹
- **Deadlock 회피 핵심**: 모든 스레드가 락을 동일한 순서로 획득하면 Circular Wait 조건 깨짐
- **Thread Safety Class2 해결**: static 상태를 인자로 전달 → `rand()` → `rand_r(int *nextp)`
- **Thread/Signal 상호작용 Deadlock**: printf 실행 중(내부 락 보유) → 시그널 → 핸들러에서 printf → 교착

### Ch13. System-Level I/O
- **Everything is a file**: 디스크, 터미널, 소켓, 커널(/proc) 모두 파일로 추상화
- **Short count 처리**: `while((n=read(fd,buf,LEN))>0) { /* process n bytes */ }`
- **fork() 후 파일**: 자식이 부모의 fd 테이블 복사 → 동일 Open File Entry 가리킴 → refcnt=2 → 동일 file pos 공유
- **I/O 리다이렉션 전체 흐름**:
  ```
  fork() → [child] open("foo.txt") = fd3
         → dup2(fd3, 1)  // stdout → foo.txt
         → close(fd3)
         → execve("ls")  // ls의 출력이 foo.txt로
  ```
- **Standard I/O 스트림**: FILE* = fd + 내부 버퍼 / fflush() 명시적 flush 가능

---

## ⑤ 시험 대비 체크리스트

### 계산/분석 문제 유형

- [ ] **주소 계산**: `D(Rb, Ri, S)` 공식으로 메모리 주소 계산
- [ ] **스택 프레임 그리기**: caller/callee 진입-실행-반환 단계별 %rsp, %rbp 위치
- [ ] **fork() 출력 순서**: Process Graph 그려서 가능/불가능한 출력 판별
- [ ] **cnt++ Race 분석**: L1-U1-S1 / L2-U2-S2 인터리빙 표로 최종 cnt 값 추적
- [ ] **Semaphore 상태 추적**: Producer-Consumer에서 empty/full 값 단계별 추적
- [ ] **dup2() 후 fd 상태**: Descriptor Table → Open File Table 변화 그리기
- [ ] **VA → PA 변환**: VPN으로 PTE 조회 → PPN + VPO = PA 계산

### 개념 문제 유형

- [ ] **예외 분류**: Interrupt/Trap/Fault/Abort 구분 + 복귀 위치
- [ ] **Caller/Callee-saved**: 레지스터별 저장 책임 주체
- [ ] **공격-방어 매핑**: Code Injection↔NX / ROP↔ASLR / 오버플로우↔Canary
- [ ] **Deadlock 4조건**: ME + Hold&Wait + No Preemption + Circular Wait
- [ ] **Thread Safety 3클래스**: 각 클래스의 원인과 해결 방법
- [ ] **GC 비교**: Reference Counting vs Mark & Sweep 장단점
- [ ] **I/O 함수 선택**: 상황별 Unix I/O / Standard I/O / RIO 선택 근거
- [ ] **VM 3가지 역할**: Caching / Memory Management / Memory Protection
- [ ] **Page Fault 처리 흐름**: 7단계 순서대로 설명
- [ ] **Segregated List**: 왜 first-fit이 best-fit에 근사하는가

---

### Ch14. Debugger & ptrace

#### 핵심 개념
- **Debugger**: 다른 프로그램(target/tracee)을 테스트·제어하는 프로그램 (GDB, strace)
- **ptrace**: tracer가 tracee의 메모리/레지스터를 관찰·제어하는 시스템 콜
  - `long ptrace(enum __ptrace_request request, pid_t pid, void *addr, void *data)`
  - GDB, strace 모두 ptrace 기반으로 구현

#### ptrace 주요 Request ★
| Request | 동작 |
|---------|------|
| PTRACE_TRACEME | 자신을 부모가 trace하도록 허용 |
| PTRACE_PEEKTEXT/DATA | Tracee 메모리 word 읽기 |
| PTRACE_POKETEXT/DATA | Tracee 메모리 word 쓰기 |
| PTRACE_GETREGS | Tracee 레지스터 전체 복사 |
| PTRACE_SETREGS | Tracee 레지스터 전체 덮어쓰기 |
| PTRACE_CONT | 정지된 tracee 재개 |
| PTRACE_SYSCALL | 다음 syscall 진입/탈출 시 정지 후 재개 |
| PTRACE_SINGLESTEP | 명령어 1개 실행 후 정지 |

#### Breakpoint 3종류 ★
- **Software**: `int 3` (opcode `0xcc`, 1바이트) 삽입 → SIGTRAP 발생 → GDB 개입 / 개수 무제한
- **Hardware**: CPU 디버그 레지스터 DR0~DR3에 주소 저장 → 최대 4개 / 코드 수정 불필요
- **Memory**: 페이지 권한 변경 → Protection Fault → 메모리 접근(읽기/쓰기) 감지

#### GDB 기반 Debugger 동작 흐름
```
fork() → 자식: PTRACE_TRACEME → execve() → SIGTRAP(자동) → 정지
부모(GDB): waitpid() → PTRACE_POKETEXT(0xcc 삽입) → PTRACE_CONT
→ 브레이크포인트 도달 → SIGTRAP → PTRACE_GETREGS → 레지스터 읽기
→ 원래 바이트 복원 → PTRACE_SINGLESTEP → 반복
```

#### GDB 주요 명령어
```
run / break *ADDR / stepi / continue
info registers / set $REG=VALUE / x ADDRESS / set *ADDRESS=VALUE
```

### Ch14 추가 체크리스트
- [ ] **ptrace Request 구분**: PEEK/POKE/GETREGS/SETREGS/CONT/SYSCALL/SINGLESTEP 역할
- [ ] **Breakpoint 3종 비교**: Software(0xcc/무제한) vs Hardware(DR레지스터/4개) vs Memory(페이지 권한)
- [ ] **GDB 동작 흐름**: fork→TRACEME→execve→SIGTRAP→waitpid→0xcc삽입→CONT 순서

### Ch15 추가 체크리스트
- [ ] **Cold Boot Attack 흐름**: DRAM 냉각 → 분리 → 다른 머신 → 키 추출 / TRESOR 대응
- [ ] **Timing Side-Channel**: strcmp 조기 반환 원리 → 복잡도 52⁹ → 52×9
- [ ] **Flush+Reload 3단계**: flush → victim 접근 대기 → reload 시간 측정
- [ ] **Meltdown 동작**: Speculative Exec → kernel_data를 인덱스로 → 캐시 흔적 → Flush+Reload
- [ ] **KPTI 부작용**: TLB flush + PT 교체 → 5~20% 성능 저하
- [ ] **Rowhammer 2가지 도전**: Cache bypass(clflush) / Address info(VA 하위 12bit=PA)
- [ ] **Rowhammer 공격 2가지**: NaCl sandbox escape / Linux 권한 상승(PTE 비트 플립)
- [ ] **Meltdown vs Rowhammer 차이**: CPU 투기적 실행 vs DRAM 물리적 비트 플립
