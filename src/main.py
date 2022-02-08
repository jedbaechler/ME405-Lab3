'''
    @file           main.py
    @brief          An adapted main file from basic_tasks.py
    @details        This file contains a demonstration program that runs 
                    some tasks, an inter-task shared variable, and a queue. 
                    The tasks don't really do anything; the example just shows
                    how these elements are created and run. 
                    We added motor control functions that act as the 
                    scheduler.

    @author         Jeremy Baechler
    @author         Kendall Chappell
    @author         Matthew Wimberley
    @date           31-Jan-2022
    '''

import gc
import pyb
import cotask
import task_share
import EncoderReader, controlloop, pyb, utime
import motor_baechler_chappell_wimberley as motor_drv



def motor1_func ():
    '''
        @brief      instantiates motor 1 object
        @details    This function reads the encoder data, which the controller
                    uses to find the new PWM, which then sets the new motor
                    speed.

    '''
    while True:
        try:
            PWM1 = controller1.run(enc1.read())
            controller1.add_data()
#             print('Motor 1 Data:', enc1.read(), PWM1)
            mot1.set_duty(PWM1)
            yield (0)
        except:
            pass
        
    

def motor2_func():
    '''
        @brief      instantiates motor 2 object
        @details    This function reads the encoder data, which the controller
                    uses to find the new PWM, which then sets the new motor
                    speed.

    '''
    while True:
        try:
            PWM2 = controller2.run(enc2.read())
            controller2.add_data()
#             print('Motor 2 Data:', enc2.read(), PWM2)
            mot2.set_duty(PWM2)
            yield (0)
        except:
            pass


def task2_fun ():
    '''
        @brief      prints data from shares and queues
        @details    Because this is a generator, we only print the data
                    at our discretion.
        '''
        
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
    
    mot1_pos = task_share.Share('h', name='mot1_pos') #shares motor1 position
    des_pos = task_share.Share('h', name='des_pos') #shares desired position
    kp = task_share.Share('h', name='kp') #shares kp
    pwm1 = task_share.Share('h', name='pwm1') #shares motor 1 duty cycle

    """ PLEASE PLUG ENCODER 1 BLUE WIRE INTO B7 AND YELLOW WIRE TO B6"""
    ENA = pyb.Pin (pyb.Pin.board.PA10, pyb.Pin.OUT_PP) #motor 1 enabler
    IN1 = pyb.Pin (pyb.Pin.board.PB4, pyb.Pin.OUT_PP) 
    IN2 = pyb.Pin (pyb.Pin.board.PB5, pyb.Pin.OUT_PP) #motor port A pins
    tim3 = pyb.Timer (3, freq=20000) #timer 3 

    """PLEASE PLUG ENCODER 2 BLUE WIRE INTO C7 AND YELLOW WIRE TO C6"""
    ENB = pyb.Pin (pyb.Pin.board.PC1, pyb.Pin.OUT_PP) #motor 2 enabler
    IN3 = pyb.Pin (pyb.Pin.board.PA0, pyb.Pin.OUT_PP)
    IN4 = pyb.Pin (pyb.Pin.board.PA1, pyb.Pin.OUT_PP) #motor port B pins
    tim5 = pyb.Timer (5, freq=20000) #using timer 5, must be different than m1

    mot1 = motor_drv.MotorDriver(ENA, IN1, IN2, tim3) #instants motor object
    enc1 = EncoderReader.EncoderReader(1) #instantiates encoder reader object
    controller1 = controlloop.ClosedLoop(.4, 30000) #sets gain and setpoint of m1

    mot2 = motor_drv.MotorDriver(ENB, IN3, IN4, tim5) #now for motor 1 
    enc2 = EncoderReader.EncoderReader(2) #now for encoder 1
    controller2 = controlloop.ClosedLoop(.4, 30000) #sets gain and setpoint of m2

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    task1 = cotask.Task (motor1_func, name = 'MotorTask_1', priority = 1, 
                         period = 10, profile = True, trace = False)
#     task2 = cotask.Task (motor2_func, name = 'MotorTask_2', priority = 1, 
#                          period = 1, profile = True, trace = False)
    #runs task on motor 2, controlling the object
    
    cotask.task_list.append (task1)
#     cotask.task_list.append (task2)

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
    
    
    for i in range(len(controller1.time)):
        print(controller1.time[i], ',', controller1.listpos[i])
    
    print('Stop Transmission')
            
    

# Print a table of task data and a table of shared information data
    print ('\n' + str (cotask.task_list))
    print (task_share.show_all ())
    print (task1.get_trace ())
    print ('\r\n')
