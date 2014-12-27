import urllib2
'''
Script to download pdf from a url, you need specify the website URL, and change the 
filename in the loop, it mostly useful to download a sequence of files with the 
filename only differ by a sequence number, e.g. CH1.PDF, CH2.PDF, CH3.PDF ...
'''

def download_file(download_url, output_name):
    '''
    Download part, 
    download_url is the url point to the file
    output_name is filename you want to output
    '''
    response = urllib2.urlopen(download_url)
    file = open(output_name, 'w')
    file.write(response.read())
    file.close()
    print(output_name + " Completed")

if __name__ == "__main__":
    
    path = 'http://www.dspguide.com/'
    
    for i in range(35):
        #exmaple of the file name is: CH1.PDF
        filename = 'CH' + str(i) + '.PDF'
        
        fileloc = path + filename
        download_file(fileloc, filename)