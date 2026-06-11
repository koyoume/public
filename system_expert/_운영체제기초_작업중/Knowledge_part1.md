# 운영체제의 기초 — 오픈북 시험 최적화 정리

> 마지막 업데이트: 2026-06-11 | Ch1~Ch12 + ACID 보충 수록 | ★ = 시험 출제 가능성 높음

---

## ① 수식 모음

| 수식 | 의미 | 챕터 |
|------|------|------|
| `Physical = Base + Offset` (if `Offset < Bound`) | Base/Bound MMU 주소 변환 | Ch1 |
| `Mode bit: 0=kernel, 1=user` (PSW) | Dual mode operation | Ch2 |
| 인자: `ebp+8`, `ebp+12`, ...  | x86 cdecl 인자 위치 (caller frame) | Ch3 |
| 지역변수: `ebp-4`, `ebp-8`, ... | x86 cdecl 지역 변수 위치 | Ch3 |
| 반환값 = `%eax` | x86 cdecl 반환값 위치 | Ch3 |
| `τ_{n+1} = α·t_n + (1-α)·τ_n` | Exponential moving average (SJF burst 예측) | Ch5 |
| `TS_i = (W_i / S_Φ) × P` | WRR/CFS time slice | Ch5 |
| `VR(τ_i, t) = (W_0/W_i) × PR(τ_i, t)` | CFS virtual runtime | Ch5 |
| `nice 1단계 = CPU ±10%` | Linux CFS nice rule | Ch5 |
| `lag = 실제_받은_CPU − 이상적_GPS_CPU` | Fair share fairness 측정 | Ch5 |
| `C_τ(t1,t2) = (W_τ/S_Φ) × (t2-t1)` | GPS perfect fairness | Ch5 |
| `Need = Max − Allocation` | Banker's algorithm | Ch7 |
| `Block size = Payload + Header + Padding (+ Footer)` | malloc block 구조 | Ch9 |
| `4가지 coalescing case: (Alloc/Free) × (Alloc/Free)` | Boundary tag coalescing | Ch9 |
| `Physical = PFN || Page_Offset` | Paging address translation | Ch10 |
| `Physical = Base_seg + (Page_Table[PFN] || Offset)` | Paged segmentation | Ch10 |
| `t_em = α·(t_c+t_m) + (1-α)·(2t_c+2t_m)` | TLB Effective Access Time | Ch10 |
| `t_em = (1-α)·t_c + (1-α)·t_m + t_c + t_m` (전개식) | TLB EAT 전개 | Ch10 |
| `t_eff_acc = p·t_mem + (1-p)·t_fault` | Demand paging EAT | Ch11 |
| Working set = `last τ초 동안 참조된 모든 page` | Working set 정의 | Ch11 |
| 32-bit, 1KB page, 4B PTE → PT 크기 16MB | Paging table 크기 폭증 예시 | Ch10 |
| 64-bit, 4KB page → 64K TB | 64-bit page table 비현실성 | Ch11 |
| Disk: seek 10~20ms + rotation 0~16ms + transfer 8~40μs | Disk 시간 (2012 기준) | Ch12 |
| Flash: read 20μs / write 200μs / erase 2000μs | Flash 동작 시간 | Ch12 |

---

## ② 핵심 비교표

### OS의 세 가지 역할 ★

| 역할 | 의미 | 예시 |
|------|------|------|
| **Coordinator** | 자원 공유 조율, 충돌 방지 | CPU scheduling, lock 관리 |
| **Illusion Generator** | 더 좋은 머신처럼 보이게 | Virtual memory, multitasking, GUI |
| **Standard Library** | 공통 함수 모음 | File system API, network stack |

### OS 진화 단계 ★

| Phase | 시기 | 특징 |
|-------|------|------|
| **Phase I** | 1950s | Single-program batch, manual loading |
| **Phase II** | 1960s | Multi-programmed batch, I/O concurrency |
| **Phase III** | 1970s~ | Time-sharing, interactive, modern OS |

### Interrupt 분류 ★

| 종류 | 동기성 | 발생 원인 | 예시 |
|------|--------|----------|------|
| **Hardware Interrupt** | Asynchronous | 외부 신호 (다른 device) | Timer, keyboard, disk I/O 완료 |
| **Software Interrupt (Trap)** | Synchronous | 명령어 실행 결과 | syscall, divide-by-zero |

### Hardware Protection 4가지 ★

