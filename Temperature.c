/*
 * Sensorenlezen.c
 *
 * Onderstaande code zorgt ervoor dat de TMP36GT9Z Low Voltage temperature sensor uitgelezen kan worden.
 *
 * Deze sensor werkt met voltage om temperatuur te meten. 
 * Hoe meer voltage hoe hoger de temperatuur. Daarom moet je de voltage omzetten in temperatuur in Celsius.
 * En omdat de ADC een 10 bits getal binnen krijgt moet je dit eerst omzetten in voltage.
 *
 */ 


#include "pinIO.h"


/* verander het 10 bits getal in het voltage */
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

