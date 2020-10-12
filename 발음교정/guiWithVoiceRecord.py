# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/	
# 하나의 윈도우 창에서 스위칭 하는 코드
import tkinter as tk

import tkinter as tk
import threading
import pyaudio
import wave


class Main(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        self.config(background="red")

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo,PageThree):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            #배경색
            frame.config(bg="MistyRose")
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame): 
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        
        label = tk.Label(self, text="Start Page")
        label.pack(pady=10,padx=10)

        button = tk.Button(self, text="Level 1",command=lambda: controller.show_frame(PageOne))
        button.pack()

        button2 = tk.Button(self, text="Level 2",command=lambda: controller.show_frame(PageTwo))
        button2.pack()
        
        button3 = tk.Button(self, text="Level 3",command=lambda: controller.show_frame(PageThree))
        button3.pack()    


class PageOne(tk.Frame):
    
    chunk = 1024 
    sample_format = pyaudio.paInt16 
    channels = 2
#     fs = 44100 
    fs = 16000 
    
    audio_frames = [] 

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.isrecording = False
        
        label = tk.Label(self, text="Page One!!!")
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Back to Home",command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Page Two",command=lambda: controller.show_frame(PageTwo))
        button2.pack()
        
        button3 = tk.Button(self, text="Page Three",command=lambda: controller.show_frame(PageThree))
        button3.pack()
        
        #Record 녹음
        button4 = tk.Button(self, text='rec',command=self.startrecording)
        button4.pack()
        button5 = tk.Button(self, text='stop',command=self.stoprecording)
        button5.pack()
        
    def startrecording(self):
        self.p = pyaudio.PyAudio()  
        self.stream = self.p.open(format=self.sample_format,channels=self.channels,rate=self.fs,frames_per_buffer=self.chunk,input=True)
        self.isrecording = True
        
        print('Recording')
        t = threading.Thread(target=self.record)
        t.start()

    def stoprecording(self):
        self.isrecording = False
        print('recording complete')
        self.filename = "test.wav"
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.sample_format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(self.audio_frames))
        wf.close()
#         main.destroy()
    def record(self):
       
        while self.isrecording:
            data = self.stream.read(self.chunk)
            self.audio_frames.append(data)


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!")
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Back to Home",command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Page One",command=lambda: controller.show_frame(PageOne))
        button2.pack()
        
        button3 = tk.Button(self, text="Page Three",command=lambda: controller.show_frame(PageThree))
        button3.pack()
        
class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Three!!!")
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Back to Home",command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Page One",command=lambda: controller.show_frame(PageOne))
        button2.pack()
        
        button3 = tk.Button(self, text="Page Two",command=lambda: controller.show_frame(PageTwo))
        button3.pack()

def main():
    app = Main()
    #윈도우 크기
    app.geometry('800x420')
    app.resizable(width=0, height=0)
    #창 이름
    app.title("configure method")
    #ESC 키
    app.bind("<Escape>", lambda e: app.destroy())
    app.mainloop()

if __name__ == '__main__':
    main()
