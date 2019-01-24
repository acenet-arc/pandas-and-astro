import pandas as pd
import datetime

def readFile(fileName):
  result=pd.read_fwf(fileName
    ,header=None
    ,usecols=[1,2,3,4,5,6,12]
    ,names=["year","month","day","hour","minute","second","lat"]
    )
  
  date=pd.to_datetime(result[["year","month","day","hour","minute","second"]])
  
  result=result.drop(["year","month","day","hour","minute","second"],axis=1)
  result["date"]=date
  
  #remove group data in an "intermittent" phase
  result=result[result.lat!=999999]
  
  #remove any dates that are earlier than expected
  preShape=result.shape
  result=result[result.date>pd.to_datetime("01/01/1874")]
  if(preShape!=result.shape):#compare shape before/after to detect file with strange date
    print("removed a row with a date before 01/01/1874")
  
  #note that the below line results in a empty data frame always, but the above
  #removes a point on the x-axis of the plot sometime in 1677
  #result=result[result.date<=pd.to_datetime("01/01/1874")]
  
  #this could be because the Year entry for that row is not given (e.g. just spaces)
  return result
def determinPeriodByEye(s,binCenters,plt):
  
  months=range(binCenters.size)
  
  #try to get a period manually
  #note that pandas doesn't have Fourier Transforms
  #for that we would need to introduce scipi (numpy?)
  from matplotlib import colors as mcolors
  
  colorNames=list(mcolors.CSS4_COLORS.keys())
  numColors=len(colorNames)
  while(True):
    period=input("enter a period in years (or q to quit)")
    
    
    if period=="q":
      break
    
    period=float(period)*12.0#convert period from years to months
    
    x=[]
    y=[]
    count=0
    fold=0
    foldLast=0
    for month in months:
      
      #monthsWrapped.append(month%(float(period)))
      foldLast=fold
      fold=int(month/(float(period)))
      #started a new fold
      if fold!=foldLast:
        colorIndx=fold%numColors
        print("fold="+str(fold))
        plt.plot(x,y,'-',color=colorNames[fold%numColors])
        x=[]
        y=[]
      
      x.append(month%(float(period)))
      y.append(s[count])
      count+=1
      
    plt.plot(x,y,'-',color=colorNames[0])
    plt.show()
def determinPeriodByFFT(s,n,t,plt):
  #TODO: this isn't making sense to me...
  #https://www.ritchievink.com/blog/2017/04/23/understanding-the-fourier-transform-by-example/
  import numpy as np
  trans=np.fft.fft(s)
  #t=1.0
  #n=len(binCenters)#number of months
  
  f=np.linspace(0,1.0/t,n)
  plt.bar(f[:n//2],np.abs(trans)[:n//2]*1.0/(float(n)),width=1.0/t/10000.0)
  plt.xlabel('Freq [HZ]')
  plt.ylabel('Amplitude')
  plt.show()
def main():
  
  #read data
  fileName="sunspotgroups_1874.txt"
  print("reading file "+fileName+" ...")
  
  totalData=readFile(fileName)
  for i in range(1875,2019):
    fileName="sunspotgroups_"+str(i)+".txt"
    print("reading file "+fileName+" ...")
    data=readFile(fileName)
    totalData=totalData.append(data)
  
  #make butterfly diagram
  print("plotting butterfly diagram ...")
  from matplotlib import pyplot as plt
  plt.plot(totalData["date"],totalData["lat"],'.')
  plt.show()
  
  #bin data into 1 month bins and count the number of sunspot groups in each bin
  daysInPeriod=20
  secsInPeriod=20.0*24.0*60.0*60.0
  print("binning sunspot groups into "+str(daysInPeriod)+" day bins and counting number of groups in bins ...")
  numPeriods=(2018-1875)*365.25/daysInPeriod
  freq=str(daysInPeriod)+"D"
  bins=pd.date_range("01/01/1875",periods=numPeriods,freq=freq)
  binCenters=pd.date_range("15/01/1875",periods=numPeriods-1,freq=freq)
  numBins=len(binCenters)
  print("numBins="+str(numBins))
  s=totalData.groupby(pd.cut(totalData["date"],bins=bins)).size()
  
  #show binned sunspot group count
  plt.plot(binCenters,s,'-')
  plt.show()
  
  print("performing FFT on binned data ...")
  #try a couple different methods for period determination
  #by eye methods is very awkward, could probably do just as well by looking at
  #complete time series and measure peak-to-peak distances
  #determinPeriodByEye(s,binCenters,plt)
  
  #Since FFT expects sinusoidal signals, subtracting the mean will remove the 
  #"0 HZ" component
  #Also noticed a spike at ~2.18675e-10 HZ=>145 years, our data period is 
  #2018-1874=144 years.. hmmm
  #finally got a spike at ~2.887e-9 HZ =>11 years
  s=s-s.mean()
  determinPeriodByFFT(s,numBins,secsInPeriod,plt)
  
if __name__=="__main__":
  main()