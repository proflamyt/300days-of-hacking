
# Adverserial Image


What do you see? 

<img width="1080" height="1920" alt="adversarial" src="https://github.com/user-attachments/assets/0b0f0108-5ce5-44e9-a820-b83eaa465b98" />

I am sure we all see a dog right ?

If ask an AI model what it sees we may be getting a diffrent , Infact this image has been intentionally distorted to fool an image classifier it is a frog . This classfier predicts this as a frog with 95% probablility

The problem we see here is an example of an adverserial example whereby what looks so clear to humans can be perceived differently by a machine learning model



An adversarial example is:

An input intentionally modified so the model makes a mistake.

Example:

Real image: panda
Model says: panda

After tiny attack:
Human still sees panda
Model says: gibbon



The modified image i provided was infact from this original image , the model is trained on ImageNet , which is trained to classify 1000 classes of images 

<img width="1080" height="1920" alt="trixi" src="https://github.com/user-attachments/assets/f8188b5b-2d0b-4029-821f-f8d2b2a49e82" />



The provided model is a mobilenet, an AI image recognition model designed to run on devices with limited power


<img width="714" height="290" alt="image" src="https://github.com/user-attachments/assets/d76ce5eb-c4bb-4732-8fa8-04158d672185" />


Providing the original image (Dog) to this image classifier, we can see it predicts it correctly, getting the breed as malinois  with 88.2% certainty, which is pretty high . It predicts frog as 0% , meaning the model currently "sees" this clearly and in  no way see this as a frog


<img width="854" height="423" alt="image" src="https://github.com/user-attachments/assets/b427b779-8567-4345-b240-8fdfac41e5ad" />

We can also test the model by providing it an image of a frog , which it was able to identify with 98.6% accuracy 

<img width="395" height="500" alt="image" src="https://github.com/user-attachments/assets/ec0005b4-63a3-48fb-9217-47c006c88bc8" />


<img width="914" height="517" alt="image" src="https://github.com/user-attachments/assets/a39df02c-fd85-4626-8e9a-ceea5b106a57" />

# Adversarial Example


The goal is to distort this exact image seen by this model as a dog (malinois) without changing the human perceived appearace (We still see it as dog) while the model sees it as frog


Goal :

we want to nudge the dog image pixel by pixel until the model thinks it's a frog.


1. We want to Figure out where and by how muh to change the pixels

"If I brighten this pixel slightly, does the model become more or less convinced it's a frog?"
It asks this for every pixel simultaneously by trying random nudges and measuring the result.
This is the gradient estimate — it's a compass telling you which way to walk.

2. Take a small step in that direction, once we figure out the direction we took that makes it look more like a frog to the model

Move every pixel slightly toward making the model say "frog".
Then immediately pull back any pixel that has drifted too far from the original — we don't want the image to visibly change.

3. Then we check if the model is convinced enough 

Print the current top prediction and frog confidence.
If frog confidence hits 95%, stop — the attack worked.

We want the model to predict the image , which should clearly show as a dog to human as a tree_frog 


To proceed, we want the model to be convinced with > 95% certainty our adverseerial image (which is a dog) is infact a frog

```
TARGET_CLASS = 31      # tree_frog
THRESHOLD    = 0.95    # stop when frog confidence exceeds this
EPSILON = 0.30
```


We calculate the loss as a clear signal every time we make a prediction to check how close we are to the right prediction "frog". if the loss reduced to 0.0 that is 100% confidence


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


The final image produced gives a confidence of 99.6% 

<img width="853" height="368" alt="image" src="https://github.com/user-attachments/assets/d49e1baa-37f8-462d-8281-c4790b2e216f" />


The single pixel that changed the most shifted by 76.50 out of a possible 255. That's about 30% of the full brightness range for that one pixel ,  On average, every pixel shifted by 34 out of 255. The final image produced.

<img width="1139" height="741" alt="image" src="https://github.com/user-attachments/assets/e3b6d371-be72-4dba-9041-af2da6485f00" />


