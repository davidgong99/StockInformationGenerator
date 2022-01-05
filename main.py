import AppConfig
from GoogleSheets import GoogleSheets
    

def main():
    print('as')
    AppConfig.init()
    gs = GoogleSheets()
    # gs.readRange()

if __name__=='__main__':
    main()