EESchema Schematic File Version 4
LIBS:Vbot-cache
EELAYER 26 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L MCU_Module:Arduino_Nano_v3.x A1
U 1 1 5C85782C
P 4100 3950
F 0 "A1" H 4100 2864 50  0000 C CNN
F 1 "Arduino_Nano_v3.x" H 4100 2773 50  0000 C CNN
F 2 "Module:Arduino_Nano" H 4250 3000 50  0001 L CNN
F 3 "http://www.mouser.com/pdfdocs/Gravitech_Arduino_Nano3_0.pdf" H 4100 2950 50  0001 C CNN
	1    4100 3950
	1    0    0    -1  
$EndComp
$Comp
L Motor:Motor_DC Vibrate_Motor_1
U 1 1 5C857934
P 7150 3250
F 0 "Vibrate_Motor_1" H 7308 3246 50  0000 L CNN
F 1 "3.3-5V" H 7308 3155 50  0000 L CNN
F 2 "" H 7150 3160 50  0001 C CNN
F 3 "~" H 7150 3160 50  0001 C CNN
	1    7150 3250
	1    0    0    -1  
$EndComp
$Comp
L Motor:Motor_DC Vibrate_Motor_2
U 1 1 5C8579A5
P 8400 3200
F 0 "Vibrate_Motor_2" H 8558 3196 50  0000 L CNN
F 1 "3.3V-5V" H 8558 3105 50  0000 L CNN
F 2 "" H 8400 3110 50  0001 C CNN
F 3 "~" H 8400 3110 50  0001 C CNN
	1    8400 3200
	1    0    0    -1  
$EndComp
$Comp
L Rom_Custom_Library:HC_05 U1
U 1 1 5C857A26
P 5850 3050
F 0 "U1" H 6228 2565 50  0000 L CNN
F 1 "HC_05" H 6228 2474 50  0000 L CNN
F 2 "" H 5900 3200 50  0001 C CNN
F 3 "" H 5900 3200 50  0001 C CNN
	1    5850 3050
	1    0    0    -1  
$EndComp
$Comp
L Device:R_US R1
U 1 1 5C857B9E
P 5400 4600
F 0 "R1" H 5468 4646 50  0000 L CNN
F 1 "1k" H 5468 4555 50  0000 L CNN
F 2 "" V 5440 4590 50  0001 C CNN
F 3 "~" H 5400 4600 50  0001 C CNN
	1    5400 4600
	1    0    0    -1  
$EndComp
$Comp
L Device:R_US R2
U 1 1 5C857BF6
P 5750 4600
F 0 "R2" H 5818 4646 50  0000 L CNN
F 1 "2K" H 5818 4555 50  0000 L CNN
F 2 "" V 5790 4590 50  0001 C CNN
F 3 "~" H 5750 4600 50  0001 C CNN
	1    5750 4600
	1    0    0    -1  
$EndComp
$Comp
L Device:Battery BT1
U 1 1 5C858370
P 2700 3900
F 0 "BT1" H 2808 3946 50  0000 L CNN
F 1 "9V" H 2808 3855 50  0000 L CNN
F 2 "" V 2700 3960 50  0001 C CNN
F 3 "~" V 2700 3960 50  0001 C CNN
	1    2700 3900
	1    0    0    -1  
$EndComp
Wire Wire Line
	2700 3700 2700 2800
Wire Wire Line
	2700 4100 2700 5000
Wire Wire Line
	4100 5000 4100 4950
Wire Wire Line
	6050 4100 6050 4250
Wire Wire Line
	5000 4250 5000 2950
Wire Wire Line
	5000 2950 4300 2950
Wire Wire Line
	5950 4100 5950 5000
Connection ~ 4100 5000
Wire Wire Line
	5000 4250 6050 4250
Wire Wire Line
	4100 5000 5750 5000
Wire Wire Line
	5400 4450 5750 4450
Wire Wire Line
	5750 4100 5750 4450
Connection ~ 5750 4450
Wire Wire Line
	5750 4750 5750 5000
Connection ~ 5750 5000
Wire Wire Line
	5400 4750 4850 4750
Wire Wire Line
	4850 4750 4850 2650
Wire Wire Line
	4850 2650 3450 2650
