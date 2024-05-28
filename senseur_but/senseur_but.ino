#include <ArduinoBLE.h>

BLEService babyfootService("fff0");

BLEIntCharacteristic goal("fff1", BLERead | BLEBroadcast);
BLEBooleanCharacteristic batteryLow("fff2", BLERead | BLEBroadcast);
BLEBooleanCharacteristic resetGame("fff3", BLEWrite | BLERead | BLENotify);

// Advertising parameters should have a global scope. Do NOT define them in 'setup' or in 'loop'
const uint8_t manufactData[4] = {0x01, 0x02, 0x03, 0x04};
const uint8_t serviceData[2] = {0x00, 0x01};

// Build advertising data packet
BLEAdvertisingData advData;

int sensorPin = A1;
#define PIEZO_THRESHOLD 200

void setup() {
  Serial.begin(9600);
  while (!Serial);

  if (!BLE.begin()) {
    Serial.println("failed to initialize BLE!");
    while (1);
  }

  babyfootService.addCharacteristic(goal);
  babyfootService.addCharacteristic(batteryLow);
  babyfootService.addCharacteristic(resetGame);

  BLE.addService(babyfootService);

  // Build scan response data packet
  BLEAdvertisingData scanData;
  // Set parameters for scan response packet
  scanData.setLocalName("Babyfoot Sensor");
  // Copy set parameters in the actual scan response packet
  BLE.setScanResponseData(scanData);

  // Set parameters for advertising packet
  advData.setManufacturerData(0x004C, manufactData, sizeof(manufactData));
  advData.setAdvertisedService(babyfootService);
  advData.setAdvertisedServiceData(0xfff0, serviceData, sizeof(serviceData));

  // Copy set parameters in the actual advertising packet
  BLE.setAdvertisingData(advData);

  // assign event handlers for connected, disconnected to peripheral
  BLE.setEventHandler(BLEConnected, blePeripheralConnectHandler);
  BLE.setEventHandler(BLEDisconnected, blePeripheralDisconnectHandler);

  BLE.advertise();
  Serial.print("advertising");
  Serial.println("...");
 
}

void blePeripheralConnectHandler(BLEDevice central) {
  // central connected event handler
  Serial.print("Connected event, central: ");
  Serial.println(central.address());
}

void blePeripheralDisconnectHandler(BLEDevice central) {
  // central disconnected event handler
  Serial.print("Disconnected event, central: ");
  Serial.println(central.address());
}


static int localGoal = 0;
static int localReset = 0;

void scoreGoal(){
  localGoal = localGoal + 1;
  goal.writeValue(localGoal);
}

void resetGoal(){
  localGoal = 0;
  goal.writeValue(localGoal);
}

void loop() {
  BLE.poll();

  if(resetGame.value()){
    Serial.println("Game reset");
    resetGoal();
    resetGame.writeValue(false);
  }

  if(analogRead(sensorPin) > PIEZO_THRESHOLD){
    Serial.println("GOAL!!!");
    scoreGoal();
    delay(1000);
  }

  checkBattery();
}

bool isBatteryLow = false;

 void checkBattery()
{
  static bool batteryStatusChanged = true;
  int sensorValue = analogRead(A0); //read the A0 pin value
  float voltage = sensorValue * (5.00 / 1023.00) * 2; //convert the value to a true voltage.
  if (voltage < 6.50) //set the voltage considered low battery here
  {
    if (!isBatteryLow) {
      isBatteryLow = true;
      batteryStatusChanged = true;
    }
  } else {
    if (isBatteryLow) {
      isBatteryLow = false;
      batteryStatusChanged = true;
    }
  }
  
  if (batteryStatusChanged){
    Serial.print("voltage = ");
    Serial.print(voltage); //print the voltage to LCD
    Serial.println(" V");
    batteryLow.writeValue(!isBatteryLow);
    batteryStatusChanged = false;
  }
}