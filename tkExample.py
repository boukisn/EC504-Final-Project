from dataExchange import *
from Tkinter import *
import ttk

def calculate(*args):
	#'169.254.226.186'
	clientSync(filename='DC1-sampleQueries.txt', ip_to=db2_ip_address.get(), ip_from='169.254.106.129')
	
	#'127.0.0.1'
	clientSync(filename='client_out.txt', ip_to=db3_ip_address.get(), ip_from='127.0.0.1')

def output_frame_setup():
    for i in range(8):
       ttk.Label(output_frame, text=" ").grid(row=i,column=0)

def callback(sv):
	search_row_0.set(sv.get())
	search_row_1.set(sv.get())
	search_row_2.set(sv.get())
	search_row_3.set(sv.get())

root = Tk()
root.title("PageCacheSyncher")
root.resizable(width=FALSE, height=FALSE)

mainframe = ttk.Frame(root, padding="25 25 25 25")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

db2_ip_address = StringVar()
db3_ip_address = StringVar()
filename = StringVar()
search = StringVar()
search_row_0 = StringVar()
search_row_1 = StringVar()
search_row_2 = StringVar()
search_row_3 = StringVar()
search.trace("w", lambda name, index, mode, sv=search: callback(search))

db2_ip_address_entry = ttk.Entry(mainframe, width=20, textvariable=db2_ip_address)
db2_ip_address_entry.grid(column=2, row=1, columnspan=2, sticky=(W, E))

db3_ip_address_entry = ttk.Entry(mainframe, width=20, textvariable=db3_ip_address)
db3_ip_address_entry.grid(column=2, row=2, columnspan=2, sticky=(W, E))

filename_entry = ttk.Entry(mainframe, width=20, textvariable=filename)
filename_entry.grid(column=2, row=3, columnspan=2, sticky=(W, E))

output_frame = ttk.Frame(mainframe, width=3, height=10, padding="5 5 5 5", relief="sunken")
output_frame.grid(column=1, row=6, columnspan=3, sticky=(N, W, E, S))
output_frame_setup()

search_entry = ttk.Entry(mainframe, width=10, textvariable=search)
search_entry.grid(column=2, row=17, sticky=(W, E))

search_results_frame = ttk.Frame(mainframe, width=3, height=10, padding="5 5 5 5", relief="sunken")
search_results_frame.grid(column=1, row=18, columnspan=3, sticky=(N, W, E, S))
ttk.Label(search_results_frame, textvariable=search_row_0, text=" ").grid(row=0,column=0)
ttk.Label(search_results_frame, textvariable=search_row_1, text=" ").grid(row=1,column=0)
ttk.Label(search_results_frame, textvariable=search_row_2, text=" ").grid(row=2,column=0)
ttk.Label(search_results_frame, textvariable=search_row_3, text=" ").grid(row=3,column=0)

#ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))
ttk.Button(mainframe, text="Sync", command=calculate).grid(column=2, row=4, sticky=W)

# Labels
ttk.Label(mainframe, text="DB2 IP Address").grid(column=1, row=1, sticky=E)
ttk.Label(mainframe, text="DB3 IP Address").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text="Filename").grid(column=1, row=3, sticky=E)
ttk.Label(mainframe, text="Search").grid(column=1, row=17, sticky=E)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

filename_entry.focus()
root.bind('<Return>', calculate)

root.mainloop()