

#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>

#define F_CPU 16000000UL			     // 16.0 Mhz clock
#define F_CPU_div    F_CPU/1000000


#define TimeOutTime  300				// MAX time (on msec) for TimeOut Error
#define Delay_Until_New_Measure 60		// Delay between measures (on msec) , may occur problem if delay is short.Check datasheet
#define max_ticks   TimeOutTime * F_CPU_div*1000	// MAX ticks Timer0 can reach before seems like Timeout to us.

volatile uint32_t distance_avg = 0;
volatile char Ultra_is_on = 0;
volatile char is_measuring = 0;
volatile uint32_t Timer0_counter = 0 ;
volatile char TimeOUT = 0;
volatile uint8_t distance;
volatile int i=0;

#define trigPin 0
#define echoPin 3


/* Ultrasenoorsensor
*********************************************************************************************************************/

void setUpUltra(){
	digital_config(trigPin, OUT); // trigger pin wordt output
	digital_config(echoPin, IN); // echo pin is input
}

void setUpInterrupt(){
	PORTD |= (1<<echoPin);		// Enable PD2 pull-up resistor. // digital_write(echoPin, 1)
	
	EIMSK  |= (1<<INT1);			// Enable INT1 interrupts.
	
	EICRA |= (1<<ISC01) ;		// Any logical change on INT1 generates an interrupt request.
}

void setUpTimer0(){
	TCCR0B |= (1<<CS00);						   // NO prescaller , every tick is 1us  - START
	TCNT0 = 0;								   // Clear counter
	TIMSK0 |= (1<<TOIE0);					   // Enable Timer0-Overflow interrupts
	sei();										// Global interrupts Enabled.
}

void startPulse(){
	digital_write(trigPin, LOW); // zorg ervoor dat trigger leeg is!
	_delay_ms(2);
	
	digital_write(trigPin, HIGH);
	Ultra_is_on = 1;
	_delay_us(10);
	digital_write(trigPin, LOW);
	
}


	/* dit is een soort van de main functie. Hierdoor krijg je de juiste afstand terug. Dit in scheduler gooien */
uint8_t getDistance(){
		if (is_measuring == 0)
		{
			startPulse();
	
		}

		return distance;	
}
	
	
	
ISR(TIMER0_OVF_vect)  // Here every time Timer0 Overflow
{
	if(Ultra_is_on)	   // Only if sensor is active
	{
		Timer0_counter++;          // How many times Timer0 got OVF ?
		uint32_t ticks = Timer0_counter * 256 + TCNT0;		// calculate total Timer0 ticks
		TimeOUT=0;
		
		if(ticks > max_ticks)
		{
			Ultra_is_on = 0;	 // ** Free the sensor to new measures**/
			is_measuring = 0;		 //  *************************
			TimeOUT =1 ;        // Timeout ; Used it as you want.
				
		}
				
	}

}




ISR(INT1_vect)
{
	if (is_measuring == 1.)		// Care only if sensor is started
	{
		if (Ultra_is_on == 0)  // High_Pulse '0' -> '1' , start time measure
		{
		TCNT0 = 0;			    // Reset Timer0/Counter
		Ultra_is_on = 1;	// Now its not free
		Timer0_counter = 0;		// Clear counter
		}


		else					// Low Pulse '1' -> '0', we have  our result
		{
		Ultra_is_on = 0 ;
		distance = (Timer0_counter * 256 + TCNT0) / (F_CPU_div * 58);
		// us/58 = .. cm.  Every 8 ticks is 1us (8Mhz clock, NO prescaler). http://www.micropik.com/PDF/HCSR04.pdf
		is_measuring = 0 ;    // Ready for new measure

					}
			}

}

