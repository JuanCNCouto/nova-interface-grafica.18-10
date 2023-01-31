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

  pinMode(2,OUTPUT);// pin do sensor
  pinMode(3,OUTPUT);
  pinMode(4,OUTPUT); // pin do peltier

  if (!bme.begin(0x76)) {
    Serial.println("Could not find a valid BME280 sensor, check wiring!");
    while (1);
  }
}

void loop() 
{ 

   if(Serial.available()) // teste de conexão do arduino com o pc
    {

      if(Serial.read() == 'c')
      { 
        aux=1;
        Serial.println(1);
        digitalWrite(3,HIGH);
      }
    }





  while(aux == 1) // enquanto o arduino conectado ao pc
  {   

     if(Serial.available())
      { 
        leitura = Serial.read();
        if(leitura == 'd') // desconecta o arduino com o pc
        { 
          aux=0;
          Serial.println(1);
          digitalWrite(3,LOW);
          digitalWrite(2,LOW);
        }
        if(leitura == 'a'){ // sinal 'a' liga o peltier
          //Serial.println("entrei");
          if(co==0){
            digitalWrite(4,HIGH);
            co=1; // muda a constante para q na proxima vez q mandar o sinal 'a' o peltier vai desligar no else
            Serial.println(1);
          }
          else{ 
            digitalWrite(4,LOW);
            co=0;  // muda a constante para q na proxima vez q mandar o sinal 'a' o peltier vai ligar no else
            Serial.println(0);
          }
        }
          
        if(leitura == 'm') // sinal 'm' ativa a função de medir
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
