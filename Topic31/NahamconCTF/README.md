# NahamCon CTF 2023 

I had a very interesting weekend playing this, although i had a hard time battling with bad internet coverage and very little time at hand (new location lol), was still able to get 257th place out of 2577 teams and 5725  players.
Well, point is, i learnt a great deal and had an interesting weekend.

Here are some of the writeups for the challenges i managed to solved. As always i will go over my thought process and how i approached the challenges

## Zombie
- Category: Misc
- Difficulty: Easy

The challenge provided an ssh credential to a linux instance, after logging in, I did some basic enumeration to know the details of the instance i am currently on. The priviledges i have and other users of the system.



Now that i knew where i was, i listed the current directory of the home user with, showing the permissions and the files including hidden once in that directory

```
ls -al
```

![](https://github.com/proflamyt/300days-of-hacking/blob/main/Topic31/NahamconCTF/Screenshot%20from%202023-06-18%2011-41-04.png)

One of the files in particular caught my attension *.user-entrypoint.sh* , it's a script that would have caught your attention too, checking the content of the script a particular line was **nohup tail -f /home/user/flag.txt >/dev/null 2>&1**.

Now, what does the 'nohup' comand do, a quick google search showed me the "nohup" is a short for "no hang up." it is a command that allows a process to continue running even after the user who started the process has logged out or terminated their session.
In short "zombie process", that makes sense now, Now you would see one the reason you are always adviced to close files after opening with "fclose()" or use "with" in python.

You see, when you open a file, thread, socket, etc in a process, the operating system assigns a Handle (windows) / File discriptor (unix) to them. Its a non negative number, The defaults ones on unix are :

- 0 : stdin
- 1 : stdout
- 2 : stderr

Back to our command, a file **/home/user/flag.txt**'s last part was read with *tail* command, the output was redirected into oblivion "/dev/null", if any errors exits (stderr) its redirected to the same location as the standard output which is redirected to oblivion.

**nohup** makes me suspect the process still exists in memory, so i did what any of you would do, i checked the process running with **ps -aux** , I saw the tail command with process ID 11, so i checked where linux keeps it process-related information. The **/proc** folder for that particular process ID,
**/proc/11**, then i checked it's file discriptor directory **/proc/11/fd** for opened file descriptors, the redirected output to **/dev/null** ensures that neither stdout nor stderr will have any significant output or error messages. So i checked the fd 3, and eureka !!, The Flag.



