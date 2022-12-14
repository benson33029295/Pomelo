print("請稍等一會~ 可愛的杜杜鳥值得您的等待")
from bs4 import BeautifulSoup 
import requests
from pandas import DataFrame
##########################################################################
print_choice = input("想要藥理分類請輸入1, 想要中文適應症請輸入2 , 都想要請輸入3:")
doc_num=input('DOC帳號: ')
password_num=input("密碼:")
global login_session
login_session=requests.Session()

global section_num
global vs_num
global ward_num
global bed_num
global chart_num
section_num = input("科別:")
vs_num = input("主治DOC:")
ward_num = input("病房:")
bed_num = input('床號:')
chart_num=input("病歷號:")


def get_oc(address) :  # 按照網頁的請求構造請求頭
    headers = {
            #'User-Agent': user_agent.random,
            'Connection': 'keep-alive',
            #'Referer': referlink,
            'Origin': 'http://f5-ws5.ndmctsgh.edu.tw',
            'Referer': 'http://f5-ws5.ndmctsgh.edu.tw/eForm/Account/Login'
        }



    data = {
        'login_id': doc_num,
        'password': password_num
    }
    # 按照服務端的需要構造請求，並獲得session，記錄在login_session
    response = login_session.post(address, data=data, verify=False, headers=headers)
    return(response)


def get_pt_oc():
    ptsearchdata = {
            'SearchChartno': chart_num,
            'SearchChinaname': "",
            'SearchIDNo': '', #身分證號
            'SearchSectionNo': section_num,
            'SearchNRCode': ward_num,
            'SearchBedCode': bed_num,
            'SearchVSDR': vs_num,
            'SearchSpecialNote': '',
            'SearchCcGroup[]': ''
    }
# 按照網頁的請求構造請求頭
    headers = {
            #'User-Agent': user_agent.random,
            'Connection': 'keep-alive',
            #'Referer': referlink,
            'Origin': 'http://f5-ws5.ndmctsgh.edu.tw',
            'Referer': 'http://f5-ws5.ndmctsgh.edu.tw/eForm/Account/Login'
        }

    # 按照服務端的需要構造請求，並獲得session，記錄在login_session
    response = login_session.post("http://f5-ws5.ndmctsgh.edu.tw/eForm/Patient/Result", data=ptsearchdata, verify=False, headers=headers)
    return(response)

def create_pt_list():
    pt_oc=get_pt_oc() ## get patient list page original code as Request object
    pt_list= pt_oc.json() ##retract a list of partient information from patient list original code
    global outdates
    global chartnums 
    global hcasenums 
    global NameGenderAges
    global NrBedNos
    global indatetimes
    global vsnames
    outdates=[]
    chartnums=[]
    #六碼者labdataurl會有Q   ===> ok
    hcasenums=[]

    NameGenderAges = []
    NrBedNos = []
    indatetimes = []
    vsnames = []


    for x in pt_list:
        outdate1 = x['OUTDATETIME']
        print("出院日" + outdate1)
        outdates.append(outdate1)
##EXCLUDE PATIENT WITH ONE DAY DISCHARGE
        if outdate1 == "":
            chartnum1 = x['CHARTNO']
            print("病歷號" + chartnum1)
            chartnums.append(chartnum1)

            hcasenum1 = x['HCASENO']
            print(hcasenum1)
            hcasenums.append(hcasenum1)

            NameGenderAge1 = x['NameGenderAge']
            NrBedNo1 = x['NrBedNo']
            
            indatetime1 = x['INDATETIME'][:7]
            vsname1 = x['VSDRNAME']
            NameGenderAges.append(NameGenderAge1)
            NrBedNos.append(NrBedNo1)
            indatetimes.append(indatetime1)
            vsnames.append(vsname1)
####
def aligns_last(string, length = 73):
    difference = length - len(string) 

    new_string = ""
    space = " "
    # 計算限定長度為20時需要補齊多少個空格
    if difference == 0: # 若差值為0則不需要補
        return string


    elif difference < 0: 
        print('錯誤：限定的對齊長度小於字元串長度!') 
        return None


    else: 
        new_string = string[:-31] + space * difference + string[-31:]
        return new_string
    # 若是全形，則不轉換 return new_string + space*(difference) 
    # 返回補齊空格後的字元串 

def aligns_long(string, length = 86):
    difference = length - len(string) 

    new_string = ""
    space = " "
    # 計算限定長度為20時需要補齊多少個空格
    if difference == 0: # 若差值為0則不需要補
        return string


    elif difference < 0: 
        print('錯誤：限定的對齊長 度小於字元串長度!') 
        return None



    else: 
        new_string = string[:-44] + space * difference + string[-44:]
        return new_string

