"""!
@file basic_tasks.py
    This file contains a demonstration program that runs some tasks, an
    inter-task shared variable, and a queue. The tasks don't really @b do
    anything; the example just shows how these elements are created and run.

@author JR Ridgely
@date   2021-Dec-15 JRR Created from the remains of previous example
@copyright (c) 2015-2021 by JR Ridgely and released under the GNU
    Public License, Version 2. 
"""

import gc
import pyb
import cotask
import task_share
import EncoderReader, controlloop, pyb, utime
import motor_baechler_chappell_wimberley as motor_drv



def motor1_func ():
    """!
    
    """
    while True:
        try:
            PWM1 = controller1.run(enc1.read())
            controller1.add_data()
            print('Motor 1 Data:', enc1.read(), PWM1)
            mot1.set_duty(PWM1)
            yield (0)
        except:
            print('Sending Data!')
            mot1.set_duty(0)
            for i in range(len(controller1.time)):
                print(controller1.time[i], controller1.listpos[i])
        

def motor2_func():
    """!
    
    """
    while True:
        try:
            PWM2 = controller2.run(enc2.read())
            controller2.add_data()
            print('Motor 2 Data:', enc2.read(), PWM2)
            mot2.set_duty(PWM2)
            yield (0)
        except:
            print('Sending Data!')
            mot2.set_duty(0)
            for i in range(len(controller2.time)):
                print(controller2.time[i], controller2.listpos[i])


def task2_fun ():
    """!
    Task which takes things out of a queue and share to display.
    """
    while True:
        # Show everything currently in the queue and the value in the share
        print ("Share: {:}, Queue: ".format (share0.get ()), end='');
        while q0.any ():
            print ("{:} ".format (q0.get ()), end='')
        print ('')

        yield (0)


# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    print ('\033[2JTesting ME405 stuff in cotask.py and task_share.py\r\n'
           'Press ENTER to stop and show diagnostics.')

    # Create a share and a queue to test function and diagnostic printouts
    share0 = task_share.Share ('h', thread_protect = False, name = "Share 0")
    q0 = task_share.Queue ('L', 16, thread_protect = False, overwrite = False,
                           name = "Queue 0")
    
    mot1_pos = task_share.Share('h', name='mot1_pos')
    des_pos = task_share.Share('h', name='des_pos')
    kp = task_share.Share('h', name='kp')
    pwm1 = task_share.Share('h', name='pwm1')

    """ PLEASE PLUG ENCODER 1 BLUE WIRE INTO B7 AND YELLOW WIRE TO B6"""
    ENA = pyb.Pin (pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
    IN1 = pyb.Pin (pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
    IN2 = pyb.Pin (pyb.Pin.board.PB5, pyb.Pin.OUT_PP) #motor port A pins
    tim3 = pyb.Timer (3, freq=20000)

    """PLEASE PLUG ENCODER 2 BLUE WIRE INTO C7 AND YELLOW WIRE TO C6"""
    ENB = pyb.Pin (pyb.Pin.board.PC1, pyb.Pin.OUT_PP)
    IN3 = pyb.Pin (pyb.Pin.board.PA0, pyb.Pin.OUT_PP)
    IN4 = pyb.Pin (pyb.Pin.board.PA1, pyb.Pin.OUT_PP) #motor port B pins
    tim5 = pyb.Timer (5, freq=20000)

    mot1 = motor_drv.MotorDriver(ENA, IN1, IN2, tim3)
    enc1 = EncoderReader.EncoderReader(1)
    controller1 = controlloop.ClosedLoop(.15, 13000)

    mot2 = motor_drv.MotorDriver(ENB, IN3, IN4, tim5)
    enc2 = EncoderReader.EncoderReader(2)
    controller2 = controlloop.ClosedLoop(.15, 13000)

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    task1 = cotask.Task (motor1_func, name = 'MotorTask_1', priority = 1, 
                         period = 10, profile = True, trace = False)
    task2 = cotask.Task (motor2_func, name = 'MotorTask_2', priority = 1, 
                         period = 10, profile = True, trace = False)
    
    cotask.task_list.append (task1)
    cotask.task_list.append (task2)

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect ()

    # Run the scheduler with the chosen scheduling algorithm. Quit if any 
    # character is received through the serial port
    vcp = pyb.USB_VCP ()
    while not vcp.any ():
        cotask.task_list.pri_sched ()

    # Empty the comm port buffer of the character(s) just pressed
    vcp.read ()

    # Print a table of task data and a table of shared information data
    print ('\n' + str (cotask.task_list))
    print (task_share.show_all ())
    print (task1.get_trace ())
    print ('\r\n')
