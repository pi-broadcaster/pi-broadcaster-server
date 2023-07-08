# Import library
from tkinter import *
from tkinter import ttk
import pysftp, paramiko, json, math, sys, os, subprocess, socket
import time as tm
# PyInstaller compatible
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
# Configure connection
sftp = None
test_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
test_sock.connect(("10.2.1.1", 80))
with test_sock:
    private_ip, *_ = test_sock.getsockname()
private_ip = ".".join(private_ip.split('.')[0:-1]) + '.'
b = subprocess.check_call("for /L %N in (1,1,255) do start /b ping -n 1 -w 200 " + private_ip + "%N", shell=True)
hostname = "pi.local"
username = "pi"
password = "pi"
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
localFilePath = resource_path('config.json')
remoteFilePath = '/media/PB/PB/config.json'
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
# Initial
id = 0
top = Tk()
top.state("zoomed")
top.title('Bảng điều khiển')
top.iconbitmap(resource_path("icon.ico"))
# Status bar
status_bar = Text(top, height=1)
status_bar.pack(fill=BOTH)
# Table
table_frame = Frame(top)
table_frame.pack(fill=BOTH)
# Scroll bar for table
scroller = Scrollbar(table_frame)
scroller.pack(side=RIGHT, fill=Y)

scroller = Scrollbar(table_frame,orient='horizontal')
scroller.pack(side= BOTTOM,fill=X)

table = ttk.Treeview(table_frame,yscrollcommand=scroller.set, xscrollcommand =scroller.set)
table.pack(fill=BOTH)

scroller.config(command=table.yview)
scroller.config(command=table.xview)
# Columns for table
table['columns'] = ('id', 'link', 'time_hour', 'time_min', 'weekday')

table.column("#0", width=0,  stretch=NO)
table.column("id",anchor=CENTER, width=80)
table.column("link",anchor=CENTER, width=80)
table.column("time_hour",anchor=CENTER,width=80)
table.column("time_min",anchor=CENTER,width=80)
table.column("weekday",anchor=CENTER,width=80)
# Headers
table.heading("#0",text="",anchor=CENTER)
table.heading("id",text="Số thứ tự",anchor=CENTER)
table.heading("link",text="Liên kết danh sách phát YouTube/Lời nhắc",anchor=CENTER)
table.heading("time_hour",text="Giờ phát",anchor=CENTER)
table.heading("time_min",text="Phút phát",anchor=CENTER)
table.heading("weekday",text="Ngày phát",anchor=CENTER)
# Input frame
input = Frame(top)
input.pack(pady=20)

# Input labels
id= Label(input,text = "Số thứ tự")
id.grid(row=0, column=0)
link= Label(input,text = "Liên kết danh sách phát YouTube/Lời nhắc")
link.grid(row=0, column=1)
time = Label(input,text="Giờ phát")
time.grid(row=0,column=2)
time_min = Label(input,text="Phút phát")
time_min.grid(row=0,column=3)
weekday = Label(input,text="Ngày phát")
weekday.grid(row=0,column=4)
# Inputs
inp_id= Entry(input, width=30)
inp_id.grid(row= 1, column=0)
inp_link= Entry(input, width=30)
inp_link.grid(row= 1, column=1)
inp_time_hour = Entry(input)
inp_time_hour.grid(row=1,column=2)
inp_time_min = Entry(input)
inp_time_min.grid(row=1,column=3)
inp_weekday = Entry(input)
inp_weekday.grid(row=1,column=4)
# Button's function
def select_record():
    inp_id.delete(0,END)
    inp_link.delete(0,END)
    inp_time_hour.delete(0,END)
    inp_time_min.delete(0,END)
    inp_weekday.delete(0,END)
    
    selected=table.focus()
    print(selected)
    values = table.item(selected,'values')
    
    inp_id.insert(0,values[0])
    inp_link.insert(0,values[1])
    inp_time_hour.insert(0,values[2])
    inp_time_min.insert(0,values[3])
    inp_weekday.insert(0,values[4])

def data_duplicate(id):
    for i in range(0, len(data)):
        if data[i]["id"] == id:
            return i + 1
    return -1

def edit_record():
    selected=table.focus()
    table.item(selected,text="",values=(inp_id.get(), inp_link.get(),inp_time_hour.get(),inp_time_min.get(), inp_weekday.get()))
    
    inp_id.delete(0,END)
    inp_link.delete(0,END)
    inp_time_hour.delete(0,END)
    inp_time_min.delete(0,END)
    inp_weekday.delete(0,END)

    values = table.item(selected,'values')

    wkday = []
    for day in [*set(values[4].replace(" ", "").split(","))]:
        if day != "":
            wkday.append(int(day) - 2)

    id = int(values[0])
    kind = "text"
    if values[1].find("list=") != -1:
        kind = "link"
    if kind == "link" and data_duplicate(values[1].replace("https://www.youtube.com/playlist?list=", "")) != -1:
        id = data_duplicate(values[1].replace("https://www.youtube.com/playlist?list=", ""))

    cell = {"dir": str(id),
    "type": kind,
    "id": values[1].replace("https://www.youtube.com/playlist?list=", ""),
    "time": float(values[2]) + float(float(values[3]) / 60),
    "day": wkday
    }
    data[int(selected)] = cell

