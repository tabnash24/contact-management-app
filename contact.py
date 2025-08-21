from tkinter import *
from tkinter import ttk
import pymysql
from tkinter import messagebox
import re

class Contact:
    def __init__(self,root):
        self.root = root
        self.root.title("Contact Management System")
        self.root.geometry("1350x700+0+0")

        title=Label(self.root,text="Contact Management System",bd=10,relief=RIDGE,font=("times new roman",40,"bold"),bg="light blue",fg="black")
        title.pack(side=TOP,fill=X)

         # variables
        self.id_var = StringVar()
        self.fname_var=StringVar()
        self.lname_var=StringVar()
        self.phone_var=StringVar()
        self.email_var=StringVar()

        self.search_by=StringVar()
        self.search_txt=StringVar()


#          Manage Frame

        Manage_Frame=Frame(self.root,bd="4",relief=RIDGE,bg="light grey")
        Manage_Frame.place(x=30,y=100,width=450,height=650)

        m_title=Label(Manage_Frame,text="Manage Contacts",bg="light grey",font=("times new roman",20,"bold"))
        m_title.grid(row=0,columnspan=2,pady=20)

#name

        lbl_fname=Label(Manage_Frame,text="First Name",bg="light grey",font=("times new roman",12,"bold"))
        lbl_fname.grid(row=1,column=0,pady=10,padx=20,sticky="w")

        lbl_lname=Label(Manage_Frame,text="Last Name",bg="light grey",font=("times new roman",12,"bold"))
        lbl_lname.grid(row=2,column=0,pady=10,padx=20,sticky="w")

        txt_fname=Entry(Manage_Frame,textvariable=self.fname_var,font=("times new roman",11,"bold"),bd=5,relief=GROOVE)
        txt_fname.grid(row=1,column=1,pady=5,sticky="w")

        txt_lname=Entry(Manage_Frame,textvariable=self.lname_var,font=("times new roman",11,"bold"),bd=5,relief=GROOVE)
        txt_lname.grid(row=2,column=1,pady=5,sticky="w")

#phone no

        lbl_phone=Label(Manage_Frame,text="Phone No.",bg="light grey",font=("times new roman",12,"bold"))
        lbl_phone.grid(row=3,column=0,pady=10,padx=20,sticky="w")

        txt_phone=Entry(Manage_Frame,textvariable=self.phone_var,font=("times new roman",12,"bold"),bd=5,relief=GROOVE)
        txt_phone.grid(row=3,column=1,pady=10,sticky="w")

#email id

        lbl_email=Label(Manage_Frame,text="Email",bg="light grey",font=("times new roman",12,"bold"))
        lbl_email.grid(row=4,column=0,pady=10,padx=20,sticky="w")

        txt_email=Entry(Manage_Frame,textvariable=self.email_var,font=("times new roman",12,"bold"),bd=5,relief=GROOVE,width=25)
        txt_email.grid(row=4,column=1,pady=10,sticky="w")

#address

        lbl_address=Label(Manage_Frame,text="Address",bg="light grey",font=("times new roman",12,"bold"))
        lbl_address.grid(row=5,column=0,pady=12,padx=20,sticky="w")

        self.txt_address=Text(Manage_Frame,width=30,height=5)
        self.txt_address.grid(row=5,column=1,pady=10,sticky="w")


#button frame
         
        btn_Frame=Frame(Manage_Frame,bd="1",relief=RIDGE,bg="light grey")
        btn_Frame.place(x=15,y=400,width=410)

        Addbtn=Button(btn_Frame,text="Add",width=10,command=self.add_contact).grid(row=0,column=0,padx=10,pady=10)
        Updatebtn=Button(btn_Frame,text="Update",width=10,command=self.update_data).grid(row=0,column=1,padx=10,pady=10)
        Deletebtn=Button(btn_Frame,text="Delete",width=10,command=self.delete_data).grid(row=0,column=2,padx=10,pady=10)
        Clearbtn=Button(btn_Frame,text="Clear",width=10,command=self.clear).grid(row=0,column=3,padx=10,pady=10)

