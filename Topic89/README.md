---
title: "VHDL for Hardware Security"
topic: "vhdl"
tags: [vhdl, fpga, hardware, digital-logic, hardware-security]
difficulty: advanced
day: 89
layout: default
parent: Topics
nav_order: 89
---

# VHDL for Hardware Security

## What You Will Learn
- What VHDL is and how it describes hardware
- The basic structure of a VHDL design (entity and architecture)
- How VHDL is used in security-relevant hardware (FPGAs, crypto modules)
- How to implement a simple cipher or logic gate in VHDL

## What Is It?

**VHDL (VHSIC Hardware Description Language)** is a language used to describe the behavior and structure of digital circuits. VHSIC stands for Very High Speed Integrated Circuit — it was originally developed for the US Department of Defense.

VHDL is used to program **FPGAs (Field-Programmable Gate Arrays)** and design **ASICs (Application-Specific Integrated Circuits)**. Unlike software, VHDL describes hardware — logic that runs in parallel, not sequentially.

Security-relevant uses of VHDL:
- Implementing AES, RSA, or SHA in hardware
- Building hardware security modules (HSMs)
- Side-channel resistant crypto implementations
- ChipWhisperer FPGA targets for fault injection research
- Secure boot hardware enforcement

## Why It Matters

- Many embedded security devices (smartcards, TPMs, HSMs) use FPGA or ASIC designs
- Hardware crypto implementations can be attacked with power analysis (SPA/DPA) — understanding VHDL helps you analyze them
- Secure boot enforcement is often implemented in programmable logic
- Reverse engineering FPGA bitstreams is an emerging area of hardware security research

## VHDL Structure

Every VHDL design has two parts: an **entity** (the interface) and an **architecture** (the implementation).

```vhdl
-- Entity: describes inputs and outputs
entity AND_GATE is
    port (
        A : in  std_logic;
        B : in  std_logic;
        Y : out std_logic
    );
end AND_GATE;

-- Architecture: describes behavior
architecture Behavioral of AND_GATE is
begin
    Y <= A and B;
end Behavioral;
```

## Data Types

The most important VHDL types for digital logic:

| Type | Description | Example |
|------|-------------|---------|
| `std_logic` | Single bit: 0, 1, Z (high-impedance), X (unknown) | `signal clk : std_logic` |
| `std_logic_vector` | Multi-bit bus | `signal data : std_logic_vector(7 downto 0)` |
| `integer` | Integer number | `signal count : integer range 0 to 255` |
| `boolean` | True/false | `signal enable : boolean` |

```vhdl
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;
```

These library imports are needed for `std_logic` and arithmetic operations.

## D Flip-Flop

A flip-flop stores one bit of state. This is the building block of registers, counters, and state machines:

```vhdl
entity D_FF is
    port (
        clk : in  std_logic;
        rst : in  std_logic;
        D   : in  std_logic;
        Q   : out std_logic
    );
end D_FF;

architecture Behavioral of D_FF is
begin
    process(clk, rst)
    begin
        if rst = '1' then
            Q <= '0';
        elsif rising_edge(clk) then
            Q <= D;
        end if;
    end process;
end Behavioral;
```

## XOR Block (Cipher Building Block)

XOR is the foundation of many stream ciphers and block cipher rounds:

```vhdl
entity XOR_BLOCK is
    port (
        plaintext : in  std_logic_vector(7 downto 0);
        key       : in  std_logic_vector(7 downto 0);
        ciphertext: out std_logic_vector(7 downto 0)
    );
end XOR_BLOCK;

architecture Behavioral of XOR_BLOCK is
begin
    ciphertext <= plaintext xor key;
end Behavioral;
```

This is a 1-round XOR cipher — trivially broken but the pattern is the same for AES S-box implementations.

## VHDL and Side-Channel Attacks

When a hardware device computes AES, the power it draws correlates with the data being processed. VHDL implementations that are not hardened against side channels leak key material through:
- **Power traces**: current drawn at each clock cycle
- **EM emissions**: electromagnetic radiation from switching logic

A naive VHDL AES S-box:

```vhdl
-- Vulnerable: power consumption varies with sbox_out value
sbox_out <= SBOX(to_integer(unsigned(plaintext)));
```

A side-channel hardened implementation would use **masking** — XOR all intermediate values with a random mask so that power consumption does not correlate with secret data.

## Simulation and Testing

VHDL designs are tested with a **testbench** — a simulation that drives inputs and checks outputs:

```vhdl
entity AND_GATE_TB is
end AND_GATE_TB;

architecture Behavioral of AND_GATE_TB is
    component AND_GATE
        port (A, B : in std_logic; Y : out std_logic);
    end component;
    signal A, B, Y : std_logic;
begin
    uut : AND_GATE port map (A => A, B => B, Y => Y);

    process
    begin
        A <= '0'; B <= '0'; wait for 10 ns;
        A <= '0'; B <= '1'; wait for 10 ns;
        A <= '1'; B <= '0'; wait for 10 ns;
        A <= '1'; B <= '1'; wait for 10 ns;
        wait;
    end process;
end Behavioral;
```

## Tools

```bash
# GHDL — open-source VHDL simulator
ghdl -a and_gate.vhd          # analyze (compile)
ghdl -e AND_GATE               # elaborate
ghdl -r AND_GATE --wave=out.ghw  # run simulation

# Vivado (Xilinx/AMD) — industry FPGA toolchain
# Quartus (Intel) — alternative FPGA toolchain

# GTKWave — view waveform output
gtkwave out.ghw
```

## Resources

- [GHDL — Open Source VHDL Simulator](https://ghdl.github.io/ghdl/)
- [VHDL Reference Manual — IEEE 1076](https://ieeexplore.ieee.org/document/8938196)
- [ChipWhisperer — FPGA-based Hardware Security](https://www.newae.com/chipwhisperer)
- [FPGAwars — Free VHDL Learning](https://github.com/Obijuan/open-fpga-verilog-tutorial)
- [Practical Side-Channel Attacks — CHES Papers](https://ches.iacr.org/)
