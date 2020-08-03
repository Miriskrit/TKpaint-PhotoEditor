from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import Image, ImageDraw, ImageTk, ImageGrab, ImageFilter
from random import randint, random
import time
from color_list import colors_l
import os


class Program(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.color = 'black' # кисть по умолчанию
        self.brush_size = 2
        self.brush_type = 0
        self.setUI()
        self.pilImage = None

    #_______________________________________System_Functions()________________________________________
    def q(self):
        quit()
    
    def open_img(self):
        self.size = (1200,800)                              #максимальный размер
        self.name = askopenfilename()                       #имя файла
        self.pilImage = Image.open(self.name)               #открытие файла
        self.pilImage.thumbnail(self.size)                  #кадрирование
        self.image = ImageTk.PhotoImage(self.pilImage)      #подготовка к использованию tkinter
        self.canv.create_image(600,400,image=self.image)    #установка в canvas
        (self.w, self.h) = self.pilImage.size               #получение размеров изображения 

    def canvas_image_paste(self, something_img):
        self.image = ImageTk.PhotoImage(something_img)
        self.canv.create_image(600,400,image=self.image)

    def save_img(self):
        name = os.path.join('TK_Saves','img'+ str(randint(0,10000))+'.png')
        self.new_img.save(name)

    def save_as(self):
        name1 = asksaveasfilename(filetypes=[(("Log files"), "*.*")])
        self.new_img.save(str(name1) + '.png')

    def _canvas(self): 
        x=self.canv.winfo_rootx()+self.canv.winfo_x()
        y=self.canv.winfo_rooty()+self.canv.winfo_y()
        x1=x+self.canv.winfo_width()
        y1=y+self.canv.winfo_height()
        box=(x,y,x1,y1)
        return box
    
    def save_canvas(self):
        canvas = self._canvas()
        time.sleep(1.0)
        self.grabcanvas = ImageGrab.grab(bbox=canvas)
        self.grabcanvas.show()
        self.grabcanvas.save(os.path.join('TK_Saves', 'cvs'+ str(randint(10000,30000))+'.png'))
    #__________________;
    
    #_______________________________________Drawing_Functions()________________________________________
    def set_color(self, new_color):
        self.color = new_color
        self.label_current_color['text'] = new_color
        self.label_current_color2['bg'] = new_color

    def set_brush_size(self, new_size):
        self.brush_size = new_size
        self.label_current_size['text'] = str(new_size)

    def modofy_brush_size(self, size):
        self.label_current_size['text'] = str(self.brush_size + size) 
        self.brush_size += size
        
    def brush_type_select(self, b_type):
        self.brush_type = b_type    
        
    def select_brush(self):
        window = Toplevel(self)
        window.title('Brushes')
        b_frame = Frame(window)
        b_frame.pack()
        b_1 = Button(b_frame,bg = 'LightCyan3',fg = 'white',bd = 7,relief = 'ridge', text='deflaut', width=15, command = lambda:self.brush_type_select(0))
        b_2 = Button(b_frame,bg = 'LightCyan3',fg = 'white',bd = 7,relief = 'ridge', text='color+black', width=15, command = lambda:self.brush_type_select(1))
        b_3 = Button(b_frame,bg = 'LightCyan3',fg = 'white',bd = 7,relief = 'ridge', text='with_outline', width=15, command = lambda:self.brush_type_select(2))
        b_4 = Button(b_frame,bg = 'LightCyan3',fg = 'white',bd = 7,relief = 'ridge', text='rectangle', width=15, command = lambda:self.brush_type_select(3))
        b_5 = Button(b_frame,bg = 'LightCyan3',fg = 'white',bd = 7,relief = 'ridge', text='oval', width=15, command = lambda:self.brush_type_select(4))
        b_1.pack()
        b_2.pack()
        b_3.pack()
        b_4.pack()
        b_5.pack()
        

    def draw(self, event):
        if self.brush_type == 0:
            self.canv.create_oval(event.x - self.brush_size,
                                event.y - self.brush_size,
                                event.x + self.brush_size,
                                event.y + self.brush_size,
                                fill=self.color, outline=self.color)   
        elif self.brush_type == 1:
            self.canv.create_oval(event.x - self.brush_size,
                                event.y - self.brush_size,
                                event.x + self.brush_size,
                                event.y + self.brush_size,
                                fill=self.color, outline=self.color)  
            self.canv.create_oval(event.x - self.brush_size + 2,
                                event.y - self.brush_size + 2,
                                event.x + self.brush_size - 2,
                                event.y + self.brush_size - 2,
                                fill='black', outline=self.color)  
        elif self.brush_type == 2:
            self.canv.create_oval(event.x - self.brush_size,
                                event.y - self.brush_size,
                                event.x + self.brush_size,
                                event.y + self.brush_size,
                                fill=self.color, outline='black') 
        elif self.brush_type == 3:
            self.canv.create_rectangle(event.x - self.brush_size,
                                event.y - self.brush_size,
                                event.x + self.brush_size,
                                event.y + self.brush_size,
                                fill=self.color, outline=self.color) 
        elif self.brush_type == 4:
            self.canv.create_oval(event.x - self.brush_size//2 - self.brush_size,
                                event.y - self.brush_size,
                                event.x + self.brush_size//2 + self.brush_size,
                                event.y + self.brush_size,
                                fill=self.color, outline=self.color) 

    def select_color(self):
        def release(event):
            self.set_color(event.widget['bg'])
            self.label_current_color2['bg'] = event.widget['bg']
        COLORS  =  colors_l()
        window = Toplevel(self)
        window.title('Colors')
        enter_frame = Frame(window)
        enter_frame.pack()
        r = 0; c = 0
        for i in range(len(COLORS)):
            b = Button(enter_frame, bg = COLORS[i], width = 5)
            b.bind('<Button-1>', release)
            if c<=11:
                b.grid(row = r, column = c)
                c+=1
            else:
                r+=1
                c = 0
                b.grid(row = r, column = c)
    #__________________;
    
    #_______________________________________Canals_Functions()________________________________________
    def mix_canals(self, mode): 
        if self.pilImage:
            img = self.pilImage
            select = self.rgb_select.get()[:3:]
            slpit_img = img.split()
            if len(slpit_img) == 3:
                r, g, b = slpit_img
            elif len(slpit_img) == 4:
                r, g, b, _ = slpit_img
            cn = [r,g,b]
            arr = []
            if mode == 1:
                self.new_img = Image.merge('RGB', (b, g, r))
            if mode == 2:
                self.new_img = Image.merge('RGB', (g, b, r))
            if mode == 3:
                self.new_img = Image.merge('RGB', (r, b, g))
            if mode == 4:
                self.new_img = Image.merge('RGB', (b, r, r))
            if mode == 5:
                self.new_img = Image.merge('RGB', (r, g, b))
            if mode == 6:
                rand = (cn[randint(0,2)], cn[randint(0,2)], cn[randint(0,2)])
                self.new_img = Image.merge('RGB', rand)
            if mode == 7:
                for i in range(3):
                    if select[i] == 'r':
                        arr.append(r)
                    if select[i] == 'g':
                        arr.append(g)
                    if select[i] == 'b':
                        arr.append(b)
                self.new_img = Image.merge('RGB', (arr[0], arr[1], arr[2]))
            self.new_img.thumbnail(self.size)
            self.canvas_image_paste(self.new_img)
    #__________________;
    
    def blur_img(self):
        self.new_img = self.pilImage.filter(ImageFilter.BLUR)
        self.canvas_image_paste(self.new_img)

    def contur_img(self):
        self.new_img = self.pilImage.filter(ImageFilter.CONTOUR)
        self.canvas_image_paste(self.new_img)


    #_______________________________________Filters_Functions()________________________________________
    def D_img(self, i):
        if i == 3:
            r = randint(2,64)
        if i == 2:
            r = randint(15,64)
        if i == 1:
            r = randint(2,7)
        arr = []
        for _ in range (3*r**3):
            arr.append(random())
        self.new_img = self.pilImage.filter(ImageFilter.Color3DLUT(r,arr))
        self.canvas_image_paste(self.new_img)
    #__________________;

    #_______________________________________Image_Functions()________________________________________
    def about_img(self):
        if self.pilImage:
            self.pixellabel['text'] = (': width = ' + str(self.w) + ' height = '+ str(self.h) )


    def color_cube(self):
        if self.pilImage:
            for i in range(self.w):
                    for j in range(self.h):
                            pix = self.pilImage.getpixel((i, j)) 
                            
                            if i%10 <= 3 and j%10 <= 3 :
                                    new_pix = (pix[0]+30, pix[1], pix[2])
                            elif 3<i%10<=6 and 3<j%10<=6:
                                    new_pix = (pix[0], pix[1]+30, pix[2])
                            else:
                                    new_pix = (pix[0], pix[1], pix[2]+30)

                            self.pilImage.putpixel((i, j), new_pix)
            self.new_img = self.pilImage
            self.canvas_image_paste(self.new_img)

    def miroow(self):
        if self.pilImage:
            for i in range(int(self.w/2)):
                    for j in range(self.h):
                            pix = self.pilImage.getpixel((i, j)) 
                            new_pix = (pix[0], pix[1], pix[2])
                            self.pilImage.putpixel((self.w-1-i , j), new_pix)
            self.new_img = self.pilImage
            self.canvas_image_paste(self.new_img)

    def noize(self):
        if self.pilImage:
            for i in range(self.w):
                    for j in range(int(self.h)):
                            pix = self.pilImage.getpixel((i, j)) 
                            new_pix = (pix[0]+randint(-100,100), pix[1]+randint(-100,100), pix[2]+randint(-100,100))
                            self.pilImage.putpixel((i , j), new_pix)
            self.new_img = self.pilImage
            self.canvas_image_paste(self.new_img)

    def contrast(self, operation):
        if self.pilImage:
            if operation == 1:
                for i in range(self.w):
                        for j in range(int(self.h)):
                                pix = self.pilImage.getpixel((i, j)) 
                                if pix[0] <= 125 and pix[1] <= 125 and pix[2] <= 125:
                                    new_pix = (pix[0]-10,pix[1]-10,pix[2]-10)
                                elif pix[0] > 125 and pix[1] > 125 and pix[2] > 125:
                                    new_pix = (pix[0]+10,pix[1]+10,pix[2]+10)
                                else:
                                    new_pix = (pix[0],pix[1],pix[2])
                                self.pilImage.putpixel((i , j), new_pix)
            if operation == 2:
                for i in range(self.w):
                        for j in range(int(self.h)):
                                pix = self.pilImage.getpixel((i, j)) 
                                if pix[0] <= 125 and pix[1] <= 125 and pix[2] <= 125:
                                    new_pix = (pix[0]+10,pix[1]+10,pix[2]+10)
                                elif pix[0] > 125 and pix[1] > 125 and pix[2] > 125:
                                    new_pix = (pix[0]-10,pix[1]-10,pix[2]-10)
                                else:
                                    new_pix = (pix[0],pix[1],pix[2])
                                self.pilImage.putpixel((i , j), new_pix)
            self.new_img = self.pilImage
            self.canvas_image_paste(self.new_img)

    def levels(self):
        if self.pilImage:
            for i in range(self.w):
                        for j in range(int(self.h)):
                            pix = self.pilImage.getpixel((i, j)) 
                            if pix[0] <= 25 and pix[1] <= 25 and pix[2] <= 25:
                                new_pix = (0,0,0)
                            elif pix[0] <= 75 and pix[1] <= 75 and pix[2] <= 75:
                                new_pix = (50,50,50)
                            elif pix[0] <= 150 and pix[1] <= 150 and pix[2] <= 150:
                                new_pix = (100,100,100)
                            elif pix[0] <= 200 and pix[1] <= 200 and pix[2] <= 200:
                                new_pix = (175,175,175)
                            elif pix[0] <= 255 and pix[1] <= 255 and pix[2] <= 255:
                                new_pix = (250,250,250)
                            self.pilImage.putpixel((i , j), new_pix)
            self.new_img = self.pilImage
            self.canvas_image_paste(self.new_img)
        
    def rainbow(self):
        if self.pilImage:
            d = self.h//10
            line_h = (self.h//10)//7
            for i in range(self.w):
                for j in range(int(self.h)):
                    pix = self.pilImage.getpixel((i, j))
                    if j%d <= line_h:
                        new_pix = (pix[0]+80, pix[1], pix[2])   # R G B # 80
                    elif line_h<j%d<=line_h*2:
                        new_pix = (pix[0]+45, pix[1]+35, pix[2])
                    elif line_h*2<j%d<=line_h*3:
                        new_pix = (pix[0]+40, pix[1]+40, pix[2])
                    elif line_h*3<j%d<=line_h*4:
                        new_pix = (pix[0], pix[1]+80, pix[2])
                    elif line_h*4<j%d<=line_h*5:
                        new_pix = (pix[0], pix[1]+35, pix[2]+45)
                    elif line_h*5<j%d<=line_h*6:
                        new_pix = (pix[0], pix[1], pix[2]+80)
                    elif line_h*6<j%d<=line_h*7:
                        new_pix = (pix[0]+40, pix[1], pix[2]+40)
                    else:
                        new_pix = (pix[0]+80, pix[1], pix[2])
                    self.pilImage.putpixel((i , j), new_pix)
            self.new_img = self.pilImage
            self.canvas_image_paste(self.new_img)         
                
        
    def return_img(self):
        if self.name:
            self.pilImage = Image.open(self.name)
            self.pilImage.thumbnail(self.size) 
            self.new_img = self.pilImage
            self.canvas_image_paste(self.new_img)
    #__________________;
    def setUI(self):
        self.parent.title('TK photo editor')  # Устанавливаем название окна
        self.grid(row = 0, column = 0)  # Размещаем активные элементы на родительском
        self.parent["bg"] = "gray72"    #Цвет
        #------------------------------------------------
        main_menu = Menu(self.parent)
        self.parent.configure(menu = main_menu)
        item = Menu(main_menu, tearoff = 0 )
        item2 = Menu(main_menu, tearoff = 0 )
        main_menu.add_cascade(label = 'file', menu = item)
        main_menu.add_cascade(label = 'options', menu = item2)
        item.add_command(label = 'Open(img)', command=lambda: self.open_img())
        item.add_command(label = 'QuickSave(img)',command=lambda: self.save_img())
        item.add_command(label = 'SaveAs(img)',command=lambda: self.save_as())
        item.add_command(label = 'Save(Canvas)',command=lambda: self.save_canvas())
        item.add_command(label = 'exit',command=lambda: self.q())
        item2.add_command(label = 'clear_all', command=lambda: self.canv.delete("all"))
        #------------------------------------------------
        #_DRAWING
        self.brush_frame = Frame(self.parent)
        self.brush_frame.grid(row = 0, column = 0)
        color_lab = Label(self.brush_frame, text="Color: ") 
        color_lab.grid(row=0, column=0, padx=6) 
        red_btn = Button(self.brush_frame,bg = 'red',fg = 'white',bd = 7,relief = 'ridge', text="Red", width=10,command=lambda: self.set_color("red")) 
        green_btn = Button(self.brush_frame,bg = 'green',fg = 'white',bd = 7,relief = 'ridge', text="Green", width=10,command=lambda: self.set_color("green"))
        blue_btn = Button(self.brush_frame,bg = 'blue',fg = 'white',bd = 7,relief = 'ridge', text="Blue", width=10,command=lambda: self.set_color("blue"))
        black_btn = Button(self.brush_frame,bg = 'black',fg = 'white',bd = 7,relief = 'ridge', text="Black", width=10,command=lambda: self.set_color("black"))
        white_btn = Button(self.brush_frame,bg = 'white',fg = 'black',bd = 7,relief = 'ridge', text="Erather", width=10,command=lambda: self.set_color("white"))
        red_btn.grid(row=0, column=1) 
        green_btn.grid(row=0, column=2)
        blue_btn.grid(row=0, column=3)
        black_btn.grid(row=0, column=4)
        white_btn.grid(row=0, column=5)
        self.label_current_color = Label(self.brush_frame, text = 'black', bg = 'LightCyan3', width = 15,bd = 7)
        self.label_current_color2 = Label(self.brush_frame, bg = 'black',width = 5,bd = 7)
        self.label_current_size = Label(self.brush_frame, text = '2', bg = 'LightCyan3',width = 5,bd = 7)
        
        self.label_current_color.grid(row=0, column=8)
        self.label_current_color2.grid(row=0, column=9)
        self.label_current_size.grid(row=0, column=10)

        new_color_btn = Button(self.brush_frame,bg = 'LightCyan3',fg = 'black',bd = 7,relief = 'ridge', text='Select_Color', width=10, command=lambda: self.select_color())
        new_color_btn.grid(row=0, column=6)
        size_lab = Label(self.brush_frame, text="Brush size: ")
        size_lab.grid(row=1, column=0, padx=5)
        one_btn = Button(self.brush_frame,bg = 'LightCyan3',fg = 'black',bd = 7,relief = 'ridge', text="Two", width=10, command=lambda: self.set_brush_size(2))
        two_btn = Button(self.brush_frame,bg = 'LightCyan3',fg = 'black',bd = 7,relief = 'ridge', text="Five", width=10, command=lambda: self.set_brush_size(5))
        five_btn = Button(self.brush_frame,bg = 'LightCyan3',fg = 'black',bd = 7,relief = 'ridge', text="Seven", width=10, command=lambda: self.set_brush_size(7))
        seven_btn = Button(self.brush_frame,bg = 'LightCyan3',fg = 'black',bd = 7,relief = 'ridge', text="Ten", width=10, command=lambda: self.set_brush_size(10))
        ten_btn = Button(self.brush_frame,bg = 'LightCyan3',fg = 'black',bd = 7,relief = 'ridge', text="Twenty", width=10, command=lambda: self.set_brush_size(20))
        twenty_btn = Button(self.brush_frame,bg = 'LightCyan3',fg = 'black',bd = 7,relief = 'ridge', text="Fifty", width=10, command=lambda: self.set_brush_size(50))
        sizeplus_btn = Button(self.brush_frame,bg = 'LightCyan3',fg = 'black',bd = 7,relief = 'ridge', text=" + ", width=10, command=lambda: self.modofy_brush_size(1))
        sizemin_btn = Button(self.brush_frame,bg = 'LightCyan3',fg = 'black',bd = 7,relief = 'ridge', text=" - ", width=10, command=lambda: self.modofy_brush_size(-1))
        twenty_btn.grid(row=1, column=6, sticky=W)
        one_btn.grid(row=1, column=1)
        two_btn.grid(row=1, column=2)
        five_btn.grid(row=1, column=3)
        seven_btn.grid(row=1, column=4)
        ten_btn.grid(row=1, column=5)
        sizeplus_btn.grid(row=1, column=6)
        sizemin_btn.grid(row=1, column=7)
        
        brushes_btn = Button(self.brush_frame,bg = 'LightCyan3',fg = 'black',bd = 7,relief = 'ridge', text='BRUSHES', width=10, command=lambda: self.select_brush())
        brushes_btn.grid(row=1,column=8)
        #------------------------------------------------
        #_Canvas
        self.canvas_frame = Frame(self.parent)
        self.canvas_frame.grid(row = 1, column = 0)

        self.canv = Canvas(self.canvas_frame,width=1200,height=800, bg = 'white')
        self.canv.pack()  
        self.canv.bind("<B1-Motion>", self.draw)
        #------------------------------------------------
        #Filters
        self.filter_frame = Frame(self.parent)
        self.filter_frame.grid(row = 1, column = 1)

        canal_lab = Label(self, text="Преобразования: ")
        canal_lab.grid(row=0, column=0, padx=5)
        color_btn1 = Button(self.filter_frame, text="RGB -> BGR", width=11, command=lambda: self.mix_canals(1))
        color_btn2 = Button(self.filter_frame, text="RGB -> GBR", width=11, command=lambda: self.mix_canals(2))
        color_btn3 = Button(self.filter_frame, text="RGB -> RBG", width=11, command=lambda: self.mix_canals(3))
        color_btn4 = Button(self.filter_frame, text="RGB -> BRR", width=11, command=lambda: self.mix_canals(4))
        Label(self.filter_frame,text = '--------------').grid(row = 5, column = 0)
        color_btn5 = Button(self.filter_frame, text="--- -> RGB", width=11, command=lambda: self.mix_canals(5))
        color_btn6 = Button(self.filter_frame, text="RANDOM", width=10, command=lambda: self.mix_canals(6))
        Label(self.filter_frame,text = '--------------').grid(row = 8, column = 0)
        lb_about = Label(self.filter_frame,text = 'mix \"rgb\" :')
        self.rgb_select = Entry(self.filter_frame,width=10)
        color_select_btn = Button(self.filter_frame, text="ENTER", width=10, command=lambda: self.mix_canals(7))
        color_btn1.grid(row = 1, column = 0)
        color_btn2.grid(row = 2, column = 0)
        color_btn3.grid(row = 3, column = 0)
        color_btn4.grid(row = 4, column = 0)
        color_btn5.grid(row = 6, column = 0)
        color_btn6.grid(row = 7, column = 0)
        lb_about.grid(row=9, column=0, padx=6)
        self.rgb_select.grid(row = 10, column = 0)
        color_select_btn.grid(row = 11, column = 0)
        Label(self.filter_frame,text = '--------------').grid(row = 12, column = 0)

        blur_btn = Button(self.filter_frame, text = 'BLUR', width=10 , command=lambda: self.blur_img())
        contur_btn = Button(self.filter_frame, text = 'CONTUR', width=10 , command=lambda: self.contur_img())
        dmin_btn = Button(self.filter_frame, text = '3D_minimal', width=10 , command=lambda: self.D_img(1))
        dmax_btn = Button(self.filter_frame, text = '3D_max', width=10 , command=lambda: self.D_img(2))
        drand_btn = Button(self.filter_frame, text = '3D_random', width=10 , command=lambda: self.D_img(3))
        blur_btn.grid(row = 13, column = 0)
        contur_btn.grid(row = 14, column = 0)
        dmin_btn.grid(row = 15, column = 0)
        dmax_btn.grid(row = 16, column = 0)
        drand_btn.grid(row = 17, column = 0)

        #------------------------------------------------
        #convert
        self.pix_frame = Frame(self.parent)
        self.pix_frame.grid(row = 2, column = 0)

        self.pixellabel = Label(self.pix_frame, text = '__________________')
        self.pixellabel.grid(row = 0, column = 1, columnspan = 4)
        add_red_btn = Button(self.pix_frame, text = 'Get_info', width=10 , command=lambda: self.about_img())
        add_red_btn.grid(row = 0, column = 0)
        return_btn = Button(self.pix_frame, text = 'RESET', width=10 , command=lambda: self.return_img())
        color_cube_btn = Button(self.pix_frame, text = 'Color_cube', width=10 , command=lambda: self.color_cube())
        mirrow_btn = Button(self.pix_frame, text = 'Mirrow', width=10 , command=lambda: self.miroow())
        noize_btn = Button(self.pix_frame, text = 'Noize', width=10 , command=lambda: self.noize())
        contrast_btn1 = Button(self.pix_frame, text = 'Contrast + ', width=10 , command=lambda: self.contrast(1))
        contrast_btn2 = Button(self.pix_frame, text = 'Contrast - ', width=10 , command=lambda: self.contrast(2))
        levels_btn = Button(self.pix_frame, text = 'levels', width=10 , command=lambda: self.levels())
        rainbow_btn = Button(self.pix_frame, text = 'rainbow', width=10 , command=lambda: self.rainbow())

        return_btn.grid(row = 1, column = 0)
        color_cube_btn.grid(row = 1, column = 1)
        mirrow_btn.grid(row = 1, column = 2)
        noize_btn.grid(row = 1, column = 3)
        contrast_btn1.grid(row = 0, column = 4)
        contrast_btn2.grid(row = 1, column = 4)
        levels_btn.grid(row = 0, column = 5)
        rainbow_btn.grid(row = 1, column = 5)
        #------------------------------------------------


def main():
    root = Tk()
    root.resizable(width=False, height=False)
    app = Program(root)
    root.mainloop()
    

if __name__ == '__main__':
    main()