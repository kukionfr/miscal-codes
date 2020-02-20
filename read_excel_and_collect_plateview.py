#! C:\Users\user\Anaconda2
# Name: Kyu Sang Han
# Project: Chromosome Instability

import os
# mport re
import pandas as pd
from shutil import copyfile


def main():
    print "script is running at", os.getcwd(), "\n"
    dirname = '//serverdw/Pei-Hsun Wu 2/Stiffness and Chromosome instability project/Data/ASproject phase 4x scanning'
    datelist = [_ for _ in os.listdir(dirname) if "ASproject phase 4x scanning" in _]

    #read excel data
    df = pd.read_excel('//serverdw/Pei-Hsun Wu 2/Stiffness and Chromosome instability project/imaging stitching console/image database list_CINatStiffness.xlsx', sheetname='Sheet1')
    week = []
    day = []
    for i in df.index:
        week.append(df['on substrate week'][i])
        day.append(df['days after replating'][i])

    src= '//serverdw/Pei-Hsun Wu 2/Stiffness and Chromosome instability project/Data/ASproject phase 4x scanning/'
    dst= '//serverdw/Pei-Hsun Wu 2/Stiffness and Chromosome instability project/Data/ASproject phase 4x scanning/PlateView/'
    j=0
    for date in datelist:
        stiffnesslist = [_ for _ in os.listdir(dirname + '/' + date + '/') if "Evelyn" in _ or "evelyn" in _ or "kyu" in _ or "Kyu" in _]
        for stiffness in stiffnesslist:
            dstnew = dst+ date.replace(' ASproject phase 4x scanning','') + '_' + stiffness + "_week_"+ str(int(week[j])) + "_day_" + str(int(day[j])) +".tif"
            if os.path.exists(dstnew) == False:
                copyfile(src + date +'/' + stiffness + '/PlateView/plateMHL000_expID_plateview.tif', dstnew)
            j = j+1


main()


    #read excel data
#    df = pd.read_excel('//serverdw/Pei-Hsun Wu 2/Stiffness and Chromosome instability project/imaging stitching console/image database list_CINatStiffness.xlsx', sheetname='Sheet1')
#    imagedate = []
#    for i in df.index:
#        text = str(df['image location path'][i])
#        m = re.search(r'scanning(.+?)ASproject', text)
#        if m:
#            found = m.group(1)
#        imagedate.append(found.replace(" ","").replace("\\",""))
#    print imagedate








