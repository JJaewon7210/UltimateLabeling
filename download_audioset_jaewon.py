
"""
Downloads youtube video locally
"""

import pandas as pd
import os
import pafy
import yt_dlp
import cv2


APIKEY_PATH   = 'D:/Construction Video/Data/youtubeAPIKEY.txt'
CSVFILE_PATH  = 'D:/Construction Video/Data/vggss_videolists.csv'
OUTPUT_PATH   = 'D:/Construction Video/Data/'
# OUTPUT_PATH + '/audio
# OUTPUT_PATH + '/audio_full
# OUTPUT_PATH + '/video
# OUTPUT_PATH + '/video_full

### download youtube video using URL ###

class downloadYTV():
    def __init__(self, CSVFILE_PATH,OUTPUT_PATH,APIKEY_PATH):
        with open(APIKEY_PATH,"r") as f: pafy.set_api_key(f.readline())
        self.CSVFILE_PATH = CSVFILE_PATH
        self.OUTPUT_PATH  = OUTPUT_PATH
        self.readCSV()
        self.videoNumber = len(self.DF)

    def readCSV(self):
        '''
        csv should have 3 columns
        1) # file : 9xAft5LlgW8
        2) start_time : 3 (second)
        3) end_time : 13 (second)
        '''
        self.DF = pd.read_csv(self.CSVFILE_PATH)

    def downloadFullLengthYoutubeVideo(self,DFstart,DFend):

        for i in range(DFstart,DFend):
            url         = self.DF.loc[i,'# file']
            start_time  = self.DF.loc[i,'start_time']
            end_time    = self.DF.loc[i,'end_time']
            duration    = end_time - start_time
            link        = "https://www.youtube.com/watch?v={}".format(url)
            outputvideo  = '{}/video_full/{}.mp4'.format(self.OUTPUT_PATH,url)
            trimvideo    = '{}/video/{}_{:06d}.mp4'.format(self.OUTPUT_PATH,url,int(start_time))
            outputaudio  = '{}/audio_full/{}.flac'.format(self.OUTPUT_PATH,url)
            trimaudio    = '{}/audio/{}_{:06d}.flac'.format(self.OUTPUT_PATH,url,int(start_time))
            
            
            if not os.path.isfile(outputvideo):
                ydl_opts = {'format': 'bestvideo[ext=mp4]+bestaudio/best',
                            'outtmpl': outputvideo}
                # ydl_opts = {'format': 'bestvideo/best',
                #             'outtmpl': outputvideo}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([link])
                
            if not os.path.isfile(outputaudio):
                ydl_opts = {'format': 'bestaudio/best',
                            'outtmpl': outputaudio}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([link])
                
            if not os.path.isfile(trimvideo):
                os.system("ffmpeg -i {} -t {} -ss {} -r 30 {}".format(outputvideo, duration, start_time, trimvideo))
                
            if not os.path.isfile(trimaudio):
                os.system("ffmpeg -i {} -t {} -ss {} {}".format(outputaudio, duration, start_time, trimaudio))


if __name__ == '__main__':
    work = downloadYTV(CSVFILE_PATH,OUTPUT_PATH,APIKEY_PATH)
    work.downloadFullLengthYoutubeVideo(0,work.videoNumber)
