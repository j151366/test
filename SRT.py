import pysrt
import glob


def main():
    # filename = 'Better Call Saul - 1x10 - Marco.HDTV.x264-LOL.en.srt'

    lists = find_all_txt_to_list()
    for list in lists:
        print(list)
        open_and_print_all_srt(list)


def open_and_print_all_srt(filename=''):
    try:
        subs = pysrt.open(filename)
    except:
        return None
    else:
        with open(filename[:-3]+'txt', 'w', encoding='utf-8') as f:
            for sub in subs:
                #print(sub.text)
                #print()
                try:
                    f.write(sub.text)
                    f.write("\n")
                    f.write("\n")
                except:
                    try:
                        f.write(sub.text.encode('utf8'))
                    except:
                        print(sub.text.encode('utf8'))


def find_all_txt_to_list():
    return glob.glob('*.srt')


if __name__ == '__main__':
    main()
