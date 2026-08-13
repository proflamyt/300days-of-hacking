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


# Voltage Glitching

```py
value = 20
value_1 = 30
value_2 = 30
sum = value + value_1 + value_2

if sum == 80:
    print("Normal Execution")
else:
    print("How Could this ever happen")
```

Under normal execution, this program should always print `Normal Execution`. We trust the CPU to correctly perform the calculation `20 + 30 + 30`, which should always give us `80`.

But what if we mess with the "brain" of the computer while it is running the program?

If we introduce a voltage glitch at just the right moment, we can sometimes interfere with what the CPU is doing. During the calculation, the CPU might not behave exactly as it normally would, and we could end up with an unexpected result.

For example, instead of getting `80`, imagine that the CPU somehow ends up with a different value. When that happens, the condition `sum == 80` is no longer true, and the program takes a path that it normally would never take.

This is what we are trying to achieve with voltage glitching. We intentionally disturb the CPU while it is performing a particular operation and try to influence the result.

The tricky part is **timing**. We need to glitch the CPU at roughly the right moment. If we glitch it too early, we might affect a different operation. Too late, and the calculation may already be finished. If the glitch is too strong, we might simply make the CPU crash or reset.

So the goal is not just to make the CPU fail. We want to disturb it at the right moment so that it keeps running, but the specific operation we care about doesn't behave quite as it normally would.

## Glitching Our First Hardware Example From Hextree

Now that we have a basic idea of what a voltage glitch is doing to the CPU, let's try it on an example hardware target.

For this experiment, we need two things:

* **Glitch Tag** — the hardware we want to glitch.
  
  <img width="1060" height="2080" alt="67992" src="https://github.com/user-attachments/assets/0ae27c4b-4ce2-4fd8-9c13-3332a05995ef" />

* **Faultier** — the hardware tool we will use to generate and precisely control the voltage glitch.

  <img width="1060" height="2080" alt="20260807_185756" src="https://github.com/user-attachments/assets/9483da83-38dd-4fa3-9ab3-91db8686f5ad" />

We first need to put some custom code on the Glitch Tag. The idea is simple: we create a piece of code that normally behaves in a completely predictable way, and then try to disturb the CPU while it is executing that code.

```c
#define LOOP_LENGTH 100

void glitch_target() {
    // R - Indicates that the device reset
    print_uart("R");

    // =================================  < - glitch window
    // Generate a short trigger signal on IO 2
    gpio_pin_set_dt(&trigger, 1);
    k_msleep(10);
    gpio_pin_set_dt(&trigger, 0);

    uint32_t cnt = 0, i, j;

    for (i = 0; i < 100; i++)
    {
        for (j = 0; j < 100; j++)
        {
            cnt++;
        }
    }

    // Counter should be exactly LOOP_LENGTH * LOOP_LENGTH
    if (i != 100 || j != 100 || cnt != (100 * 100))
    {
        // Counter does not match!
        // X = Success!
        print_uart("X");
        print_uart("HXT{...}"); // Flag
    } else {
        // N = Normal execution
        print_uart("N");
    }

    // Endless loop
    while (1) {}
}
```

This sample program runs on the Glitch Tag. It first prints `"R"` over UART to indicate that the device has reset. It then generates a pulse on the trigger pin before starting the nested loops.

Under normal execution, the loops always perform the same number of iterations. The outer loop runs 100 times, the inner loop runs 100 times for each outer iteration, and `cnt` is therefore incremented exactly `100 × 100` times.

When the loops finish, `i` and `j` have both reached `100`, and `cnt` is `10000`. Because of this, the condition inside the `if` statement should be false during normal execution, so the program should reach the `else` branch and print `"N"`.

In other words, we have created a small piece of code with a very predictable outcome. Under normal conditions, it should always follow the same path.

### Using a Trigger

The next problem is timing. We don't know exactly when the CPU will be executing the part of the program we want to disturb.

This is where the **trigger signal** comes in.

