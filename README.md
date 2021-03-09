This project is for communicating text in morse code using a LED and a light resistor.

It uses example code from Freenove

Standards implemented:
- Morse code
- RS-232
- UTF-8

Binary Packet structure :  
0 = led on  
1 = led off

| Position    | Length                | Description           |
| :---------- | :-------------------: | --------------------: |
| 0           | 1                     | Start signal (led on) |
| 1           | 7                     | Length of data        |
| 17          | Length                | Data                  |

File structure :

- Length of file (24 bit)
- File name zero-terminated
- File data
