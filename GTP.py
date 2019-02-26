import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googletrans.gtoken import TokenAcquirer
import requests

def main():
    url = 'https://docs.google.com/spreadsheets/d/1KyXxb_G4nD7O92Bl1biKMqdm_i1Pvkz4QBJQOuY5EBo/edit?usp=sharing'
    wb = get_workbook_credentials(url)
    # print(wb.sheet1.get_all_values())
    val = wb.sheet1.acell('A8').value

    token = get_text_token(str(val))
    # print(token)
    json = get_translated_list(token, str(val))
    jsonlist = list(json)
    wb.sheet1.update_acell('B8', 'Definition: ' + jsonlist[-1][0][1][0][0] + ' Example: ' + jsonlist[-1][0][1][0][2])
    print('Definition: ' + jsonlist[-1][0][1][0][0] + ' Example: ' + jsonlist[-1][0][1][0][2])
    # print('Definition: ' + jsonlist[-1][0][1][1][0] + ' Example: ' + jsonlist[-1][0][1][1][2])
    # print('Definition: ' + jsonlist[-1][0][1][2][0] + ' Example: ' + jsonlist[-1][0][1][2][2])
    # print(list(jsonlist))
    # wb.sheet1.update_cells(list(jsonlist))


def get_workbook_credentials(url=''):

    try:
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('My Cloud AI Lab-102db0e9c9c4.json', scope)
        gc = gspread.authorize(credentials)
    except:
        print('google_credentials_error')
        return None
    else:
        try:
            workbook = gc.open_by_url(url)
            return workbook
        except:
            print('url_error')
            return None


def get_text_token(text=''):
    try:
        acquirer = TokenAcquirer()
        tk = acquirer.do(text)
    except:
        print('get_token_error')
        return None
    else:
        return tk


def get_translated_list(token='', vocabulary=''):
    url = 'https://translate.google.com/translate_a/single?client=webapp&sl=auto&tl=zh-TW&hl=en&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&otf=1&ssel=3&tsel=3&kc=4&tk='+token+'&q='+vocabulary
    list = requests.get(url).json()
    return list


if __name__ == '__main__':
    main()