| 보호 | 메커니즘 | 무엇을 막는가 |
|------|----------|--------------|
| **Dual Mode** | Mode bit + privileged inst | 모든 보호의 기반 |
| **I/O Protection** | I/O instructions = privileged | I/O 독점 |
| **Memory Protection** | Base/bound register | 다른 메모리 침범 |
| **CPU Protection** | Hardware timer + interrupt | CPU 독점 (무한 루프) |

### x86 Stack Frame Layout (cdecl) ★

| 위치 | 내용 |
|------|------|
| ebp + 4·(N+1) | 인자 N |
| ... | ... |
| ebp + 12 | 인자 2 (y) |
| ebp + 8 | 인자 1 (x) |
| ebp + 4 | return address |
| ebp + 0 | saved old ebp ← **%ebp** |
| ebp − 4 | 지역 변수 1 |
| ebp − 8 | 지역 변수 2 |
| ... | ... ← **%esp (top)** |

### Process State Transition ★

| 전이 | 트리거 |
|------|------|
| New → Ready | 프로세스 생성 완료 |
| Ready → Running | Dispatched |
| Running → Ready | Interrupted (timer/preemption) |
| Running → Waiting | I/O 요청 또는 event 대기 |
| Waiting → Ready | I/O 완료 또는 event 발생 |
| Running → Terminated | exit() 또는 abort() |

### Process vs Thread ★

| 항목 | Process | Thread |
|------|---------|--------|
| 자원 단위 | ✓ (자원 소유) | ✗ |
| 실행 단위 | ✓ | ✓ |
| 주소 공간 | 독립 | 공유 |
| 스택 | 자기 것 | 자기 것 |
| Code/Data/Heap | 독립 | 공유 |
| 생성 비용 | 비쌈 | 쌈 |
| 통신 | IPC 필요 | 공유 메모리 직접 |

### Thread 구현 3가지 ★

| 방식 | Kernel 인식 | Processor 할당 단위 | 장점 | 단점 |
|------|------------|---------------------|------|------|
| **ULT** | 모름 | Process | Mode switch 없음, app-specific scheduling | Blocking syscall이 전체 process block |
| **KLT** | 완전히 앎 | Thread | 동시 다중 코어 실행, blocking이 thread만 영향 | Thread switch마다 2번 mode switch |
| **Combined** | 부분 (KLT만) | Thread | ULT의 빠름 + KLT의 multi-core | 복잡도 |

### Scheduling Policy 진화 ★

| 정책 | 핵심 아이디어 | 한계 |
|------|--------------|------|
| **FIFO/FCFS** | 도착 순 | Convoy effect (긴 작업이 짧은 작업 막음) |
| **SJF/SRTF** | 짧은 burst부터 | 미래 burst 길이 예측 불가 |
| **RR** | 모두 같은 time slice | Time slice 크기 선택 문제 |
| **MLFQ** | Priority 큐 + 적응적 time slice | Fair share 불가 |
| **GPS** | 무한히 작은 quantum + weight 비례 | 구현 불가 (이상) |
| **WRR** | Weight × interval = time slice | Weak fairness |
| **WFQ** | Virtual runtime, 가장 작은 것 실행 | O(N) overhead |
| **CFS** | RB-tree, leftmost = 다음 실행 | Linux 표준 |

### Page Replacement Algorithms ★

| 알고리즘 | 핵심 아이디어 | 특성 |
|---------|--------------|------|
| **OPT** | 미래에 가장 늦게 쓸 page 버림 | 이론적 최적, 구현 불가 |
| **LRU** | 가장 오래 안 쓴 것 버림 | OPT 근사, 정확 구현 비쌈 |
| **FIFO** | 가장 먼저 들어온 것 버림 | 단순, Belady's anomaly 발생 |
| **Random** | 임의 선택 | 놀랍게 잘 동작 |
| **Clock (2nd chance)** | Reference bit 순환 검사 | 실제 OS 표준 |
| **Enhanced Clock** | Reference + Dirty bit | dirty page 우선 보존 |

### Memory Management 진화 ★

| 단계 | 해결 | 도입 문제 |
|------|------|----------|
| Base/Bound (1 segment) | 단순 보호 | Sharing 불가 |
| Multiple Segments | Sharing, 논리 단위 | External fragmentation |
| Paging | External fragmentation 해결 | Internal frag, 큰 page table |
| Paged Segmentation | 두 단계 매핑, table 작게 | Translation overhead |
| + TLB | Translation 가속 | (해결됨) |
| Multi-level Page Table | 64-bit space 지원 | Lookup multi-step |

### Fragmentation 종류 ★

| 종류 | 정의 | 발생 위치 |
|------|------|----------|
| **Internal** | 할당된 블록 안의 미사용 공간 | Block size > payload (alignment 등) |
| **External** | 전체 free 공간은 충분하나 단일 연속 영역이 없음 | malloc, segmentation |

