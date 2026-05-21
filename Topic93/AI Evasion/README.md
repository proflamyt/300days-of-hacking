---
title: "AI Evasion — Adversarial Images"
topic: "ai-evasion"
tags: [ai, machine-learning, adversarial-examples, evasion, security]
difficulty: intermediate
day: 93
layout: default
parent: Topics
nav_order: 93
---

# Adversarial Image

## What You Will Learn

- What an adversarial image is and why it fools AI models
- How an image classifier "sees" a picture compared to how we see it
- How tiny pixel changes (invisible to us) can completely flip a model's prediction
- How to craft an adversarial example step by step, with real code

---

## What Do You See?

<img width="360" height="640" alt="adversarial" src="https://github.com/user-attachments/assets/0b0f0108-5ce5-44e9-a820-b83eaa465b98" />

I'm pretty sure we all see a dog, right?

But if you ask an AI model what it sees, you might get a completely different answer. This image has actually been intentionally distorted to fool an image classifier into thinking it's a frog. And not just a soft guess either — the classifier predicts "frog" with **95% confidence**.

That's the whole problem in one picture. What looks crystal clear to us as humans can be perceived in a totally different way by a machine learning model. This is what people call an **adversarial example**.

## So What Is an Adversarial Example?

In simple words:

> An input that has been intentionally modified so the model makes a mistake.

Example:

- Real image: **panda**
- Model says: **panda** ✅

After a tiny attack on the pixels:

- You still see a **panda**
- Model now says: **gibbon** ❌

The image barely changes to our eyes, but the model gets completely thrown off. That's the magic (and the danger) of adversarial examples.

---

## The Original Image

The modified image above actually came from this original picture. The model we're attacking is trained on **ImageNet**, a dataset used to classify 1000 different image classes.

<img width="360" height="640" alt="trixi" src="https://github.com/user-attachments/assets/f8188b5b-2d0b-4029-821f-f8d2b2a49e82" />

The model itself is a **MobileNet** — an AI image recognition model designed to run on devices with limited power, like phones and small edge devices.

<img width="714" height="290" alt="mobilenet architecture" src="https://github.com/user-attachments/assets/d76ce5eb-c4bb-4732-8fa8-04158d672185" />

When we feed the original dog image to the classifier, it gets it right. It predicts the breed as **malinois** with **88.2% certainty**, which is pretty solid. At the same time, it predicts "frog" at **0%** — meaning the model clearly sees this as a dog and has no doubt about it.

<img width="700" height="347" alt="dog prediction result" src="https://github.com/user-attachments/assets/b427b779-8567-4345-b240-8fdfac41e5ad" />

To double-check the model isn't broken, we also tested it on an actual frog image. It identified it correctly with **98.6% accuracy**. So the model knows what a frog looks like.

<img width="320" height="405" alt="frog test image" src="https://github.com/user-attachments/assets/ec0005b4-63a3-48fb-9217-47c006c88bc8" />

<img width="700" height="395" alt="frog prediction result" src="https://github.com/user-attachments/assets/a39df02c-fd85-4626-8e9a-ceea5b106a57" />

---

# Crafting the Adversarial Example

The goal here is to distort the dog image just enough that the model is fooled into thinking it's a frog — **without changing what we see**. To our eyes, it should still clearly look like a dog. To the model, it should look like a frog.

## The Goal

We want to nudge the dog image pixel by pixel until the model thinks it's a frog. The trick is to do it so subtly that a human can't tell anything changed.

Here's how we approach it:

### 1. Figure out where (and how much) to change the pixels

We basically ask the model:

> "If I brighten this pixel slightly, does the model become more or less convinced it's a frog?"

We ask this for every pixel at once by trying small random nudges and measuring how the model reacts. This gives us what's called the **gradient estimate** — think of it as a compass that tells us which way to walk to make the model more confident in the wrong answer.

### 2. Take a small step in that direction

