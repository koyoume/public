# 컴퓨터구조 Knowledge

> 삼성DS · COD (Computer Organization & Design) RISC-V  
> 최종 업데이트: 2026-04-13 · Ch1

---

## ① 수식 모음

| 수식 | 의미 | 변수 설명 | 비고 |
|------|------|----------|------|
| (Ch1에서는 성능 수식이 다루어지지 않음 — Ch1은 개념/배경 챕터) | | | 이후 챕터에서 누적 추가 |

---

## ② 핵심 비교표

| 비교 항목 | A | B | 차이점 |
|----------|---|---|--------|
| **ISA vs ABI** | ISA: HW/SW 인터페이스 (명령어 집합) | ABI: ISA + 시스템 SW 인터페이스 (시스템콜 규약, 레지스터 규약 등) | ISA가 같아도 OS가 다르면 ABI가 달라 바이너리 호환 불가 |
| **ISA vs Implementation** | ISA: "무엇을 할 수 있는가" (인터페이스 명세) | Implementation: "어떻게 구현하는가" (마이크로아키텍처) | 같은 x86 ISA를 Intel과 AMD가 다르게 구현 가능 |
| **Resistive vs Capacitive 터치** | 두 전도층의 물리적 접촉 | 손가락의 정전용량 변화 감지 | Capacitive: 멀티터치 가능, 대부분 스마트폰 사용 |
| **SRAM vs DRAM (개요)** | 빠르고 비쌈 (캐시) | 느리고 저렴 (메인 메모리) | 메모리 계층의 핵심 — Ch5에서 상세 |
| **P-core vs E-core** | Performance core (고성능, 고전력) | Efficiency core (저전력, 백그라운드) | 이종 코어 아키텍처 (Intel Arrow Lake, ARM big.LITTLE) |
| **Desktop vs Server vs Embedded** | 범용/비용-성능 트레이드오프 | 높은 용량·성능·신뢰성 / 전력·비용 제약 엄격 | 설계 최적화 기준이 다름 |

---

## ③ 용어 정의

| 용어 | 정의 |
|------|------|
| ABI (Application Binary Interface) | ISA에 시스템 소프트웨어 인터페이스(시스템콜 규약, 레지스터 사용 규약 등)를 더한 것. 같은 ISA라도 OS가 다르면 ABI가 다를 수 있음 |
| Abstraction (추상화) | 하위 수준의 복잡한 세부사항을 숨기고 상위 수준에서는 단순화된 인터페이스만 노출하는 설계 원칙 |
| Assembly Language | 기계어의 텍스트(니모닉) 표현. Assembler가 이진 기계어로 변환 |
| Cache Memory | CPU 내부 또는 근처에 위치한 소형 고속 SRAM. 자주 사용되는 데이터를 보관하여 메인 메모리 접근 지연을 줄임 |
| Cloud Computing | 창고 규모 컴퓨터(WSC)에서 SaaS 형태로 서비스 제공. 소프트웨어 일부는 클라이언트, 일부는 서버에서 실행 |
| Compiler | 고수준 언어(HLL) 소스코드를 기계어(어셈블리→이진)로 번역하는 시스템 소프트웨어 |
| Control | 프로세서 내부에서 명령어를 해석(decode)하고 Datapath에 제어 신호를 보내는 유닛 |
| Datapath | 프로세서 내부에서 실제 데이터 연산(ALU, 레지스터 읽기/쓰기 등)을 수행하는 유닛 |
| Embedded Computer | 다른 시스템(자동차, 가전 등)의 내부 부품으로 숨어 있는 컴퓨터. 전력/성능/비용 제약이 엄격 |
| Frame Buffer | 디스플레이에 표시할 픽셀 데이터를 저장하는 메모리 영역. 화면은 이 버퍼 내용을 반영 |
| HLL (High-Level Language) | C, Java, Python 등 인간이 읽기 쉬운 프로그래밍 언어. 컴파일러가 기계어로 변환 |
| Implementation | ISA 명세를 실제로 구현한 하드웨어의 세부 설계 (마이크로아키텍처) |
| ISA (Instruction Set Architecture) | 하드웨어와 소프트웨어 사이의 인터페이스. 프로세서가 이해하는 명령어 집합과 규약을 정의 |
| Moore's Law (무어의 법칙) | 집적 회로의 트랜지스터 수가 약 2년마다 2배로 증가한다는 경험적 관찰 (물리 법칙 아님) |
| Operating System (OS) | I/O 처리, 메모리/저장장치 관리, 태스크 스케줄링 및 자원 공유를 담당하는 시스템 소프트웨어 |
| Pixel (Picture Element) | 디스플레이 화면을 구성하는 최소 단위. 프레임 버퍼의 비트 값이 색상/밝기를 결정 |
| PMD (Personal Mobile Device) | 배터리 구동, 인터넷 연결, 수백 달러 가격대의 개인 모바일 장치 (스마트폰, 태블릿 등) |
| SoC (System on Chip) | CPU, GPU, NPU, 메모리 컨트롤러 등을 하나의 칩에 집적한 형태. PMD 시대의 주류 설계 |
| Supercomputer | 최고 성능의 과학/공학 계산용 컴퓨터. 시장 비중은 작지만 최고 성능 추구 |
| WSC (Warehouse Scale Computer) | 클라우드 서비스를 위한 창고 규모의 대형 컴퓨팅 시스템 |

