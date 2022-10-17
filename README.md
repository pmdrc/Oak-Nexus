# Oak-Nexus
  
![IMG_1138 Medium](https://user-images.githubusercontent.com/41960992/192067053-c70deedc-36ae-4e50-a165-0ba0c17e565a.jpeg)  

0: RASPBIAN OS 64BITS
   With Raspberry Pi Imager --> burn the 64 bits Bullseye with Desktop into and micro-SD card ( V30 , A2 speed )
  (in extra settings pre-define the Wifi, hostname and user/pass)
      
   After 1st boot ssh to it and run :  
   
    sudo raspi-conf
  
  Enble VNC and SPI
  
    sudo apt update & sudo apt upgrade -y
    
1: Servo deamon PWM
  
    sudo pigpiod

2: Install the Edge TPU runtime

    echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
    sudo apt-get update
    sudo apt-get install libedgetpu1-std
  
* Install with maximum operating frequency (optional)  
    sudo apt-get install libedgetpu1-max
  
3: Install the PyCoral library  
  
    sudo apt-get install python3-pycoral

3.1: reboot the system

    sudo reboot

3.5: Install new Picamera (already ???)

    # sudo apt install -y python3-picamera2
    sudo apt install libatlas-base-dev
    
3.6 Install OPENCV 4.5.x 
    https://qengineering.eu/install-opencv-4.5-on-raspberry-64-os.html
    

4: Install LCD 1.47 display  
  
    wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.71.tar.gz
    tar zxvf bcm2835-1.71.tar.gz 
    cd bcm2835-1.71/
    sudo ./configure && sudo make && sudo make check && sudo make install

    #Bullseye branch system use the following command:
    git clone https://github.com/WiringPi/WiringPi
    cd WiringPi
    ./build
    gpio -v
    
    sudo wget https://www.waveshare.com/w/upload/8/8d/LCD_Module_RPI_code.zip
    sudo unzip ./LCD_Module_RPI_code.zip -d ./LCD_Module_RPI_code/
    cd LCD_Module_RPI_code/RaspberryPi/LCD_Module_RPI_code/RaspberryPi/python/example
    python 1inch47_LCD_test.py 

![IMG_1139 Medium](https://user-images.githubusercontent.com/41960992/192067059-17f529b8-6a2c-44ea-bc89-8f842d3518eb.jpeg)
  
![IMG_0694 Medium](https://user-images.githubusercontent.com/41960992/192067065-fd887765-edf2-44ca-98a8-872a1a8f63c8.jpeg)

0: Hardware

  - 4 Wheel Robot Chassis Smart Car with 4 DC motors Speed and Tacho Encoder  (eBay)  £20
  <img width="456" alt="image" src="https://user-images.githubusercontent.com/41960992/194170707-3ea1bfbf-7d53-4876-9df2-3adab031e023.png">
  
  - L298N DC Motor Driver Module (PiHut)  = £3.5
![image](https://user-images.githubusercontent.com/41960992/194168423-119747a6-4b3d-4f79-aad2-e248a6547235.png)
  
   - FPV Gimbal Pan Tilt Camera Platform Mount optional 2x SG90 Servos + Guide (eBay) = £12  
   <img width="402" alt="image" src="https://user-images.githubusercontent.com/41960992/194170061-a07206d8-397b-451c-b312-14c2a46a2a4e.png">
   
   - 4x HC-SR04 Ultrasonic Range Finder Distance Measuring Module Sensor = £8 (£2 each)  
  ![image](https://user-images.githubusercontent.com/41960992/194171275-1be89dd5-60c4-4521-95e9-d9f91c9dfd28.png)  
   
   - Seamuing Raspberry Pi 4 Power Supply UPS Hat USB Expansion Board Power with 10000mAh Battery for Raspberry 4B 3B+ 3B 2B+ 2B = £32  
   <img width="572" alt="image" src="https://user-images.githubusercontent.com/41960992/194173704-0d94bd89-fa95-467e-a2da-653993637650.png">  
   
   - Raspberry Pi 4 Model B 8GB = £85.5  
   ![image](https://user-images.githubusercontent.com/41960992/194174738-5821bd6a-0977-4d84-863e-572c130acf5b.png)

   -Raspberry Pi Camera Module V2.1 = £28.5  
   ![image](https://user-images.githubusercontent.com/41960992/194174114-b8d20fe0-fad8-46fb-9b25-8bf07ce3d97f.png)

   - Dual Fan Heatsink Case for Raspberry Pi 4 = £14  
   ![image](https://user-images.githubusercontent.com/41960992/194181285-f81cedf6-155c-436f-a5bd-6b2ae65b789e.png)

   - Google Coral USB Accelerator - Edge TPU = £80  
   <img width="276" alt="image" src="https://user-images.githubusercontent.com/41960992/194181510-7f9a89f0-42ef-49b6-88b8-14ccb76040b0.png">
  
   - 1.47" Rounded SPI LCD Display Module (172x320) = £12
   ![image](https://user-images.githubusercontent.com/41960992/194182305-4b4b8869-b018-4d42-9cb4-4ad8756fcb99.png)

   - L-shabe USB-c to USB short power cable
   - small breadboard 30 lines
   - 8x 1.2v AA rechargeble batteries
   - GPIO extender
  
*References*
  
    https://www.electronicshub.org/raspberry-pi-l298n-interface-tutorial-control-dc-motor-l298n-raspberry-pi/
    https://github.com/garyexplains/examples/tree/master/servo
    https://github.com/gadgetoid/Pinout.xyz
    https://www.waveshare.com/wiki/1.47inch_LCD_Module
    https://lastminuteengineers.com/l298n-dc-stepper-driver-arduino-tutorial/
    https://github.com/raspberrypi/picamera2
  
    sudo apt update
    sudo apt install build-essential
    sudo apt install libatlas-base-dev
    sudo apt install python3-pip
    pip3 install tflite-runtime
    pip3 install opencv-python==4.4.0.46
    pip3 install pillow
    pip3 install numpy

Notes: 
gpio22 = front midle sensor + resistor yello
gpio27 = front midle sensor
gpio17 = back sensor + resistor + yello
gpio04 = back midle sensor
