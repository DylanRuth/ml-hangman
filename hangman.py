import numpy as np

class Hangman(object) :
    def __init__(self , 
                 word_src, 
                 max_lives = 6 , 
                 win_reward = 30,
                 correct_reward = 1,
                 repeated_guessing_penalty = -100,
                 lose_reward = -0, 
                 false_reward = -0,
                 verbose = False) :
        if type(word_src) == list :
            self.words = word_src
        else :
            with open(word_src, 'r') as f :
                self.words = f.read().splitlines()
        self.max_lives = max_lives
        self.win_reward = win_reward
        self.correct_reward = correct_reward
        self.lose_reward = lose_reward
        self.false_reward = false_reward
        self.verbose = verbose
        self.repeated_guessing_penalty = repeated_guessing_penalty
        
    def pick_random(self) :
        self.guess_word = np.random.choice(self.words)
        
    def reset(self) :
        self.curr_live = self.max_lives
        self.pick_random()
        self.guessing_board = ['-' for i in range(len(self.guess_word))]
        self.correct_guess = 0
        self.guessed = []
        self.done = False
        if self.verbose :
            print('Game Starting')
            print('Current live :', self.curr_live)
        return self.show_gameboard()
        

    def show_gameboard(self) :
        board = ''.join(self.guessing_board)
        if self.verbose:
            print(board)
            print()
        return board
        
    def step(self, letter) :
        if not(letter.isalpha()) :
            raise TypeError('Can only accept alphabet')
        letter = letter.lower()

        if letter not in self.guessed :
            self.guessed.append(letter)
        else :
            if self.verbose :
                print('Word used already')
            return self.show_gameboard(), self.repeated_guessing_penalty, self.done, {}


        if letter in self.guess_word :
            for i in range(len(self.guess_word)) :
                if letter == self.guess_word[i] :
                    self.guessing_board[i] = letter
                    self.correct_guess += 1
            if self.correct_guess == len(self.guess_word) :
                self.done = True
                if self.verbose :
                    print('You Win')
                    print('Word is', self.guess_word)
                return self.guess_word, self.win_reward, self.done, {'ans' : self.guess_word}
            else :                
                return self.show_gameboard(), self.correct_reward, self.done, {}
        else :
            self.curr_live -= 1
            if self.curr_live == 0 :
                self.done = True
                if self.verbose :
                    print('You Lose')
                    print('Word is', self.guess_word)
                return self.show_gameboard(), self.lose_reward, self.done, {'ans' : self.guess_word}
            else :
                if self.verbose :
                    print('Current lives :', self.curr_live)
                return self.show_gameboard(), self.false_reward, self.done, {}


if __name__=='__main__' :
    from argparse import ArgumentParser

    parser = ArgumentParser()

    parser.add_argument("-w", "--wordsrc", help = 'Text File that contains the word the game is based on', default = 'words.txt')
    parser.add_argument("-l", "--lives", help = "maximum number of false attempt", default = 6, type = int)

    args = parser.parse_args()
    word_src = args.wordsrc
    max_lives = args.lives
    env = Hangman(word_src, max_lives, verbose = True)

    env.reset()

    done = False
    
    while not done :
        ans = 'empty'
        while len(ans) > 1 :
            ans = input('Guessing letter : ')

        _, _ , done, _ = env.step(ans)