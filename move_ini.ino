#include <Servo.h>
#include <string.h>
#include <stdio.h>
Servo myservoLR;
Servo myservoTB;
String pt1s,pt2s;
int pos = 0;
int pt1,pt2;
const byte numChars = 32;
char receivedChars[numChars];

boolean newData = false;

void setup()

{

Serial.begin(9600);
while (!Serial);
Serial.println("-------------------------");
Serial.println("ARos is loading....");
delay(1000);
Serial.println("ARos loaded succesfully");
Serial.println("-------------------------");
myservoLR.attach(9);
myservoTB.attach(10);

Serial.println("calibrating servoLR...");
for(pos = 0; pos <= 180; pos += 1)
myservoLR.write(0);
delay(1000);
myservoLR.write(170);
delay(1000);
myservoLR.write(90);
delay(1000);
Serial.println("servo calibrated");
Serial.println("-------------------------");



Serial.println("calibrating servoTB...");
for(pos = 0; pos <= 180; pos += 1)
myservoTB.write(0);
delay(1000);
myservoTB.write(170);
delay(1000);
myservoTB.write(90);
delay(1000);
Serial.println("servo calibrated");
Serial.println("-------------------------");
Serial.println("Command input online, write command to perform action");
Serial.println("-------------------------");

}

void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;
 
 // if (Serial.available() > 0) {
    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}



void loop() {

if (Serial.available())


{ recvWithStartEndMarkers();


sscanf(receivedChars, "%d,%d", &pt1,&pt2);
//pt1=pt1s.toInt();
//pt2=pt2s.toInt();
if (pt1 >= 3 && pt1 < 170)
  if (pt2 >= 3 && pt2 < 170)
{  myservoLR.write(pt1);
   myservoTB.write(pt2);
   Serial.print("turning servo to ");
   Serial.print(pt1);
   Serial.print(",");
   Serial.print(pt2); 
   Serial.println(" degrees");
  
} 
}

}



