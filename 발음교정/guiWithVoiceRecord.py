# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/	
# 하나의 윈도우 창에서 스위칭 하는 코드
# 필요 콘텐츠 화면
# 왼쪽                                                오른쪽
# |홈/1레벨1/2레벨/3레벨 버튼   ||                         |
# |이미지                       || 맞음/틀림 이미지        |
# |이미지설명 텍스트            || 현재 점수 텍스트         |
# |소리/녹음/녹음멈춤 버튼      || 전이미지/다음이미지 버튼 |
# 왼쪽은 거의 다 만든 듯

import tkinter as tk

#녹음
import threading
import pyaudio
import wave

#mp3 파일 재생
import pygame, mutagen.mp3

#이미지
from PIL import ImageTk, Image, ImageDraw 

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
        
        label = tk.Label(self, text="Select Your level")
        label.place(x=50, y=20, width=100, height=50)

        button = tk.Button(self, text="Level 1",command=lambda: controller.show_frame(PageOne))
        button.place(x=50, y=100, width=100, height=50)

        button2 = tk.Button(self, text="Level 2",command=lambda: controller.show_frame(PageTwo))
        button2.place(x=50, y=200, width=100, height=50)
        
        button3 = tk.Button(self, text="Level 3",command=lambda: controller.show_frame(PageThree))
        button3.place(x=50, y=300, width=100, height=50)

#Level1
class PageOne(tk.Frame):
    
    chunk = 1024 
    sample_format = pyaudio.paInt16 
    channels = 2
#     fs = 44100 
    fs = 16000 
    
    audio_frames = [] 

    def __init__(self, parent, controller):
        
        voice_name = 0
        mp3level = "level\\level1\\audio\\"
        mp3Name = mp3level+str(voice_name)+".mp3"
        
        image_name = 0
        imageLevel = "level\\level1\\image\\"
        imageDir = imageLevel+str(voice_name)+".jpg"
        print(imageDir)
        
        tk.Frame.__init__(self, parent)
        self.isrecording = False

        label = tk.Label(self, text="Page One!!!")
        label.place(x=100, y=0, width=100, height=30)
        
        button1 = tk.Button(self, text="Back to Home",command=lambda: controller.show_frame(StartPage))
        button1.place(x=0, y=0, width=100, height=30)

        button2 = tk.Button(self, text="Page Two",command=lambda: controller.show_frame(PageTwo))
        button2.place(x=200, y=0, width=100, height=30)
        
        button3 = tk.Button(self, text="Page Three",command=lambda: controller.show_frame(PageThree))
        button3.place(x=300, y=0, width=100, height=30)
        
        #이미지
        load = Image.open(imageDir)
        load = load.resize((350, 250))
        render = ImageTk.PhotoImage(load)
        img = tk.Label(self, image=render)
        img.image = render
        img.place(x=25, y=50)
        
        #설명
        questionText=tk.Text(self)
        questionText.insert("current", "Hello")
        questionText.place(x=27, y=300, width=350, height=30)
        
        #음성 재생 lambda 없으면 가장 먼저 실행 후 죽어버림
        button4=tk.Button(self, text="voice",command=lambda: self.voice(mp3Name))
        button4.place(x=50, y=360, width=100, height=50)
        
        #Record 녹음
        button5 = tk.Button(self, text='rec',command=self.startrecording)
        button5.place(x=150, y=360, width=100, height=50)
        button6 = tk.Button(self, text='stop',command=self.stoprecording)
        button6.place(x=250, y=360, width=100, height=50)
        
        
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
            
    def voice(self,mp3Name):
        sound_dir = mp3Name
        self.playmusic(sound_dir)
        
    def playmusic(self,mp3Name):
        pygame.init()

        bitsize = -16   # signed 16 bit. support 8,-8,16,-16
        channels = 1    # 1 is mono, 2 is stereo
        buffer = 2048   # number of samples (experiment to get right sound)
        mp3 = mutagen.mp3.MP3(mp3Name)
        frequency=mp3.info.sample_rate

        pygame.mixer.init()
        clock= pygame.time.Clock()
        pygame.mixer.music.load(mp3Name)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
    #         print("Playing... - func => playingmusic")
            clock.tick(1000)


class PageTwo(tk.Frame):
    
    chunk = 1024 
    sample_format = pyaudio.paInt16 
    channels = 2
