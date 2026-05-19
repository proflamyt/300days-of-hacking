---
title: "Fault Injection"
topic: "fault-injection"
tags: [fault-injection, voltage-glitching, clock-glitching, em-fault-injection, hardware-security]
difficulty: advanced
day: 85
layout: default
parent: Topics
nav_order: 85
---

# Fault Injection

## What You Will Learn
- What fault injection is and how it differs from side channel analysis
- How voltage, clock, and electromagnetic fault injection work
- Key parameters for a voltage glitch attack
- What targets are vulnerable to fault injection

## What Is It?

**Fault injection** is a hardware attack technique that deliberately introduces errors into a running system to cause unexpected behavior. Unlike side channel attacks (which passively observe), fault injection **actively disrupts** execution.

The goal is often to:
- Skip a security check (e.g., skip a PIN verification)
- Force a branch to take the wrong path
- Corrupt a cryptographic operation to leak key material

## Why It Matters

- Smartcards, microcontrollers, and secure elements are common targets
- Bypasses software security without needing the source code
- Used in hardware hacking competitions and embedded device security research
- Countermeasures are expensive to implement correctly

## Types of Fault Injection

### Electromagnetic Fault Injection (EMFI)

An electromagnetic probe is placed near the target chip. A strong EM pulse induces currents that cause bit flips or instruction skips.

EMFI can be highly targeted — focusing on a specific area of a chip.

### Voltage Fault Injection (VFI)

The supply voltage to the chip is briefly dropped or spiked. The chip's logic receives insufficient power for a brief moment — causing incorrect computations or skipped instructions.

This is called **voltage glitching**.

### Clock Fault Injection

The clock signal is manipulated — injecting extra clock edges or temporarily speeding up the clock. This causes the CPU to execute instructions out of order or skip setup time requirements.

## Voltage Glitch Parameters

A voltage glitch attack requires tuning three key parameters:

- **Pulse length**: How long to drop (or spike) the voltage
- **Delay**: Time before the voltage drop (relative to a trigger signal)
- **Trigger**: The event that starts the delay countdown (e.g., a specific GPIO signal, start of communication)

```
Voltage
|
|
|----------------------------------------         -------------
|                                        \       /
|                                         \ _ _ /    <-- glitch
|
|
|_____________________________________________Time

             Delay
<------------------------------->
                                  Pulse Length
                                 <------------>
```

## Voltage Glitch Attack Flow

1. **Identify the target operation** — what instruction to corrupt (e.g., PIN check, signature verification)
2. **Set up a trigger** — find a signal that fires just before the target (e.g., UART activity, GPIO toggle)
3. **Set the delay** — tune delay to match when the target instruction executes
4. **Set the pulse length** — short enough to glitch, long enough to have effect
5. **Repeat** — glitching requires many attempts due to randomness in timing

## Example: Bypassing PIN Check

```
Normal execution:
  cmp pin_input, correct_pin
  jne wrong_pin            ← want to skip this
  jmp authenticated

Glitched execution (skip the jne):
  cmp pin_input, correct_pin
  ; jne skipped due to glitch
  jmp authenticated        ← now always executes
```

## Tools and Hardware

- **ChipWhisperer** — open-source hardware/software for fault injection and side channel analysis
- **PicoEMP** — low-cost EMFI tool
- **Custom voltage glitcher** — FPGA or microcontroller with fast GPIO

```python
# ChipWhisperer glitch example
import chipwhisperer as cw

scope = cw.scope()
scope.glitch.clk_src = "clkgen"
scope.glitch.output = "enable_only"
scope.glitch.trigger_src = "ext_single"
scope.glitch.repeat = 1
scope.glitch.width = 10      # pulse width in cycles
scope.glitch.offset = 0      # offset from trigger
```

## Countermeasures

- **Voltage monitoring**: Detect drops below threshold and reset/lock device
- **Clock monitoring**: Detect unexpected clock edges
- **Redundant computation**: Execute critical code multiple times and compare
- **Voltage regulators**: LDO regulators smooth voltage glitches
- **Glitch detectors**: On-chip sensors that detect fault injection attempts and trigger a lockout

## Resources

- [ChipWhisperer — Open-Source Fault Injection](https://www.newae.com/chipwhisperer)
- [Riscure — Introduction to Fault Injection](https://www.riscure.com/fault-injection/)
- [Colin O'Flynn — Hardware Hacking Techniques](https://www.youtube.com/@ColinOFlynn)
- [TryHackMe — Hardware Hacking](https://tryhackme.com/room/hardwarehacking101)
- [CHES Conference — Hardware Security Research](https://ches.iacr.org/)
