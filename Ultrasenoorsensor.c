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

// # include library PIN uitlezen
// # include library voor Rx Tx verbinding etc...

const int trigPin = 9;
const int echoPin = 10;

long duration;
int distance;

void setUp(){
	// trigPin = OUTPUT;
	// echoPin = INPUT;
	
}

void startPulse(){
	trigPin = LOW; // zorg ervoor dat trigger leeg is!
	delay(2ms);
	
	trigPin = HIGH;
	delay(10ms);
	trigPin = LOW;
	
}

long readPulse(){
	duration = read echoPin;
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
	distance(readPulse());
	
	return distance;
	
}



