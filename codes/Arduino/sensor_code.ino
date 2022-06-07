#include <OneWire.h>
#include <Servo.h>
#include <DallasTemperature.h>

//input
#define ONE_WIRE_BUS A0//수온센서
#define takpin  A1 //탁도센서

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

int mode=0;

float temp(){//온도센서
  float tem=0;
  sensors.requestTemperatures();
  tem=sensors.getTempCByIndex(0);
  return tem;
}
float takdo(){//탁도센서
  int sensorValue = analogRead(takpin); 
  float voltage = sensorValue * (5.0 / 1024.0)+3;
//  Serial.write((char)voltage+3);
  return voltage;
}
//void servo(){//서보모터
////  servo1.write(FILL_DEGREE); 
//  delay(1000); // delay for 1 second
//  servo1.write(DISPENSE_DEGREE); 
//  delay(1000);
//  servo1.write(FILL_DEGREE); 
//}
void setup(void)
{ 
  Serial.begin(9600);
}


void loop(){

  Serial.print(temp());
  Serial.print(" ");
  Serial.println(takdo()); 
  delay(300);
  
  

}
