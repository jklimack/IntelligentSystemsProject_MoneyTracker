import os
import matplotlib
from tkinter import Tk, Button, LabelFrame, Entry, Label, StringVar, ttk, Radiobutton, LabelFrame, IntVar, Text
from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import pic_to_text as p2t
import text2obj as t2o
from classifier import Classifier




class UI:

    def __init__(self):
        """
        Initialization of the user interface. Creates the GUI window, and all of the
        associated widgets, and places them on the window. Finally, the main loop of
        application is begun at the end of the method.
        """
        # some important variables
        self.classifier = Classifier()
        self.use_ocr = False # whether to use OCR tool, or preprocessed text files
        self.chart_size = 350 # dimensions of the displayed charts
        self.r_img_width = 300 # width of displayed receipt image
        self.r_img_height = 500 # height of displayed receipt image
        self.data_file = "history.csv" # log file storing spending history
        matplotlib.use('Agg')

        # create GUI window
        self.window = Tk()
        self.window.title("Money Tracker")
        self.window.geometry("1500x600")

        # Get Receipt Image Name  -----------------------------------------
        # Information extraction panel. All widgets used for information extraction will
        # be added to this panel.
        self.extract_frame = LabelFrame(self.window, text="Product Extraction Information")
        self.extract_frame.grid(row=1, column=0)

        # simple label for user instruction
        #lbl_receipt_img = Label(self.extract_frame, text="Receipt Image")
        #lbl_receipt_img.grid(row=0, column=0)
        btn_select_img = Button(self.extract_frame, text="Select Image", command = lambda: self.load_img(tk.filedialog.askopenfilename()))
        btn_select_img.grid(row=0, column=0)

        # text box for user input
        var_txt_r_img = StringVar(None)
        self.txt_r_img = Entry(self.extract_frame, textvariable=var_txt_r_img, text="R. Image...", state='readonly')
        self.txt_r_img.grid(row=0, column=1)

        # Load receipt data  -----------------------------------------
        # button to load the receipt data
        btn_r_img = Button(self.extract_frame, text="Extract Products", command=lambda: self.extract_image_text(self.txt_r_img.get()))
        btn_r_img.grid(row=0, column=2)

        # receipt image display
        self.receipt_img = Label(self.extract_frame)
        self.receipt_img.grid(row=1, column=0, columnspan=3, rowspan=3)

        # Product Information display  -----------------------------------------
        # display product information column
        self.lbl = Label(self.extract_frame, text="Product Names:")
        self.lbl.grid(row=1, column=3)
        self.txt_product_info = Text(self.extract_frame, width=30, height=30)
        self.txt_product_info.grid(row=2, column=3)

        # display category information column
        self.lbl = Label(self.extract_frame, text="Categories:")
        self.lbl.grid(row=1, column=4)
        self.txt_cat_info = Text(self.extract_frame, width=20, height=30)
        self.txt_cat_info.grid(row=2, column=4)

        # display price information column
        self.lbl = Label(self.extract_frame, text="Prices:")
        self.lbl.grid(row=1, column=5)
        self.txt_price_info = Text(self.extract_frame, width=10, height=30)
        self.txt_price_info.grid(row=2, column=5)

        # Product Information display  -----------------------------------------
        # button to add info to history.csv
        btn_save = Button(self.extract_frame, text="Save to History",
                          command=lambda: self.save_history(self.txt_cat_info.get("1.0",END), self.txt_price_info.get("1.0",END)))
        btn_save.grid(row=0, column=3, columnspan=3)

        # Display Plots -----------------------------------------
        # new panel to houes the displayed charts
        self.display_frame = LabelFrame(self.window, text="Purchase History")
        self.display_frame.grid(row=1, column=1)

        # call function to display the current status of the charts
        self.display_history()

        # begin the applications main loop. When the window closes, the program stops.
        #self.window.mainloop()
        while True:
            try:
                Tk.update_idletasks(self.window)
                Tk.update(self.window)
            except:
                print("System exitting. ")
                exit(0)

    def load_img(self, filename):
        """
        Function used to load the selected image file, and display it to
        the screen.
        """
        if filename =="":
            self.display_error_msg(1)
            return
        try:
            # display image path
            self.txt_r_img.configure(state='normal')
            self.txt_r_img.delete(0, END)
            self.txt_r_img.insert(0, filename)
            self.txt_r_img.configure(state='readonly')
            # display the image to the UI
            self.r_img = ImageTk.PhotoImage(Image.open(filename).resize((self.r_img_width, self.r_img_height)))
            self.receipt_img.configure(image=self.r_img) # Label(self.extract_frame, image=self.r_img).grid(row=1, column=0, columnspan=3)
        except:
            self.display_error_msg(2, filename)

    def extract_image_text(self, filename):
        """
        Function to extract the text from the provided image, products and
        price, and classify the products into categories. The resulting
        product-category-price trios are displayed in columns.
        """
        # extract the text from the image
        try:
            if self.use_ocr:
                text = p2t.pic2text(filename)
            else:
                f = filename.split("/")[-1]
                f = "output/"+f+".txt"
                f = open(f, 'r', encoding='utf-8')
                text = f.read()
                f.close()
        except:
            self.display_error_msg(3, filename)
            return
        # extract the product information from the text
        try:
            receipt = t2o.text2object(text)
            products = receipt['PRODUCTS']
            prices = [str(x) for x in receipt['PRICES']]
        except:
            self.display_error_msg(4)
            return

        if len(products) == 0 or len(prices) == 0:
            self.display_error_msg(5)
            return

        # Product classification
        try:
            categories = self.classifier.classify(products)
        except:
            self.display_error_msg(6)
            return
        # display products, categories, and prices to the UI
        products = "\n\n".join(products)
        categories = "\n\n".join(categories)
        prices = "\n\n".join(prices)

        self.txt_product_info.delete('1.0', END)
        self.txt_product_info.insert(END, products)

        self.txt_cat_info.delete('1.0', END)
        self.txt_cat_info.insert(END, categories)

        self.txt_price_info.delete('1.0', END)
        self.txt_price_info.insert(END, prices)

    def display_history(self):
        """
        Function used to load the purchase history from the log
        file "self.data_file", and create both a bar chart, and
        a pie chart. The charts are saved in the "temp" directory,
        and then reloaded in order to display them to the screen.
        """
        # read the log file
        try:
            df = pd.read_csv(self.data_file)
        except:
            self.display_error_msg(7, self.data_file)
            return
        try:
            # extract the categories
            categories = df['Category']
            categories = np.unique(categories)
            # sum the total money spent on each category
            x = []
            for cat in categories:
                vals = df.loc[df['Category'] == cat]
                vals = vals['Price']
                p = np.sum(vals)
                x.append(p)
        except:
            self.display_error_msg(8, self.data_file)
            return
        try:
            # save bar chart
            plt.bar(categories, height=x)
            plt.title("Money Spent per Category")
            plt.xlabel("Product Category")
            plt.xticks(rotation=45)
            plt.ylabel("Money Spent")
            plt.savefig("temp/history_bar.png", bbox_inches='tight')
            plt.close()
            # save pie chart
            plt.title("Ratio of Money Spent per Category")
            plt.pie(x, labels=categories, autopct='%1.1f%%')
            plt.savefig("temp/history_pie.png", bbox_inches='tight')
            plt.close()
            # load and display bar chart
            self.img_bar = ImageTk.PhotoImage(Image.open("temp/history_bar.png").resize((self.chart_size, self.chart_size)))
            self.plot_img = Label(self.display_frame, image=self.img_bar).grid(row=0, column=0)
            # load and display pie chart
            self.img_pie = ImageTk.PhotoImage(Image.open("temp/history_pie.png").resize((self.chart_size, self.chart_size)))
            self.plot_img = Label(self.display_frame, image=self.img_pie).grid(row=0, column=1)
        except:
            self.display_error_msg(9)
            return

    def save_history(self, categories, prices):
        """
        Append the category and price information pairs to the
        log file. categories and prices are provided as input
        from the Text widgets of the GUI, and are string values.
        """
        categories = categories.split("\n")
        prices = prices.split("\n")
        txt = ""
        for i in range(len(categories)-1):
            if categories[i]=="" or prices[i]=="":
                pass
            else:
                p = str(prices[i])
                p.replace(",",".")
                try:
                    p = float(p)
                except ValueError:
                    self.display_error_msg(11, p)
                    return
                txt = txt+categories[i]+"," + str(p) + "\n"
        try:
            with open(self.data_file, "a") as f:
                f.write(txt)
                f.close()
        except:
            self.display_error_msg(10, self.data_file)
            return
        self.txt_product_info.delete('1.0', END)
        self.txt_cat_info.delete('1.0', END)
        self.txt_price_info.delete('1.0', END)
        self.display_history()

    def display_error_msg(self, e, info=None):
        standard_msg = "ERROR CODE {}: ".format(e)
        if e==1:
            msg = "No file has been selected."
        elif e==2:
            msg = "Could not load file '{}'.\n\nPlease ensure the file exists and is an image. ".format(info)
        elif e==3:
            msg = "Could not extract text from image '{}'. Please ensure the file exists, and is an " \
                                 "image. \n\nIf the problem continues please make sure that tesseract-ocr is properly " \
                                 "installed on your computer. It is recommended to use Linux OS. If you are using Linux" \
                                 ", then tesseract-ocr can be installed by the following command in the terminal:\n\n" \
                                 "sudo apt install tesseract-ocr\n\n".format(info)
        elif e==4:
            msg = "Reading product/price information from the extracted receipt failed."
        elif e==5:
            msg = "Insufficient product and/or price information found on the receipt image. "
        elif e==6:
            msg = "Product classification failed."
        elif e==7:
            msg = "Failed to read data file: '{}'. Please ensure the file exists, and is of type CSV.".format(info)
        elif e==8:
            msg = "Failed to read data file: '{}'. Ensure the contents of the CSV file contain only two columns: " \
                  "'Category' and 'Price'. Also check that there are only character [0-9] or '.' under the price" \
                  "column. ".format(info)
        elif e==9:
            msg = "Failed to plot spending history data. Ensure the 'temp' directory still exists. "
        elif e==10:
            msg = "Failed to write to data file '{}'. Enusure the file exists. ".format(info)
        elif e==11:
            msg = "Price {} is not a number. ".format(info)
        msg = standard_msg + msg
        self.txt_product_info.delete('1.0', END)
        self.txt_cat_info.delete('1.0', END)
        self.txt_price_info.delete('1.0', END)
        self.txt_product_info.insert(END, msg)

# main: initialize the GUI
ui = UI()