def add_record():
    table.insert(parent='',index='end',iid=len(table.get_children()),text='', values=(len(table.get_children()) + 1, '',0, 0,''))

    data.append({"dir": str(len(table.get_children()) + 1),
    "type": "text",
    "id": "",
    "time": 0.0,
    "day": []
    })

def del_record():
    selected = table.focus()
    data.pop(table.index(selected))
    table.delete(selected)

# Buttons
action = Frame(top)
action.pack()

add_button = Button(action, text='Thêm lịch phát', width=25, command=add_record)
add_button.pack(pady = 5, side = LEFT)

del_button = Button(action, text='Xóa lịch phát', width=25, command=del_record)
del_button.pack(pady = 5, side = LEFT)

select_button = Button(action,text="Chọn lịch phát", width=25, command=select_record)
select_button.pack(pady = 5, side = LEFT)

edit_button = Button(action,text="Lưu lịch phát", width=25,command=edit_record)
edit_button.pack(pady = 5, side = LEFT)

guide = Text(top)
guide.pack(fill=X)

guileline = """Để thêm một lịch phát, nhấn Thêm lịch phát
Để chọn một lịch phát để sửa đổi, nhấn Chọn lịch phát

Nhập lời nhắc đúng chính tả, không viết tắt.
Muốn lấy liên kết danh sách phát YouTube, hãy truy cập vào danh sách phát đó, sao chép liên kết trên thanh địa chỉ và dán vào ô nhập

Khi nhập ngày phát, hãy nhập những ngày trong tuần mà bạn muốn phát theo dạng:
Thứ 2: 2 ; Thứ 3: 3 ; Thứ 4: 4 ; Thứ 5: 5 ; Thứ 6: 6 ; Thứ 7: 7 ; Chủ nhật: 8
Mỗi ngày cách nhau bởi một dấu phẩy
Ví dụ: Bạn muốn phát vào thứ 2, 3, 5, 6 và chủ nhật thì nhập: 2, 3, 5, 6, 8

Giờ phát trong khoảng 0-23, phút phát trong khoảng 0-59

Sau khi sửa xong lịch phát, nhấn Lưu lịch phát
Sau khi bạn cấu hình xong, nhấn Lưu cấu hình vào thiết bị"""
guide.insert(INSERT, guileline)

status_bar.insert(END, "Đang kết nối với thiết bị...")
top.update()
sftp = None
if hostname == "unknown":
    status_bar.delete(1.0, END)
    status_bar.insert(END, "Không thể kết nối với thiết bị. Đợi khoảng 10-15 giây nữa rồi quay lại.")
    top.update()
    tm.sleep(2)
    sys.exit()
else:
    try:
        sftp = pysftp.Connection(host=hostname, username=username, password=password, cnopts=cnopts, port=22)
    except:
        status_bar.delete(1.0, END)
        status_bar.insert(END, "Không thể kết nối với thiết bị. Đợi khoảng 10-15 giây nữa rồi quay lại.")
        top.update()
        tm.sleep(2)
        sys.exit()

def update_record():
    status_bar.delete(1.0, END)
    status_bar.insert(END, "Đang lưu cấu hình vào thiết bị...")
    data.sort(key=lambda x: x["time"])
    for cell in data:
        cell["dir"] = str(data.index(cell) + 1)
    open("config.json", "w", encoding="utf-8").write(json.dumps(data))
    sftp.put(localpath=localFilePath, remotepath=remoteFilePath)
    print(data)
    status_bar.delete(1.0, END)

update_button = Button(action,text="Lưu cấu hình vào thiết bị", width=25,command=update_record)
update_button.pack(pady = 5, side = LEFT)

status_bar.delete(1.0, END)
ssh.connect(hostname=hostname, username=username, password=password)
sftp.get(remotepath=remoteFilePath, localpath=localFilePath)
f = open(localFilePath, "r", encoding="utf-8")
data = json.loads(f.read())
f.close()

for config in data:
    min, hour = math.modf(config["time"])
    table.insert(parent='',index='end',iid=len(table.get_children()),text='', values=(len(table.get_children()) + 1, ("https://www.youtube.com/playlist?list=" if config["type"] == "link" else "") + config["id"], int(hour), int(min * 60), json.dumps(list(day + 2 for day in config["day"])).replace("[", "").replace("]", "")))

top.mainloop()

sftp.close()
ssh.exec_command("sudo shutdown -r now")
ssh.close()
print('fin')