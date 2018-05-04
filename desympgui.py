from runner import recurseRunAll
from tkinter import *
from logicobjects import Sentence
from logicobjects import Atom
from symbol_convert import LogicSymbols
from sentence_parser import SentenceParser


class DesympGUI(object):

    def __init__(self):
        self.master = Tk()

        self.sen_label = Label(
            self.master, text='Sentence').grid(row=0, column=0)
        self.e1 = Entry(self.master)
        self.e1.bind('<Return>', self.evaluate)
        self.e1.grid(row=0, column=1)

        self.iter_label = Label(
            self.master, text='Iterations').grid(row=1, column=0)
        self.e2 = Entry(self.master)
        self.e2.insert(END, 1)
        self.e2.bind('<Return>', self.evaluate)
        self.e2.grid(row=1, column=1)

        self.step_label = Label(
            self.master, text='Steps per iteration').grid(row=2, column=0)
        self.e3 = Entry(self.master)
        self.e3.insert(END, 1)
        self.e3.bind('<Return>', self.evaluate)
        self.e3.grid(row=2, column=1)

        self.result_text = []

    def start(self):
        self.master.mainloop()

    def add_text(self, text, row_num):
        res = Text(self.master, height=1)
        res.insert(1.0, text)
        res.grid(row=4 + row_num, column=1)
        res.configure(bg=self.master.cget('bg'), relief=FLAT)
        self.result_text.append(res)

    def remove_text(self):
        for text in self.result_text:
            text.delete(1.0, END)

    def _handle_input(self):
        user_in = self.e1.get()
        iterations = int(self.e2.get())
        steps = int(self.e3.get())

        user_in = "".join(user_in.split())

        return user_in, iterations, steps

    def evaluate(self, event):
        self.remove_text()
        user_in, iterations, steps = self._handle_input()

        if iterations < 0:
            add_text('Cannot iterate <0 times')
            return

        if steps < 0:
            add_text('Cannot apply <0 steps')
            return

        sp = SentenceParser()
        sen = sp.parseInput(user_in)

        if sen is None:
            return

        Label(self.master, text='User input: ' + str(sen)).grid(row=3)

        sentences = {sen}

        for i in range(iterations):
            temp_sentences = []
            for sentence in sentences:
                temp = recurseRunAll(sentence, steps * iterations)
                temp_sentences.extend(temp)
            for sentence in temp_sentences:
                sentences.add(sentence)

        if sen in sentences:
            sentences.remove(sen)

        i = 0
        for sen in sentences:
            steps = sen.get_steps()
            if len(steps) > 0:
                step_str = steps[0]
                for j in range(len(steps) - 1):
                    step_str += ', ' + steps[j + 1]

            self.add_text(str(sen) + ' by ' + step_str, i)
            i += 1
