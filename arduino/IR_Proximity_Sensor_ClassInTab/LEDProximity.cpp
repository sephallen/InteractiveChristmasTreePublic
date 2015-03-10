#include "Arduino.h"
#include "LEDProximity.h"

LEDProximity::LEDProximity(int led, int IRPin, int IRemitter, int proximity) {
	_led = led;
	_IRPin = IRPin;
	_IRemitter = IRemitter;
	_proximity = proximity;

};

void LEDProximity::setupProximity() {
        pinMode(_led, OUTPUT);
	pinMode(_IRemitter, OUTPUT);
	digitalWrite(_IRemitter, LOW);
	int _ambientIR;
	int _obstacleIR;
	int _value[10];
	int _distance;
}

int LEDProximity::_readIR(int _times) {
	for (int x = 0; x < _times; x++) {
		digitalWrite(_IRemitter, LOW);
		delay(1);
		_ambientIR = analogRead(_IRPin);
//                Serial.println(_ambientIR);
		digitalWrite(_IRemitter, HIGH);
		delay(1);
		_obstacleIR = analogRead(_IRPin);
//                Serial.println(_obstacleIR);
		_value[x] = _ambientIR - _obstacleIR;
	}

	for (int x = 0; x < _times; x++) {
		_distance += _value[x];
	}
	return (_distance/_times);
};

void LEDProximity::controlLED() {
        _distanceRead();
//	Serial.println(_distance);
	if (_distance > _proximity) {
    	  digitalWrite(_led, HIGH);
	} else {
    	  digitalWrite(_led, LOW);
	}
};

void LEDProximity::_distanceRead() {
//        Serial.println(_distance);
//        Serial.println(readIR(5));
        _distance = _readIR(2);
}