def aligns_drugname(string, length = 20):
    difference = length - len(string) 

    new_string = ""
    space = " "
    # 計算限定長度為20時需要補齊多少個空格
    if difference == 0: # 若差值為0則不需要補
        return string


    elif difference < 0: 
        print('錯誤：限定的對齊長度小於字元串長度!') 
        return string[:40]


    else: 
        new_string = string + space * difference
        return new_string
    # 若是全形，則不轉換 return new_string + space*(difference)
    # 返回補齊空格後的字元串 
##################


def get_druglist():
    global patients_drugs
    patients_drugs=[]
    global patients_drugs_forsearch 
    patients_drugs_forsearch = []
    for h in range(len(hcasenums)):
        print("drug" + str(h)*10)
        ###################################################################################################
        #drug

        drug_url = 'http://mobilereport.ndmctsgh.edu.tw/mr/HISEXNDREPORT.aspx?login_id=' + doc_num + '&special=n&cno=' + chartnums[h]
        headers = {
        #'User-Agent': user_agent.random,
        'Connection': 'keep-alive',
        #'Referer': referlink,
        'Origin': 'http://f5-ws5.ndmctsgh.edu.tw',
        'Referer': 'http://f5-ws5.ndmctsgh.edu.tw/eForm/Account/Login'
        }
        drug_oc = login_session.get(drug_url, verify=False, headers=headers)
        #print(response.content)


        if drug_oc.status_code == requests.codes.ok:
            print("取得成功")
        else:
            print("取得失敗")

        #print(htmlfile4.text)


        drug_soup=BeautifulSoup(drug_oc.text, 'lxml')


        #div data-role="content"
        drugdata = drug_soup.find('div', {'data-role': 'content'})
        #print("資料型態", type(table))
        #print("串列長度", len(table))
        #print(drugdata)
        print(drugdata.text)
        print(drugdata.text[87:-1])  ##delete the most upper line

        #patients_drugs.append(drugdata.text[86:])




        druglist = drugdata.text[87:-1].splitlines() ##put a bunch of string seperated by \n into 


        drugs= []

        drug_dose = []

        drug_freq = []

        drug_method = []

        drug_start_time = []
        #drugothers = []

        #drugs_forsearch = []

        for drugline in druglist:
            #diff = 84-len(drugline)        
            #if len(drugline) > 75:
            #    drugline = aligns_long(drugline)
            #else:
            #    drugline = aligns_last(drugline)
            global druglinecut
            print(drugline)
            if len(drugline)<=78:
                drugname = drugline[:40]
                druglinecut=drugline[-31:]
                if drugname in drugs:
                    ind = drugs.index(drugname)
                    drug_dose1 = druglinecut[0:6]
                    drug_dose[ind] += ("|"+drug_dose1)
                    drug_freq1 = druglinecut[6:14]
                    drug_freq[ind]+=("|"+drug_freq1)
                    drug_method1 = druglinecut[14:20]
                    drug_method[ind]+=("|"+drug_method1)
                    drug_start_time1 = druglinecut[20:25]
                    drug_start_time[ind]+=("|"+drug_start_time1)

                else:

                    drugs.append(drugname)
                    drug_dose1 = druglinecut[0:6]
                    drug_dose.append(drug_dose1)
                    drug_freq1 = druglinecut[6:14]
                    drug_freq.append(drug_freq1)
                    drug_method1 = druglinecut[14:20]
                    drug_method.append(drug_method1)
                    drug_start_time1 = druglinecut[20:25]
                    drug_start_time.append(drug_start_time1)
                    #drugs.append(drugname + drugother)

            else:
                drugname = drugline[:40]
                druglinecut=drugline[-44:]
                if drugname in drugs:
                    ind = drugs.index(drugname)
                    drug_dose1 = druglinecut[0:6]
                    drug_dose[ind] += ("|"+drug_dose1)
                    drug_freq1 = druglinecut[6:14]
                    drug_freq[ind]+=("|"+drug_freq1)
                    drug_method1 = druglinecut[14:20]
                    drug_method[ind]+=("|"+drug_method1)
                    drug_start_time1 = druglinecut[20:25]
                    drug_start_time[ind]+=("|"+drug_start_time1)

                else:

                    drugs.append(drugname)
                    drug_dose1 = druglinecut[0:6]
                    drug_dose.append(drug_dose1)
                    drug_freq1 = druglinecut[6:14]
                    drug_freq.append(drug_freq1)
                    drug_method1 = druglinecut[14:20]
                    drug_method.append(drug_method1)
                    drug_start_time1 = druglinecut[20:25]
                    drug_start_time.append(drug_start_time1)
                    #drugs.append(drugname + drugother)

        #drugdata_cut = '\n'.join(drugs)
        #patients_drugs.append(drugdata_cut)
        global druginfo_dataframe
        druginfo_dataframe = DataFrame(list(zip(drugs, drug_dose, drug_freq,  drug_method, drug_start_time)),
                                    columns=["商品名", "dose", "freq", "method", "開始時間"])








        patients_drugs.append(druginfo_dataframe)

        patients_drugs_forsearch.append(drugs)


        druginfo_dataframe

