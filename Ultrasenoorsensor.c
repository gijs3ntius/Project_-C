/*
 * Ultrasenoorsensor
 *
 * Onderstaande code zorgt ervoor dat de HC-SR04 sensor uitgelezen kan worden.
 *
 * De sensor zendt een geluid uit op 40 000 Hz. 
 * Dit reist door de lucht. Als er een object is stuit dit signaal weer terug naar de sensor. 
 * Door te kijken hoe lang de reis duurt en de snelheid van geluid kun je de afstand in centimeters berekenen.
 * Formule = afstand = tijd * 0.034 (snelheid geluid in ms) / 2
 * bron: http://howtomechatronics.com/tutorials/arduino/ultrasonic-sensor-hc-sr04/
 */ 

#include "pinIO.h"

const int trigPin = 9;
const int echoPin = 10;

long duration;
int distance;

void setUp(){
	trigPin = digital_config(9, OUT); // trigger pin wordt output
	echoPin = digital_config(10, IN); // echo pin is input
}

void startPulse(){
	trigPin = digital_write(LOW); // zorg ervoor dat trigger leeg is!
	_delay_ms(2);
	
	trigPin = digital_write(HIGH);
	_delay_ms(10);
	trigPin = digital_write(LOW);
	
}

long readPulse(){
	duration = digital_read(echoPin);
	return duration;
}

int distance(duration){
	distance = (duration * 0.034) / 2;
	return distance;
}


/* dit is een soort van de main functie. Hierdoor krijg je de juiste afstand terug. Dit in scheduler gooien */
int getDistance(){
	
	setUp();
	
	startPulse();
	distance = distance(readPulse());
	
	return distance;
	
}



