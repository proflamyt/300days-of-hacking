# NahamCon CTF 2023 

I had a very interesting weekend playing this, although i had a hard time battling with bad internet coverage and very little time at hand (due projects & new location lol), was able to get 257th place out of 2577 teams and 5725  players.
Well, point is, i learnt a great deal and had an interesting weekend.

Here are some of the writeups for the challenges i managed to solved. As always i will go over my thought process and how i approached the challenges

## Zombie
- Category: Misc
- Difficulty: Easy

The challenge provided a ssh credential to a linux instance, after logging in, I did some basic enumeration to know the details of the instance i am currently on. The priviledges i have and other users of the system.



Now that i knew where i was, i listed the current directory of the home user with, 

```
ls -al
```

showing the permissions and the files including hidden once in that directory


![](https://github.com/proflamyt/300days-of-hacking/blob/main/Topic31/NahamconCTF/Screenshot%20from%202023-06-18%2011-41-04.png)

One of the files in particular caught my attension *.user-entrypoint.sh* , it's a shell script that would have caught your attention too, checking the content of the script a particular line was **nohup tail -f /home/user/flag.txt >/dev/null 2>&1**.

Now, what does the 'nohup' command do, a quick google search showed me the "nohup" is a short for "no hang up." it is a command that allows a process to continue running even after the user who started the process has logged out or terminated their session.

In short "zombie process", that makes sense now, Now you would see one the reason you are always adviced to close files after opening with "fclose()" or use "with" in python.

You see, when you open a file, thread, socket,... etc in a process, the operating system assigns a Handle (windows) / File discriptor (unix) to them. Its a non negative number which the OS uses as handles or references that allow processes to interact with these resources.

The defaults ones on unix are :

- 0 : stdin
- 1 : stdout
- 2 : stderr

Back to our command, a file **/home/user/flag.txt**'s last part was read with *tail* command, the output was redirected into oblivion "/dev/null", if any errors exits (stderr) its redirected to the same location as the standard output which is redirected to oblivion.

**nohup** makes me suspect the process still exists in memory, so i did what any of you would do, i checked the process running with **ps -aux** , I saw the tail command with process ID 11, so i checked where linux keeps it process-related information.

![](https://github.com/proflamyt/300days-of-hacking/blob/main/Topic31/NahamconCTF/Screenshot%20from%202023-06-17%2013-17-28.png)


The **/proc** folder for that particular process ID, **/proc/11**, then i checked it's file discriptor directory **/proc/11/fd** for opened file descriptors, the redirected output to **/dev/null** ensures that neither stdout nor stderr will have any significant output or error messages. So i checked the fd 3, and eureka !!, The Flag.

![](https://github.com/proflamyt/300days-of-hacking/blob/main/Topic31/NahamconCTF/Screenshot%20from%202023-06-17%2013-17-07.png)




## Fortune Teller

Category: Android


The Chalenge provided an apk file. 

![image](https://github.com/proflamyt/300days-of-hacking/assets/53262578/81dbdf75-cbbc-4a52-9fdd-881949021d84)

Opening the apk file in an android emulator, i was greeted with just an activity which asks me to guess a word, everytime I input a word it brings a popup that says **Hello toast!**. Alright, what is happening underneath the hood ? , i had the same question. 

So, I passed the apk through one of my favourite decompiler, jadx-gui. Now it is important to understand when decompiling it easy to get lost in a ton of information relevant and irrelevant to what you have as your goal. with this in mind, I had a specific goal in mind **Get the correct guess word**.

The first place i visited was the android MainActivity, This is the logic behind the first page we saw. Remember don't get lost with the tons of information you get from decompiling, the developers probably spent months writing, debugging, testing this code, you stand no chance !!.

Getting to the main activity, i saw an interesting method depicting what the application is doing underneath the hood.


![image](https://github.com/proflamyt/300days-of-hacking/assets/53262578/63f4de8d-7438-43d1-b383-34ba420cf5e5)


```java
    public final void guess(View v) {
        Intrinsics.checkNotNullParameter(v, "v");
        Companion companion = Companion;
        companion.setGuessString(getGuessInput().getText().toString());
        String string = getString(C0881R.string.correct_guess);
        Intrinsics.checkNotNullExpressionValue(string, "getString(R.string.correct_guess)");
        setCorrectString(string);
        if (Intrinsics.areEqual(companion.getGuessString(), getCorrectString())) {
            ImageView imageView = new ImageView(this);
            setContentView(imageView);
            getDecrypt().decrypt(this);
            Bitmap bitmap = BitmapFactory.decodeFile(getDecrypt().getOutputFile().getAbsolutePath());
            imageView.setImageBitmap(bitmap);
            return;
        }
        Toast toast = Toast.makeText(this, "Hello toast!", 0);
        toast.show();
    }
```



The method takes our provided input (guess word) and gets an already stored word, which is the correct word. It compares both , if it is equal , it sends our input to decrypt an image, if not equal, it shows a toast that says "Hello toast!". Now the next step is to look for what word is this method comparing our input with.

```
String string = getString(C0881R.string.correct_guess);
```

This line of code here is the line responsible for fetching the stored string. following **C0881R.string.correct_guess** i came across this line of code here 

```
public static final int correct_guess = 2131755048;

```
![image](https://github.com/proflamyt/300days-of-hacking/assets/53262578/21093c47-faa0-4783-b7d3-50e3b4660021)


One may think **correct_guess** variable is the correct word , wrong !!. This is an id to the word i am looking for, the function  getString() in android takes in a name and used it to retrieve localized string resources from the application's resource files. The application resource file for string is located in **res/values/strings.xml**. 

Armed with the name refrence and where to look for, i went ahead to the file and looked for **correct_guess** in the xml file .

![image](https://github.com/proflamyt/300days-of-hacking/assets/53262578/e105dcaf-fdc8-43ac-84d8-464ae606d6e1)

voila !! , the value of the string is **you win this ctf**

![image](https://github.com/proflamyt/300days-of-hacking/assets/53262578/215ad341-e948-445e-a9ad-c4ee48b74de3)


putting this as the guess word, displayed the flag !!




##  JNInjaspeak

Category: Android


![image](https://github.com/proflamyt/300days-of-hacking/assets/53262578/0c82951d-b144-4cc0-a8bc-2d0572194758)



The Chalenge provided an apk file. 

I had to run the application in an emulator, to see it work first before decompiling . It asked for my input and translates it to jinjaSpeak.

Upon decompiling the apk and checking it's MainActivity, i tracesd where my input **EditText** is ending at, 

![image](https://github.com/proflamyt/300days-of-hacking/assets/53262578/bbee462e-eb2a-4f4a-86ef-6cb44cc19139)

```
translate(companion.getTranslateString())
```

this line shows one the sink of my input, a translate function, tracing the translate function and where it is being imported, i discovered it's is a native function that takes string as argument.


![image](https://github.com/proflamyt/300days-of-hacking/assets/53262578/58e52055-c0f4-47f9-8de3-7f2a22c50f43)


A native function in Android refers to a function that is implemented in a native programming language like C or C++ and is called from the Java code of an Android application. These native functions provide a way to access low-level system functionalities, interact with native libraries, or optimize performance-critical tasks. 

Now i had to look for where the binary is being loaded into the android application, once i found that. i could deduce the name of the binary in question is **jninjaspeak**.

![image](https://github.com/proflamyt/300days-of-hacking/assets/53262578/2a202956-ddc2-46c8-b2e0-cd53de22e085)


So where are the binary files locate **/lib/<architecture>**,  I chose the 32bit binary x86 to decompile using ghidra, (i am more familiar with 32 bit architectures)


![image](https://github.com/proflamyt/300days-of-hacking/assets/53262578/44f896b1-7fed-43b7-a8f9-ffc8800f52eb)

    
After decompiling the binary in ghidra, i Found the flag being used to encrypt the input i supplied eearlier.
    
 ![image](https://github.com/proflamyt/300days-of-hacking/assets/53262578/24d0e2b3-b419-41e7-b456-dfe45942e5c6)