---

## ④ 주제별 상세

### Chapter 1: Computer Abstractions and Technology

#### 1-1. 무어의 법칙과 컴퓨터 혁명

무어의 법칙은 "IC의 트랜지스터 수가 약 2년마다 2배 증가"한다는 경험적 관찰이다. 1971년 Intel 4004 (2,300개)에서 2018년 72-core Xeon (수십억 개)까지, 로그 스케일 그래프에서 거의 직선으로 증가했다.

```
트랜지스터 수 (로그)
 50B ─ ● 72-core Xeon (2018~)
 10B ─
  1B ─ ● Dual-core Itanium 2 (2006~)
100M ─ ● Pentium 4 (2000~)
 10M ─ ● Pentium (1993)
  1M ─ ● Intel 80486 (1989)
100K ─ ● Intel 80386 (1985)
 10K ─ ● Intel 8080 (1974)
  1K ─ ● Intel 4004 (1971)
      └──────────────────────
       1970    1990    2010
```

- **핵심 응용**: 자동차 컴퓨터, 스마트폰, 유전체 프로젝트, WWW, 검색 엔진, ML/AI
- **주의**: 물리 법칙이 아닌 경험적 관찰. 미세공정 한계로 둔화 → 병렬 처리 중요성 증대

**예시 문제**: 무어의 법칙에 따르면 트랜지스터 수가 2년마다 2배가 된다. 현재 10억 개 트랜지스터를 가진 칩이 있을 때, 10년 후 예상 트랜지스터 수는?

풀이:
- 10년 / 2년 = 5번 두 배
- 10억 × 2^5 = 10억 × 32 = **320억 개**

#### 1-2. 컴퓨터의 분류

| 클래스 | 목적 | 핵심 설계 기준 |
|--------|------|---------------|
| Personal Computer | 범용, 다양한 SW | 비용/성능 트레이드오프 |
| Server | 네트워크 기반 서비스 | 높은 용량, 성능, 신뢰성 |
| Supercomputer | 과학/공학 계산 | 최고 성능 (시장 비중 작음) |
| Embedded | 시스템 내부 부품 | 전력/성능/비용 제약 엄격 |

PostPC 시대 (2011~): PMD (배터리, 인터넷, 수백 달러) + Cloud Computing (WSC, SaaS)

#### 1-3. 8가지 위대한 아이디어 (Eight Great Ideas)

| # | 아이디어 | 설명 | 관련 챕터/개념 |
|---|---------|------|-------------|
| 1 | Design for Moore's Law | 완성 시점의 기술 수준에 맞춰 설계 | 전체 |
| 2 | Use Abstraction | 복잡성을 계층적으로 숨김 | ISA, 전체 |
| 3 | Make Common Case Fast | 자주 발생하는 경우를 빠르게 | Amdahl's Law |
| 4 | Performance via Parallelism | 여러 작업 동시 수행 | 멀티코어 |
| 5 | Performance via Pipelining | 작업을 단계별로 나누어 중첩 | Ch4 파이프라인 |
| 6 | Performance via Prediction | 예측하고 틀리면 복구 | Branch prediction |
| 7 | Hierarchy of Memories | 빠른-비싼 / 느린-싼 메모리 계층 배치 | Ch5 캐시 |
| 8 | Dependability via Redundancy | 중복으로 신뢰성 확보 | RAID, ECC |

#### 1-4. 소프트웨어 계층 구조

```
┌─────────────────────────────┐
│     Applications Software    │  ← HLL로 작성
├─────────────────────────────┤
│      Systems Software        │
│  Compiler: HLL → 기계어       │
│  OS: I/O, 메모리, 스케줄링     │
├─────────────────────────────┤
│         Hardware             │
│  Processor, Memory, I/O     │
└─────────────────────────────┘
```

프로그램 코드 변환 과정 (swap 예시):

