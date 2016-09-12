from multiprocessing import Pool
import html
from urllib import request
from textGetter import search, searchAll
import time
import pickle

from Parser import Parser

log_file_location = "/Applications/Hearthstone/Logs/Power.log"

url = "http://www.hearthpwn.com/"
decks_url = "http://www.hearthpwn.com/decks?filter-deck-tag=1&page="
pickle_outfile_loc = "top_decks.p"
pages = 10
threads = 8

import sys

if len(sys.argv) == 2:
    force_update = True if sys.argv[1] == "True" else False
else:
    force_update = False
my_username = "Lachjames"

decks = []

playing_game = False

enemy_deck = []

player_id = -1

def main():
    global enemy_deck
    load_decks()
    print("Loaded decks")
    log_file = open(log_file_location, 'r')
    
    cur_matches = []
    
    w = Parser(decks, my_username)

    for log_line in monitor_game(log_file):
        w.parse_line(log_line)
        w.cur_state()

def monitor_game(thefile):
    thefile.seek(0,2) # Go to the end of the file
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1) # Sleep briefly
            continue
        yield line
    
def load_decks():
    global decks
    try:
        if force_update:
            raise Exception("Need to force deck update")
        decks = pickle.load(open(pickle_outfile_loc, 'rb'))
    except:
        decks = get_decks()
        for deck in decks:
            print(deck)
        
        pickle.dump(decks, open(pickle_outfile_loc, 'wb'))

def get_decks():
    top_decks = get_top_decks()
    
    p = Pool(threads)
    decks = [x for x in p.map(get_deck, top_decks)]
    return decks
        
def get_top_decks ():
    #Returns the addresses of the top decks at the moment in Hearthstone
    urls = []
    for page in range(pages):
        try:
            site = request.urlopen(decks_url + str(page))
        except:
            return []
        
        siteDump = str(site.read())
        
        lines = [x for x in searchAll(siteDump, r'<span class="tip" title="', r'</a></span>')]
        urls += [url + search(x, r'><a href="', r'">') for x in lines]
        #print(urls)
    print("Found Top Decks")
    return urls

def get_deck(addr):
    #Returns a list containing the names of all the cards in the deck
    try:
        site = request.urlopen(addr)
    except:
        return []
    
    siteDump = str(site.read())
    
    searchable = search(siteDump, r'<div class="details t-deck-details">', r'<div class="u-typography-format deck-description">')
    
    card_names = searchAll(searchable, r'<a href="/cards/', r'" data-Id="')    
    
    deck = []
    
    for card in card_names:
        card_line = search(searchable, card, r'>')
        card_count = int(search(card_line, r'data-Count="', '"'))
        for _ in range(card_count):
            deck += [" ".join(card.split('-')[1:]).lower()]
    
    return deck
        
class Card:
    def __init__(self, name, count):
        self.name = name
        self.count = count
            
if __name__ == "__main__": main()