### Heap Free List 구현 3종 ★

| 방법 | 추적 대상 | 할당 시간 | 메모리 오버헤드 |
|------|---------|----------|----------------|
| **Implicit list** | 모든 block | O(전체 블록) | Header만 |
| **Explicit list** | Free block만 | O(가용 블록) | Header + prev/next |
| **Segregated list** | Size class별 list | O(1) 근사 | + 여러 list head |

### Coalescing 4 Cases (Boundary Tags) ★

| Case | 좌 (prev) | 우 (next) | 결과 |
|------|-----------|-----------|------|
| 1 | Alloc | Alloc | 자기만 free |
| 2 | Alloc | Free | 자기 + 우 |
| 3 | Free | Alloc | 좌 + 자기 |
| 4 | Free | Free | 좌 + 자기 + 우 |

### Deadlock의 4 Necessary Conditions (Coffman) ★

| 조건 | 의미 | 깨는 prevention 전략 |
|------|------|---------------------|
| **Mutual Exclusion** | 자원 공유 불가 | 자원 공유 가능하게 (대부분 불가) |
| **No Preemption** | 강제 회수 불가 | 자원 선점 허용 |
| **Hold and Wait** | 잡은 채 대기 | 한꺼번에 다 요청 |
| **Circular Wait** | 순환 대기 | **Ordered request** (실용적) |

### TLB Hit Ratio와 EAT ★

| α (hit ratio) | t_c=10ns, t_m=100ns → t_em |
|---------------|--------------------------|
| 0.98 | 112ns (1.12× of mem) |
| 0.90 | 120ns (1.2× of mem) |
| 0.50 | 160ns (1.6× of mem) |
| 0.00 | 220ns (TLB도 한 번 거침) |

### Linux Memory Allocation ★

| 크기 | 사용 메커니즘 | 특성 |
|------|--------------|------|
| < mmap threshold (보통 64KB or 4MB) | **Heap** (sbrk 기반) | Free 후 mapping 재사용 (성능 ↑) |
| ≥ mmap threshold | **AMO** (anonymous mmap) | Free 시 physical frame 즉시 반환 (메모리 효율 ↑) |

### Major vs Minor Page Fault ★

| 종류 | Page mapping | Disk I/O | 비용 |
|------|-------------|----------|------|
| **Minor** | ✓ | ✗ | μs 단위 |
| **Major** | ✓ | ✓ | ms 단위 (1000배) |

### Linux Device 분류 ★

| 종류 | 전송 단위 | 예시 | 특징 |
|------|----------|------|------|
| **Character** | byte | mouse, keyboard, tty | 파일처럼 접근, 직접 read/write |
| **Block** | block (수 KB) | disk, CD-ROM | 파일처럼 접근, buffer cache 사용 |
| **Network** | packet | eth0 | socket API 사용 |

### Device File Major/Minor ★

| 필드 | 의미 |
|------|------|
| **Type** | block 또는 character |
| **Major number** | 어떤 driver를 쓸지 결정 (cdevsw/bdevsw index) |
| **Minor number** | 같은 driver 내에서 어느 instance |

### I/O Routine 4가지 조합 ★

| 조합 | CPU 자원 | 응답성 | 사용처 |
|------|---------|--------|--------|
| **Polling + Blocking** | 낭비 | OK | 단순 char device |
| **Polling + Non-blocking** | 낭비 | 즉시 return | 빠른 retry |
| **Interrupt + Blocking** | 효율적 | sleep | 일반 char device |
| **Interrupt + Blocking + Buffer Cache** | 효율적 | 두 단계 sleep 가능 | block device 표준 |

---

## ③ 용어 정의 모음

### 챕터 1-2: 기반

- **Stored-program concept**: 코드와 데이터를 메모리에 함께 저장 (von Neumann 1945)
- **Multiprogramming**: 여러 프로세스가 메모리에 있음 (메모리 관점)
- **Multiprocessing**: 여러 프로세스가 동시 실행 (CPU 관점)
- **FDE cycle**: Fetch → Decode → Execute (instruction의 일생)
- **MMU**: Memory Management Unit, virtual→physical address 변환
- **PSW**: Processor Status Word, mode bit 등 포함
- **Bus master**: bus transaction을 시작할 수 있는 컴포넌트 (CPU, DMA controller)
- **PIC**: Programmable Interrupt Controller, 여러 IRQ를 CPU의 단일 INTR에 다중화
- **System call**: User → Kernel mode 전환을 동반하는 함수 호출