#     fs = 44100 
    fs = 16000 
    
    audio_frames = [] 

    def __init__(self, parent, controller):
        
        voice_name = 0
        mp3level = "level\\level1\\audio\\"
        mp3Name = mp3level+str(voice_name)+".mp3"
        
        tk.Frame.__init__(self, parent)

        button1 = tk.Button(self, text="Back to Home",command=lambda: controller.show_frame(StartPage))
        button1.place(x=0, y=0, width=100, height=30)

        button2 = tk.Button(self, text="Page One",command=lambda: controller.show_frame(PageOne))
        button2.place(x=100, y=0, width=100, height=30)
        
        label = tk.Label(self, text="Page Two!!!")
        label.place(x=200, y=0, width=100, height=30)
        
        button3 = tk.Button(self, text="Page Three",command=lambda: controller.show_frame(PageThree))
        button3.place(x=300, y=0, width=100, height=30)
        
        #음성 재생 lambda 없으면 가장 먼저 실행 후 죽어버림
        button4=tk.Button(self, text="voice",command=lambda: self.voice(mp3Name))
        button4.place(x=50, y=360, width=100, height=50)
        
        #Record 녹음
        button5 = tk.Button(self, text='rec',command=self.startrecording)
        button5.place(x=150, y=360, width=100, height=50)
        button6 = tk.Button(self, text='stop',command=self.stoprecording)
        button6.place(x=250, y=360, width=100, height=50)
    
        
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
            
    def voice(self,mp3Name):
        sound_dir = mp3Name
        self.playmusic(sound_dir)
        
    def playmusic(self,mp3Name):
        pygame.init()

        bitsize = -16   # signed 16 bit. support 8,-8,16,-16
        channels = 1    # 1 is mono, 2 is stereo
        buffer = 2048   # number of samples (experiment to get right sound)
        mp3 = mutagen.mp3.MP3(mp3Name)
        frequency=mp3.info.sample_rate

        pygame.mixer.init()
        clock= pygame.time.Clock()
        pygame.mixer.music.load(mp3Name)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
    #         print("Playing... - func => playingmusic")
            clock.tick(1000)
        
class PageThree(tk.Frame):
    
    chunk = 1024 
    sample_format = pyaudio.paInt16 
    channels = 2
#     fs = 44100 
    fs = 16000 
    
    audio_frames = [] 

    def __init__(self, parent, controller):
        
        voice_name = 0
        mp3level = "level\\level1\\audio\\"
        mp3Name = mp3level+str(voice_name)+".mp3"
        
        tk.Frame.__init__(self, parent)

        button1 = tk.Button(self, text="Back to Home",command=lambda: controller.show_frame(StartPage))
        button1.place(x=0, y=0, width=100, height=30)

        button2 = tk.Button(self, text="Page One",command=lambda: controller.show_frame(PageOne))
        button2.place(x=100, y=0, width=100, height=30)
        
        button3 = tk.Button(self, text="Page Two",command=lambda: controller.show_frame(PageTwo))
        button3.place(x=200, y=0, width=100, height=30)
        
        label = tk.Label(self, text="Page Three!!!")
        label.place(x=300, y=0, width=100, height=30)
        
        #음성 재생 lambda 없으면 가장 먼저 실행 후 죽어버림
        button4=tk.Button(self, text="voice",command=lambda: self.voice(mp3Name))
        button4.place(x=50, y=360, width=100, height=50)
        
        #Record 녹음
        button5 = tk.Button(self, text='rec',command=self.startrecording)
        button5.place(x=150, y=360, width=100, height=50)
        button6 = tk.Button(self, text='stop',command=self.stoprecording)
        button6.place(x=250, y=360, width=100, height=50)
    
        
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
            
    def voice(self,mp3Name):
        sound_dir = mp3Name
        self.playmusic(sound_dir)
        
    def playmusic(self,mp3Name):
        pygame.init()

        bitsize = -16   # signed 16 bit. support 8,-8,16,-16
        channels = 1    # 1 is mono, 2 is stereo
        buffer = 2048   # number of samples (experiment to get right sound)
        mp3 = mutagen.mp3.MP3(mp3Name)
        frequency=mp3.info.sample_rate

        pygame.mixer.init()
        clock= pygame.time.Clock()
        pygame.mixer.music.load(mp3Name)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
    #         print("Playing... - func => playingmusic")
            clock.tick(1000)

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
