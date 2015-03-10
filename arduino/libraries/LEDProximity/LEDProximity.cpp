#include "Arduino.h"
#include "LEDProximity.h"

LEDProximity::LEDProximity(int led, int IRPin, int IRemitter, int proximity) {
	pinMode(led, OUTPUT);
	_led = led;
	_IRPin = IRPin;
	pinMode(IRemitter, OUTPUT);
	digitalWrite(IRemitter, LOW);
	_IRemitter = IRemitter;
	_proximity = proximity;
	int _readIR = readIR(int);
	int _ambientIR;
	int _obstacleIR;
	int _value[10];
	int _distance;
};

int LEDProximity::readIR(int _times) {
	for (int _x = 0; _x < _times; _x++) {
		digitalWrite(_IRemitter, LOW);
		delay(1);
		_ambientIR = analogRead(_IRPin);
		digitalWrite(_IRemitter, HIGH);
		delay(1);
		_obstacleIR = analogRead(_IRPin);
		_value[_x] = _ambientIR - _obstacleIR;
	}

	for (int _x = 0; _x < _times; _x++) {
		_distance += _value[_x];
	}
	return (_distance / _times);
};

void LEDProximity::controlLED() {
	_distance = _readIR(5);
	Serial.println(_distance);
	if (_distance > _proximity) {
    	digitalWrite(_led, HIGH);
	} else {
    	digitalWrite(_led, LOW);
	}
};

// void LEDProximity::distanceread() {
// 	_distance = readIR(5);
// }