Once we know the direction that pushes the model toward "frog", we move every pixel slightly that way. Then we immediately pull back any pixel that drifted too far from the original, because we don't want the image to visibly change to our eyes.

### 3. Check if the model is convinced enough

After each step, we print out the current top prediction and the frog confidence. If the frog confidence hits **95%**, we stop — the attack worked.

---

## Setting It Up

We want the model to predict our adversarial image (which is clearly a dog to a human) as `tree_frog` with more than **95% certainty**.

```python
TARGET_CLASS = 31      # tree_frog
THRESHOLD    = 0.95    # stop when frog confidence exceeds this
EPSILON      = 0.30
```

Every time we make a prediction, we calculate a **loss** value. This is a clear signal telling us how close we are to the target prediction "frog". If the loss drops to `0.0`, that means **100% confidence** the image is a frog.

## The Attack Loop

```python
x_adv = x_orig.copy()

for step in range(N_ITER):

    # Estimate gradient
    grad = np.zeros_like(x_adv)
    for _ in range(K):
        d     = (np.random.randint(0, 2, x_adv.shape).astype(np.float32) * 2 - 1)
        grad += (loss(np.clip(x_adv + d * nudge_size, 0, 255)) -
                 loss(np.clip(x_adv - d * nudge_size, 0, 255))) / (2 * nudge_size) * d
    grad /= K

    # Update and clip
    x_adv = x_adv - step_size * np.sign(grad)
    x_adv = np.clip(x_adv, x_orig - max_change, x_orig + max_change)
    x_adv = np.clip(x_adv, 0.0, 255.0)

    # Progress every 50 steps
    if (step + 1) % 50 == 0:
        label, conf, frog_conf = predict(x_adv)
        current_loss           = loss(x_adv)
        print(f"  Step {step+1:4d}/{N_ITER} | "
              f"top: {label:20s} ({conf:.1%}) | "
              f"frog: {frog_conf:.4f}% | "
              f"loss: {current_loss:.4f}")

        if frog_conf >= THRESHOLD:
            print(f"\n  Attack succeeded at step {step+1}!")
            break
```

---

## The Result

After running the attack, the final image fools the model with **99.6% confidence** that it's a frog.

<img width="800" height="345" alt="attack success output" src="https://github.com/user-attachments/assets/d49e1baa-37f8-462d-8281-c4790b2e216f" />

And here's the interesting part — the single pixel that changed the most only shifted by **76.5 out of 255**. That's about **30%** of the full brightness range, and only for one pixel. On average, every pixel shifted by just **34 out of 255**. Small enough that to your eyes, the image still looks like the same dog.

<img width="800" height="520" alt="final adversarial image comparison" src="https://github.com/user-attachments/assets/e3b6d371-be72-4dba-9041-af2da6485f00" />

## Why This Matters

This isn't just a cool trick. Adversarial examples are a real security concern for any system that depends on AI vision:

- **Self-driving cars** could be tricked into misreading a stop sign
- **Face recognition** systems could be bypassed with carefully crafted patterns
- **Content moderation** AI could be fooled into letting harmful content slip through
- **Malware classifiers** can be evaded by adversarially modified binaries

The model isn't broken — it's actually really good at its job. The problem is that it learned patterns we don't fully understand, and those patterns can be exploited.

## Resources

- [Goodfellow et al. — "Explaining and Harnessing Adversarial Examples"](https://arxiv.org/abs/1412.6572)
- [OpenAI blog — Attacking Machine Learning with Adversarial Examples](https://openai.com/research/attacking-machine-learning-with-adversarial-examples)
- [CleverHans library — adversarial attacks toolkit](https://github.com/cleverhans-lab/cleverhans)
- [Foolbox — Python toolbox for adversarial attacks](https://github.com/bethgelab/foolbox)
- [MobileNet paper](https://arxiv.org/abs/1704.04861)
