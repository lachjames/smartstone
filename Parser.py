from textGetter import search, searchAll

hero_powers = ["totemic call", "armor up", "reinforce", "the_coin"]

class Parser:
    def __init__(self, decks, my_username):
        self.my_username = my_username
        self.decks = decks
        self.dirty = True
        self.reset()

    def reset(self):
        self.enemy_deck = []
        self.player_id = -1
        self.in_mulligan = False
    
    def parse_line(self, line):
        self.check_if_in_mulligan(line)
        self.get_player_id(line)
        if self.is_reset(line):
            self.reset()
            self.dirty = True

        c = self.is_card(line)

        if c is not None:
            self.enemy_deck += [c]
            self.dirty = True
        
    def check_if_in_mulligan(self, line):
        if "BEGIN_MULLIGAN" in line:
            print("In mulligan")
            #self.dirty = True
            self.in_mulligan = True
        if "GameState.SendChoices()" in line and "ChoiceType=MULLIGAN" in line:
            print("Out of mulligan")
            self.in_mulligan = False

    def is_reset(self, line):
        return "GameState.DebugPrintPower() - CREATE_GAME" in line

    def get_player_id(self, line):
        if not self.in_mulligan:
            return False
        if "NUM_CARDS_DRAWN_THIS_TURN value=3" in line and self.my_username in line:
            self.player_id = 0
            print("Setting Player ID to player 0")
            return True
        if "NUM_CARDS_DRAWN_THIS_TURN value=4" in line and self.my_username in line:
            self.player_id = 1
            print("Setting Player ID to player 1")
            return True

    def is_card(self, line):
        if "PowerTaskList.DebugPrintPower() - BLOCK_START BlockType=POWER Entity=[name" in line and "player={}] EffectCardId".format("1" if self.player_id == 2 else "2") in line:
            card_name = search(line, r'name=', r' id=')
            if card_name in hero_powers:
                return None
            return None if card_name == None else card_name.lower().replace("'", "")
        return None

    def cur_state(self):
        if not self.dirty:
            return
        cur_matches = []
        for deck in self.decks:
            cur_matches += [(self.match_level(self.enemy_deck, deck), deck),]
        
        cur_matches = sorted(cur_matches, key=lambda x: x[0], reverse=True)

        top_match = cur_matches[0]

        self.cls()
        if len(self.enemy_deck) == 0:
            conf = 0
        else:
            conf = (cur_matches[0][0] / len(self.enemy_deck)) * ((30 - cur_matches[1][0]) / len(self.enemy_deck))
        print("Confidence: {}/{}; {}".format(top_match[0], len(self.enemy_deck), conf))
        
        print(bcolors.FAIL + "PID: {}; MULL: {}".format(self.player_id, self.in_mulligan))

        for card in self.enemy_deck:
            print(bcolors.OKBLUE + card + bcolors.ENDC)
        
        for card in self.subtract(cur_matches[0][1],self. enemy_deck):
            print(bcolors.OKGREEN + card + bcolors.ENDC)

        self.dirty = False

    def match_level(self, cards, deck):
        return len([c for c in cards if c in deck])
    

    def cls(self):
        #Clear the screen
        for _ in range(100):
            print("")
                    
    def subtract(self, list1, list2):
        import copy
        A = copy.deepcopy(list1)
        for x in list2:
            loc = None
            try:
                loc = A.index(x)
            except ValueError:
                loc = -1
            if loc >= 0:
                #Found the index
                del A[loc]
        return A

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