The program generates a pulse on a GPIO pin just before entering the code we want to target:

```c
gpio_pin_set_dt(&trigger, 1);
k_msleep(10);
gpio_pin_set_dt(&trigger, 0);
```

This gives the Faultier a timing reference. The trigger line briefly goes high to 5 V, signaling that the loop is about to begin.

```text
        __________
_______|          |_______
```

When the pin goes high, the Faultier can detect that transition and use it as a reference for when to apply the glitch. The trigger does not magically tell us the exact CPU instruction currently being executed, but it gives us a repeatable point in the program from which we can measure our glitch timing.

From the software's point of view, everything is predictable. The loops increment `cnt`, the counters reach their expected values, and the final check succeeds.

But underneath all of this, the CPU is executing a stream of machine instructions. The counters are represented by values held in registers and, depending on the compiler and architecture, possibly memory as well. The processor is repeatedly loading values, incrementing them, comparing them, and branching through the loops.

What happens if we briefly disturb the CPU while it is doing all of this?

This is where voltage glitching becomes interesting.

The goal is not to shut the device down or force it to reset. Instead, we want to lower the supply voltage for a very short period so that the CPU is disturbed while executing the instructions we care about.

A successful glitch can cause the processor to behave differently from normal. Depending on the hardware and exactly where the glitch lands, an instruction or computation may produce an unexpected result, a register may contain an incorrect value, or a control flow decision may behave differently.

If we manage to affect the loops or the instructions involved in the final check, one of the values may no longer be what the program expects. That could cause the condition to become true and send execution into the branch that prints the flag.

And this is where the real challenge begins.

We need to find **when** to inject the glitch and **how long** it should last.

A glitch that is too early may affect code we don't care about. One that is too late may miss the interesting operation completely. A glitch that is too short may have no observable effect, while a glitch that is too long or too severe may simply crash or reset the processor.

We can think of this as searching for the right combination of **offset** — when the glitch happens relative to the trigger — and **width** — how long the voltage disturbance lasts.

Finding that sweet spot, where the CPU is disturbed just enough to behave differently but still continues running, is the core of the experiment.

# Causing a Voltage Glitch with Faultier

Now that we have our target program, let's look at the hardware setup we'll use to actually cause the voltage glitch.

**Faultier** is the tool we will use to control the glitching process, while the firmware running on the **Glitch Tag** is the program we are trying to interfere with.

## Glitch Tag

The Glitch Tag needs three things from our setup: **power, communication, and a way to inject the glitch**.

### Power

First, we need to power the Glitch Tag. For this experiment, the Faultier will provide the power.

We connect the Glitch Tag's **VCC** to **MUX 0** on the Faultier and connect **GND** to one of the Faultier's ground pins.

### Communication

We also need a way for the Glitch Tag to communicate with us so we can see what the program is doing.

We will use **GPIO 0** for UART output. The tag sends its `R`, `N`, and `X` messages through this pin, so we connect it to the **RX** pin on the Faultier.

**GPIO 2** is used for the trigger signal. Remember the trigger we added to the program earlier? When the code reaches that point, GPIO 2 produces a pulse. We connect this pin to **EXT0** on the Faultier so it can detect that pulse and use it as a timing reference for the glitch.

So, at a high level, our connections look like this:

```text
Glitch Tag                  Faultier

VCC        ----------------> MUX 0
GND        ----------------> GND

GPIO 0     ----------------> RX
             UART output

GPIO 2     ----------------> EXT0
             Trigger
```

There is one more important part of the setup: **the glitch itself**.

The Glitch Tag has already been modified to make voltage glitching much easier. The board exposes the appropriate connection to the CPU's power supply, so the Faultier can disturb the CPU's supply voltage directly instead of us having to modify the board ourselves.

The technique being used here is **crowbar glitching**. In simple terms, the Faultier briefly creates a low-resistance path that pulls the target's supply voltage down for a very short period. This creates the voltage disturbance that we are trying to use to interfere with the CPU's execution.

