from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
import cx_Oracle
from tkinter import messagebox
import sqlite3
def connect_to_db():
    # for ORACLE-SQL USE = 'username@localhost:1521/orcl'
    #conn=cx_Oracle.connect('username@localhost:1521/orcl')
    conn=sqlite3.connect('sqlite.db')
    # print(conn.version())
    c=conn.cursor()
    return conn,c

def book():
    def insert():
        try:
            conn,cur=connect_to_db()
            pname = str(e1.get())
            phno = int(e2.get())
            age = int(e3.get())
            sex = str(e5.get())
            dose_no = int(e4.get())
            loc = str(city.get())
            cname = str(hosp.get())
            try:
                if(dose_no == 2):    
                    for i in cur.execute(f"select C_id from patient_info where P_name = '{pname}' and ph_no = {phno}"):
                        d = i[0]
                    print(d)
                    cur.execute(f"delete from patient_vaccine where P_name = '{pname}' and ph_no={phno}")
                    cur.execute(f"delete from patient_info where P_name = '{pname}' and ph_no={phno}")
            except Exception:  
                    messagebox.showerror("ERROR",f"{pname} You Havent taken first dose.so please take dose 1")
                    return
            print(loc,cname)
            print(var.get())
            if var.get()==1:
                vaccine="Covaxin"
            else:
                vaccine="Covishield"
            cid = 0
            for i in cur.execute(f"select C_id from vaccination_centre where c_name='{cname}' and location='{loc}'"):
                print(i)
                cid=i[0]
                break
            st = ""
            if var2.get() == 1:
                st = "FN"
            else:
                st = "AN"
            dt = cal.get_date()
            date = dt.strftime("%d-%B-%Y")
            cur.execute(f"insert into patient_info values('{pname}',{age},{phno},'{sex}','{cid}','{dose_no}','{date}','{st}')")
            cur.execute(f"insert into patient_vaccine values('{pname}',{phno},'{vaccine}')")
            print("Inserted")
            print(date)
            print(var2.get())
            cur.execute(f"update booking_slot set no_of_slots = no_of_slots - 1 where bookdate = '{date}' and session_time = '{st}'")
            print("Updated")
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("SUCCESSFUL", "YOUR VACCINATION SLOT HAS BEEN SUCCESSFULLY RESERVED.THANK YOU FOR VACCINATING")
        except Exception as e:
            messagebox.showerror("ERROR",e)
    root1=Toplevel()
    root1.geometry("450x600")
    root1.title("vaccination Booking")
    x=Label(root1,text='Please enter the following details for reserving your vaccine',font=('Arial',12),fg='blue')
    x.pack()
    def hospital(e):
     print("inside")
     x=city.get()
     print(x)
     if(x == 'Chennai'):
         val1=['Apollo','CURI Hospital','Vcure Hospital']
         hosp.config(value=val1)
     elif(x == 'Madurai'):
         val2=['LP Anand Hospital','Apollo']
         hosp.config(value=val2)
     elif(x == 'Coimbatore'):
         val2=['Apollo']
         hosp.config(value=val2)
     elif(x == 'Trichy'):
         val2=['GVN Hospital']
         hosp.config(value=val2)
     elif(x == 'Salem'):
         val2=['SKS Hospital']
         hosp.config(value=val2)
     elif(x == 'Tirunalveli'):
         val2=['Galaxy Hospital']
         hosp.config(value=val2)
     elif(x == 'Tirupur'):
         val2=['TMF Hospital']
         hosp.config(value=val2)
                         
    l1 = Label(root1, text="NAME")
    #l1.place(x=100, y=20)
    l1.pack()
    e1 = Entry(root1, width=35)
    #e1.place(x=150, y=20, width=100)
    e1.pack()
    
    l2 = Label(root1, text="PHONE")
    #l2.place(x=100, y=50)
    l2.pack()
    e2 = Entry(root1, width=35)
    #e2.place(x=150, y=50, width=100)
    e2.pack()

    l3 = Label(root1, text="AGE")
    #l3.place(x=100, y=80)
    l3.pack()
    e3 = Entry(root1, width=35)
    #e3.place(x=150, y=80, width=100)
    e3.pack()
    
    
    l5 = Label(root1, text="SEX")
    #l5.place(x=100, y=120)
    l5.pack()
    e5 = Entry(root1, width=35)
    #e5.place(x=150, y=120, width=100)
    e5.pack()
    
    l4 = Label(root1, text="DOSE_NO")
    #l4.place(x=100, y=100)
    l4.pack()
    e4 = Entry(root1, width=35)
    #e4.place(x=150, y=100, width=100)
    e4.pack()
    
    l10=Label(root1,text='VACCINE')
    l10.pack()
    
    var = IntVar()
    R1 = Radiobutton(root1, text="Covaxin", variable=var, value=1)
    R1.pack()
    
    R2 = Radiobutton(root1, text="Covishield", variable=var, value=2)
    R2.pack()
    
    l6=Label(root1,text="DATE")
    l6.pack()
    cal = DateEntry(root1, width= 16, background= "magenta3", foreground= "white",bd=2)
    cal.pack()
    dt = cal.get_date()
    date = dt.strftime("%d-%B-%Y")
    print(date)
    
    
    l8=Label(root1,text="CITY")
    l8.pack()
    places=['Chennai','Madurai','Coimbatore','Trichy','Salem','Tirunelveli','Tirupur']
    city=ttk.Combobox(root1,width=15,value=places)
    city.current(0)
    city.pack()
    city.bind("<<ComboboxSelected>>",hospital)
    l9=Label(root1,text="VACCINATION CENTER")
    l9.pack()
    hosp=ttk.Combobox(root1,width=15,value=[" "])
    hosp.current(0)
    hosp.pack()
    l7=Label(root1,text="SLOT")
    l7.pack()
    var2 = IntVar()
    R3 = Radiobutton(root1, text="FN", variable=var2, value=1)
    R3.pack()
    
    R4 = Radiobutton(root1, text="AN", variable=var2, value=2)
    R4.pack()   
    
    b = Button(root1, text="SUBMIT", bg="light blue",command= insert,activebackground='cyan',width=20)
    b.pack() 	
    

