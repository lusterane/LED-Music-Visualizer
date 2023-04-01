#include <FastLED.h>

#define LED_PIN     6
#define NUM_LEDS    60

CRGB leds[NUM_LEDS];
int brightness = 50; // Initial brightness
int rgb[] = {255, 255, 255};
int power = 255;
int lighting_preset = 0;
void setup() {
  FastLED.addLeds<WS2812, LED_PIN, GRB>(leds, NUM_LEDS);
  set_all_lights_color();
  FastLED.show();

  Serial.begin(250000);
}

void loop() {
  while (!Serial.available());
  String readString = "";
  while (Serial.available()) {
      char c = Serial.read();
      readString = readString + c;
   }
   processString(readString);
  // processPowerString(readString);
  
  switch (lighting_preset) {
    case '0':
      moving_lights_add_rgb();
      break;
    case '1':
      set_all_lights_color();
      break;
    case '2':
      middle_moving_lights_add_rgb();
      break;
  }
  FastLED.setBrightness(power);
  FastLED.show();
}

void processString(String s) {
  lighting_preset = s[0];
  rgb[0] = s.substring(1,4).toInt();
  rgb[1] = s.substring(4,7).toInt();
  rgb[2] = s.substring(7,10).toInt();
  power = s.substring(10,13).toInt();
}

void processPowerString(String s) {
  power = s.toInt();
}

void middle_moving_lights_add_rgb() {
  int m = 30;
  leds[m] = CRGB (rgb[0],rgb[1],rgb[2]);
  CRGB prev = leds[m];
  int i = m - 1;
  int j = m + 1;
  
  while (i > -1 && j < NUM_LEDS) {
    CRGB temp_i = leds[i];
    CRGB temp_j = leds[j];
    leds[i] = prev;
    leds[j] = prev;

    // update prev
    leds[i+1] = temp_i;
    leds[j-1] = temp_j;
    
    prev = leds[i];
    i-=1;
    j+=1;
  }
}

void moving_lights_add_rgb() {
  CRGB prev = leds[0];
  for (int i = 1; i <= NUM_LEDS; i++) {
    CRGB temp = leds[i];
    leds[i] = prev;
    prev = temp;
  }
  leds[0] = CRGB (rgb[0],rgb[1],rgb[2]);
}

void set_all_lights_color() {
  for (int i = 0; i <= NUM_LEDS; i++) {
    leds[i] = CRGB (rgb[0],rgb[1],rgb[2]);
  }
}