# Voltage Fault Injection With Faultier Hextree

Modern CPUs are built from billions of tiny components called **transistors**. A transistor essentially acts as an incredibly small electrical switch. By combining these switches in different arrangements, processors can build logic circuits that perform calculations, make decisions, and store data.

For these circuits to work correctly, signals need enough time to propagate through the CPU and settle to the correct values. During a clock cycle, a signal travels through multiple transistors and logic gates, with each stage taking a small amount of time to respond to the change from the previous stage. By the time the appropriate clock edge arrives, the resulting signal should have settled to a voltage that clearly represents either a 0 or a 1, allowing the register to capture the correct value or passed to the next stage of the circuit. 

The clock effectively gives the circuit a fixed window of time to complete this process. If the signal has not reached the expected value by the time it is captured, the register may store the wrong value.

This is where **voltage fault injection** becomes interesting.

A voltage disturbance can temporarily change the electrical conditions under which the transistors operate. Depending on the timing and severity of the disturbance, some transistors may switch more slowly, switch incorrectly, or fail to produce the expected result within the available time.

For example, imagine a circuit that is supposed to produce a `1`. A voltage glitch occurs while the computation is in progress, disrupting one or more transistors along the way. The signal may fail to reach the expected voltage before the next clock edge, causing the CPU to capture an incorrect value.

But the effects of voltage glitching are not limited to computations. CPUs also contain circuits that **store state**, including registers and various forms of on-chip memory. These circuits use electrical signals to represent `0` and `1`, and those states need to remain stable.

A sufficiently strong voltage disturbance can reduce the circuit's **noise margin**, the amount of electrical variation it can tolerate and, in some circumstances, cause a stored value to change.

So, depending on where and when the fault occurs, a voltage disturbance can interfere with a computation, corrupt a stored value, alter the CPU's execution path, or cause the processor to crash.
