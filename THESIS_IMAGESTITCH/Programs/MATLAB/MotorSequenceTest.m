test=false;

if test
    clear rpi;
    rpi=raspi('192.168.137.10','pi','raspberry');
    
    for i=1:120

       system(rpi, 'python3 /home/pi/Desktop/Programs/XLeft.py');

       if mod(i,20) == 0     
            
            for j=1:20
                system(rpi, 'python3 /home/pi/Desktop/Programs/XRight.py');
            end
                        
           system(rpi, 'python3 /home/pi/Desktop/Programs/XRight.py');
           system(rpi, 'python3 /home/pi/Desktop/Programs/YDown.py');
           pause(1);
       end
    end
    
    system(rpi, 'python3 /home/pi/Desktop/Programs/YUp.py');
end