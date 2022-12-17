# Import Module
import os
import pandas as pd

######################################### folder or file 경로 설정
# path = "C:/Users/21052/Desktop/49CCTAT16MGC_D2"
path = os.getcwd()
# path = os.path.dirname(os.path.realpath(__file__))

# Change the directory
# os.chdir(path)
# file_list = os.chdir(path)

######################################### Text data 불러와서 가공 및 저장 함수
def cal(file_path):
    # ========================================================== OI_log.txt 파일 불러오기
    # global variable setting
    global df

    # file open and read
    with open(file_path, 'r') as f:
        # mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as s:

        # List type 으로 data read
        DUT_log = f.readlines()

        #DUT_log의 List type data 를 opstr의 String type data 로 변환
        opstr = ' '
        for x in DUT_log:
            opstr += ' ' + x

        # opstr 에서 원하는 값을 찾아서 그 값의 Index 값을 추출
        index = opstr.find('Barcode')
        str_avs_barcode = opstr[index:index+29]

        index = opstr.find('--> ./wl avs_voltage')
        str_avs_vol = opstr[index+20:index+35]
        # if s.find(b'--> ./wl avs_voltage') != -1:

        # ========================================================== String type을 List로 변환
        list_avs_barcode = str_avs_barcode.split(sep=None, maxsplit=-1)
        str_avs_barcode = list_avs_barcode[2]
        list_avs_barcode = str_avs_barcode.split(sep=None, maxsplit=-1)

        list_avs_vol = str_avs_vol.split(sep=None, maxsplit=-1)
        str_avs_voltage = list_avs_vol[0]
        str_avsCode = list_avs_vol[1]

        list_avs_vol = str_avs_voltage.split(sep=None, maxsplit=-1)
        list_avsCode = str_avsCode.split(sep=None, maxsplit=-1)

        # ========================================================== list를 Dataframe로 변환
        df_avs_barcode = pd.DataFrame(list_avs_barcode)
        df_avs_vol = pd.DataFrame(list_avs_vol)
        df_avsCode = pd.DataFrame(list_avsCode)

        # ========================================================== Dataframe에서 열이름 추가 및 2DID만 추출
        df_avs_barcode.columns = ['barcode']
        df_barcode_value = df_avs_barcode

        # ========================================================== Dataframe에서 열이름 추가 및 avs voltage만 추출
        df_avs_vol.columns = ['avs']
        df_avs_value = df_avs_vol

        # ========================================================== Dataframe에서 열이름 추가 및 avs voltage만 추출
        df_avsCode.columns = ['avsCode']
        df_avsCode_value = df_avsCode
    
        # ========================================================== Dataframe 행 합치기
        df =pd.concat([df_barcode_value, df_avs_value, df_avsCode_value], axis = 1)

######################################### iterate through all file
for i in range(16):
    os.chdir(f"{path}/DUT%s"%i)
    for file in os.listdir():
        if 'log' in file and file.endswith(".txt"):
            file_path = f"{path}/DUT%s/{file}"%i
            print(file_path)
            cal(file_path)

            if not os.path.exists(f'{path}/OTP_avs_log.csv'):
                df.to_csv(f'{path}/OTP_avs_log.csv', index=False, mode='a', encoding='utf-8-sig')
            else:
                df.to_csv(f'{path}/OTP_avs_log.csv', index=False, mode='a', encoding='utf-8-sig', header=False)