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
#include <util/delay.h>

const int trigPin = 9;
const int echoPin = 10;

const int light;

long duration;
int distance;


/* Ultrasenoorsensor */
void setUpUltra(){
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
	
	setUpUltra();
	
	startPulse();
	distance = distance(readPulse());
	
	return distance;
	
}

/* Temperatuursensor
* verander het 10 bits getal in het voltage */
float voltage(analog){
	float voltage = analog * 5.0 / 1024;
	// keer 5.0 omdat het om 5 volt gaat en gedeelt door 1024 omdat het een 10 bits getal is
	// voorbeeld: 2.5 volt = 512 * 5.0 / 1024. Je krijgt 512(0x200) binnen
	return voltage;
	
}


/* Deze functie zorgt ervoor dat de gemeten voltage omgezet wordt naar temperatuur */
float temperatureInC(voltage){
	float temperatureC = (voltage - 0.5) * 100;
	// de formule die ervoor zorgt dat het omgezet wordt.
	// voorbeeld: (1.2 - 0.5) * 100 = 70 graden Celsius.
	return temperatureC;
	
}


float measure_Temp(){
	float tempInC = temperatureInC(voltage(analog_read(0))); // lees ADC uit (A0) en maak er volt van en dan Celsius
	return tempInC;

}


int getTemp() {
	int temperature;
	temperature= measure_Temp(); // roep de functie aan die temperatuur uitleest
	return temperature;
}


/* Photocell sensor */
int getLight(){
	light = analog_read(1); // lees A1 uit // deze functie nog uit Gijs zijn library halen
	return light;
}


