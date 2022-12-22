#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

#define SEALEVELPRESSURE_HPA (1013.25)

Adafruit_BME280 bme;

int i,aux=0,co=0;

float temp,pres;

char leitura;

void setup() {
  Serial.begin(9600);

  pinMode(2,OUTPUT);
  pinMode(3,OUTPUT);
  pinMode(4,OUTPUT);

  if (!bme.begin(0x76)) {
    Serial.println("Could not find a valid BME280 sensor, check wiring!");
    while (1);
  }
}

int desconectar(void)
{

  if(Serial.available())
  { 
      if(Serial.read() == 'd')
      { 
        aux=0;
        return(1);
      }
      else
        return(0); 

  }
}

int conectar(void)
{

    if(Serial.available())
    {

      if(Serial.read() == 'c')
      { 
        aux=1;
        return(1);
      }
      else
        return(0); 
    }

}

void loop() 
{ 

   if(Serial.available())
    {

      if(Serial.read() == 'c')
      { 
        aux=1;
        Serial.println(1);
        digitalWrite(3,HIGH);
      }
    }





  while(aux == 1)
  {   

     if(Serial.available())
      { 
        leitura = Serial.read();
        if(leitura == 'd')
        { 
          aux=0;
          Serial.println(1);
          digitalWrite(3,LOW);
          digitalWrite(2,LOW);
        }
        if(leitura == 'a'){
          //Serial.println("entrei");
          if(co==0){
            digitalWrite(4,HIGH);
            co=1;
            Serial.println(1);
          }
          else{
            digitalWrite(4,LOW);
            co=0;
            Serial.println(0);
          }
        }
          
        if(leitura == 'm')
        { 
          digitalWrite(2,HIGH);
          temp=pres=0;

          for(i = 0; i < 100 ; i++)
          {
             temp= temp+bme.readTemperature(); 
             pres= pres+bme.readPressure() / 100.0F;  
          }

          temp=temp/100.0;
          pres=pres/100.0;
          Serial.println(temp);
          delay(2000);
          Serial.println(pres);
          digitalWrite(2,LOW);
        }

      }




   }

}
