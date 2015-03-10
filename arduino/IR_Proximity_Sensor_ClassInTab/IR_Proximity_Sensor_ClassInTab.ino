#define BUFFER_SIZE 64
#include "LEDProximity.h"

LEDProximity ledproximity(3, A0, 2, 1);
LEDProximity ledproximity2(5, A1, 4, 1);
LEDProximity ledproximity3(7, A2, 6, 1);
LEDProximity ledproximity4(9, A3, 8, 1);
LEDProximity ledproximity5(11, A4, 10, 1);
LEDProximity ledproximity6(13, A5, 12, 1);
LEDProximity ledproximity7(15, A6, 14, 4);
LEDProximity ledproximity8(17, A7, 16, 4);
LEDProximity ledproximity9(19, A8, 18, 4);
LEDProximity ledproximity10(21, A9, 20, 4);
LEDProximity ledproximity11(23, A10, 22, 4);
LEDProximity ledproximity12(25, A11, 24, 4);
LEDProximity ledproximity13(27, A12, 26, 4);
LEDProximity ledproximity14(29, A13, 28, 4);
LEDProximity ledproximity15(31, A14, 30, 4);
LEDProximity ledproximity16(33, A15, 32, 4);

void setup() {
//  Serial.begin(9600);
  ledproximity.setupProximity();
  ledproximity2.setupProximity();
  ledproximity3.setupProximity();
  ledproximity4.setupProximity();
  ledproximity5.setupProximity();
  ledproximity6.setupProximity();
  ledproximity7.setupProximity();
  ledproximity8.setupProximity();
  ledproximity9.setupProximity();
  ledproximity10.setupProximity();
  ledproximity11.setupProximity();
  ledproximity12.setupProximity();
  ledproximity13.setupProximity();
  ledproximity14.setupProximity();
  ledproximity15.setupProximity();
  ledproximity16.setupProximity();
}

void loop() {
  ledproximity.controlLED();
  ledproximity2.controlLED();
  ledproximity3.controlLED();
  ledproximity4.controlLED();
  ledproximity5.controlLED();
  ledproximity6.controlLED();
  ledproximity7.controlLED();
  ledproximity8.controlLED();
  ledproximity9.controlLED();
  ledproximity10.controlLED();
  ledproximity11.controlLED();
  ledproximity12.controlLED();
  ledproximity13.controlLED();
  ledproximity14.controlLED();
  ledproximity15.controlLED();
  ledproximity16.controlLED();
}
