#! /usr/bin/env python3

""" -----------------------------------------

Download WL data from FFWC website

Nazmul Ahasan Shawn	 
nzahasan@gmail.com

-----------------------------------------"""


import re,requests,pandas as pd,sys,datetime as dt

def ffwcWL():
	# regx
	datesRe =  r'<td.{12}>River.Name</td><td.{12}>Location</td><td.{12}>Danger.Level.<br..><i>.mPWD.</i></td><td>(..-..)</td><td>(..-..)</td>'
	wlRe = r'<td.{62}>Jamuna</td><td.{62}>Bahadurabad</td><td.{88}>.{1,2}\..{1,2}</td><td.{79}>(.{1,2}\..{1,2})</td><td.{79}>(.{1,2}\..{1,2})</td>'

	try:
		webpage = requests.get('http://www.ffwc.gov.bd/ffwc_charts/waterlevel.php')
		if webpage.status_code !=200: return None
	except: 
		return None
	

	wl = re.findall(wlRe,webpage.text)
	date = re.findall(datesRe,webpage.text)


	return [ date[0][0],wl[0][0] ],[ date[0][1],wl[0][1] ]



def main():

	if len(sys.argv)>=3:
		simDate = sys.argv[1]
		baseDir = sys.argv[2]
		
		if baseDir[-1]!='/':
			baseDir+='/'
	else:
		print("Atleast 2 argument: date baseDir")

	try:
		simYear = int(dt.datetime.strptime(simDate,'%Y%m%d').strftime('%Y'))
		currYear = int(dt.datetime.today().strftime('%Y'))
	except:
		print('Failed to parse date YYYYMMDD format')
		sys.exit()	

	obsWLcsv = baseDir+'DATA/QDATA/BH.WL.'+str(simYear)+'.csv'
	
	try:
		open(obsWLcsv,'r').close()
	except:
		file = open(obsWLcsv,'w')
		file.write('Date,WL\n')
		file.close()
		

	if simYear!=currYear: 
		print('-- Not downloading WL data from FFWC website\n-- SIM year is not current year...')
		return

	ffwcData = ffwcWL()

	csvDat = pd.read_csv(obsWLcsv)
	# csvDat.to_frame()

	for item in ffwcData:
		itemDate = item[0].replace('-','/')+'/'+str(currYear)
		itemData = float(item[1])
		

		if csvDat['Date'][csvDat['Date']==itemDate].shape[0] ==0:	

			rowFrame = pd.DataFrame([[itemDate,itemData]],columns=['Date','WL'])
			csvDat = csvDat.append(rowFrame,ignore_index=True)
			
	csvDat.to_csv(obsWLcsv,index=False)
	print('Data downloading done ... ')
	



if __name__ == '__main__':
	main()