```
C (HLL)                    RISC-V Assembly           Binary Machine Code
swap(int v[], int k)       swap:                     00000000001011010...
{int temp;                   slli x6, x11, 3         00000000011010010...
    temp = v[k];             add  x6, x10, x6        ...
    v[k] = v[k+1];          ld   x5, 0(x6)
    v[k+1] = temp;          ld   x7, 8(x6)
}                            sd   x7, 0(x6)
        │                    sd   x5, 8(x6)
        ▼ Compiler           jalr x0, 0(x1)
                                    │
                                    ▼ Assembler
```

#### 1-5. 하드웨어 5대 구성 요소

모든 컴퓨터 (Desktop, Server, Supercomputer, Embedded) 동일:

```
                ┌──────────────────────┐
                │      Computer        │
 Input ────►    │  ┌────────────────┐  │  ────► Output
                │  │   Processor    │  │
                │  │ ┌──────┐┌────┐│  │
                │  │ │Control││Data││  │
                │  │ │      ││path││  │
                │  │ └──────┘└────┘│  │
                │  └───────┬────────┘  │
                │          │           │
                │  ┌───────▼────────┐  │
                │  │    Memory      │  │
                │  └────────────────┘  │
                └──────────────────────┘
```

- **Datapath**: 데이터 연산 수행 (ALU, 레지스터)
- **Control**: 명령어 해석, 제어 신호 생성
- **Cache Memory**: CPU 내부 소형 고속 SRAM
- **I/O**: User-interface (디스플레이, 키보드, 마우스), Storage (HDD, SSD), Network

#### 1-6. 프로세서 진화: 단일코어 → 이종코어 SoC

```
2007 AMD Barcelona     2024 Intel Arrow Lake        2025 Apple A18 Pro
┌──────────────┐      ┌───────────────────┐       ┌──────────────┐
│ Core1  Core2 │      │ P-core×8  E-core×4│       │ CPU  5c-GPU  │
│ Core4  Core3 │      │ (Lion Cove+Skymont)│       │ NPU  MemCtrl │
│  2MB L3共有   │      │ Ring + 36MB L3    │       │ 단일 SoC 집적  │
└──────────────┘      └───────────────────┘       └──────────────┘
   동종 멀티코어           이종 하이브리드            모바일 SoC
```

#### 1-7. 추상화: ISA / ABI / Implementation

```
Application
     │
  HLL (C, Java, ...)
     │
═══ ABI ═══  (ISA + 시스템 SW 인터페이스)
     │
  OS / Compiler
     │
═══ ISA ═══  (HW/SW 인터페이스)
     │
  Hardware (Implementation)
```

- **ISA**: 프로세서가 이해하는 명령어 집합 정의 (RISC-V, ARM, x86)
- **ABI**: ISA + 시스템콜 규약 + 레지스터 사용 규약
- **Implementation**: ISA를 실제로 구현한 마이크로아키텍처

**예시 문제**: "같은 ISA인데 왜 Intel과 AMD의 CPU 성능이 다른가?"

풀이: ISA는 "무엇을 할 수 있는가"의 명세이고, Implementation은 "어떻게 구현하는가"의 세부사항이다. 같은 x86 ISA라도 파이프라인 깊이, 캐시 크기, 분기 예측 알고리즘 등 마이크로아키텍처가 다르면 성능이 달라진다. ISA는 SW 호환성을, Implementation은 HW 성능을 결정한다.

---

## ⑤ 시험 대비 체크리스트

### 개념 문제 유형
- [ ] 무어의 법칙 정의, 한계, "물리 법칙 아님" 구분
- [ ] 컴퓨터 4분류 (PC/Server/Super/Embedded) 각각의 설계 기준
- [ ] PostPC 시대: PMD vs Cloud의 정의와 특징
- [ ] 8가지 Great Ideas 전체 나열 및 각각 1줄 설명
- [ ] ISA vs ABI vs Implementation 차이
- [ ] 소프트웨어 3계층 (Application/System/Hardware) 및 각 역할
- [ ] Compiler vs OS의 역할 구분
- [ ] Datapath vs Control의 역할 구분
- [ ] Cache Memory의 목적 (SRAM, 빠른 접근)
- [ ] 프레임 버퍼와 디스플레이의 관계
- [ ] Resistive vs Capacitive 터치스크린 차이

### 계산 문제 유형
- [ ] 무어의 법칙 적용: n년 후 트랜지스터 수 계산 (현재 × 2^(n/2))
- [ ] (이후 챕터에서 CPU Time, CPI, Amdahl's Law 등 추가 예정)
