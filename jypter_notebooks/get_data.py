import urllib.request

#Data from:
#http://fenyi.solarobs.csfk.mta.hu/DPD/
#with data formats described here: 
#http://fenyi.solarobs.csfk.mta.hu/ftp/pub/DPD/DPDformat.txt

# older data here:
#http://fenyi.solarobs.csfk.mta.hu/GPR/index.html

def downloadFile(url,fileName):
  req=urllib.request.urlopen(url)
  file=open(fileName,'wb')
  size=1024
  data=req.read(size)
  while data:
    file.write(data)
    data=req.read(size)
  file.close()
  
def downloadDataSet(baseURL,start,stop):
  ext=".txt"
  for i in range(start,stop):
    url=baseURL+str(i)+ext
    print("downloading "+url+" ...")
    outputFileName="./sunspotgroups_"+str(i)+".txt"
    downloadFile(url,outputFileName)

def main():
  
  downloadDataSet("http://fenyi.solarobs.csfk.mta.hu/ftp/pub/GPR/data/gGPR",1874,1974)
  downloadDataSet("http://fenyi.solarobs.csfk.mta.hu/ftp/pub/DPD/data/gDPD",1974,2019)
  
if __name__=="__main__":
  main()