#       Detail frame        
        
        Detail_Frame=Frame(self.root,bd="4",relief=RIDGE,bg="light grey")
        Detail_Frame.place(x=490,y=100,width=1010,height=650)

        
        lbl_search=Label(Detail_Frame,text="Search by",bg="light grey",font=("times new roman",12,"bold"))
        lbl_search.grid(row=0,column=1,pady=10,padx=20,sticky="w")


        combo_search=ttk.Combobox(Detail_Frame,textvariable=self.search_by,width=10,font=("times new roman",11),state='readonly')
        combo_search['values']=("First Name","Last Name","Phone No.")
        combo_search.grid(row=0,column=2,padx=20,pady=20)

        txt_search=Entry(Detail_Frame,textvariable=self.search_txt,width=30,font=("times new roman",11,"bold"),bd=5,relief=GROOVE)
        txt_search.grid(row=0,column=3,pady=20,padx=20,sticky="w")

        # Bind Enter key to search
        txt_search.bind("<Return>", lambda event: self.search_data())

        searchbtn=Button(Detail_Frame,text="Search",width=10,command=self.search_data).grid(row=0,column=4,padx=10,pady=20)
        showallbtn=Button(Detail_Frame,text="Show All",width=10,command=self.fetch_data).grid(row=0,column=5,padx=10,pady=20) 
        
#         Table Frame

        Table_Frame=Frame(Detail_Frame,bd="4",relief=RIDGE,bg="light grey")
        Table_Frame.place(x=10,y=70,width=980,height=560)

