import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext
import subprocess
import time
from turtle import color

CMP_CUSTOM = "custom"
CMP_KILL_PORT = "killport"
CMP_MUL_CMD = "mul_cmd"
CMP_MUL_TEST = "mul_test"

END = "end"
cmd_arr_test = ["java -version",
                "ipconfig"]

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):

        self.cntMul = 0
        
        self.txt_input1 = tk.Entry(width=113)

        self.contents = tk.StringVar()
        self.txt_input1["textvariable"] = self.contents
        self.txt_input1.bind("<Key-Return>", self.excutef)
    
        self.txt_input2 = scrolledtext.ScrolledText(height = 4, width=85)
        
        self.cmp_var = tk.StringVar()
        self.combobox = ttk.Combobox(self, textvariable = self.cmp_var)
        
        self.combobox['values'] = [CMP_CUSTOM, CMP_KILL_PORT, CMP_MUL_CMD, CMP_MUL_TEST]
        self.combobox['state'] = 'readonly'
        self.combobox.pack()
        self.combobox.current(0)
        self.combobox.bind('<<ComboboxSelected>>', self.modified)    

        self.varchkConfirm = tk.BooleanVar(value=True)
        self.chkConfirm = tk.Checkbutton( text='Observe mode',variable=self.varchkConfirm, onvalue=True, offvalue=False)
        self.chkConfirm.pack()
        self.chkConfirm.place(x=180, y=0)

        self.excutebtn = tk.Button()
        self.excutebtn["text"] = "Excute"
        self.excutebtn["command"] = self.excutef
        self.excutebtn.pack()
        self.excutebtn.place(x=30, y=120)
        
        self.clear_input = tk.Button(text="Clear", command = self.clear_input2)
        self.clear_input.pack()
        self.clear_input.place(x=90, y=120)

        self.txtresult = scrolledtext.ScrolledText(height=15, width=85)
        self.txtresult.pack()
        self.txtresult.place(x=30, y=150)
        
        self.clear = tk.Button(text="Clear", command = self.clear_result)
        self.clear.pack()
        self.clear.place(x=30, y=400)
     
        self.txt_input2.pack()
        self.txt_input2.place(x=30, y=40)
        self.combobox.current(2)
        

    def excutef(self, event = None):
        txtcmd = ""
        select = self.cmp_var.get()
        if select == CMP_KILL_PORT :
             txtcmd = self.txt_input1.get().strip()
             if txtcmd.isnumeric():
                   self.kill_port(txtcmd)
             else:
                   self.txtresult.insert(END, "PID not found or not a number : {}".format(txtcmd))
          
        elif select == CMP_CUSTOM :
             txtcmd = self.txt_input1.get().strip()
             self.exc_cmd(txtcmd)
        elif select == CMP_MUL_CMD or select == CMP_MUL_TEST:
             txtcmd = self.txt_input2.get(1.0,END).strip()
             arr_res = txtcmd.split('\n')
             self.exc_multi_cmd(arr_res)

    def kill_port(self, txtcmd):
         FIND_PID = 'netstat -ano|findstr "PID :{}"'
         KILL_TASK = 'taskkill /PID {} /F'
         
         cmd_res = self.exc_cmd(FIND_PID.format(txtcmd))
         arr_res = cmd_res.split('\n')
         
         pid = ""
         pid_cnt = 0
         for line in arr_res:
              if line != None and "LISTENING" in line:
                   pid = line.split()[-1].strip()
                   pid_cnt += 1
         if pid_cnt>2:
              self.txtresult.insert(END, "more than 1 port has found!, please confirm!")
              return
         
         if pid.isnumeric():
              self.exc_cmd(KILL_TASK.format(pid))
         else:
              self.txtresult.insert(END, "PID not found or not a number : {}".format(pid))
                   
         
    def exc_cmd(self, cmd):
        if not cmd:
          return
        result ="\n{} >> {}\n".format(time.strftime("%H:%M:%S"),cmd)
        cmd_res = subprocess.getoutput(cmd) + "\n"
        result += cmd_res
        self.txtresult.insert(END, result)
        self.txtresult.see(END)
        return cmd_res
   
    def exc_multi_cmd(self, arr_cmd):
        exc_one = self.varchkConfirm.get()
        if exc_one == False:
          for cmd in arr_cmd:
               self.exc_cmd(cmd)
        else:
          cmd = arr_cmd[self.cntMul] 
          self.exc_cmd(cmd)  
          if not cmd:
           return
          self.cntMul += 1
          if self.cntMul == len(arr_cmd):
               self.txtresult.insert(END, "\nDone!!")
               self.txtresult.insert(END, "\n==========================")
               self.txtresult.see(END)
               self.cntMul = 0
               time.sleep(1)
        
    def clear_result(self):
        self.txtresult.delete(1.0, END)
        
    def clear_input2(self):
        self.txt_input2.delete(1.0, END)
        
    def modified(self, event=None):
        select = self.cmp_var.get()
        if select == CMP_MUL_CMD :
          self.show_input2(True)
          
        elif select == CMP_MUL_TEST:
          self.show_input2(True)
          self.clear_input2
          cmd = self.convert_arr_to_string(cmd_arr_test)
          self.txt_input2.insert(END, cmd)
          
        else:
          self.show_input2(False)
             
          
    def show_input2(self, is_show):
        if is_show == True :
               self.txt_input2.pack()
               self.txt_input2.place(x=30, y=40)
               self.txt_input1.pack_forget()
               self.txt_input1.place_forget()
        else:
               self.txt_input2.pack_forget()
               self.txt_input2.place_forget()
               self.txt_input1.pack()
               self.txt_input1.place(x=30, y=40)
               
    def convert_arr_to_string(self, arr):
         res = ""
         for cmd in arr:
               res += cmd+"\n"
         return res

root = tk.Tk()
app = Application(master=root)
app.master.title("Cmd app")
app.master.minsize(750, 500)
app.mainloop()
