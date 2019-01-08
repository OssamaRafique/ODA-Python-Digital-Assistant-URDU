# -*- coding: utf-8 -*-
import subprocess
import wx
import wikipedia
import wolframalpha
import speech_recognition as sr
from mtranslate import translate

app_id = "U3JTX2-8U7TH2Y6W5"
client = wolframalpha.Client(app_id)
FirstQuestion = 'yes'
buck2uni = {
            u"\u0627":"A",
            u"\u0627":"A", 
            u"\u0675":"A", 
            u"\u0673":"A", 
            u"\u0630":"A", 
            u"\u0622":"AA", 
            u"\u0628":"B", 
            u"\u067E":"P", 
            u"\u062A":"T", 
            u"\u0637":"T", 
            u"\u0679":"T", 
            u"\u062C":"J", 
            u"\u0633":"S", 
            u"\u062B":"S", 
            u"\u0635":"S", 
            u"\u0686":"CH", 
            u"\u062D":"H", 
            u"\u0647":"H", 
            u"\u0629":"H", 
            u"\u06DF":"H", 
            u"\u062E":"KH", 
            u"\u062F":"D", 
            u"\u0688":"D", 
            u"\u0630":"Z", 
            u"\u0632":"Z", 
            u"\u0636":"Z", 
            u"\u0638":"Z", 
            u"\u068E":"Z", 
            u"\u0631":"R", 
            u"\u0691":"R", 
            u"\u0634":"SH", 
            u"\u063A":"GH", 
            u"\u0641":"F", 
            u"\u06A9":"K", 
            u"\u0642":"K", 
            u"\u06AF":"G", 
            u"\u0644":"L", 
            u"\u0645":"M", 
            u"\u0646":"N", 
            u"\u06BA":"N", 
            u"\u0648":"O", 
            u"\u0649":"Y", 
            u"\u0626":"Y", 
            u"\u06CC":"Y", 

            u"\u06D2":"E", 
            u"\u06C1":"H",
            u"\u064A":"E"  ,
            u"\u06C2":"AH"  ,
            u"\u06BE":"H"  ,
            u"\u0639":"A"  ,
            u"\u0643":"K" ,
            u"\u0621":"A",
            u"\u0624":"O",
            u"\u060C":"" #seperator ulta comma
}
def printAndSpeak(query):
	print query
	odaSpeak(query)
def odaAnswers(query):
	if query.lower() == "what is your name":
		print 'My name is ODA (Ossama\'s Digital Assistant)'
		odaSpeak('Mera Naam oda hai')
	elif query.lower() == "who are you":
		print 'Mera naam oda hai, Mein Ossama ka personal digital assistant hoon'
		odaSpeak('Mera naam oda hai, Mein Ossama ka personal digital assistant hoon')
	elif query.lower() == "who made you":
		print 'I was made by Ossama'
		odaSpeak('I was made by Ossama')
	else:
		searchAnswer(query)
def odaSpeak(query):
	speakoutput = '"' + query + '"';
	subprocess.call('espeak ' + str(speakoutput), shell = True)
def searchAnswer(input):
    try:
        res = client.query(input)
        answer = next(res.results).text
        print 'Answer in English : '+answer
        print 'Answer in Urdu : '+translate(answer,'ur-PK')
        odaSpeak(convertToRoman(translate(answer,'ur-PK')))
    except:
        try:
            input = input.split(' ')
            input = ' '.join(input[2: ])
            printAndSpeak(wikipedia.summary(input))
        except:
            print "Sorry I can not answer your question"
def convertToRoman(string, reverse=0):
	    for k, v in buck2uni.items():
	      if not reverse:
	            string = string.replace(k, v)
	      else:
	            string = string.replace(v, k)
	    return string

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None,
            pos=wx.DefaultPosition, size=wx.Size(450, 100),
            style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION |
             wx.CLOSE_BOX | wx.CLIP_CHILDREN,
            title="ODA | Ossama's Digital Assistant")
        panel = wx.Panel(self)
        my_sizer = wx.BoxSizer(wx.VERTICAL)
        lbl = wx.StaticText(panel,
        label=translate("I am Osama's Digital Assistant",'ur-PK'))
        my_sizer.Add(lbl, 0, wx.ALL, 5)
        self.txt = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER,size=(400,30))
        self.txt.SetFocus()
        self.txt.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)
        my_sizer.Add(self.txt, 0, wx.ALL, 5)
        panel.SetSizer(my_sizer)
        self.Show()
    def OnEnter(self, event):
    	global FirstQuestion
        input = self.txt.GetValue()
        input = input.lower()
        if input == "":
			r = sr.Recognizer()
			with sr.Microphone() as source:
				if FirstQuestion == 'yes':
					printAndSpeak("Ap mere se koi bhe sawaal kar sakte hein")
					FirstQuestion = 'no'
				else :
				    print "Sawal Karein"
				audio = r.listen(source)
			try:
				stt=r.recognize_google(audio,language='ur-PK')
				self.txt.SetValue(stt)
				print 'Question in Urdu : '+stt
				engQ=translate(stt.encode(encoding='UTF-8',errors='ignore'), 'en')
				print 'Question in English : '+engQ
				odaAnswers(engQ)
				self.txt.SetValue("")
			except sr.UnknownValueError:
				printAndSpeak("Mein apko theek tarha sun ni sak raha")
			except sr.RequestError as e:
				print "Could not process your request error :"+format(e)
        else:
        	searchAnswer(input)
	        


if __name__ == "__main__":
    app = wx.App(True)
    frame = MyFrame()
    app.MainLoop()