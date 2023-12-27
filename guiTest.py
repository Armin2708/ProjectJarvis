import tkinter as tk


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.configDiscordChanId = None
        self.configDiscordBotToken = None
        self.configGuildId = self.newWidget()
        self.configSelfDestroy = None
        self.configRun = None
        self.configPos2 = None
        self.configPos1 = None
        self.grid(sticky=tk.N + tk.S + tk.E + tk.W)
        self.createWidgets()


    def newWidget(self):
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.widgetTest = tk.Entry(self)
        self.widgetTest.grid(row=0, column=0)

        self.validationTest = tk.Button(self, text="validate")
        self.widgetTest.grid(row=0, column=1)



    def createWidgets(self):
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        #Widgets start here
        self.quit = tk.Button(self, text='Quit', command=self.quit)
        self.quit.grid(row=0, column=0)

        self.configPos1 = tk.Button(self, text='configure position 1 key', command=self.configPos1)
        self.configPos1.grid(row=0, column=1)

        self.configPos2 = tk.Button(self, text='configure position 2 key', command=self.configPos2)
        self.configPos2.grid(row=0, column=2)

        self.configRun = tk.Button(self, text='configure run key', command=self.configRun)
        self.configRun.grid(row=0, column=3)

        self.configSelfDestroy = tk.Button(self, text='configure self destruct key', command=self.configSelfDestroy)
        self.configSelfDestroy.grid(row=1, column=0)

        self.configGptApiKey = tk.Button(self, text='configure gpt api key', command=self.newWidget())
        self.configGptApiKey.grid(row=1, column=1)

        self.configDiscordBotToken = tk.Button(self, text='configure discord bot token', command=self.configDiscordBotToken)
        self.configDiscordBotToken.grid(row=1, column=2)

        self.configDiscordChanId = tk.Button(self, text='configure discord channel id', command=self.configDiscordChanId)
        self.configDiscordChanId.grid(row=1, column=3)



app = Application()
app.master.title('Sample application')
app.mainloop()