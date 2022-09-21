#!/usr/bin/env python3
"""
Module Docstring
"""
__author__ = "Parth"
__version__ = "0.1.0"
__license__ = "MIT"
import time, os, sys, re
#usage: python tokenGen.py <inputfile>    <tokenmapfile>  <PriceMonitorFile> <pymuxConfigFile>     <TTIAFile>             <TTGatewayFile>
#usage: python tokenGen.py MarketData.log TokenMap.config PriceMonitor.config  InstMasterInfo.config FIXInputAdapter.config FixContractTT_REGULAR.csv
def main():
    multiplier = 10000
    startTokenNo = 125
    timeZoneTZ = "UTC"
    expiryTime = "00:00:00"
    tokenNo = startTokenNo
    inputFile = open(sys.argv[1], 'r')
    tokenmapfile = open(sys.argv[2], 'w')
    priceMonitorFile = open(sys.argv[3], 'w')
    pymuxConfigFile = open(sys.argv[4], 'w')
    TTIAFile = open(sys.argv[5], 'w')
    TTGatewayFile = open(sys.argv[6], 'w')
    while True:
        line = inputFile.readline()
        if not line:
            inputFile.close()
            tokenmapfile.close()
            priceMonitorFile.close()
            pymuxConfigFile.close()
            TTIAFile.close()
            TTGatewayFile.close()
            break
    if "Received Security Definition" in line and "SecurityType(167)=OPT" in line:
        line_tokenized = re.split(':|,|\|', line)
        for token in line_tokenized:
            if "Symbol(55)" in token:
                underlyingSymbol = re.split('=', token)[1]
            if "SecurityExchange(207)" in token:
                exchange = re.split('=', token)[1]
            if "SecurityType(167)" in token:
                securityType = re.split('=', token)[1]
            if "MaturityDate(541)" in token:
                expiryDate = re.split('=', token)[1]
            if "SecurityID(48)" in token:
                SecurityID = re.split('=', token)[1]
            if "PutOrCall(201)" in token:
                PutOrCall = re.split('=', token)[1]
            if "StrikePrice(202)" in token:
                strikePrice = re.split('=', token)[1]
        # Prepare Our Instrument String
        lOptionType = ""
        if PutOrCall == "0":
            lOptionType = "PE"
        else:
            lOptionType = "CE"
        lStrikePrice = str(int((float(strikePrice) * multiplier) + 0.1))
        lYear = expiryDate[2:4]
        lMonth = expiryDate[4:6]
        if lMonth == "01":
            lMonth = "JAN"
        elif lMonth == "02":
            lMonth = "FEB"
        elif lMonth == "03":
            lMonth = "MAR"
        elif lMonth == "04":
            lMonth = "APR"
        elif lMonth == "05":
            lMonth = "MAY"
        elif lMonth == "06":
            lMonth = "JUN"
        elif lMonth == "07":
            lMonth = "JUL"
        elif lMonth == "08":
            lMonth = "AUG"
        elif lMonth == "09":
            lMonth = "SEP"
        elif lMonth == "10":
            lMonth = "OCT"
        elif lMonth == "11":
            lMonth = "NOV"
        elif lMonth == "12":
            lMonth = "DEC"
        InstrumentString = underlyingSymbol + lYear + lMonth + lStrikePrice + lOptionType

        # tokenmapfile
        d = expiryDate + " " + expiryTime
        p = '%Y%m%d %H:%M:%S'
        os.environ['TZ'] = timeZoneTZ
        epochTimeForExpiry = int(time.mktime(time.strptime(d, p)))
        outputLine = str(tokenNo) + "," + InstrumentString + ",Option," + lStrikePrice + "," + lOptionType[
            0] + ",1," + str(epochTimeForExpiry) + ",1,10,20,40," + str(multiplier) + "," + "\n"
        tokenmapfile.write(outputLine)

        # pymuxConfigFile
        outputLine = str(tokenNo) + "," + InstrumentString + "," + str(multiplier) + ",IB,MUL," + "\n"
        pymuxConfigFile.write(outputLine)

        # priceMonitorFile
    outputLine = str("1,") + InstrumentString + ",0.00," + str(multiplier) + "," + "\n"
    priceMonitorFile.write(outputLine)

    # TTIAFile
    outputLine = "1," + InstrumentString + "," + InstrumentString + "," + exchange + "," + SecurityID + "," + str(
        multiplier) + "," + "262=" + InstrumentString + "|263=1|264    =0|265=1|266=Y|267=3|269=0|269=1|269=2|146=1|55=" + underlyingSymbol + "|48=" + SecurityID + "|207=" + exchange + "|," + "\n"
    TTIAFile.write(outputLine)

    # TTGatewayFile
    outputLine = str(tokenNo) + "," + underlyingSymbol + "," + str(
        multiplier) + ",15=USD|207=" + exchange + "|100=" + exchange + "|1028=N|18=o 2|167=OPT|200=" + expiryDate[
                                                                                                       0:4] + expiryDate[
                                                                                                              4:6] + "|201=" + PutOrCall + "|202=" + strikePrice + "|59=W|,," + "\n"
    TTGatewayFile.write(outputLine)


    tokenNo = tokenNo + 1

if __name__ == "__main__":
    main()