### 챕터 3: Stack

- **Stack frame (activation record)**: 한 함수 호출이 만드는 스택 위 영역
- **Prologue**: `pushl %ebp; movl %esp,%ebp; subl $N,%esp` (함수 시작)
- **Epilogue**: `movl %ebp,%esp; popl %ebp; ret` (함수 종료)
- **Calling convention**: 인자 전달, 반환값, register 저장 책임 등의 규약 (x86은 cdecl)
- **leal**: Load Effective Address — 주소 계산만 하고 메모리 접근 X (덧셈 트릭으로 사용)

### 챕터 4: Process/Thread

- **PCB**: Process Control Block, 프로세스 정보 저장
- **TCB**: Thread Control Block
- **Context switch**: 한 프로세스에서 다른 프로세스로 CPU 전환
- **Dispatcher**: Mechanism — 실제 전환 수행
- **Scheduler**: Policy — 누구를 다음에 실행시킬지 결정
- **fork()**: 현재 프로세스 복제 (deep copy → COW로 최적화)
- **exec()**: 현재 프로세스 이미지를 새 프로그램으로 교체
- **COW**: Copy-on-Write — fork 시 page 공유, 쓸 때만 복사
- **TLS**: Thread-Local Storage — 각 thread별 독립적 전역 변수

### 챕터 5: Scheduling

- **CPU burst**: 프로세스가 CPU에서 계속 실행되는 구간 (I/O 사이)
- **Convoy effect**: 긴 process 뒤에 짧은 process가 줄서는 현상 (FIFO)
- **Exponential moving average**: 과거 burst들로 다음 burst 예측 (`τ = αt + (1-α)τ_prev`)
- **MLFQ**: Multi-Level Feedback Queue — priority 별 큐, time slice 2^k
- **GPS**: Generalized Processor Sharing — fair share의 이상 (불가능)
- **WRR**: Weighted Round Robin — weight 비례 time slice
- **WFQ**: Weighted Fair Queuing — virtual runtime 기반
- **CFS**: Completely Fair Scheduler — Linux의 fair share (RB-tree)
- **Virtual Runtime**: 실제 CPU 시간을 weight로 정규화한 값
- **Nice value**: -20 (높은 priority) ~ 19 (낮은 priority), 0이 default

### 챕터 6: Synchronization

- **Race condition**: 여러 실행 흐름이 공유 자원 접근 시 타이밍에 따라 결과 달라짐
- **Critical section**: 한 번에 한 process만 실행 가능한 코드 영역
- **Atomicity**: 쪼개지지 않는 연산 (interrupt 불가)
- **Mutual exclusion**: 한 번에 한 process만 어떤 일을 함
- **Semaphore**: 정수 값 + atomic P/V (Dijkstra)
- **P (wait)**: 0 아니면 1 감소
- **V (signal)**: 1 증가
- **Binary semaphore = Mutex**: 0/1만 가짐
- **Counting semaphore**: 임의 음이 아닌 정수
- **Condition variable**: 값 없는 event, wait/signal/broadcast
- **Mesa semantics**: signal 후 조건 재확인 필요 (현대 표준 → while 사용)
- **Hoare semantics**: signal 후 즉시 깨어난 측이 진행 (이론적)
- **Monitor**: ADT + 자동 lock + condition variable

### 챕터 7: Deadlock

- **Deadlock**: 모든 프로세스가 서로의 자원을 기다려 진행 불가
- **Safe state**: 어떤 순서로든 모든 프로세스의 max를 만족시킬 수 있는 상태
- **Unsafe state**: deadlock 가능성 있는 상태 (반드시 deadlock은 아님)
- **Banker's algorithm**: 자원 할당이 safe state를 유지하는지 검사
- **Resource Allocation Graph**: process-resource 의존 그래프, cycle 검사
- **Ordered request**: 자원에 전역 순서 부여, 그 순서로만 요청 (실용적 prevention)

### 챕터 8: Linker

- **ELF**: Executable and Linkable Format, .o/.so/a.out의 공통 포맷
- **Section vs Segment**: section은 link time (compile/linking용), segment는 run time (loading용)
- **text/data/bss/rodata**: 코드/초기화된 전역/0초기화 전역/읽기전용 데이터
- **Strong symbol**: function + initialized global
- **Weak symbol**: uninitialized global + extern
- **Symbol Resolution**: 심볼 참조를 정확히 하나의 정의에 연결
- **Relocation**: section 병합 + 상대 주소를 절대 주소로 변환
- **Static library (.a)**: archive of .o, 링크 시 사용된 .o만 들어감
- **Dynamic library (.so)**: load time 또는 runtime에 동적 link, 공유 가능
- **PIC**: Position-Independent Code (`-fpic`)
- **dlopen/dlsym/dlclose**: runtime dynamic linking API

