import pysrt
import glob


def main():
    # filename = 'Better Call Saul - 1x10 - Marco.HDTV.x264-LOL.en.srt'

    lists = find_all_txt_to_list()
    for list in lists:
        open_and_print_all_srt(list)


def open_and_print_all_srt(filename=''):
    try:
        subs = pysrt.open(filename)
    except:
        return None
    else:
        with open(filename[:-3]+'txt', 'w') as f:
            for sub in subs:
                print(sub.text)
                print()
                f.write(sub.text)
                f.write("\n")
                f.write("\n")


def find_all_txt_to_list():
    return glob.glob('*.srt')


if __name__ == '__main__':
    main()