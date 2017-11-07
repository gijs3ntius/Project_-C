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
#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>
//#inculde distance_sensor


/* Temperatuursensor
* verander het 10 bits getal in het voltage 
***************************************************************************************************************/

/* Deze functie zorgt ervoor dat de gemeten voltage omgezet wordt naar temperatuur */
float temperatureInC(uint16_t analog){
	float volt = analog * 5.0 / 1024;
	// keer 5.0 omdat het om 5 volt gaat en gedeelt door 1024 omdat het een 10 bits getal is
	// voorbeeld: 2.5 volt = 512 * 5.0 / 1024. Je krijgt 512(0x200) binnen
	float temperatureC = (volt - 0.5) * 100;
	// de formule die ervoor zorgt dat het omgezet wordt.
	// voorbeeld: (1.2 - 0.5) * 100 = 70 graden Celsius.
	return temperatureC;
	
}


uint8_t getTemp(){
	uint8_t tempInC = temperatureInC(analog_read(0)); // lees ADC uit (A0) en maak er volt van en dan Celsius
	return tempInC;
}


/* Photocell sensor 
*********************************************************************************************************************/


uint8_t getLight(){
	uint8_t light = (analog_read(1)>>2); 
	// lees A1 uit, met een shift /4 
	// Je krijgt een 10 bits getal. We schuiven hem twee keer naar rechts zodat je 8 bits hebt.
	// Je verliest hier alleen de waarden 0-3 mee. Voor dit project niet erg.
	
	return light;
}


