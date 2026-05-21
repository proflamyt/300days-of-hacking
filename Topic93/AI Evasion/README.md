
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


Goals :
We want the model to predict the image , which should clearly show as a dog to human as a tree_frog 
TARGET_CLASS = 31      # tree_frog
THRESHOLD    = 0.95    # stop when frog confidence exceeds this