##MAIN CODE
progressnote_oc= get_oc("http://f5-ws5.ndmctsgh.edu.tw/eForm/Account/Login")## get progress note main page original code
progressnote_soup=BeautifulSoup(progressnote_oc.text, "lxml") ##Soup the progress note page

###above neccessary??

create_pt_list()
get_druglist()
#testing
print(NameGenderAges)
print(NrBedNos)
    #print("Prof:"+ a["NameGenderAge"] + "   CHARTNO"+ a["CHARTNO"] + "   VS:" + a["VSDRNAME"] +"   Bednumber:" + a['NrBedno'] + "\n")

################################################################################################################

global h_dataframes
h_dataframes = []
global h_dataframes2
h_dataframes2 = []
global h_dataframes3
h_dataframes3 = []

for h in range(len(hcasenums)):
    print("drug" + str(h)*10)   
    global objtagdrugnames
    global objtagdrugnames_short
    global objtagdrugtypes
    global objtagdrugindis
    global objtagdrugpaths
    objtagdrugnames = []
    objtagdrugnames_short = []
    objtagdrugtypes = []
    objtagdrugindis = []
    objtagdrugpaths = []
    
    for i in range(len(patients_drugs_forsearch[h])):
        print("drug" + str(h)*10 + str(i)*10)  

        
        
        #querydrug = druglist[i][:30]
        querydrug = patients_drugs_forsearch[h][i]
        print(querydrug)
        
        print(querydrug)
        url = "http://f5-eserver101.ndmctsgh.edu.tw/Med/web/MedList.aspx?QryType=1&PrefixName=" + querydrug
        
        

        response = requests.get(url)
        #print(response.text)
        
        objSoup1=BeautifulSoup(response.text, 'lxml')
        print(type(objSoup1))
        
        
        objtag1 = objSoup1.find("td")
        
        
        if objtag1 == None:
            objtagdrugnames.append("None!")
            objtagdrugnames_short.append("None!")
            objtagdrugtypes.append("None!")
            objtagdrugindis.append("None!")
            objtagdrugpaths.append("None!")
            continue
            
        
        objtag2 = objtag1.find("a")
        
        drugurl = "http://f5-eserver101.ndmctsgh.edu.tw/Med/web/" + objtag2.get("href")
        
        print(drugurl)
        
        #抓藥物資料
        
        response2 = requests.get(drugurl)

        
        objSoup2=BeautifulSoup(response2.text, 'lxml')
        print(type(objSoup2))
        
        
        objtag3 = objSoup2.find('div', {'id': 'accordion'})


        
        
        #學名
        print("學名" )
        # <span id="labDrugElemCode1">
        objtagdrugname1 = objtag3.find('span', {'id': 'labDrugElemCode1'})
        objtagdrugname2 = objtag3.find('span', {'id': 'labDrugElemCode2'})
        objtagdrugname3 = objtag3.find('span', {'id': 'labDrugElemCode3'})
        objtagdrugname4 = objtag3.find('span', {'id': 'labDrugElemCode4'})


        objtagdrugpath1_1 = ""
        objtagdrugpath1_2 = ""
        objtagdrugpath1_3 = ""

        
        objtagdrugpath2_1 = ""
        objtagdrugpath2_2 = ""
        objtagdrugpath2_3 = ""

        
        objtagdrugpath3_1 = ""
        objtagdrugpath3_2 = ""
        objtagdrugpath3_3 = ""

        
        objtagdrugpath4_1 = ""
        objtagdrugpath4_2 = ""
        objtagdrugpath4_3 = ""
        
        if objSoup2.find("li",{'id':'AHFS1'}).find('a', {'id': 'labAHFSA1'}) != None :
            objtagdrugpath1_1 = objSoup2.find("li",{'id':'AHFS1'}).find('a', {'id': 'labAHFSA1'}).text
        if objSoup2.find("li",{'id':'AHFS1'}).find('a', {'id': 'labAHFSA2'}) != None :
            objtagdrugpath1_2 = objSoup2.find("li",{'id':'AHFS1'}).find('a', {'id': 'labAHFSA2'}).text
        if objSoup2.find("li",{'id':'AHFS1'}).find('a', {'id': 'labAHFSA3'}) != None :
            objtagdrugpath1_3 = objSoup2.find("li",{'id':'AHFS1'}).find('a', {'id': 'labAHFSA3'}).text

        if objSoup2.find("li",{'id':'AHFS1'}).find('a', {'id': 'labAHFSB1'}) != None:
            objtagdrugpath2_1 = objSoup2.find("li",{'id':'AHFS1'}).find('a', {'id': 'labAHFSB1'}).text
        if objSoup2.find("li",{'id':'AHFS1'}).find('a', {'id': 'labAHFSB2'}) != None:
            objtagdrugpath2_2 = objSoup2.find("li",{'id':'AHFS1'}).find('a', {'id': 'labAHFSB2'}).text
        if objSoup2.find("li",{'id':'AHFS1'}).find('a', {'id': 'labAHFSB3'}) != None:
            objtagdrugpath2_3 = objSoup2.find("li",{'id':'AHFS1'}).find('a', {'id': 'labAHFSB3'}).text

        if objSoup2.find("li",{'id':'AHFS1'}).find('a', {'id': 'labAHFSC1'}) != None :
            objtagdrugpath3_1 = objSoup2.find("li",{'id':'AHFS1'}).find('a', {'id': 'labAHFSC1'}).text
        if objSoup2.find("li",{'id':'AHFS1'}).find('a', {'id': 'labAHFSC2'}) != None :
            objtagdrugpath3_2 = objSoup2.find("li",{'id':'AHFS1'}).find('a', {'id': 'labAHFSC2'}).text
        if objSoup2.find("li",{'id':'AHFS1'}).find('a', {'id': 'labAHFSC3'}) != None :
            objtagdrugpath3_3 = objSoup2.find("li",{'id':'AHFS1'}).find('a', {'id': 'labAHFSC3'}).text

        if objSoup2.find("li",{'id':'AHFS1'}).find('a', {'id': 'labAHFSD1'}) != None:
            objtagdrugpath4_1 = objSoup2.find("li",{'id':'AHFS1'}).find('a', {'id': 'labAHFSD1'}).text
        if objSoup2.find("li",{'id':'AHFS1'}).find('a', {'id': 'labAHFSD2'}) != None:
            objtagdrugpath4_2 = objSoup2.find("li",{'id':'AHFS1'}).find('a', {'id': 'labAHFSD2'}).text
        if objSoup2.find("li",{'id':'AHFS1'}).find('a', {'id': 'labAHFSD3'}) != None:
            objtagdrugpath4_3 = objSoup2.find("li",{'id':'AHFS1'}).find('a', {'id': 'labAHFSD3'}).text

        
        objtagdrugname_1234 = objtagdrugname1.text +"/"+ objtagdrugname2.text +"/"+ objtagdrugname3.text +"/"+ objtagdrugname4.text
        
        namecount = 0
        if objtagdrugname1.text != "":
            namecount += 1
        if objtagdrugname2.text != "":
            namecount += 1
        if objtagdrugname3.text != "":
            namecount += 1
        if objtagdrugname4.text != "":
            namecount += 1
        print(objtagdrugname_1234.strip())
        objtagdrugpath1_1234 = ""
        objtagdrugpath2_1234 = ""
        objtagdrugpath3_1234 = ""
        objtagdrugpath4_1234 = ""
        
        if namecount == 1:
            objtagdrugpath1_1234 = objtagdrugpath1_1+">>" + objtagdrugpath1_2 + ">>" +objtagdrugpath1_3
        if namecount == 2:
            objtagdrugpath1_1234 = objtagdrugpath1_1+">>" + objtagdrugpath1_2 + ">>" +objtagdrugpath1_3
            objtagdrugpath2_1234 = objtagdrugpath2_1+">>" + objtagdrugpath2_2 + ">>" +objtagdrugpath2_3
        if namecount == 3:
            objtagdrugpath1_1234 = objtagdrugpath1_1+">>" + objtagdrugpath1_2 + ">>" +objtagdrugpath1_3
            objtagdrugpath2_1234 = objtagdrugpath2_1+">>" + objtagdrugpath2_2 + ">>" +objtagdrugpath2_3
            objtagdrugpath3_1234 = objtagdrugpath3_1+">>" + objtagdrugpath3_2 + ">>" +objtagdrugpath3_3
        if namecount == 4:
            objtagdrugpath1_1234 = objtagdrugpath1_1+">>" + objtagdrugpath1_2 + ">>" +objtagdrugpath1_3
            objtagdrugpath2_1234 = objtagdrugpath2_1+">>" + objtagdrugpath2_2 + ">>" +objtagdrugpath2_3
            objtagdrugpath3_1234 = objtagdrugpath3_1+">>" + objtagdrugpath3_2 + ">>" +objtagdrugpath3_3
            objtagdrugpath4_1234 = objtagdrugpath4_1+">>" + objtagdrugpath4_2 + ">>" +objtagdrugpath4_3
            
        objtagdrugpath_1234 = objtagdrugpath1_1234 +" / " +objtagdrugpath2_1234 +" / "+ objtagdrugpath3_1234 +" / "+ objtagdrugpath4_1234
        
        if objtagdrugname_1234.strip() == "":
            objtagdrugnames.append("None!")
            objtagdrugnames_short.append("None!")
            objtagdrugtypes.append("None!")
            objtagdrugindis.append("None!")
            objtagdrugpaths.append("None!")
            continue
        
        objtagdrugnames.append(objtagdrugname_1234.strip().title())
        objtagdrugnames_short.append(aligns_drugname(objtagdrugname_1234.strip().title()))
        objtagdrugpaths.append(objtagdrugpath_1234)
        
        
        
        
        #分類
        print("分類" )
        #<a id="labAHFSA1"
        objtagdrugtype0 = objtag3.find('span',{'id':'labATC'})
        print(objtagdrugtype0.text.strip())
        objtagdrugtypes.append(objtagdrugtype0.text.strip())

        
        
        
        #Indication
        print("Indication")
        #<span id="labDOHINDICATION"><br>高血壓。</span>
        objtagdrugindi = objtag3.find('span', {'id': 'labDOHINDICATION'})
        
        print(objtagdrugindi.text[:20])
        objtagdrugindis.append(objtagdrugindi.text)
        

        
    patients_drugs[h]["Drugtypes"] = objtagdrugtypes
    patients_drugs[h]["學名"] = objtagdrugnames
    patients_drugs[h]["Drugnames_short"] = objtagdrugnames_short
    patients_drugs[h]["Indications"] = objtagdrugindis
    patients_drugs[h]["PATH"] = objtagdrugpaths
    
    drugdataframe2 = patients_drugs[h].sort_values(by=['Drugtypes', "學名"], ascending=True)

    #localtimes = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()).replace(":","")
    #drugdataframe2.to_excel('try drug' + chartnums[h] + NameGenderAges[h] + '.xls')

    drugdataframe2.index = drugdataframe2["商品名"]
    #排對再append

    drugdataframe3 = drugdataframe2[[ "學名", "dose", "freq", "method", "開始時間", "Indications"]]
    h_dataframes.append(drugdataframe3)
    drugdataframe4 = drugdataframe2[[ "學名", "dose", "freq", "method", "開始時間", "PATH"]]
    h_dataframes2.append(drugdataframe4)
    drugdataframe5 = drugdataframe2[[  "學名", "PATH", "Indications"]]
    h_dataframes3.append(drugdataframe5)
    
    