def cancel():
    root2=Tk()
    root2.geometry("400x300")
    root2.title("vaccination cancellation")
    x=Label(root2,text='Please enter the following details for cancellation',font=('Arial',12),fg='blue')
    x.pack()
    l1=Label(root2,text="NAME")
    l1.pack()
    e1=Entry(root2,width=30)
    e1.pack()
    
    l2=Label(root2,text="PHONE")
    l2.pack()
    e2=Entry(root2,width=30)
    e2.pack()

    def delete():
        conn,cur=connect_to_db()
        pname = str(e1.get())
        phno = int(e2.get())
        try:
            for i in cur.execute(f"select bookdate,session_time,C_id from patient_info where P_name = '{pname}' and ph_no = {phno}"):
                print(i[0])
                print(i[1])
                print(i[2])
            # d = str(i[0])
            d = str(i[0]).split()[0]
            d = i[0].strftime("%d-%B-%Y")
            print("d = ",d)
            e = i[1]
            c = i[2]
            print("e = ",e)
            cur.execute(f"update booking_slot set no_of_slots = no_of_slots + 1 where bookdate = '{d}' and session_time = '{e}' and C_id = '{c}'")
            print("Updated")
            cur.execute(f"delete from patient_vaccine where P_name = '{pname}' and ph_no = {phno}")
            cur.execute(f"delete from patient_info where P_name = '{pname}' and ph_no = {phno}")
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("CANCELLED", "YOUR VACCINATION RESERVATION HAS BEEN CANCELLED!")
        except Exception:
            messagebox.showinfo("ERROR", "Record Not found. Cancellation Failed")

    b = Button(root2, text="CANCEL", bg="light blue",command=delete,activebackground='cyan',width=20)
    b.pack()    
    
    root2.mainloop()
def show():
    def display():
            li = Listbox(root3)
            li.insert(END,"PATIENT NAME")
            li.insert(END,"")
            li.pack()
            conn,cur = connect_to_db()
            d = int(e.get())
            print(d)
            for i in cur.execute(f"select P_name from patient_info where dose_no = {d}"):
                li.insert(END,i[0])
                print(END,i[0])

            conn.commit()
            cur.close()
            conn.close()

    root3=Tk()
    root3.geometry("400x500")
    root3.title("Details")
    l = Label(root3, text="DOSE_NO")
    l.pack()
    e = Entry(root3, width=20)
    e.pack()
    b1=Button(root3, text="SUBMIT", command=display,activebackground='cyan',bg='light blue',width=15)
    b1.pack(pady=(10,0))
    root3.mainloop()    
# GUI Design
root = Tk()
root.geometry("500x400")
root.title("cowin")
bg = PhotoImage(file = "vaccine.png")
imglabel = Label( root, image = bg)
imglabel.place(x = 18, y = -105)
l=Label(root,text="VACCINATION 19",font=("Calisto MT",15),fg='blue',pady=5)
l.pack()
scrollbar = Scrollbar(root)
scrollbar.pack( side = RIGHT, fill = Y )
print("hello")
lframe1 = LabelFrame(root, text="BOOKING", bd=3,bg='light yellow',fg="red")
lframe1.pack()
lbook=Label(lframe1,text="For reservation of vaccination please click here",font=('Arial',12),bg='light yellow')
lbook.pack()
b1=Button(lframe1, text="Booking", command=book,activebackground='cyan',bg='light blue')
b1.pack()
gap=Label(root,pady=5)
gap.pack()
lframe2 = LabelFrame(root, text="CANCELLATION",bd=3,bg='light yellow',fg="red")
lframe2.pack()
lcancel=Label(lframe2,text="For cancelling your vaccination reservation please click here",font=('Arial',12),bg='light yellow')
lcancel.pack()
b2=Button(lframe2,text="CANCEL", command=cancel,activebackground='cyan',bg='light blue')
b2.pack()
gap1=Label(root,pady=5)
gap1.pack()
lframe3 = LabelFrame(root, text="DISPLAY",bd=3,bg='light yellow',fg="red")
lframe3.pack()
ldisp=Label(lframe3,text="For Displaying Patient details",font=('Arial',12),bg='light yellow')
ldisp.pack()
b3=Button(lframe3,text="SHOW", command=show,activebackground='cyan',bg='light blue')
b3.pack()
root.mainloop()