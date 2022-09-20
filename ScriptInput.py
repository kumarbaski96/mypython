 1 #!/usr/bin/env python3
  2 """
  3 Module Docstring
  4 """
  5
  6 __author__ = "Parth"
  7 __version__ = "0.1.0"
  8 __license__ = "MIT"
  9
 10 import time, os, sys, re
 11 #usage: python tokenGen.py <inputfile>    <tokenmapfile>  <PriceMonitorFile> <pymuxConfigFile>     <TTIAFile>             <TTGatewayFile>
 12 #usage: python tokenGen.py MarketData.log TokenMap.config PriceMonitor.config  InstMasterInfo.config FIXInputAdapter.config FixContractTT_REGULAR.csv
 13
 14 def main():
 15         #1) configurations
 16         multiplier = 10000
 17         startTokenNo=125
 18         timeZoneTZ = "UTC"
 19         expiryTime = "00:00:00"
 20         tokenNo = startTokenNo
 21         inputFile = open(sys.argv[1], 'r')
 22         tokenmapfile = open(sys.argv[2], 'w')
 23         priceMonitorFile = open(sys.argv[3], 'w')
 24         pymuxConfigFile = open(sys.argv[4], 'w')
 25         TTIAFile = open(sys.argv[5], 'w')
 26         TTGatewayFile = open(sys.argv[6], 'w')
 27         while True:
 28                 line = inputFile.readline()
 29                 if not line:
 30                         inputFile.close()
 31                         tokenmapfile.close()
 32                         priceMonitorFile.close()
 33                         pymuxConfigFile.close()
 34                         TTIAFile.close()
 35                         TTGatewayFile.close()
 36                         break
 37                 if "Received Security Definition" in line and "SecurityType(167)=OPT" in line:
 38                         line_tokenized = re.split(':|,|\|', line)
 39                         for token in line_tokenized:
 40                                 if "Symbol(55)" in token:
 41                                         underlyingSymbol = re.split('=',token)[1]
 42                                 if "SecurityExchange(207)" in token:
 43                                         exchange = re.split('=',token)[1]
 44                                 if "SecurityType(167)" in token:
 45                                         securityType = re.split('=',token)[1]
 46                                 if "MaturityDate(541)" in token:
 47                                         expiryDate = re.split('=',token)[1]
 48                                 if "SecurityID(48)" in token:
 49                                         SecurityID = re.split('=',token)[1]
 50                                 if "PutOrCall(201)" in token:
 51                                         PutOrCall = re.split('=',token)[1]
 52                                 if "StrikePrice(202)" in token:
 53                                         strikePrice = re.split('=',token)[1]
 54                         #Prepare Our Instrument String
 55                         lOptionType = ""
 56                         if PutOrCall == "0":
 57                                 lOptionType = "PE"
 58                         else:
 59                                 lOptionType = "CE"
 60                         lStrikePrice = str(int((float(strikePrice)*multiplier)+0.1))
 61                         lYear = expiryDate[2:4]
 62                         lMonth = expiryDate[4:6]
 63                         if lMonth == "01":
 64                                 lMonth = "JAN"
 65                         elif lMonth == "02":
 66                                 lMonth = "FEB"
 67                         elif lMonth == "03":
 68                                 lMonth = "MAR"
 69                         elif lMonth == "04":
 70                                 lMonth = "APR"
 71                         elif lMonth == "05":
 72                                 lMonth = "MAY"
 73                         elif lMonth == "06":
 74                                 lMonth = "JUN"
 75                         elif lMonth == "07":
 76                                 lMonth = "JUL"
 77                         elif lMonth == "08":
 78                                 lMonth = "AUG"
 79                         elif lMonth == "09":
 80                                 lMonth = "SEP"
 81                         elif lMonth == "10":
 82                                 lMonth = "OCT"
 83                         elif lMonth == "11":
 84                                 lMonth = "NOV"
 85                         elif lMonth == "12":
 86                                 lMonth = "DEC"
 87                         InstrumentString = underlyingSymbol + lYear + lMonth + lStrikePrice + lOptionType
 88
 89                         #tokenmapfile
 90                         d=expiryDate + " " + expiryTime
 91                         p='%Y%m%d %H:%M:%S'
 92                         os.environ['TZ']=timeZoneTZ
 93                         epochTimeForExpiry = int(time.mktime(time.strptime(d,p)))
 94                         outputLine = str(tokenNo) + "," + InstrumentString + ",Option," + lStrikePrice + "," + lOptionType[0] + ",1," + str(epochTimeForExpiry) + ",1,10,20,40," + str(multiplier    ) + "," + "\n"
 95                         tokenmapfile.write(outputLine)
 96
 97                         #pymuxConfigFile
 98                         outputLine = str(tokenNo) + "," + InstrumentString + "," + str(multiplier) + ",IB,MUL," + "\n"
 99                         pymuxConfigFile.write(outputLine)
100
101                         #priceMonitorFile
102                         outputLine = str("1,") + InstrumentString + ",0.00," + str(multiplier) + "," + "\n"
103                         priceMonitorFile.write(outputLine)
104
105                         #TTIAFile
106                         outputLine = "1," + InstrumentString + "," + InstrumentString + "," + exchange + "," + SecurityID + "," + str(multiplier) + "," + "262=" + InstrumentString + "|263=1|264    =0|265=1|266=Y|267=3|269=0|269=1|269=2|146=1|55=" + underlyingSymbol + "|48=" + SecurityID + "|207=" + exchange + "|," + "\n"
107                         TTIAFile.write(outputLine)
108
109                         #TTGatewayFile
110                         outputLine = str(tokenNo) + "," + underlyingSymbol + "," + str(multiplier) + ",15=USD|207=" + exchange + "|100=" + exchange + "|1028=N|18=o 2|167=OPT|200=" + expiryDate[    0:4] + expiryDate[4:6] + "|201=" + PutOrCall + "|202=" + strikePrice + "|59=W|,," + "\n"
111                         TTGatewayFile.write(outputLine)
112
113                         tokenNo = tokenNo + 1
114
115 if __name__ == "__main__":
116         main()