global html
html='<br>'+"POMELO Ver1.3   PROGRAMMED BY M118 T.Y.H , INSPIRED BY M117 H.R.T"
      
if print_choice == '2':
    for i in range(len(h_dataframes)):
        html=html+'<br>'+str(NrBedNos[i]) +" "+ NameGenderAges[i] +"  病歷號:"+chartnums[i]+"  入院日期:"+indatetimes[i]
        html=html+h_dataframes2[i].to_html()
        
if print_choice == '1':
    for i in range(len(h_dataframes)):
        html=html+'<br>'+str(NrBedNos[i]) +" "+ NameGenderAges[i] +"  病歷號:"+chartnums[i]+"  入院日期:"+indatetimes[i]
        html=html+h_dataframes2[i].to_html()
if print_choice == '3':
    for i in range(len(h_dataframes)):
        html=html+'<br>'+str(NrBedNos[i]) +" "+ NameGenderAges[i] +"  病歷號:"+chartnums[i]+"  入院日期:"+indatetimes[i]
        html=html+h_dataframes3[i].to_html()

with open("dodobird_is_cute.html",'w', encoding="UTF-8") as _file:
    _file.write(html)

input("dodobird_is_cute.html 檔案在此資料夾產生 \n 注意如果重複執行程式會覆蓋原有檔案 \n 建議使用GOOGLE CHROME開啟並按下ctrlA再ctrlP列印整個網頁\n列印時使用橫式列印縮放50%最為理想")      
