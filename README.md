# Oak-Nexus

0: Hardware

  - 4 Wheel Robot Chassis Smart Car with 4 DC motors Speed and Tacho Encoder  (eBay)  £20
  <img width="456" alt="image" src="https://user-images.githubusercontent.com/41960992/194170707-3ea1bfbf-7d53-4876-9df2-3adab031e023.png">
  
  - L298N DC Motor Driver Module (PiHut)  
![image](https://user-images.githubusercontent.com/41960992/194168423-119747a6-4b3d-4f79-aad2-e248a6547235.png)
  
   - FPV Gimbal Pan Tilt Camera Platform Mount optional 2x SG90 Servos + Guide (eBay)  
   <img width="402" alt="image" src="https://user-images.githubusercontent.com/41960992/194170061-a07206d8-397b-451c-b312-14c2a46a2a4e.png">
   
   - 4x HC-SR04 Ultrasonic Range Finder Distance Measuring Module Sensor  
  ![image](https://user-images.githubusercontent.com/41960992/194171275-1be89dd5-60c4-4521-95e9-d9f91c9dfd28.png)  
   
   - Seamuing Raspberry Pi 4 Power Supply UPS Hat USB Expansion Board Power with 10000mAh Battery for Raspberry 4B 3B+ 3B 2B+ 2B  
   <img width="572" alt="image" src="https://user-images.githubusercontent.com/41960992/194173704-0d94bd89-fa95-467e-a2da-653993637650.png">  
   
   - Raspberry Pi 4 Model B 8GB  
   ![image](https://user-images.githubusercontent.com/41960992/194174738-5821bd6a-0977-4d84-863e-572c130acf5b.png)

   -Raspberry Pi Camera Module V2.1 - £28.5
   ![image](https://user-images.githubusercontent.com/41960992/194174114-b8d20fe0-fad8-46fb-9b25-8bf07ce3d97f.png)

1: Install the Edge TPU runtime

    echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
    sudo apt-get update

* Install with maximum operating frequency (optional)  
    sudo apt-get install libedgetpu1-max
  
2: Install the PyCoral library  
  
    sudo apt-get install python3-pycoral

    sudo apt install -y python3-picamera2

![IMG_1138 Medium](https://user-images.githubusercontent.com/41960992/192067053-c70deedc-36ae-4e50-a165-0ba0c17e565a.jpeg)
  
![IMG_1139 Medium](https://user-images.githubusercontent.com/41960992/192067059-17f529b8-6a2c-44ea-bc89-8f842d3518eb.jpeg)
  
![IMG_0694 Medium](https://user-images.githubusercontent.com/41960992/192067065-fd887765-edf2-44ca-98a8-872a1a8f63c8.jpeg)


*References*
  
    https://www.electronicshub.org/raspberry-pi-l298n-interface-tutorial-control-dc-motor-l298n-raspberry-pi/

Notes: 
gpio22 = front midle sensor + resistor yello
gpio27 = front midle sensor
gpio17 = back sensor + resistor + yello
gpio04 = back midle sensor
