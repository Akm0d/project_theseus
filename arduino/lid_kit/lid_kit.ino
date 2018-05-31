// Arduino code for something something
// Kristian Sims
// Insert whatever OSS license here idk

#include <Keypad.h>
#include <Wire.h>

#define I2C_ADDRESS 0x70

// Set up keypad
#define NROWS 4
#define NCOLS 3
char keys[NROWS][NCOLS] = {
    {'1', '2', '3'},
    {'4', '5', '6'},
    {'7', '8', '9'},
    {'*', '0', '#'}
};
byte rows_pins[NROWS] = {5, 7, 12, 13};
byte cols_pins[NCOLS] = {A0, A1, A2};
// If the keypad isn’t behaving as expected, you may have to swap those:
// byte rows_pins[NROWS] = {A2, A1, A0, 13};
// byte cols_pins[NCOLS] = {12, 7, 5};```


Keypad keypad = Keypad(makeKeymap(keys), rows_pins, cols_pins, NROWS, NCOLS);
// Keypress buffer
#define BUFLEN 16
char key_buffer[BUFLEN];
int buffer_count = 0;

// LED Pins and 8-bit color scaling (which I made up, feel free to tweak)
#define LEDR 9
#define LEDG 10
#define LEDB 11

// Color maps for 8-bit color (vaguely logarithmic). Duty cycle is (255-x)/255.
byte led2bit[4] = {255, 191, 127, 0};  // 0%, 25%, 50%, 100%
byte led3bit[8] = {255, 223, 191, 159, 127, 63, 0, 0}; // w/e


void setup() {
    // Set up I2C as a slave
    Wire.begin(I2C_ADDRESS);
    Wire.onRequest(i2c_request);
    Wire.onReceive(i2c_receive);
    // Set up keypad. If you get duplicate keypress, increase debounce time. >200 is too much.
    keypad.setDebounceTime(50);
    keypad.addEventListener(keypad_event);
}

void loop() {
    // Nothing to do here. Sadly, Arduino will just spin forever anyway.
}

// On I2C read, return buffered characters, or a single "." for no keypress
void i2c_request() {
    if (buffer_count > 0) {
        Wire.write(key_buffer);
        // Clear buffer so string termination is automatic
        while (buffer_count > 0)
            key_buffer[--buffer_count] = 0;
    } else {
        Wire.write(".");
    }
}

// On I2C write, receive a value and light the LED
// Note that the LED pins are 5 V to pin, so lower PWM is a brighter light.
void i2c_receive(int byte_count) {
    if (byte_count == 1) {
        // If 1 byte sent, interpret as analog color
        byte b = Wire.read();
        analogWrite(LEDB, led2bit[b & 0x03]);
        b >>= 2;
        analogWrite(LEDG, led3bit[b & 0x07]);
        b >>= 3;
        analogWrite(LEDR, led3bit[b & 0x07]);
    } else if (byte_count == 3) {
        // If 3 bytes sent, interpret as raw values
        analogWrite(LEDR, 255 - Wire.read());
        analogWrite(LEDG, 255 - Wire.read());
        analogWrite(LEDB, 255 - Wire.read());
    } else {
        // Um, just ignore other byte counts, flush buffer
        while (Wire.available())
            Wire.read();
    }
}

// When a debounced keypress is detected, add it to the buffer
void keypad_event(KeypadEvent key) {
    if (keypad.getState() == PRESSED)
        if (buffer_count < BUFLEN)
            key_buffer[buffer_count++] = key;
}
