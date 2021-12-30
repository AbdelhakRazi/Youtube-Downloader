from pytube import YouTube
import pytube
import threading
import os
from PyQt5 import QtCore
import urllib
class Video :
    def __init__(self,path,link,quality,format):
        self.path = path
        self.link = link
        self.quality = quality
        self.format = format
    def downloadVideo(self,progress,complete_text):
         threading.Thread(
            target=self._downloadVideo, args=(progress, complete_text), daemon=True
        ).start()
    def _downloadVideo(self,progress,complete_text):
        def on_progress(chunk,filehandler,bytes_remaining):
            p=int( -((bytes_remaining*100)/chunk.filesize-100))
            progress.setValue(p)
        try:
            yt = YouTube(self.link,on_progress_callback=on_progress,)
            if(self.format=="MP4"):
                strm = yt.streams.filter(mime_type="video/mp4",res=self.quality).first()
                progress.show()
                strm.download(output_path=self.path)
            else:
                strm = yt.streams.filter(only_audio=True).first()
                progress.show()
                out_file = strm.download(output_path=self.path)
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'
                os.rename(out_file, new_file)    
        except urllib.error.URLError:
            _translate = QtCore.QCoreApplication.translate
            complete_text.setGeometry(QtCore.QRect(340, 480, 437, 20))
            complete_text.setText(_translate("MainWindow","No Internet"))
            complete_text.show()    
        except pytube.exceptions.RegexMatchError:
            _translate = QtCore.QCoreApplication.translate
            complete_text.setGeometry(QtCore.QRect(340, 480, 437, 20))
            complete_text.setText(_translate("MainWindow","Url is not valid"))
            complete_text.show()    