import tkinter as tk
from wonderwords import RandomWord
import time
import threading


class TypeSpeedTest():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("typing speed test")
        self.root.geometry("760x400")
        self.root.resizable(False, False)
        self.root.config(padx=30, pady=30)

        self.index = tk.IntVar()
        self.index = 0
        self.words = []
        self.errors = 0
        self.game_started = False
        self.keep_playing = False
        fontsize = 20
        self.playtime = 60

        self.lbl_timer = tk.Label(self.root, text=self.playtime, font=("Arial", 30, 'bold'))
        self.lbl_timer.grid(row=0, column=0, pady=20, sticky='w')

        self.lbl_help = tk.Label(self.root,
                                 text="Just start typing. End with Return or Space",
                                 font=("Arial", 16, 'bold'), foreground='grey')
        self.lbl_help.grid(row=0, columnspan=3, column=1, pady=20, sticky='w')

        self.lbl_previous = tk.Label(self.root, text="", foreground="#aaaaaa", font=("Arial", fontsize))
        self.lbl_previous.grid(row=1, column=0)

        self.lbl_current = tk.Label(self.root, text="current", foreground="blue2", font=("Arial", fontsize))
        self.lbl_current.grid(row=1, column=1, padx=10, sticky='w')

        self.lbl_next = tk.Label(self.root, text="next", font=("Arial", fontsize))
        self.lbl_next.grid(row=1, column=2)

        self.lbl_tprevious = tk.Label(self.root, text="", font=("Arial", fontsize))
        self.lbl_tprevious.grid(row=2, column=0)

        self.text = tk.StringVar()
        self.textbox = tk.Entry(self.root, textvariable=self.text, width=20, bg='white', font=("Arial", fontsize))
        self.textbox.bind('<KeyRelease>', self.keypress_in_entry)
        self.textbox.grid(row=2, column=1, padx=10, pady=10)

        self.lbl_result = tk.Label(self.root, text="", font=("Arial", fontsize))
        self.lbl_result.grid(row=3, columnspan=3, pady=20, sticky='w')

        self.lbl_dummy = tk.Label(self.root, text="                        ", font=("Arial", fontsize))
        self.lbl_dummy.grid(row=4, pady=0, sticky='w')

        self.btn_start = tk.Button(self.root, text="play again", state='disabled', command=self.main)
        self.btn_start.grid(row=5, column=2)

        self.btn_exit = tk.Button(self.root, text="exit", command=self.close)
        self.btn_exit.grid(row=5, column=4)

        self.main()

        tk.mainloop()

    def main(self):
        """The game starts when the player starts typing. The timer runs in a separate thread and disables the
        entry box when the game ends"""
        r = RandomWord()
        self.words = r.random_words(100)
        # print(self.words)
        self.lbl_current.config(text=self.words[0])
        self.lbl_next.config(text=self.words[1])
        self.textbox.config(state='normal')
        self.textbox.focus_set()
        self.lbl_result.config(text="")
        self.lbl_previous.config(text="")
        self.lbl_tprevious.config(text="")
        self.lbl_timer.config(text=self.playtime)
        self.game_started = False

    def run_timer(self):
        """separate thread to control play time"""
        start_time = time.time()
        end_time = time.time()
        # print(f"start: {start_time}")
        # print(f"end: {end_time}")
        while end_time < start_time + self.playtime:
            # print(f"run timer: {end_time - start_time}")
            self.lbl_timer.config(text=(self.playtime - int(end_time - start_time)))
            end_time = time.time()
            time.sleep(1)

        self.lbl_timer.config(text=0)
        self.textbox.config(state='disabled')
        self.text.set('')
        self.show_score()

    def show_score(self):
        wordcount = self.index
        correct = wordcount -  self.errors
        self.lbl_result.config(text=f"result:   {wordcount} words, {self.errors} with errors, "
                                    f"{correct} correct")
        self.btn_start.config(state='normal')

    def keypress_in_entry(self, event):
        """Start game with first keypress. Space and Return move to the next word."""
        if not self.game_started:
            self.game_started = True
            timer_thread = threading.Thread(target=self.run_timer)
            timer_thread.daemon = True
            timer_thread.start()
        # print(f"pressed {event.keysym}, ")
        if event.keysym == 'space':
            self.next_word()
        elif event.keysym == 'Return':
            self.next_word()
        else:
            self.check_spelling()

    def check_spelling(self):
        """Display spelling errors in red"""
        typed = self.textbox.get()
        target = self.lbl_current.cget("text")
        slice = target[:len(typed)]
        # print(f"typed={typed}, target={target}, slice={slice}")
        # print(f"type={type(typed)}, slice={type(slice)}")
        if typed != slice:
            self.textbox.config(foreground='red')
        else:
            self.textbox.config(foreground='black')

    def next_word(self):
        old_word = self.lbl_current.cget("text")
        self.lbl_previous.config(text=old_word)
        self.lbl_tprevious.config(text=self.text.get())

        print(f"self.lbl_tprevious.cget('text')={self.lbl_tprevious.cget('text')},"
              f"oldword={old_word}")
        if self.lbl_tprevious.cget('text').strip() != old_word:
            self.lbl_tprevious.config(foreground='red')
            self.errors += 1
        else:
            self.lbl_tprevious.config(foreground='#aaaaaa')
        self.index += 1
        self.lbl_current.config(text=self.words[self.index])
        self.lbl_next.config(text=self.words[self.index + 1])
        self.text.set('')
        self.textbox.focus()

    def close(self):
        self.root.destroy()


TypeSpeedTest()

# examples
# https://www.livechat.com/typing-speed-test/#/
# https://www.typingtest.com/result.html?acc=100&nwpm=2&gwpm=2&ncpm=13&gcpm=13&dur=60&time=60&chksum=1313&unit=wpm&kh=998&td=null&err=0&hits=13&textfile=difficultText.txt&mobile=0
#