Wire Wire Line
	3450 2650 3450 3650
Wire Wire Line
	3450 3650 3600 3650
Wire Wire Line
	5850 4100 5850 4350
Wire Wire Line
	5850 4350 4750 4350
Wire Wire Line
	4750 4350 4750 2550
Wire Wire Line
	4750 2550 3300 2550
Wire Wire Line
	3300 2550 3300 3550
Wire Wire Line
	3300 3550 3600 3550
Wire Wire Line
	5750 5000 5950 5000
Wire Wire Line
	3150 3750 3600 3750
$Comp
L Transistor_BJT:2N3904 Q?
U 1 1 5C8654C7
P 7050 3900
F 0 "Q?" H 7241 3946 50  0000 L CNN
F 1 "2N3904" H 7241 3855 50  0000 L CNN
F 2 "Package_TO_SOT_THT:TO-92_Inline" H 7250 3825 50  0001 L CIN
F 3 "https://www.fairchildsemi.com/datasheets/2N/2N3904.pdf" H 7050 3900 50  0001 L CNN
	1    7050 3900
	1    0    0    -1  
$EndComp
$Comp
L Transistor_BJT:2N3904 Q?
U 1 1 5C865543
P 8300 3900
F 0 "Q?" H 8491 3946 50  0000 L CNN
F 1 "2N3904" H 8491 3855 50  0000 L CNN
F 2 "Package_TO_SOT_THT:TO-92_Inline" H 8500 3825 50  0001 L CIN
F 3 "https://www.fairchildsemi.com/datasheets/2N/2N3904.pdf" H 8300 3900 50  0001 L CNN
	1    8300 3900
	1    0    0    -1  
$EndComp
Wire Wire Line
	7150 3400 7150 3550
Wire Wire Line
	7150 3950 7150 4100
Wire Wire Line
	8400 3950 8400 4100
Connection ~ 8400 4100
Wire Wire Line
	8400 4100 8400 5000
Wire Wire Line
	8400 3350 8400 3500
Connection ~ 8400 3500
Wire Wire Line
	8400 3500 8400 3700
Wire Wire Line
	7150 3550 7150 3700
Connection ~ 7150 3550
Wire Wire Line
	7150 5000 8400 5000
Connection ~ 7150 5000
Connection ~ 7150 4100
Wire Wire Line
	7150 4100 7150 5000
Wire Wire Line
	7150 2950 7150 3050
Wire Wire Line
	8400 3000 8400 2950
Wire Wire Line
	8400 2950 7150 2950
Connection ~ 7150 2950
Wire Wire Line
	3150 2350 3150 3750
Wire Wire Line
	3600 3850 3050 3850
Wire Wire Line
	3050 3850 3050 2250
Wire Wire Line
	3050 2250 7750 2250
$Comp
L Device:R_US R?
U 1 1 5C873E60
P 6650 3900
F 0 "R?" H 6718 3946 50  0000 L CNN
F 1 "1k" H 6718 3855 50  0000 L CNN
F 2 "" V 6690 3890 50  0001 C CNN
F 3 "~" H 6650 3900 50  0001 C CNN
	1    6650 3900
	0    -1   -1   0   
$EndComp
$Comp
L Device:R_US R?
U 1 1 5C874868
P 7900 3900
F 0 "R?" H 7968 3946 50  0000 L CNN
F 1 "1k" H 7968 3855 50  0000 L CNN
F 2 "" V 7940 3890 50  0001 C CNN
F 3 "~" H 7900 3900 50  0001 C CNN
	1    7900 3900
	0    -1   -1   0   
$EndComp
Wire Wire Line
	5950 5000 7150 5000
Connection ~ 5950 5000
Wire Wire Line
	6850 3900 6800 3900
Wire Wire Line
	8100 3900 8050 3900
Wire Wire Line
	6500 3900 6500 2350
Wire Wire Line
	6500 2350 3150 2350
Wire Wire Line
	7750 3900 7750 2250
Wire Wire Line
	5000 2950 7150 2950
Connection ~ 5000 2950
Wire Wire Line
	4000 2800 4000 2950
Wire Wire Line
	2700 2800 4000 2800
Wire Wire Line
	2700 5000 4100 5000
$EndSCHEMATC
