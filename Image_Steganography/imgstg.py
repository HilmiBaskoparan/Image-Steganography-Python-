
import sys
import imgstg_support
import image_Steganography
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True





def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    top = RunPage (root)
    imgstg_support.init(root, top)
    root.mainloop()

w = None
def create_RunPage(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = tk.Toplevel (root)
    top = RunPage (w)
    imgstg_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_RunPage():
    global w
    w.destroy()
    w = None

selectedImage = ""
selectedTextFile = ""

class RunPage:



    def encodeButton(self):
        if len(self.textentry.get(1.0,END)) > 1 and selectedTextFile != "":
            #print(len(self.textentry.get(1.0,END)))
            from tkinter import messagebox
            messagebox.showinfo("WARNING", "You can only encode one text at the same time !")
            return
        elif len(self.textentry.get(1.0,END)) == 1 and selectedTextFile == "" :
            from tkinter import messagebox
            messagebox.showinfo("WARNING", "Choose text file to be encoded !")
            return
        if len(self.textentry.get(1.0,END)) > 1:
            text = self.textentry.get(1.0,END)
            c = 1
        else:
            text = selectedTextFile
            c = 0
        if len(selectedImage)==0:
            from tkinter import messagebox
            messagebox.showinfo("WARNING", "Choose image !")
            return
        image_Steganography.encode(selectedImage,text,c)
        photo = Image.open(selectedImage.split(".")[0]+"_encoded."+selectedImage.split(".")[1])
        photo = photo.resize((260, 260), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(photo)
        self.embimg.config(image=photo)
        self.embimg.photo_ref = photo

    def openImagesButton(self):
        if len(selectedImage)==0:
            from tkinter import messagebox
            messagebox.showinfo("WARNING", "Choose image, then encode or decode a text from the image !")

        if selectedImage.__contains__("_encoded"):
            firstimage = selectedImage
            secondimage = selectedImage.split('.')[0]+'_decoded.'+selectedImage.split('.')[1]
        else:
            firstimage = selectedImage
            secondimage = selectedImage.split('.')[0]+'_encoded.'+selectedImage.split('.')[1]
        import subprocess, os
        if sys.platform.startswith('darwin'):
            subprocess.call(('open', firstimage))
            subprocess.call(('open', secondimage))
        elif os.name == 'nt':  # For Windows
            os.startfile(firstimage)
            os.startfile(secondimage)
        elif os.name == 'posix':  # For Linux, Mac, etc.
            subprocess.call(('xdg-open', firstimage))
            subprocess.call(('xdg-open', secondimage))


    def openRedPixelledImagesButton(self):
        if len(selectedImage)==0:
            from tkinter import messagebox
            messagebox.showinfo("WARNING", "Choose image, then encode or decode a text from the image !")

        if selectedImage.__contains__("_encoded"):
            secondimage = selectedImage.split('.')[0]+'_decoded_redpixelled.'+selectedImage.split('.')[1]
        else:
            secondimage = selectedImage.split('.')[0]+'_encoded_redpixelled.'+selectedImage.split('.')[1]
        import subprocess, os
        if sys.platform.startswith('darwin'):
            subprocess.call(('open', secondimage))
        elif os.name == 'nt':  # For Windows
            os.startfile(secondimage)
        elif os.name == 'posix':  # For Linux, Mac, etc.
            subprocess.call(('xdg-open', secondimage))


    def decodeButton(self):
        if len(selectedImage)==0:
            from tkinter import messagebox
            messagebox.showinfo("WARNING", "Choose image !")
            return
        data = image_Steganography.decode(selectedImage)
        photo = Image.open(selectedImage.split(".")[0] + "_decoded." + selectedImage.split(".")[1])
        photo = photo.resize((260, 260), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(photo)
        self.embimg.config(image=photo)
        self.embimg.photo_ref = photo
        self.decodedmsg.insert(1.0,data)


    def reset(self):
        global selectedImage
        global selectedTextFile
        self.textlink.configure(text="")
        self.imginfo.configure(text="")
        self.imglink.configure(text="")
        self.orimg.configure(image="")
        self.embimg.configure(image="")
        self.textentry.delete(1.0,END)
        self.decodedmsg.delete(1.0,END)
        selectedImage = ""
        selectedTextFile = ""




    def openImageFile(self):
        image = filedialog.askopenfile(filetypes=(("PNG-Files (*.png)", "*.png"), ("JPG Files (*.jpg)", "*.jpg")))
        global selectedImage
        selectedImage = image.name
        photo = Image.open(str(image.name))
        photo = photo.resize((260, 260), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(photo)
        self.orimg.config(image=photo)

        self.orimg.photo_ref = photo
        self.imglink.configure(text=image.name)

        image = Image.open(selectedImage, 'r')
        height, width = image.size
        pix = height * width
        imageinfo = "Image Format : " + str(image.format) + "\n\nImage Mode : "+ str(image.mode) + "\n\nImage Size : "+ str(image.size) + "\n\nImage Pixels : "+ str(pix)
        self.imginfo.configure(text=imageinfo)

    def openTextFile(self):
        global selectedTextFile
        text = filedialog.askopenfile(filetypes=(("TXT-Files(*.txt)", "*.txt"), ("All Files", "*.*")))
        self.textlink.configure(text=text.name)
        selectedTextFile = text.name




    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85' 
        _ana2color = '#ececec' # Closest X11 color: 'gray92' 
        font10 = "-family {Segoe UI} -size 10 -weight bold -slant "  \
            "roman -underline 0 -overstrike 0"
        font11 = "-family {Segoe UI} -size 9 -weight normal -slant "  \
            "italic -underline 0 -overstrike 0"
        font9 = "-family {Segoe UI} -size 12 -weight bold -slant roman"  \
            " -underline 0 -overstrike 0"
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("1109x657+31+84")
        top.title("Image Steganography")
        top.configure(background="#ffffff")
        top.configure(highlightcolor="#646464")

        self.imgslcbtn = tk.Button(top)
        self.imgslcbtn.place(relx=0.018, rely=0.061, height=24, width=147)
        self.imgslcbtn.configure(activebackground="#ececec")
        self.imgslcbtn.configure(activeforeground="#000000")
        self.imgslcbtn.configure(background="#eaeaea")
        self.imgslcbtn.configure(disabledforeground="#a3a3a3")
        self.imgslcbtn.configure(font=font10)
        self.imgslcbtn.configure(foreground="#000000")
        self.imgslcbtn.configure(highlightbackground="#d9d9d9")
        self.imgslcbtn.configure(highlightcolor="black")
        self.imgslcbtn.configure(pady="0")
        self.imgslcbtn.configure(text='''Select Image''')
        self.imgslcbtn.configure(width=147)
        self.imgslcbtn.configure(command=self.openImageFile)

        self.txtslcbtn = tk.Button(top)
        self.txtslcbtn.place(relx=0.018, rely=0.122, height=24, width=147)
        self.txtslcbtn.configure(activebackground="#ececec")
        self.txtslcbtn.configure(activeforeground="#000000")
        self.txtslcbtn.configure(background="#d9d9d9")
        self.txtslcbtn.configure(disabledforeground="#a3a3a3")
        self.txtslcbtn.configure(font=font10)
        self.txtslcbtn.configure(foreground="#000000")
        self.txtslcbtn.configure(highlightbackground="#d9d9d9")
        self.txtslcbtn.configure(highlightcolor="black")
        self.txtslcbtn.configure(pady="0")
        self.txtslcbtn.configure(text='''Select Text''')
        self.txtslcbtn.configure(width=147)
        self.txtslcbtn.configure(command=self.openTextFile)

        self.TSeparator1 = ttk.Separator(top)
        self.TSeparator1.place(relx=0.424, rely=0.0, relheight=0.944)
        self.TSeparator1.configure(orient="vertical")

        self.Label1 = tk.Label(top)
        self.Label1.place(relx=0.018, rely=0.183, height=21, width=144)
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(font=font10)
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(text='''Text a Message''')
        self.Label1.configure(width=144)

        self.Label2 = tk.Label(top)
        self.Label2.place(relx=0.018, rely=0.487, height=21, width=144)
        self.Label2.configure(background="#d9d9d9")
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(font=font10)
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(text='''Image Information''')
        self.Label2.configure(width=144)

        self.TSeparator2 = ttk.Separator(top)
        self.TSeparator2.place(relx=0.0, rely=0.441, relwidth=0.424)

        self.TSeparator3 = ttk.Separator(top)
        self.TSeparator3.place(relx=0.0, rely=0.7, relwidth=0.424)

        self.encodebtn = tk.Button(top)
        self.encodebtn.place(relx=0.027, rely=0.746, height=34, width=97)
        self.encodebtn.configure(activebackground="#ececec")
        self.encodebtn.configure(activeforeground="#000000")
        self.encodebtn.configure(background="#d9d9d9")
        self.encodebtn.configure(disabledforeground="#a3a3a3")
        self.encodebtn.configure(font=font10)
        self.encodebtn.configure(foreground="#000000")
        self.encodebtn.configure(highlightbackground="#d9d9d9")
        self.encodebtn.configure(highlightcolor="black")
        self.encodebtn.configure(pady="0")
        self.encodebtn.configure(text='''Encode''')
        self.encodebtn.configure(width=97)
        self.encodebtn.configure(command=self.encodeButton)

        self.decodebtn = tk.Button(top)
        self.decodebtn.place(relx=0.027, rely=0.852, height=34, width=97)
        self.decodebtn.configure(activebackground="#ececec")
        self.decodebtn.configure(activeforeground="#000000")
        self.decodebtn.configure(background="#d9d9d9")
        self.decodebtn.configure(disabledforeground="#a3a3a3")
        self.decodebtn.configure(font=font10)
        self.decodebtn.configure(foreground="#000000")
        self.decodebtn.configure(highlightbackground="#d9d9d9")
        self.decodebtn.configure(highlightcolor="black")
        self.decodebtn.configure(pady="0")
        self.decodebtn.configure(text='''Decode''')
        self.decodebtn.configure(width=97)
        self.decodebtn.configure(command=self.decodeButton)

        self.showimgbtn = tk.Button(top)
        self.showimgbtn.place(relx=0.153, rely=0.746, height=34, width=117)
        self.showimgbtn.configure(activebackground="#ececec")
        self.showimgbtn.configure(activeforeground="#000000")
        self.showimgbtn.configure(background="#d9d9d9")
        self.showimgbtn.configure(disabledforeground="#a3a3a3")
        self.showimgbtn.configure(font=font10)
        self.showimgbtn.configure(foreground="#000000")
        self.showimgbtn.configure(highlightbackground="#d9d9d9")
        self.showimgbtn.configure(highlightcolor="black")
        self.showimgbtn.configure(pady="0")
        self.showimgbtn.configure(text='''Show Images''')
        self.showimgbtn.configure(width=117)
        self.showimgbtn.configure(command=self.openImagesButton)

        self.exitbtn = tk.Button(top)
        self.exitbtn.place(relx=0.298, rely=0.852, height=34, width=97)
        self.exitbtn.configure(activebackground="#ececec")
        self.exitbtn.configure(activeforeground="#000000")
        self.exitbtn.configure(background="#d9d9d9")
        self.exitbtn.configure(disabledforeground="#a3a3a3")
        self.exitbtn.configure(font=font10)
        self.exitbtn.configure(foreground="#000000")
        self.exitbtn.configure(highlightbackground="#d9d9d9")
        self.exitbtn.configure(highlightcolor="black")
        self.exitbtn.configure(pady="0")
        self.exitbtn.configure(text='''Exit''')
        self.exitbtn.configure(width=97)
        self.exitbtn.configure(command=exit)

        self.embpxbtn = tk.Button(top)
        self.embpxbtn.place(relx=0.153, rely=0.852, height=34, width=117)
        self.embpxbtn.configure(activebackground="#ececec")
        self.embpxbtn.configure(activeforeground="#000000")
        self.embpxbtn.configure(background="#d9d9d9")
        self.embpxbtn.configure(disabledforeground="#a3a3a3")
        self.embpxbtn.configure(font=font10)
        self.embpxbtn.configure(foreground="#000000")
        self.embpxbtn.configure(highlightbackground="#d9d9d9")
        self.embpxbtn.configure(highlightcolor="black")
        self.embpxbtn.configure(pady="0")
        self.embpxbtn.configure(text='''Embedded Pixels''')
        self.embpxbtn.configure(width=117)
        self.embpxbtn.configure(command=self.openRedPixelledImagesButton)

        self.resetbtn = tk.Button(top)
        self.resetbtn.place(relx=0.298, rely=0.746, height=34, width=97)
        self.resetbtn.configure(activebackground="#ececec")
        self.resetbtn.configure(activeforeground="#000000")
        self.resetbtn.configure(background="#d9d9d9")
        self.resetbtn.configure(disabledforeground="#a3a3a3")
        self.resetbtn.configure(font=font10)
        self.resetbtn.configure(foreground="#000000")
        self.resetbtn.configure(highlightbackground="#d9d9d9")
        self.resetbtn.configure(highlightcolor="black")
        self.resetbtn.configure(pady="0")
        self.resetbtn.configure(text='''Reset''')
        self.resetbtn.configure(width=97)
        self.resetbtn.configure(command=self.reset)

        self.menubar = tk.Menu(top,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)

        self.Label5 = tk.Label(top)
        self.Label5.place(relx=0.487, rely=0.046, height=31, width=184)
        self.Label5.configure(background="#ffffff")
        self.Label5.configure(disabledforeground="#a3a3a3")
        self.Label5.configure(font=font9)
        self.Label5.configure(foreground="#000000")
        self.Label5.configure(text='''Original Image''')
        self.Label5.configure(width=184)

        self.Label5_3 = tk.Label(top)
        self.Label5_3.place(relx=0.775, rely=0.046, height=31, width=184)
        self.Label5_3.configure(activebackground="#f9f9f9")
        self.Label5_3.configure(activeforeground="black")
        self.Label5_3.configure(background="#ffffff")
        self.Label5_3.configure(disabledforeground="#a3a3a3")
        self.Label5_3.configure(font=font9)
        self.Label5_3.configure(foreground="#000000")
        self.Label5_3.configure(highlightbackground="#d9d9d9")
        self.Label5_3.configure(highlightcolor="black")
        self.Label5_3.configure(text='''Embedded Image''')

        self.TSeparator4 = ttk.Separator(top)
        self.TSeparator4.place(relx=0.424, rely=0.563, relwidth=0.577)

        self.Label5_4 = tk.Label(top)
        self.Label5_4.place(relx=0.631, rely=0.594, height=31, width=184)
        self.Label5_4.configure(activebackground="#f9f9f9")
        self.Label5_4.configure(activeforeground="black")
        self.Label5_4.configure(background="#ffffff")
        self.Label5_4.configure(disabledforeground="#a3a3a3")
        self.Label5_4.configure(font=font9)
        self.Label5_4.configure(foreground="#000000")
        self.Label5_4.configure(highlightbackground="#d9d9d9")
        self.Label5_4.configure(highlightcolor="black")
        self.Label5_4.configure(text='''Decoded Message''')

        self.imglink = tk.Label(top)
        self.imglink.place(relx=0.162, rely=0.061, height=21, width=254)
        self.imglink.configure(background="#ffffff")
        self.imglink.configure(disabledforeground="#a3a3a3")
        self.imglink.configure(font=font11)
        self.imglink.configure(foreground="#000000")
        self.imglink.configure(text='''Click button to select image''')
        self.imglink.configure(width=254)

        self.textlink = tk.Label(top)
        self.textlink.place(relx=0.162, rely=0.122, height=21, width=254)
        self.textlink.configure(activebackground="#f9f9f9")
        self.textlink.configure(activeforeground="black")
        self.textlink.configure(background="#ffffff")
        self.textlink.configure(disabledforeground="#a3a3a3")
        self.textlink.configure(font=font11)
        self.textlink.configure(foreground="#000000")
        self.textlink.configure(highlightbackground="#d9d9d9")
        self.textlink.configure(highlightcolor="black")
        self.textlink.configure(text='''Click button to select text''')
        self.textlink.configure(width=254)

        self.imginfo = tk.Label(top)
        self.imginfo.place(relx=0.162, rely=0.487, height=111, width=254)
        self.imginfo.configure(background="#f2f2f2")
        self.imginfo.configure(disabledforeground="#a3a3a3")
        self.imginfo.configure(foreground="#000000")
        self.imginfo.configure(width=254)

        self.decodedmsg = tk.Text(top)
        self.decodedmsg.place(relx=0.46, rely=0.654, height=171, width=564)
        self.decodedmsg.configure(background="#f2f2f2")
        #self.decodedmsg.configure(disabledforeground="#a3a3a3")
        #self.decodedmsg.configure(foreground="#000000")
        self.decodedmsg.configure(width=564)

        self.textentry = tk.Text(top)
        self.textentry.place(relx=0.162, rely=0.183,height=140, relwidth=0.229)
        self.textentry.configure(background="#f2f2f2")
        #self.textentry.configure(disabledforeground="#a3a3a3")
        self.textentry.configure(font="TkFixedFont")
        #self.textentry.configure(foreground="#000000")
        self.textentry.configure(insertbackground="black")
        self.textentry.configure(width=254)

        self.orimg = tk.Label(top)
        self.orimg.place(relx=0.46, rely=0.122, height=260, width=260)
        self.orimg.configure(background="#ffffff")
        self.orimg.configure(disabledforeground="#a3a3a3")
        self.orimg.configure(foreground="#000000")

        self.embimg = tk.Label(top)
        self.embimg.place(relx=0.721, rely=0.122, height=260, width=260)
        self.embimg.configure(activebackground="#f9f9f9")
        self.embimg.configure(activeforeground="black")
        self.embimg.configure(background="#ffffff")
        self.embimg.configure(disabledforeground="#a3a3a3")
        self.embimg.configure(foreground="#000000")
        self.embimg.configure(highlightbackground="#d9d9d9")
        self.embimg.configure(highlightcolor="black")

if __name__ == '__main__':
    vp_start_gui()





