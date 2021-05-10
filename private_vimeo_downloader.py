import requests, webbrowser
import PySimpleGUI as sg
import tkinter as tk
import time
from tkinter import filedialog

def get_links(text):
    text = text.split('"')
    links = [x for x in text if x.find('https://vod-progressive.akamaized.net') != -1]
    return links

def download(url, save_path):
    if not validate_save_path(save_path):
        raise ValueError("The specified save path is not valid")
    try:
        response = requests.get(url, stream=True)
        download_window_layout = [  [sg.Text("Downloading Progress:")], 
                                    [sg.ProgressBar(int(response.headers['Content-Length']) / 1024, orientation='h', size=(20, 20), key='progressbar')], 
                                    [sg.Cancel()]]
        download_window = sg.Window("Downloading", download_window_layout)
        download_window.read()
        progressbar = download_window['progressbar']
        indexer = 0
        with open(save_path, 'wb+') as mp4_file:    
            for chunk in response.iter_content(1024):
                mp4_file.write(chunk)
                progressbar.update_bar(indexer)
                indexer += 1
        download_window.close()
        sg.PopupQuickMessage("Downloaded!", title="Success")
   
    except:
        print("Error while trying to get the mp4 file")
        exit()
        
def validate_save_path(save_path):
    if type(save_path) != str:
        return False
    
    save_path = save_path.lower()

    if not save_path.endswith("mp4"):
        return False
    if save_path.find("/") != -1:
        save_path = [x for x in save_path.split("/") if x == ""]
    else:
        save_path = [x for x in save_path.split("\\") if x == ""]

    if len(save_path) != 0:
        return False

    return True

def select_link(links):
    if type(links) != list and type(links) != tuple:
        raise TypeError("select_link parmeter is list or tuple only")
    
    download_link = ""
    content_length = 0
    for link in links:
        try:
            res = requests.head(link)
        except:
            print("You are here")
        
        if content_length < int(res.headers['Content-Length']):  
            content_length = int(res.headers['Content-Length'])
            download_link = link   

    return download_link

def replace_video_in_video_viewer(video_viewer_path, mp4_path):
    try:
        with open(r"C:\Users\motig\OneDrive\ראשי\ג. מחשבים\Laboratory\Projects\ShowLecture\template.html", 'r', encoding="utf-8") as f:
            template = f.read()
        
        new_html = template.replace("{$!video!$}", mp4_path).replace("{$!title!$}", "Lecture Viewer")
        with open(video_viewer_path, 'w', encoding="utf-8") as f:
            f.write(new_html) 

    except:
        print("Failed opening video viewer")
        exit()

def main():
    lecture_viewer_path = "C:/users/motig/desktop/showlecture/video.html"
    layout = [  [sg.Text("Enter root path")],
                [sg.Input(),sg.FileBrowse()],
                [sg.Text("Enter save path")],
                [sg.Input(),sg.FolderBrowse()],
                [sg.Text("Enter new file name:")],
                [sg.Input(),sg.Text(".mp4")],
                [sg.Button("Ok")]                
            ]

    window = sg.Window("Download vimeo mp4", layout)

    while True:
        event, values = window.read()
        if '' in values:
            print(sg.Popup("Error","Not all the fields are filled."))
        else:
            break

    raw_file = values[0]
    save_folder = values[1]
    file_name = values[2] + ".mp4"
    save_path = save_folder + "\\" + file_name
    window.close()
    try:
        with open(raw_file, 'r', encoding="utf-8") as f:
            raw_vimeo_file = f.read()     
    except FileNotFoundError:
        sg.PopupQuickMessage("Error", "Can't open this file, try another file.", button_type=sg.POPUP_BUTTONS_ERROR) 
    else:
        download(select_link(get_links(raw_vimeo_file)), save_path)
        replace_video_in_video_viewer(lecture_viewer_path, save_path)
        webbrowser.open(lecture_viewer_path)

        

    
if __name__ == "__main__":
    main()