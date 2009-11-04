from pyo import *
import random

s = Server(44100, 1, 1024)

example = 5

if example == 1:
    t = HarmTable([1,0,0,.2,0,0,.1,0,0,.04])
    w = [Osc(t, random.uniform(196,204), .01).out() for i in range(100)]
    x = [Osc(t, random.uniform(296,304), .006).out() for i in range(100)]
    y = [Osc(t, random.uniform(396,404), .003).out() for i in range(100)]
    z = [Osc(t, random.uniform(496,504), .002).out() for i in range(100)]
elif example == 2:
    t = HarmTable([1-(i*.01) for i in range(100)])
    a = Osc(t, 20, .7).play()
    b = Osc(HarmTable(), .3, 500, 1000).play()
    c = Osc(HarmTable(), 1, 18, 20).play()
    f = Biquad(a, b, c, 0).out()
elif example == 3:
    a = Noise(.5).play()    
    b = Osc(HarmTable(), .3, 500, 1000).play()
    c = Osc(HarmTable(), 1, 18, 20).play()
    f = Biquad(a, b, c, 0).out()
elif example == 4:
    t = HarmTable()
    a = Osc(t, 300).play()
    b = Osc(t, 1, .48, .5).play()
    d = Disto(a, b).out()
elif example == 5:
    a = Noise(.5).out()
    b = Osc(HannTable(), .5).play()
    a *= b  
elif example == 6:
    t = SndTable('/Users/olipet/Desktop/sons/baseballmajeur_s.aif')
    a = Osc(t, t.getRate()).out()
    #b = Osc(HarmTable(), 20, 500, 750).play()
    #c = Osc(HarmTable(), 19.65, 20, 22).play()
    #f = Biquad(a, b, c).out()

    
class FreqMod:
    def __init__(self, carrier=250, ratio=.5, index=1, amplitude=1):
        self.carrierFrequency = carrier
        self.ratio = ratio
        self.index = index
        self.modulatorFrequency = carrier * ratio
        self.modulatorAmplitude = self.modulatorFrequency * index
        self.amplitude = amplitude
        
        self.table = HarmTable([1])
        self.modulator = Osc(self.table, self.modulatorFrequency, self.modulatorAmplitude, self.carrierFrequency)
        self.carrier = Osc(self.table, self.modulator, self.amplitude)
        
    def play(self):
        self.modulator.play()
        self.carrier.out()
        return self
        
    def stop(self):
        self.modulator.stop()
        self.carrier.stop()

    def setCarrier(self, carrier):
        self.carrierFrequency = carrier
        self.modulatorFrequency = carrier * self.ratio
        self.modulatorAmplitude = self.modulatorFrequency * self.index
        self.refresh()

    def setRatio(self, ratio):
        self.ratio = ratio
        self.modulatorFrequency = self.carrierFrequency * ratio
        self.modulatorAmplitude = self.modulatorFrequency * self.index
        self.refresh()

    def setIndex(self, index):
        self.index = index
        self.modulatorAmplitude = self.modulatorFrequency * index
        self.refresh()
          
    def refresh(self):    
        self.modulator.setFreq(self.modulatorFrequency) 
        self.modulator.setMul(self.modulatorAmplitude)
        self.modulator.setAdd(self.carrierFrequency)       
       