from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from tkinter import filedialog
import os
import sqlite3
conn = sqlite3.connect('LocalServer.db')
cur = conn.cursor()


class FileSearch:
    def __init__(self):
        self.root=Tk()
        
        self.p1=PanedWindow(self.root)
        self.p2=PanedWindow(self.root)

        self.lb1=Label(self.p1, text="Enter the directory location")
        self.txt1=Entry(self.p1)
        self.bt=Button(self.p1,text="Browse",command=self.browse)

        self.lb2=Label(self.p1, text="Enter search word")
        self.txt2=Entry(self.p1)
        self.bt1=Button(self.p1,text="Search",command=self.temp_DB)
        self.bt2=Button(self.p1,text="Exit",command=self.exitt)
        self.bt3=Button(self.p1,text="Ok",command=self.load_database)


        self.lb1.grid(row=0,column=0)
        self.txt1.grid(row=0,column=1)
        self.bt.grid(row=0,column=2)
        self.bt3.grid(row=0,column=3)
        self.lb2.grid(row=1,column=0)
        self.txt2.grid(row=1,column=1)
        self.bt1.grid(row=2,column=1)
        self.bt2.grid(row=3,column=3)
        

        self.t1=Treeview(self.p2,columns=("SNO","WORD","FNAME","FPATH"))
        self.t1.heading("SNO",text="INDEX")
        self.t1.heading("WORD",text="WORD")
        self.t1.heading("FNAME",text="FILE NAME")
        self.t1.heading("FPATH",text="FILE PATH")
        
        
        self.t1["show"]="headings"

        self.t1.column("SNO",width=60)
        self.t1.column("FPATH",width=500)
        
        self.t1.pack()

        self.p1.pack()
        self.p2.pack()

        self.root.mainloop()

    def browse(self):
        self.path=filedialog.askdirectory(initialdir='/Users/nimrat/Visualstudio_projects/PYTHON/FileSearchEngine')
        self.txt1.delete(0,END)
        if self.path!=None:
            self.txt1.insert(0,self.path)

    
        
    def load_database(self):
        self.initializeDB()
        cur.execute("UPDATE the_list SET frequency=0")
        self.path=str(self.txt1.get())
        filelist = os.listdir(self.path)

        for file in filelist:
            if file.endswith('.txt'):
                with open(self.path + "/" + file,'r') as f:
                    for line in f:
                        for w in line.split():
                            cur.execute(f"INSERT INTO the_list VALUES('{w}','{file}','{self.path}',1,0) ON CONFLICT(word,filename,filepath) DO UPDATE SET frequency=frequency + 1")

        conn.commit()
    '''
    def reads(self):
        if self.txt1.get()=='' or self.txt2.get()=='':
            messagebox.showwarning("Try Again", "Please fill the columns")

        self.t1.delete(*self.t1.get_children())
        
        self.path=str(self.txt1.get())
        filelist = os.listdir(self.path)

        count=0
        indx=1
        for i in filelist:  #going to every file in the directory
            #count=count+1
            self.x=[]
            freq=0
            if i.endswith(".txt"):
                with open(self.path + "/" + i,'r') as f: 
                    for line in f:  #checking each line in the file
                        if self.txt2.get() in line:
                            self.x=[self.txt2.get(),i,self.path] # word,file name
                            #self.t1.insert("",index=count,values=[indx,i])
                            indx=indx+1
                        freq=freq+int(line.count(self.txt2.get())) #frequency of word in the file
                self.x.append(freq) #word, file name , frequency of word
                #call to add into database here
                print(self.x)
                self.initializeDB()
                self.update()

        print(self.get_data())
        # lists=self.get_data()
        # for j in lists:
        #     self.t1.insert("",index=count,values=j)       
        #     count=count+1    
        

        if indx==1:
            messagebox.showinfo("showinfo", "Word not Found")
    '''
    def initializeDB(self):
        cur.execute("""CREATE TABLE IF NOT EXISTS the_list (
            word TEXT,
            filename TEXT,
            filepath TEXT,
            frequency INTEGER,
            search_freq INTEGER,
            PRIMARY KEY (word,filename,filepath)
         )""")

    def update(self): #when i reached the word, i update it's search frequency everytime
        if self.txt2.get()=='' or self.txt1.get()=='':
            messagebox.showinfo("showinfo", "Word not Found")
            
        self.t1.delete(*self.t1.get_children())
        #if i have a string
        self.w=self.txt2.get().split()
        #w is list of strings
        for i in self.w:
            cur.execute(f"UPDATE the_list SET search_freq = search_freq+1 WHERE word='{i}'")
            conn.commit()

        temp=list(self.get_data())
        c=0
        for i in temp:
            p=list(i)
            p.insert(0,c+1)
            self.t1.insert("",index=c,values=p)
            c=c+1
            


    # def get_data(self):
    #     self.temp_DB();
    #     #if i have a string
    #     self.w=self.txt2.get().split()
    #     #w is list of strings
    #     for i in self.w:
    #         cur.execute(f"SELECT * FROM the_list WHERE word='{i}' ORDER BY frequency*search_freq DESC")
        
    #     return cur.fetchall()

    def exitt(self):
        cur.execute("UPDATE the_list SET frequency=0")
        self.root.destroy()
        conn.commit()
        conn.close()

    def temp_DB(self):
        self.t1.delete(*self.t1.get_children())



        cur.execute("""CREATE TEMP TABLE table1 AS SELECT * FROM the_list""")
        cur.execute("DELETE FROM temp.table1")


        my_search=list(self.txt2.get().split())
        # print(my_search)
        
        for each in my_search:
            cur.execute(f"INSERT INTO temp.table1 SELECT * FROM the_list WHERE word='{each}'")
        cur.execute("SELECT * FROM temp.table1")
        
        cur.execute("SELECT filename,cnt FROM (SELECT MAX(frequency) freq,MAX(search_freq) search,COUNT(word) cnt,filename FROM temp.table1 GROUP BY filename) ORDER BY cnt DESC,freq*search DESC,freq DESC")
        my_list=cur.fetchall()

        temp=[]
        var=0

        for element in my_list:
            cur.execute(f"SELECT word,filename,filepath FROM temp.table1 WHERE filename='{element[0]}'")
            temp=cur.fetchall()
            word=[]
            for row in temp:
                word.append(row[0])
            word=" ".join(word)
            file_name=temp[0][1]
            file_path=temp[0][2]
            self.t1.insert("",index=var,values=[var+1,word,file_name,file_path])
            var=var+1



        #     cur.execute(f"SELECT word FROM temp.table1 WHERE filename='{element[0]}'")
        #     s=cur.fetchall()
        #     new_s=" "
        #     new_s.join(s)
        #     temp[var].insert(0,new_s)
        #     var=var+1


        # cur.execute(f"INSERT INTO temp.results SELECT word,filename,filepath FROM temp.table1 WHERE filename='{element[0]}' ON CONFLICT(filename,filepath) DO UPDATE SET word=word")


        # c=0
        # for i in temp:
        #     p=list(i)
        #     p.insert(0,c+1)
        #     self.t1.insert("",index=c,values=p)
        #     c=c+1

        
            


#----------------------------------------------------------------------------
print("----------------------------------------------------------------------------")
obj = FileSearch()


#/Users/nimrat/Visualstudio_projects/PYTHON/FileSearchEngine/Testfiles
#FileSearchEngine/Testfiles
