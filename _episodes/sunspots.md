---
layout: episode
title: "Sunspots"
teaching: 90
exercises: 0
questions:
- ""
objectives:
- ""
keypoints:
- ""
---

Sunspots are dark regions which appear on the surface of the Sun and last for a few days to a few months and frequently appear in groups. The number of sunspots varies with the approximately 11-year solar magnetic activity cycle. To learn Pandas I chose to explore Sunspot data with the specific goal of trying to determine the period of the solar cycle.

## Choosing Data

To measure the solar cycle we will need counts of sunspots or relatedly counts of sunspot groups as a function of time. I found a good source for Sunspot data here: [http://fenyi.solarobs.csfk.mta.hu/DPD/](http://fenyi.solarobs.csfk.mta.hu/DPD/). The different types of data are described here: [http://fenyi.solarobs.csfk.mta.hu/ftp/pub/DPD/DPDformat.txt](http://fenyi.solarobs.csfk.mta.hu/ftp/pub/DPD/DPDformat.txt). There are three types of data "day", "group", and "spot". The "day" data contains sums of area covered by sunspots but not counts. So that leaves either the "spot" data or the "group" data. I have choosen to use the "group" data for two main reasons:

* An older portion of the data set (1874-1976) doesn't contain "spot" data so using "group" data allows a longer baseline.
* Using group data reduces the size of the data files considerably

## Downloading Data
Now that we have decided on the data to use the next step is to download it. We could just click on each link and save the file, however there is a file for each year from 1874 to 2018, so that is 145 files. That might take a while, lets get the computer to do for us. 

I am betting that someone has probably already wanted to download something over HTTP already using Python. So I search "python http download" in google. The first hit is a stack overflow page: [https://stackoverflow.com/questions/22676/how-do-i-download-a-file-over-http-using-python](https://stackoverflow.com/questions/22676/how-do-i-download-a-file-over-http-using-python). The first answer mentions "urllib2". Some searching for urllib2 information, revealed that in Python3 (which is what we are using) they dropped the "2" so it is just urllib, and here is the documentation: [https://docs.python.org/3/library/urllib.html](https://docs.python.org/3/library/urllib.html). 

Often when I want to do something new with Python (or any language) I go through some similar process to figure out if there is something out there already that can easily do what I want. There is usually a trade off between learning a new tool (module, function, library etc.) and creating the tool your self. If the task is relatively simple finding and learning a new tool can sometimes be more work than writing your own tool from scratch. However, if the task is more complex it can often be faster to use something that has already been created for the task.

In this case urllib is fairly simple to figure out and writing code from scratch to download content over HTTP could be a fair amount of work. Looking at the [urllib](https://docs.python.org/3/library/urllib.html) docs I see "urllib.request for opening and reading URLs" sounds like maybe what I want. Lets take a look.

>urllib.request.urlopen(url, data=None, [timeout, ]*, cafile=None, capath=None, cadefault=False, context=None)
>
>Open the URL url, which can be either a string or a Request object.

Usually with Python when you "open" something you get that object back, for example when working with files you get a file object back which lets you do operations on the file, like reading and writing. In the case of <code>urllib.request.urlopen</code> what do we get back? Reading a little further I see

>For HTTP and HTTPS URLs, this function returns a http.client.HTTPResponse object slightly modified. In addition to the three new methods above, the msg attribute contains the same information as the reason attribute — the reason phrase returned by server — instead of the response headers as it is specified in the documentation for HTTPResponse.

The first part of that tells us that <code>urlopen</code> returns an [HTTPResponse](https://docs.python.org/3/library/http.client.html#http.client.HTTPResponse) object when you use an HTTP or HTTPS url. Scrolling down in the docs we find:

>HTTPResponse.read([amt])
>
>Reads and returns the response body, or up to the next amt bytes.

Ah ha! That's what we want, it returns the body of the response, or in other words the body of the webpage. In our case the webpage is a plain text file with data in it. Now we can take what we get from the <code>read</code> function and write it to a file. Ok lets try writing some Python code to try this out.

Start by opening up your the Spyder IDE. 

I want to create a folder to work in, so in the "Console" tab type:

~~~
In[1]: pwd
~~~
{: .bash}
~~~
Out[1]: 'C:\\Users\\chris'
~~~
{: .output}
~~~
In[2]: cd Desktop
~~~
{: .bash}
~~~
C:\Users\chris\Desktop
~~~
{: .output}
~~~
In[3]: mkdir sunspots
In[4]: cd sunspots
~~~
{: .bash}
~~~
C:\Users\chris\Desktop\sunspots
~~~
{: .output}
Since we know we will be downloading a bunch of data files, lets make a separate directory to save them in to keep our directory from getting cluttered up with them.
~~~
In[]: mkdir data
~~~
{: .bash}

Next save the <code>temp.py</code> file to a file under this newly created directory called <code>get_data.py</code>. 

Lets put in some very simple python code to start by checking that everything works properly.

~~~
def main():
  print("hello world")
  
if __name__ == "__main__":
  main()
~~~
{: .language-python}

To run this code in the console type:
~~~
In[5]: run get_data.py
~~~
{: .bash}
~~~
hello world
~~~
{: .output}

Looks good! Now lets try out the urllib functions, first we must import the module by adding
~~~
import urllib
~~~
{: .language-python}

Now lets copy the URL of a test data file
* [http://fenyi.solarobs.csfk.mta.hu/ftp/pub/DPD/data/gDPD1974.txt](http://fenyi.solarobs.csfk.mta.hu/ftp/pub/DPD/data/gDPD1974.txt)

Noticing that the year is appended to the end of the URL. If we look at successive years we see that they all have the same URL except that the year part of it is incremented. So we can access the data for the different years with URLS like:

* [http://fenyi.solarobs.csfk.mta.hu/ftp/pub/DPD/data/gDPD1974.txt](http://fenyi.solarobs.csfk.mta.hu/ftp/pub/DPD/data/gDPD1974.txt)
* [http://fenyi.solarobs.csfk.mta.hu/ftp/pub/DPD/data/gDPD1975.txt](http://fenyi.solarobs.csfk.mta.hu/ftp/pub/DPD/data/gDPD1975.txt)
* ...
* [http://fenyi.solarobs.csfk.mta.hu/ftp/pub/DPD/data/gDPD2018.txt](http://fenyi.solarobs.csfk.mta.hu/ftp/pub/DPD/data/gDPD2018.txt)

So we could loop over the years 1974 to 2018. Further if we look at the pre-1974 data we see a similar pattern, though with a slightly different URL.

* [http://fenyi.solarobs.csfk.mta.hu/ftp/pub/GPR/data/gGPR1872.txt](http://fenyi.solarobs.csfk.mta.hu/ftp/pub/GPR/data/gGPR1872.txt)
* [http://fenyi.solarobs.csfk.mta.hu/ftp/pub/GPR/data/gGPR1872.txt](http://fenyi.solarobs.csfk.mta.hu/ftp/pub/GPR/data/gGPR1873.txt)
* ...
* [http://fenyi.solarobs.csfk.mta.hu/ftp/pub/GPR/data/gGPR1976.txt](http://fenyi.solarobs.csfk.mta.hu/ftp/pub/GPR/data/gGPR1976.txt)

You will notice that they overlap by a couple years, in the case of duplicates I am going to choose from the "newer". So we have two base URLS
* <code>http://fenyi.solarobs.csfk.mta.hu/ftp/pub/DPD/data/gDPD</code> over the range of years [1974, 2018]
* <code>http://fenyi.solarobs.csfk.mta.hu/ftp/pub/GPR/data/gGPR</code> over the range of years [1872, 1973]

from which we can append a year and a <code>.txt</code> to generate a complete URL we can use to download the data files. Lets put some of this into code:

~~~
import urllib

def main():
  
  baseURLNew="http://fenyi.solarobs.csfk.mta.hu/ftp/pub/DPD/data/gDPD"
  newYears=range(1974,2019,1)
  baseURLOld="http://fenyi.solarobs.csfk.mta.hu/ftp/pub/GPR/data/gGPR"
  oldYears=range(1872,1974,1)
  
  for year in newYears:
    print(year)
  
if __name__ == "__main__":
  main()
~~~
{: .language-python}
~~~
1974
1975
.
.
.
2018
~~~
{: .output}

Lets actually use urllib now and read in part of one of the data files and write it out to the console to check that we are getting what we wanted.
~~~
import urllib

def main():
  
  baseURLNew="http://fenyi.solarobs.csfk.mta.hu/ftp/pub/DPD/data/gDPD"
  newYears=range(1974,2019,1)
  baseURLOld="http://fenyi.solarobs.csfk.mta.hu/ftp/pub/GPR/data/gGPR"
  oldYears=range(1872,1974,1)
  
  for year in newYears:
    url=baseURLNew+str(year)+".txt"
    req=urllib.request.urlopen(url)
    data=req.read(1024)
    print(data)
    break
  
if __name__ == "__main__":
  main()
~~~
{: .language-python}
~~~
b'g 1974 01 02 03 20 30    312          45   227    23   116 -14.86  43.24  -5.51 155.45 0.2242\r\ng 1974 01 03 00 56 30    312          58   489    30   249 -15.42  42.06   5.17 202.06 0.2296\r\ng 1974 01 04 09 52 30    312          20    79    11    43 -15.04  42.17  23.34 241.70 0.4363\r\ng 1974 01 05 02 15 30    312           0    14     0     8 -14.53  39.96  30.13 247.70 0.5273\r\ng 1974 01 06 08 00 00    312           0     5     0     4 -17.73  42.93  49.43 249.96 0.7726\r\ng 1974 01 06 08 00 00   312m           0     2     0     2 -16.98 282.47 -71.03 106.72 0.9458\r\ng 1974 01 06 08 00 00   312n           0     7     0     4 -26.99  18.48  24.98 223.10 0.5526\r\ng 1974 01 08 06 46 16    314          17    95     9    50   6.79 309.91 -17.93  59.28 0.3571\r\ng 1974 01 08 06 46 16    316          15    77    45   227 -10.56 246.85 -81.00 100.07 0.9869\r\ng 1974 01 09 07 38 33    314          34   166    17    84   6.59 309.17  -5.03  24.87 0.2055\r\ng 1974 01 09 07 38 33    316          11   132    14   175 -10.65 245.93 -'
~~~
{: .output}
That looks about right but we have these extra <code>\r\n</code> where the newlines should be. The <code>\r</code> is actually a two character representation of single non-visitable character, the return character, used to indicate newl ines on older Mac OS. The <code>\n</code> is similarly a single non-visible character for newline, used on Linux and Unix operating systems to indicate newlines. On windows (since that is where I am running this code) a combination of both characters is used to indicate new lines. So if we write this text out to a file we will get exactly what we want. Lets try it.

~~~
import urllib

def main():
  
  baseURLNew="http://fenyi.solarobs.csfk.mta.hu/ftp/pub/DPD/data/gDPD"
  newYears=range(1974,2019,1)
  baseURLOld="http://fenyi.solarobs.csfk.mta.hu/ftp/pub/GPR/data/gGPR"
  oldYears=range(1872,1974,1)
  
  for year in newYears:
    url=baseURLNew+str(year)+".txt"
    req=urllib.request.urlopen(url)
    file=open("data/sunspot_groups_"+str(year)+".txt",'wb')
    size=1024
    data=req.read(size)
    while data:
      file.write(data)
      data=req.read(size)
    file.close()
    break
  
if __name__ == "__main__":
  main()
~~~
{: .language-python}
~~~
In []: run get_data.py
In []: ls 
~~~
{: .bash}
~~~
Volume in drive C has no label.
 Volume Serial Number is 98F0-FD07

 Directory of C:\Users\chris\Desktop\sunspots

2019-01-30  02:24 PM    <DIR>          .
2019-01-30  02:24 PM    <DIR>          ..
2019-01-30  02:24 PM               576 get_data.py
2019-01-30  02:29 PM           153,330 sunspot_groups_1974.txt
               2 File(s)        153,906 bytes
               2 Dir(s)  310,510,395,392 bytes free
~~~
{: .output}
~~~
In []: less sunspot_groups_1974.txt
~~~
{: .bash}
~~~
g 1974 01 02 03 20 30    312          45   227    23   116 -14.86  43.24  -5.51 155.45 0.2242
g 1974 01 03 00 56 30    312          58   489    30   249 -15.42  42.06   5.17 202.06 0.2296
g 1974 01 04 09 52 30    312          20    79    11    43 -15.04  42.17  23.34 241.70 0.4363
.
.
.
g 1974 12 21 11 23 00   539n           0     0     0     0 999999 999999 999999 999999 999999
.
.
.
g 1974 12 31 10 51 00    546          30   217    23   172  -8.99 242.48 -50.92  99.21 0.7776
g 1974 12 31 10 51 00    547           0     4     0     3   7.46 337.75  44.36 283.46 0.7152
~~~
{: .output}

To download all the files in the "new" data set we could now just remove the <code>break</code> and the loop would continue over all the years. But before we do that lets think about how we are going to download the "old" data set also. In that case we would want to replace <code>newYears</code> with <code>oldYears</code> and also the <code>baseURLNew</code> with <code>baserURLOld</code> otherwise the code would look exactly the same. The best way to do that would be to pull the code out into a function, which takes those variables as parameters. Doing this results in:

~~~
import urllib

def downloadDataSet(baseURL, yearRange):
  for year in yearRange:
    url=baseURL+str(year)+".txt"
    req=urllib.request.urlopen(url)
    file=open("data/sunspot_groups_"+str(year)+".txt",'wb')
    size=1024
    data=req.read(size)
    while data:
      file.write(data)
      data=req.read(size)
    file.close()
    break

def main():
  
  baseURLNew="http://fenyi.solarobs.csfk.mta.hu/ftp/pub/DPD/data/gDPD"
  newYears=range(1974,2019,1)
  baseURLOld="http://fenyi.solarobs.csfk.mta.hu/ftp/pub/GPR/data/gGPR"
  oldYears=range(1872,1974,1)
  
  downloadDataSet(baseURLOld,oldYears)
  downloadDataSet(baseURLNew,newYears)
  
if __name__ == "__main__":
  main()
~~~
{: .language-python}

which now downloads the first file in each old and new data set. Lets now add a print statement so we know what file is being downloaded, and remove the <code>break</code> so the loop continues. The final code looks like:

~~~
import urllib

def downloadDataSet(baseURL, yearRange):
  for year in yearRange:
    url=baseURL+str(year)+".txt"
    print("downloading \""+url+"\" ...")
    req=urllib.request.urlopen(url)
    file=open("data/sunspot_groups_"+str(year)+".txt",'wb')
    size=1024
    data=req.read(size)
    while data:
      file.write(data)
      data=req.read(size)
    file.close()

def main():
  
  baseURLNew="http://fenyi.solarobs.csfk.mta.hu/ftp/pub/DPD/data/gDPD"
  newYears=range(1974,2019,1)
  baseURLOld="http://fenyi.solarobs.csfk.mta.hu/ftp/pub/GPR/data/gGPR"
  oldYears=range(1872,1974,1)
  
  downloadDataSet(baseURLOld,oldYears)
  downloadDataSet(baseURLNew,newYears)
  
if __name__ == "__main__":
  main()
~~~
{: .language-python}

and it downloads all our data for us. The downloading of the data will take a little time, perhaps a few minutes.

## Plotting and Analysing the Data 

So far we haven't used any Pandas libraries but that is about to change.

To work with our data in Pandas we will want to read it into a data frame. Previously we have seen how to use pandas to read in a csv file, in our case however the data files are better described as fixed with format. Lets see what Pandas has for that, googling brings us to [https://pandas.pydata.org/pandas-docs/version/0.22/generated/pandas.read_fwf.html](https://pandas.pydata.org/pandas-docs/version/0.22/generated/pandas.read_fwf.html). So lets try that out:

~~~
import pandas as pd

def main():
  df=pd.read_fwf("data/sunspot_groups_1974.txt")
  print(df)
  
if __name__ == "__main__":
  main()
~~~
{: .language-python}
~~~
      g  1974  01  02     ...           43.24      -5.51     155.45       0.2242
0     g  1974   1   3     ...           42.06       5.17     202.06       0.2296
1     g  1974   1   4     ...           42.17      23.34     241.70       0.4363
...  ..   ...  ..  ..     ...             ...        ...        ...          ...
1611  g  1974  12  31     ...          242.48     -50.92      99.21       0.7776
1612  g  1974  12  31     ...          337.75      44.36     283.46       0.7152
~~~
{: .output}

so as before, the column headers aren't correct because the data files don't have them. Lets have a look at the file describing the format of the data [http://fenyi.solarobs.csfk.mta.hu/ftp/pub/DPD/DPDformat.txt](http://fenyi.solarobs.csfk.mta.hu/ftp/pub/DPD/DPDformat.txt). Also, we don't need to store all the data, we only need a few of the columns in the data file to do our analysis. We want all the date/time columns, and if we keep the Heliographic latitude B, we could also make a butterfly diagram. In the documentation for the <code>read_fwf</code> there is also a <code>usecols</code> which allows you to specify column indices or names. In our case we don't have column names so lets use indices.

~~~
import pandas as pd

def main():
  df=pd.read_fwf("data/sunspot_groups_1974.txt",
    usecols=[1,2,3,4,5,6,12],
    names=["year","month","day","hour","minute","second","lat"])
  print(df)
  
if __name__ == "__main__":
  main()
~~~
{: .language-python}
~~~
      year  month  day  hour  minute  second        lat
0     1974      1    2     3      20      30     -14.86
1     1974      1    3     0      56      30     -15.42
...    ...    ...  ...   ...     ...     ...        ...
1613  1974     12   31    10      51       0       7.46
~~~
{: .output}

To allow plotting as a function of time, we should combine the year-second columns into a single representation of date and time, conversion to a floating point Julian date could work, but lets see if Pandas already has something that will work. It does, we can use the [<code>pandas.to_datetime</code>](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_datetime.html) function to create a single date-time representation. Lets see how we can use that function easily with what we have, e.g. separate columns in a dataframe for year, month, etc. Browsing the docs for the function in the examples section I find:

>Assembling a datetime from multiple columns of a DataFrame. The keys can be common abbreviations like [‘year’, ‘month’, ‘day’, ‘minute’, ‘second’, ‘ms’, ‘us’, ‘ns’]) or plurals of the same
> ~~~
> >>> df = pd.DataFrame({'year': [2015, 2016],
>                        'month': [2, 3],
>                        'day': [4, 5]})
> >>> pd.to_datetime(df)
> 0   2015-02-04
> 1   2016-03-05
> dtype: datetime64[ns]
> ~~~
> {: .bash}

so in this example the <code>pandas.to_datetime</code> function takes a data frame with columns named 'year', 'month', 'day' and converts it into a datetime series. How do I know it returns a series and not one of the other return types mentioned in the docs (e.g. list-like or scalar)? It depends on the input, in our case a dataframe, but the docs do not mention a dataframe? Lets look into what a dataframe and a series are a little more.

A series is a 1D array with axis labels, as paraphrased from [pandas docs on series](https://pandas.pydata.org/pandas-docs/version/0.22/generated/pandas.Series.html)). A dataframe by contrast is actually a container for multiple series. The [pandas documentation](http://pandas.pydata.org/pandas-docs/version/0.13.1/generated/pandas.DataFrame.html) states for dataframes:

>two-dimensional size-mutable, potentially heterogeneous tabular data structure with labeled axes (rows and columns). Arithmetic operations align on both row and column labels. Can be thought of as a dict-like container for Series objects. The primary pandas data structure.

So a dataframe is really a container of series so if we pass in a dataframe what we get back would most likely be a series object.

However our dataframe doesn't just have our date and time columns in it there is also a "lat" column. Previously we have seen how you can select columns of a dataframe by indexing (using the <code>[]</code> operator) into it like
~~~
df['year']
~~~
{: .language-python}
This returns the <code>'year'</code> column. But it turns out you can actually also index into it using not only a single column name but a list of column names to get multiple columns out.
~~~
df[['year','month','day','hour','minute','second']]
~~~
{: .language-python}

