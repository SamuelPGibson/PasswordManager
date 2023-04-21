from tkinter import Canvas
from chichitk import Timer


def seconds_text(sec:float):
    '''converts seconds to text in form (hh):(m)m:ss'''
    sec = int(sec)
    if sec >= 3600: # at least one hour
        return f'{sec // 3600}:{(sec % 3600) // 60:0>2}:{(sec % 60) // 1:0>2}'
    else: # less than one hour
        return f'{sec // 60}:{(sec % 60) // 1:0>2}'
    
def red_to_green(val):
    '''
    Purpose:
        returns a hex code val percent of the way between red and green
    Pre-conditions:
        :param val : float between 0 and 1 - 0 is fully red and 1 is fully green
    Post-conditions:
        (none)
    Returns:
        :return : str (hex code)
    '''
    val = max(0, min(1, val))
    hex_red = hex(int(round(255 * (1 - val), 0)))[2:]
    hex_green = hex(int(round(255 * val, 0)))[2:]
    return '#' + f'{hex_red:0>2}' + f'{hex_green:0>2}' + '00'


class TimeoutBar(Canvas):
    ''' Narrow bar to display time until lockout
        Fades from green to red as time expires
    '''
    def __init__(self, master, bg:str, duration:int, expire_function,
                 update_text_function, fps=100, height=3):
        '''
        Parameters
        ----------
            :param master tk.Frame - parent widget
            :param bg str (hex code) - background color
            :param duration int - timeout duration in seconds
            :param expire_function 0 argument function - called when time expires
            :param update_text_function 1 argument function (str) - to update text display
            :param fps: int - updates per second
            :param height: int - height of TimeoutBar in pixels
        '''
        Canvas.__init__(self, master, bg=bg, height=height, highlightthickness=0)
        self.__fps = fps # steps per second
        self.__steps = duration * self.__fps # total steps
        self.__update_text_function = update_text_function

        self.__Timer = Timer(1 / self.__fps, self.__update,
                             end_callback=expire_function,
                             max_step=self.__steps)

        self.fill_id = self.create_rectangle(0, 0, 0, 0, fill=bg, width=0)

    def restart(self):
        '''restarts timer'''
        self.__Timer.reset()
        self.__Timer.start()

    def __update(self, step:int):
        '''
        Purpose:
            updates color and coordinates of fill based step
            only called internally by self.__Timer
        '''
        perc = max(0, min(1, step / self.__steps))
        self.itemconfig(self.fill_id, fill=red_to_green(1 - perc))
        self.coords(self.fill_id, 0, 0, self.winfo_width() * perc, self.winfo_height())
        self.__update_text_function(seconds_text((self.__steps - step) / self.__fps))
