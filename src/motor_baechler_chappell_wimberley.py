'''
@file      motor_baechler_chappell_wimberley.py
@brief     sets up motor driver
@details   instantiates timer channels within constructor and sets motor duty cycle

@author    Jeremy Baechler
@author    Kendall Chappell
@author    Matthew Wimberley
@date      20-Jan-2022
'''

import pyb, utime

class MotorDriver():
    '''@brief   instantiates motor objects
       @details This takes the enable pin, channels, and timer to start a motor.
                As well, the duty cycle can be modified from here.
'''
    
    def __init__(self, en_pin, IN1, IN2, timer):
        '''@brief    takes in motor pins, channels, and timer
           @param    en_pin:    enabler pin
           @param    IN1:       channel 1
           @param    IN2:       channel 2
           @param    timer      associated timer with motor
           '''
        
        self.ENA = en_pin
        self.IN1 = IN1
        self.IN2 = IN2
        self.timer = timer
        self.timchan1 = self.timer.channel (1, pyb.Timer.PWM, pin=self.IN1)
        self.timchan2 = self.timer.channel (2, pyb.Timer.PWM, pin=self.IN2)
    
    def set_duty(self, duty):
        '''@brief    sets motor duty cycle
           @details  if the duty cycle is negative, the channels are switched to switch direction
           @param    duty: the motor output as a percent
           '''
        
        self.ENA.high()

        if duty>0:
#             print('Duty positive')
            self.timchan1.pulse_width_percent(duty)
            self.timchan2.pulse_width_percent(0)
        elif duty<=0:
#             print('Duty negative')
            self.timchan1.pulse_width_percent(0)
            self.timchan2.pulse_width_percent(abs(duty))

if __name__ == '__main__':
    '''@brief   testing block
    '''
    
#     ENA = pyb.Pin (pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
#     IN1 = pyb.Pin (pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
#     IN2 = pyb.Pin (pyb.Pin.board.PB5, pyb.Pin.OUT_PP) #motor port A pins
#     tim3 = pyb.Timer (3, freq=20000)
#     mot1 = MotorDriver(ENA, IN1, IN2, tim3)
#     mot1.set_duty(50)
