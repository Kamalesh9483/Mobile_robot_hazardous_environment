// For BMP280
#include <Wire.h>
#include <SPI.h>
#include <WiFi.h>
#include <Adafruit_BMP280.h>

#define BMP_SCK  (13)
#define BMP_MISO (12)
#define BMP_MOSI (11)
#define BMP_CS   (10)

Adafruit_BMP280 bmp; // I2C
//Adafruit_BMP280 bmp(BMP_CS); // hardware SPI
//Adafruit_BMP280 bmp(BMP_CS, BMP_MOSI, BMP_MISO,  BMP_SCK);

// For UDP Packets
#include <WiFiUdp.h>
#include <ArduinoJson.h>
#define STASSID "JioFiber 1"
#define STAPSK "Dexiatoungjio"
WiFiUDP Udp;
char buffer[80];
const char* host = "192.168.29.212";
unsigned int udpPort = 8090;
const char* ssid     = STASSID;
const char* password = STAPSK;

void setup() {
  Serial.begin(115200);
  Serial.println(F("BMP280 test"));
  WiFi.begin(ssid, password);
  Udp.begin(udpPort);

  //if (!bmp.begin(BMP280_ADDRESS_ALT, BMP280_CHIPID)) {
  if (!bmp.begin()) {
    Serial.println(F("Could not find a valid BMP280 sensor, check wiring or "
                      "try a different address!"));
    while (1) delay(10);
  }

  /* Default settings from datasheet. */
  bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     /* Operating Mode. */
                  Adafruit_BMP280::SAMPLING_X2,     /* Temp. oversampling */
                  Adafruit_BMP280::SAMPLING_X16,    /* Pressure oversampling */
                  Adafruit_BMP280::FILTER_X16,      /* Filtering. */
                  Adafruit_BMP280::STANDBY_MS_500); /* Standby time. */

}

void loop() {
    DynamicJsonBuffer jBuffer;
    JsonObject& root = jBuffer.createObject();
    
    Serial.print(F("Temperature = "));
    float temp = 0;
    float pres = 0;

    temp = bmp.readTemperature();
    Serial.print(temp);
    Serial.println(" *C");
    root["temperature"] = temp;
    
    pres = bmp.readPressure();
    Serial.print(F("Pressure = "));
    Serial.print(pres);
    Serial.println(" Pa");
    root["pressure"] = pres;
    
//    Serial.print(F("Approx altitude = "));
//    Serial.print(bmp.readAltitude(1013.25)); /* Adjusted to local forecast! */
//    Serial.println(" m");

    // Send UDP packet
    Udp.beginPacket(host, udpPort);
    root.printTo(Udp);
    Udp.println();
    Udp.endPacket();
    
    Serial.println();
    delay(2000);
}
