import tkinter as tk
from tkinter import filedialog
import json
from random import sample

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Maker")
        self.root.geometry("600x550")

        self.file_label = tk.Label(root, text="Select JSON file:",font=("arial",10))
        self.file_label.pack()

        self.file_entry = tk.Entry(root, width=50,font=("Corbel",15),border=3)
        self.file_entry.pack()

        self.browse_button = tk.Button(root, text="Browse",font=("Corbel",15),border=3, command=self.browse_file)
        self.browse_button.pack()

        self.start_button = tk.Button(root, text="Start Quiz",font=("Corbel",15),border=3, command=self.start_quiz)
        self.start_button.pack()

        self.question_label = tk.Label(root, text="", font=("Corbel",18),wraplength=400)
        self.question_label.pack()

        self.answer_frame = tk.Frame(root)
        self.answer_frame.pack()

        self.submit_button = tk.Button(root, text="Submit",font=("Corbel",18), command=self.submit_answer)
        #self.submit_button.pack()
        self.submit_button.pack_forget()

        self.score_label = tk.Label(root, text="Score: 0",font=("Corbel",15))
        #self.score_label.pack()
        self.score_label.pack_forget()

        self.question_number=0

    def browse_file(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(0, filename)

    def read_questions(self, filename):
        with open(filename, "r") as f:
            questions = json.load(f)
        return questions

    def generate_quiz(self, num_questions):
        return sample(self.questions, num_questions)

    def start_quiz(self):
        filename = self.file_entry.get()
        self.questions = self.read_questions(filename)
        self.current_quiz = self.generate_quiz(6)  
        self.current_answers = [question["answer"] for question in self.current_quiz]
        self.score = 0
        self.answer_var = tk.StringVar()
        self.next_question()
        self.file_label.pack_forget()
        self.file_entry.pack_forget()
        self.browse_button.pack_forget()
        self.start_button.pack_forget()
        self.submit_button.pack()
        self.score_label.pack()
        self.score_label.pack_forget() 

    def next_question(self):
        if not self.current_quiz:
            self.question_label.place(relx=0.5, rely=0.5, anchor="center")
            self.question_label.config(text="Quiz complete! Your score is {} out of 6".format(self.score),justify="center",font=("arial",17))
            self.answer_frame.pack_forget()
            self.submit_button.pack_forget()
            self.submit_button.config(state="disabled")
            #self.score_label.pack()
        else:
            self.question_number+=1
            question = self.current_quiz.pop(0)
            self.question_label.config(text=f"Q {self.question_number}) : {question['question']}",font=("Arial",18))
            self.create_answer_buttons(question["options"])

    def create_answer_buttons(self, options):
        for widget in self.answer_frame.winfo_children():
            widget.destroy()
        import random
        random.shuffle(options)
        for i, option in enumerate(options):
            rb = tk.Radiobutton(self.answer_frame, text=option,font=("Corbel",18),fg="#1C1C1C", variable=self.answer_var, value=option,activeforeground="#76EEC6",borderwidth=4)
            rb.pack(anchor=tk.W)

    def submit_answer(self):
        answer = self.answer_var.get()
        correct_answer = self.current_answers.pop(0)
        if answer.lower() == correct_answer.lower():
            self.score += 1
        #self.score_label.config(text="Score: {}".format(self.score))
        self.next_question()

root = tk.Tk()
app = QuizApp(root)
root.mainloop()