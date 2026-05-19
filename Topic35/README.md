---
title: "RTOS (Real-Time Operating System)"
topic: "rtos"
tags: [rtos, embedded, real-time, freertos, interrupt, scheduling, microcontroller]
difficulty: advanced
day: 35
layout: default
parent: Topics
nav_order: 35
---

# RTOS (Real-Time Operating System)

## What You Will Learn
- What an RTOS is and how it differs from a general-purpose OS
- How tasks and scheduling work in an RTOS
- What interrupts are and why they matter in real-time systems
- Common RTOS security issues

## What Is It?

A **Real-Time Operating System (RTOS)** is an operating system designed for systems that must respond to events within a **guaranteed time limit** (deadline). Missing a deadline in a real-time system can mean a physical failure — think of anti-lock brakes, pacemakers, or industrial control systems.

Unlike general-purpose operating systems (Linux, Windows), an RTOS prioritizes **predictability** over throughput. It may process fewer tasks overall, but it guarantees when each task will run.

## Why It Matters

RTOS systems are everywhere in embedded devices:
- Automotive ECUs (engine control units)
- Medical devices (insulin pumps, ventilators)
- Industrial PLCs
- Aerospace systems
- IoT firmware

These systems are increasingly targeted by attackers because they often have no memory protection, no ASLR, and minimal security features.

## Key Concepts

### Hard vs. Soft Real-Time

| Type | Deadline Behavior |
|------|------------------|
| **Hard Real-Time** | Missing a deadline causes system failure (e.g., airbag controller) |
| **Soft Real-Time** | Missing a deadline degrades performance but is acceptable (e.g., video streaming) |

### Tasks and Scheduling

In an RTOS, work is divided into **tasks** (similar to threads). Each task has a **priority**. The scheduler always runs the highest-priority ready task.

```c
// FreeRTOS task creation example
void vTaskFunction(void *pvParameters) {
    while (1) {
        // Do work
        vTaskDelay(100 / portTICK_PERIOD_MS); // sleep 100ms
    }
}

// Create a task with priority 1
xTaskCreate(vTaskFunction, "Task1", 128, NULL, 1, NULL);
```

### Interrupts

An **interrupt** is a hardware or software signal that pauses the current task and runs an **Interrupt Service Routine (ISR)**. ISRs must be short and fast because they block the scheduler.

```c
// FreeRTOS ISR example
void UART_IRQHandler(void) {
    BaseType_t xHigherPriorityTaskWoken = pdFALSE;
    
    // Notify a task from ISR
    vTaskNotifyGiveFromISR(xTaskToNotify, &xHigherPriorityTaskWoken);
    
    // Yield if a higher priority task was unblocked
    portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
}
```

### Common Scheduling Algorithms

- **Preemptive Priority**: Highest priority task always runs. Used in most RTOSes.
- **Round-Robin**: Tasks at the same priority share CPU time equally.
- **Rate-Monotonic**: Higher frequency tasks get higher priority (theoretical model).

### Inter-Task Communication

Tasks communicate through:
- **Queues**: Safe message passing between tasks
- **Semaphores**: Signaling between tasks (like a flag)
- **Mutexes**: Protect shared resources from concurrent access

```c
// Create a queue that holds 10 integers
QueueHandle_t xQueue = xQueueCreate(10, sizeof(int));

// Send to queue from one task
int value = 42;
xQueueSend(xQueue, &value, portMAX_DELAY);

// Receive in another task
int received;
xQueueReceive(xQueue, &received, portMAX_DELAY);
```

## RTOS Security Issues

- **No memory isolation**: Tasks share the same address space — a buggy task can corrupt another
- **Priority inversion**: A low-priority task holds a mutex needed by a high-priority task
- **Timing side channels**: Precise timing of ISRs can leak information
- **Stack overflows**: RTOS stacks are fixed-size; overflow is silent unless stack checking is enabled

## Resources

- [FreeRTOS — Open-source RTOS](https://www.freertos.org/)
- [Zephyr RTOS — Linux Foundation embedded OS](https://zephyrproject.org/)
- [CWE-362 — Concurrent Execution Race Condition](https://cwe.mitre.org/data/definitions/362.html)
- [TryHackMe — Embedded Systems Security](https://tryhackme.com/)
- [James Grenning — Test-Driven Development for Embedded C](https://pragprog.com/titles/jgade/test-driven-development-for-embedded-c/)