So our setup is fairly simple: the Faultier powers the Glitch Tag, receives its UART output, watches for the trigger signal, and generates the voltage glitch. The interesting part is now finding the right **timing and duration** for that glitch.






# Getting the Flag with Faultier

Before we start glitching the CPU, let's first make sure we can communicate with the Glitch Tag.

```text
Laptop  <---- UART ---->  Faultier  <---- UART ---->  Glitch Tag
```

Our laptop talks to Faultier through `pySerial`, while Faultier communicates with the Glitch Tag over UART. Since the tag's VCC is connected to **MUX 0**, Faultier can also control its power.

First, we configure the power cycle:

```python
ft.configure_glitcher(
    power_cycle_output=faultier.OUT_MUX0,
    power_cycle_length=300000
)
```

`OUT_MUX0` tells Faultier which output controls the target's power. `power_cycle_length=300000` means the power stays off for **300,000 ns (300 µs)** before being restored.

We can then power-cycle the tag and read its UART output:

```python
ft.power_cycle()
print(ser.read(5))
```

The goal here is simple: make sure Faultier can power the tag, the tag boots normally, and we can receive its output.

Power cycling is also useful during the actual glitching experiment. We may miss the timing window, or a glitch may cause the CPU to crash or end up in an unexpected state. Being able to quickly power-cycle the Glitch Tag gives us a clean restart so we can try the glitch again.


## Searching for the Right Glitch Timing

The next part is where we actually start searching for a glitch that affects the code we care about.

```python
ft.configure_glitcher(
    power_cycle_output=faultier.OUT_MUX0,
    power_cycle_length=300000,
    trigger_source=faultier.TRIGGER_IN_EXT0,
    trigger_type=faultier.TRIGGER_PULSE_POSITIVE,
    glitch_output=faultier.OUT_CROWBAR
)
```

Here, we are telling Faultier how to interact with our target.

`trigger_source = faultier.TRIGGER_IN_EXT0` tells Faultier to use the signal coming from **EXT0** as its timing reference. This is the trigger signal connected to GPIO 2 on the Glitch Tag.

`trigger_type = faultier.TRIGGER_PULSE_POSITIVE` tells Faultier to start its timing when it detects the rising edge of that pulse.

Finally, `glitch_output = faultier.OUT_CROWBAR` tells Faultier to use its crowbar output to generate the voltage glitch.

Now we can start trying different timings:

```python
for d in range(0, 100000):
    for p in range(0, 10):
        if ser.in_waiting:
            ser.read(ser.in_waiting)

        ft.glitch(delay=d, pulse=p)
        data = ser.read(3)

        if b"X" in data:
            print(f"Success! Delay: {d} Pulse: {p}")
            print(ser.read(50))
```

The two loops perform a **brute-force search**. We don't know exactly when the CPU will be executing the instructions we want to affect, so we try many different combinations of timing values.

`delay=d` controls the timing of the glitch relative to the trigger, while `pulse=p` controls the glitch pulse setting.

Before each attempt, we clear any old UART data:

```python
if ser.in_waiting:
    ser.read(ser.in_waiting)
```

This makes sure we're looking at the output from the current attempt rather than leftover data from an earlier one.

We then tell Faultier to perform the glitch:

```python
ft.glitch(delay=d, pulse=p)
```

After the attempt, we read the tag's UART output:

```python
data = ser.read(3)
```

and check whether it contains `"X"`:

```python
if b"X" in data:
```

Remember that `"X"` is what our firmware prints when the values don't match what we expect. So finding an `X` tells us that this particular glitch attempt produced the condition we were looking for.

When that happens, we print the parameters that worked:

```python
print(f"Success! Delay: {d} Pulse: {p}")
```

Now we know which `delay` and `pulse` values produced the successful result.

The nice part is that we don't have to find the timing by hand. Faultier simply tries a large number of combinations until one of them causes the target to behave differently from its normal execution.

