#include <WiFi.h>
#include <Servo.h>

Servo myservo_gripper;  // create servo object to control a servo
Servo myservo_base;
Servo myservo_arm;

// GPIO the servo is attached to
static const int servoP_gripper = 13;
static const int servoP_base = 12;
static const int servoP_arm = 14;

// Replace with your network credentials
const char* ssid     = "OnePlus 5T";
const char* password = "c813da74egys";

// Set web server port number to 80
WiFiServer server(80);

// Variable to store the HTTP request
String header;

// Decode HTTP GET value
String valueString_gripper = String(4);
String valueString_base = String(5);
String valueString_arm = String(6);
int pos1 = 0;
int pos2 = 0;
int pos3 = 0;
int pos4 = 0;
int pos5 = 0;
int pos6 = 0;

// Current time
unsigned long currentTime = millis();
// Previous time
unsigned long previousTime = 0; 
// Define timeout time in milliseconds (example: 2000ms = 2s)
const long timeoutTime = 2000;

void setup() {
  Serial.begin(115200);

  myservo_gripper.attach(servoP_gripper);  // attaches the servo on the servoP_gripperin_gripper to the servo object
  myservo_base.attach(servoP_base);  
  myservo_arm.attach(servoP_arm);  

  // Connect to Wi-Fi network with SSID and password
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  // Print local IP address and start web server
  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  server.begin();
}

void loop(){
  WiFiClient client = server.available();   // Listen for incoming clients

  if (client) {                             // If a new client connects,
    currentTime = millis();
    previousTime = currentTime;
    Serial.println("New Client.");          // print a message out in the serial port
    String currentLine = "";                // make a String to hold incoming data from the client
    while (client.connected() && currentTime - previousTime <= timeoutTime) { // loop while the client's connected
      currentTime = millis();
      if (client.available()) {             // if there's bytes to read from the client,
        char c = client.read();             // read a byte, then
        Serial.write(c);                    // print it out the serial monitor
        header += c;
        if (c == '\n') {                    // if the byte is a newline character
          // if the current line is blank, you got two newline characters in a row.
          // that's the end of the client HTTP request, so send a response:
          if (currentLine.length() == 0) {
            // HTTP headers always start with a response code (e.g. HTTP/1.1 200 OK)
            // and a content-type so the client knows what's coming, then a blank line:
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:text/html");
            client.println("Connection: close");
            client.println();

            // Display the HTML web page
            client.println("<!DOCTYPE html><html>");
            client.println("<head><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">");
            client.println("<link rel=\"icon\" href=\"data:,\">");
            // CSS to style the on/off buttons 
            // Feel free to change the background-color and font-size attributes to fit your preferences
            client.println("<style>body { text-align: center; font-family: \"Trebuchet MS\", Arial; margin-left:auto; margin-right:auto;}");
            client.println(".slider_gripper { width: 300px; }");s
            client.println(".slider_base { width: 300px; }");
            client.println(".slider_arm { width: 300px; }</style>");
            client.println("<script src=\"https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js\"></script>");
                     
            // Web Page for gripper
            client.println("</head><body><h1>Gripper Position</h1>");
            client.println("<p>Position: <span id=\"servoP_gripper\"></span></p>");          
            client.println("<input type=\"range\" min=\"0\" max=\"180\" class=\"slider_gripper\" id=\"servoslider_gripper\" onchange=\"servo_gripper(this.value)\" value=\""+valueString_gripper+"\"/>");
            
            client.println("<script>var slider_gripper = document.getElementById(\"servoslider_gripper\");");
            client.println("var servoP_gripper = document.getElementById(\"servoP_gripper\"); servoP_gripper.innerHTML = slider_gripper.value;");
            client.println("slider_gripper.oninput = function() { slider_gripper.value = this.value; servoP_gripper.innerHTML = this.value; }");
            client.println("$.ajaxSetup({timeout:1000}); function servo_gripper(pos_gripper) { ");
            client.println("$.get(\"/gripper?value=\" + pos_gripper + \"&\"); {Connection: close};}</script>");

           // Web Page for base
            client.println("</head><<h1>Base Position</h1>");
            client.println("<p>Position: <span id=\"servoP_base\"></span></p>");          
            client.println("<input type=\"range\" min=\"0\" max=\"180\" class=\"slider_base\" id=\"servoslider_base\" onchange=\"servo_base(this.value)\" value=\""+valueString_base+"\"/>");
            
            client.println("<script>var slider_base = document.getElementById(\"servoslider_base\");");
            client.println("var servoP_base = document.getElementById(\"servoP_base\"); servoP_base.innerHTML = slider_base.value;");
            client.println("slider_base.oninput = function() { slider_base.value = this.value; servoP_base.innerHTML = this.value; }");
            client.println("$.ajaxSetup({timeout:1000}); function servo_base(pos_base) { ");
            client.println("$.get(\"/base?value=\" + pos_base + \"&\"); {Connection: close};}</script>");
            

          // Web Page for arm
            client.println("</head><<h1>Arm Position</h1>");
            client.println("<p>Position: <span id=\"servoP_arm\"></span></p>");          
            client.println("<input type=\"range\" min=\"0\" max=\"180\" class=\"slider_arm\" id=\"servoslider_arm\" onchange=\"servo_arm(this.value)\" value=\""+valueString_arm+"\"/>");
            
            client.println("<script>var slider_arm = document.getElementById(\"servoslider_arm\");");
            client.println("var servoP_arm = document.getElementById(\"servoP_arm\"); servoP_arm.innerHTML = slider_arm.value;");
            client.println("slider_arm.oninput = function() { slider_arm.value = this.value; servoP_arm.innerHTML = this.value; }");
            client.println("$.ajaxSetup({timeout:1000}); function servo_arm(pos_arm) { ");
            client.println("$.get(\"/arm?value=\" + pos_arm + \"&\"); {Connection: close};}</script>");
           
            client.println("</body></html>");     


            
            //GET /?value=180& HTTP/1.1
            if(header.indexOf("GET /gripper?value=")>=0) {
              pos1 = header.indexOf('=');
              pos2 = header.indexOf('&');
              valueString_gripper = header.substring(pos1+1, pos2);

              //Rotate the servo
              myservo_gripper.write(valueString_gripper.toInt());
              Serial.println(valueString_gripper);
            }
           
            if(header.indexOf("GET /base?value=")>=0) {
              pos3 = header.indexOf('=');
              pos4 = header.indexOf('&');
              valueString_base = header.substring(pos3+1, pos4);

              //Rotate the servo
              myservo_base.write(valueString_base.toInt());
              Serial.println(valueString_base); 
            }

             if(header.indexOf("GET /arm?value=")>=0) {
              pos5 = header.indexOf('=');
              pos6 = header.indexOf('&');
              valueString_base = header.substring(pos5+1, pos6);

              //Rotate the servo
              myservo_arm.write(valueString_arm.toInt());
              Serial.println(valueString_arm); 
            }
                     
            // The HTTP response ends with another blank line
            client.println();
            // Break out of the while loop
            break;
          }
          
          else { // if you got a newline, then clear currentLine
            currentLine = "";
          }
        } else if (c != '\r') {  // if you got anything else but a carriage return character,
          currentLine += c;      // add it to the end of the currentLine
        }
      }
    }
    // Clear the header variable
    header = "";
    // Close the connection
    client.stop();
    Serial.println("Client disconnected.");
    Serial.println("");
  }
}