#scroll bar

        scroll_x=Scrollbar(Table_Frame,orient=HORIZONTAL)
        scroll_y=Scrollbar(Table_Frame,orient=VERTICAL)

        scroll_x.pack(side=BOTTOM,fill=X)
        self.Contact_table=ttk.Treeview(Table_Frame,columns=("id","fname","lname","phone","email","address"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.Contact_table.xview)
        scroll_y.config(command=self.Contact_table.yview)

        self.Contact_table.heading("id",text="ID")
        self.Contact_table.heading("fname",text="First Name")
        self.Contact_table.heading("lname",text="Last Name")
        self.Contact_table.heading("phone",text="Phone No.")
        self.Contact_table.heading("email",text="Email Id")
        self.Contact_table.heading("address",text="Address")
        self.Contact_table['show']='headings'

        self.Contact_table.column("id",width=0,stretch=NO)
        self.Contact_table.column("fname",width=150)
        self.Contact_table.column("lname",width=150)
        self.Contact_table.column("phone",width=150)
        self.Contact_table.column("email",width=200)
        self.Contact_table.column("address",width=200)
        
        self.Contact_table.pack(fill=BOTH,expand=1)
        self.Contact_table.bind("<ButtonRelease-1>",self.get_cursor)

        self.fetch_data()

    def phone_validation(self):
        if not self.phone_var.get().isdigit():
                messagebox.showerror("Invalid Input","Phone number must contain digits only.")
                return False
        elif len(self.phone_var.get()) != 10:
                messagebox.showerror("Invalid Input","Phone number must have 10 digits")
                return False
        return True
    

    def email_validation(self):
        email = self.email_var.get()
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if not re.match(pattern,email) :
                messagebox.showerror("Invalid Input", "Please enter a valid email address.")
                return False
        return True

        # CRUD operations
    
    def add_contact(self):
        if self.fname_var.get()=="" or self.phone_var.get()=="" or self.email_var.get()=="":
                messagebox.showerror("Error!","All fields are required!")
        
        if not self.phone_validation():
                return

        if not self.email_validation():
                return
        
        con = pymysql.connect(host="localhost", user="root", password="", database="system")
        cur = con.cursor()

        # Check for duplicates
        cur.execute("select * from contacts where phone=%s OR email=%s",(self.phone_var.get(), self.email_var.get()))
                
        if cur.fetchone():
                messagebox.showerror("Duplicate Entry", "Phone number or Email already exists.")
                con.close()
                
        # Insert if no duplicate
        cur.execute("insert into contacts (fname,lname,phone,email,address) VALUES (%s,%s,%s,%s,%s)",(self.fname_var.get(),
                                                                                                        self.lname_var.get(),
                                                                                                        self.phone_var.get(),
                                                                                                        self.email_var.get(),
                                                                                                        self.txt_address.get('1.0', END).strip()
                                                                                                        ))
        con.commit()
        self.fetch_data()
        self.clear()
        self.clear_search()
        con.close()
        messagebox.showinfo("Success!", "Record has been inserted")


    def fetch_data(self):
        con=pymysql.connect(host="localhost",user="root",password="",database="system")
        cur=con.cursor()
        cur.execute("select * from contacts")
        rows=cur.fetchall()
        if len(rows)!=0:
            self.Contact_table.delete(*self.Contact_table.get_children())
            for row in rows:
                self.Contact_table.insert('',END,values=row)
            
        con.close()    

    def clear(self):
        self.id_var.set("")
        self.fname_var.set("")
        self.lname_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        self.txt_address.delete('1.0',END)
        self.clear_search()

        
        
    
    def get_cursor(self,ev):
        cursor_row=self.Contact_table.focus()
        contents=self.Contact_table.item(cursor_row)
        row=contents['values']
        self.id_var.set(row[0])  # hidden id
        self.fname_var.set(row[1])
        self.lname_var.set(row[2])
        self.phone_var.set(row[3])
        self.email_var.set(row[4])
        self.txt_address.delete('1.0',END)
        self.txt_address.insert(END,row[5])
        self.clear_search()
       

    def update_data(self):
        if self.id_var.get()=="":
            messagebox.showerror("Error!", "Please select a record to update.")
            return
        if self.fname_var.get()=="" or self.phone_var.get()=="" or self.email_var.get()=="":
                messagebox.showerror("Error!","All fields are required!")
        
        if not self.phone_validation():
            return

        if not self.email_validation():
            return

        
        try:
                con = pymysql.connect(host="localhost", user="root", password="", database="system")
                cur = con.cursor()

                cur.execute("SELECT * FROM contacts WHERE (phone=%s OR email=%s) AND id!=%s",(self.phone_var.get(), self.email_var.get(), self.id_var.get()))
                if cur.fetchone():
                        messagebox.showerror("Duplicate Entry", "Phone number or Email already exists.")
                        con.close()
                        return

                cur.execute("UPDATE contacts SET fname=%s, lname=%s, phone=%s, email=%s, address=%s WHERE id=%s",(self.fname_var.get(), self.lname_var.get(), self.phone_var.get(),self.email_var.get(), self.txt_address.get('1.0', END).strip(),self.id_var.get()))

                con.commit()
                self.fetch_data()
                self.clear()
                self.clear_search()
                con.close()
                
                messagebox.showinfo("Success!", "Record has been updated successfully.")

        except Exception as ex:
                messagebox.showerror("Error!", f"Error due to: {str(ex)}")



    def delete_data(self):
        if self.id_var.get()=="":
            messagebox.showerror("Error!", "Please select a record to delete.")
            return
        
        con = pymysql.connect(host="localhost", user="root", password="", database="system")
        cur = con.cursor()
        cur.execute("delete from contacts where id=%s", (self.id_var.get(),))
        con.commit()
        con.close()
        self.fetch_data()
        self.clear()
        self.clear_search()
        messagebox.showinfo("Deleted", "Record deleted successfully")

    def clear_search(self):
        self.search_txt.set("")
        self.search_by.set("")

    def search_data(self,event=None):  #for both to work (pressing enter and clicking)
        if self.search_by.get() == "" or self.search_txt.get() == "":
                messagebox.showerror("Error!", "Please select a valid search option and enter text")
                return
        
        con = pymysql.connect(host="localhost", user="root", password="", database="system")
        cur = con.cursor()

        # Mapping values to DB column names

        column_map = {
                "First Name": "fname",
                "Last Name": "lname",
                "Phone No.": "phone",
                "Email": "email",
                "Address": "address"
        }

        try:
                column = column_map[self.search_by.get()]
                query = f"SELECT * FROM contacts WHERE LOWER({column}) LIKE %s"
                cur.execute(query, ("%" + self.search_txt.get().lower() + "%",))
                rows = cur.fetchall()

                if len(rows) != 0:
                        self.Contact_table.delete(*self.Contact_table.get_children())
                        for row in rows:
                                self.Contact_table.insert('', END, values=row)
                else:
                        messagebox.showinfo("No Result", "No records found for your search.")
        except Exception as ex:
                messagebox.showerror("Error!", f"Error due to: {str(ex)}")
        finally:
                con.close()

        



root=Tk()
ob=Contact(root)
root.mainloop()