### 챕터 9: Dynamic Memory

- **Heap**: 동적 메모리 할당 영역 (sbrk/mmap으로 확장)
- **brk pointer**: heap의 top
- **sbrk(incr)**: brk를 incr만큼 이동
- **Free list**: 사용 중이 아닌 메모리 추적 자료구조
- **Best-fit / First-fit / Next-fit / Worst-fit**: free block 선택 정책
- **Boundary tag**: block 끝에 size/allocated 복사 → bidirectional coalescing 가능
- **Coalescing**: 인접한 free block 합치기 (immediate vs deferred)
- **VMA**: Virtual Memory Area — Linux의 연속 가상 메모리 영역
- **AMO**: Anonymous Memory Object — 익명 mmap으로 만든 VMA
- **GC**: Garbage Collection, mark-and-sweep / reference counter
- **Memory leak**: 사용 안 하는데 회수 안 된 메모리
- **Dangling pointer**: 이미 free된 메모리를 가리키는 포인터

### 챕터 10: Paging

- **Segment**: 논리적 메모리 단위 (code, data, stack)
- **Page**: 고정 크기 메모리 단위 (보통 4KB)
- **Frame**: physical page (page size와 같음)
- **PTE**: Page Table Entry, PFN + protection bits
- **PTBR**: Page Table Base Register
- **STBR**: Segment Table Base Register
- **TLB**: Translation Lookaside Buffer, address translation cache
- **ASID**: Address Space ID, TLB entry의 process 식별
- **EAT**: Effective Access Time

### 챕터 11: Demand Paging

- **Virtual memory**: 일부만 메모리에 있어도 실행 가능한 환상
- **Locality**: spatial (인접 주소) + temporal (반복 접근)
- **Knuth's 90/10**: 시간의 90%가 코드의 10%에서
- **Page fault**: 메모리에 없는 page 참조 → trap
- **Major page fault**: disk I/O 동반
- **Minor page fault**: page mapping만 (anonymous page에 대한 첫 접근)
- **Demand paging vs Prepaging**: 참조 시 vs 미리 가져옴
- **Belady's anomaly**: frame 증가에도 fault 증가 (FIFO만)
- **Stack algorithm**: anomaly 면역 (LRU는 stack algorithm)
- **Working set**: 최근 τ초 동안 참조한 page들
- **Resident set**: 메모리에 있는 process의 page들
- **Balance set**: working set이 memory에 fit하는 active processes 집합
- **Thrashing**: page fault 너무 많아 진전 없음
- **OOM killer**: 메모리 부족 시 low-priority process kill
- **Memory-mapped file (mmap)**: VM 시스템으로 file I/O 처리
- **Hierarchical page table**: multi-level (x86-64 = 4-level)
- **Hashed page table**: VPN → hash → PTE chain
- **Inverted page table**: frame당 1 entry, physical memory에 비례

### 챕터 12: Device Drivers

- **I/O controller**: 장치 옆 chip, register set + control logic
- **Memory-mapped I/O**: device register를 메모리 주소로 접근
- **Port-based I/O**: 별도 I/O instruction (x86 in/out)
- **DMA**: Direct Memory Access, CPU 없이 큰 데이터 전송
- **Seek time**: head를 track으로 이동
- **Rotational latency**: sector가 head 아래로 오기 대기
- **Transfer time**: sector 읽기/쓰기
- **Cylinder**: 모든 platter의 같은 track 번호 모음
- **cdevsw/bdevsw**: character/block device switch table
- **Strategy routine**: block driver의 block request handler
- **Buffer cache**: block device의 캐싱 layer
- **Top half (ISR)**: short, interrupt disabled, ack + bottom half 활성화
- **Bottom half**: longer, interrupt enabled, deferred execution
- **Polling vs Interrupt-driven**: 반복 검사 vs sleep + wake
- **Blocking vs Non-blocking**: wait vs immediate return

### 보충: Transaction & ACID

- **Transaction**: 하나의 논리적 작업 단위 (전부 성공 or 전부 실패)
- **Atomicity (A)**: 부분 실행 안 됨
- **Consistency (C)**: invariant 유지
- **Isolation (I)**: 동시 실행 transaction 간 간섭 없음 (race condition 방지)
- **Durability (D)**: commit 후 결과 영구적
- **Serializability**: 동시 실행 결과가 어떤 순차 실행과 같음

---
