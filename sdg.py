import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests
API_KEY = "a7c0428c6217d28fb21b3e035fcf40f3"
def fetch_forecast(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}"
        response = requests.get(url)
        data = response.json()
        forecast_data = {}
        if 'list' in data:
            for entry in data['list']:
                date = entry['dt_txt']
                temperature_kelvin = entry['main']['temp']
                temperature_celsius = temperature_kelvin - 273.15
                forecast_data[date] = temperature_celsius
                if len(forecast_data) == 5:  
                    break
        return forecast_data
    except Exception as e:
        print("Error fetching forecast data:", e)
        return None
def generate_uhi_data(city, temperatures):
    urban_temperature = temperatures[0] + random.uniform(-2, 2)  
    rural_temperature = temperatures[1] - random.uniform(2, 4)  
    uhi_effect = urban_temperature - rural_temperature
    uhi_info = {
        "city": city,
        "urban_temperature": urban_temperature,
        "rural_temperature": rural_temperature,
        "uhi_effect": uhi_effect
    }
    return uhi_info
def generate_uv_data():
    return [random.uniform(0, 1) for _ in range(10)] 
def update_uhi_monitor():
    city = city_entry.get()
    if city:
        forecast_data = fetch_forecast(city)
        if forecast_data:
            temperatures = list(forecast_data.values())
            uhi_info = generate_uhi_data(city, temperatures)
            display_uhi_info(uhi_info)
            plot_pie_chart(uhi_info['urban_temperature'], uhi_info['rural_temperature'])  
            plot_spectrum_lines() 
            plot_uv_graph()  
            plot_ecg_graph() 
            display_forecast(forecast_data) 
            display_prevention_points(uhi_info['uhi_effect']) 
        else:
            messagebox.showerror("Error", "Failed to fetch forecast data.")
    else:
        messagebox.showerror("Error", "Please enter a city.")
def display_uhi_info(uhi_info):
    result_text = f"Urban Heat Island Monitor for {uhi_info['city']}:\n"
    result_text += f"Urban Area Temperature: {uhi_info['urban_temperature']}°C\n"
    result_text += f"Rural Area Temperature: {uhi_info['rural_temperature']}°C\n"
    result_text += f"UHI Effect: {uhi_info['uhi_effect']}°C\n"
    result_label.config(text=result_text, font=('Helvetica', 14, 'bold'), fg='blue')
def plot_pie_chart(urban_temp, rural_temp):
    labels = ['Urban', 'Rural']
    sizes = [urban_temp, rural_temp]
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.set_title('Temperature Distribution:', fontsize=14, fontweight='bold', color='green')
    plt.close(fig)
    canvas = FigureCanvasTkAgg(fig, master=pie_chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()
def plot_spectrum_lines():
    wavelengths = ['Gamma', 'X-ray', 'Ultraviolet', 'Visible', 'Infrared']
    intensities = [random.uniform(0, 1) for _ in range(len(wavelengths))] 
    colors = ['blue', 'orange', 'pink', 'green', 'red'] 
    fig, ax = plt.subplots()
    bars = ax.bar(wavelengths, intensities, color=colors)
    ax.set_title('Electromagnetic Spectrum', fontsize=14, fontweight='bold', color='orange')
    ax.set_ylabel('Intensity', fontsize=12)   
    def update_spectrum_lines():
        nonlocal intensities, bars
        intensities = [random.uniform(0, 1) for _ in range(len(wavelengths))]  
        for bar, intensity in zip(bars, intensities):
            bar.set_height(intensity)
        fig.canvas.draw()
        root.after(2000, update_spectrum_lines)    
    update_spectrum_lines()
    canvas = FigureCanvasTkAgg(fig, master=spectrum_plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()
def plot_uv_graph():
    uv_data = generate_uv_data()
    fig, ax = plt.subplots()
    line, = ax.plot(range(10), uv_data, color='purple')
    ax.set_title('UV Rays', fontsize=14, fontweight='bold', color='red')
    ax.set_xlabel('Time', fontsize=12)
    ax.set_ylabel('Intensity', fontsize=12)
    def update_uv_graph():
        nonlocal uv_data, line
        uv_data[:-1] = uv_data[1:]  
        uv_data[-1] = random.uniform(0, 1)  
        line.set_ydata(uv_data)
        fig.canvas.draw()
        ax.set_ylim(0, 1)  
        root.after(1000, update_uv_graph) 
    update_uv_graph()
    canvas = FigureCanvasTkAgg(fig, master=uv_plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()
def plot_ecg_graph():
    x = np.linspace(0, 10, 100)
    y = np.random.rand(100)  
    fig, ax = plt.subplots()
    line, = ax.plot(x, y, color='red')
    ax.set_title('Green House Effect', fontsize=14, fontweight='bold', color='purple')
    ax.set_xlabel('Time', fontsize=12)
    ax.set_ylabel('Effort Level', fontsize=12)
    def update_ecg_graph():
        nonlocal x, y, line
        y[:-1] = y[1:]
        y[-1] = np.random.rand()  # Modify this line
        line.set_ydata(y)
        fig.canvas.draw()
        ax.set_ylim(0, 1)
        ax.set_xlim(x[0], x[-1] + 1)
        root.after(100, update_ecg_graph)
    update_ecg_graph()
    canvas = FigureCanvasTkAgg(fig, master=ecg_plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()
def display_forecast(forecast_data):
    forecast_text = "Weather Forecast:\n"
    colors = ['darkgreen', 'blue', 'red', 'purple', 'orange']  
    for i, (date, temperature) in enumerate(forecast_data.items()):
        color = colors[i] if i < len(colors) else 'black'
        forecast_text += f"{date}: {temperature}°C\n"
        label = tk.Label(forecast_frame, text=f"{date}: {temperature}°C", font=('Helvetica', 12), fg=color)
        label.pack()

def display_prevention_points(uhi_effect):
    for widget in prevention_frame.winfo_children():
        widget.destroy()
    if uhi_effect > 1:  
        prevention_points = [
            "Enhance urban planning strategies",
            "Install green roofs",
            "Create water bodies",
            "Increase green spaces (trees, parks)",
            "Promote reflective pavements", 
            "Utilize heat-resistant materials for buildings",
            "Implement cool roofs"           
        ]
    elif uhi_effect > 0: 
        prevention_points = [
            
            "Promote reflective pavements",
            "Enhance urban planning strategies",
            "Install green roofs",
            "Increase green spaces (trees, parks)",
            "Implement cool roofs",
        ]
    else: 
        prevention_points = [
            "Increase green spaces (trees, parks)",
            "Implement cool roofs"
        ]
    title_label = tk.Label(prevention_frame, text="Prevention Ways", font=('Helvetica', 14, 'bold') ,fg='red' )
    title_label.pack(anchor="w")
    for i, point in enumerate(prevention_points, start=1):
        label = tk.Label(prevention_frame, text=f"{i}. {point}", font=('Helvetica', 12), fg='darkblue')
        label.pack(anchor="w")
root = tk.Tk()
root.title("Urban Heat Island Monitor")
root.geometry("800x600")  
for i in range(6):
    root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=1)
result_label = tk.Label(root, text="", font=('Helvetica', 14))
result_label.grid(row=0, column=0, columnspan=6, sticky="nsew")
search_frame = tk.Frame(root)
search_frame.grid(row=1, column=0, columnspan=6, sticky="nsew")
city_entry = tk.Entry(search_frame, width=30, font=('Helvetica', 12))  
city_entry.grid(row=0, column=0, padx=5)
update_button = tk.Button(search_frame, text="Update", command=update_uhi_monitor, font=('Helvetica', 12))
update_button.grid(row=0, column=1, padx=5)
uv_plot_frame = tk.Frame(root)
uv_plot_frame.grid(row=2, column=0, sticky="nsew")
pie_chart_frame = tk.Frame(root)
pie_chart_frame.grid(row=2, column=1, sticky="nsew")
spectrum_plot_frame = tk.Frame(root)
spectrum_plot_frame.grid(row=2, column=2, sticky="nsew")
ecg_plot_frame = tk.Frame(root)
ecg_plot_frame.grid(row=2, column=3, sticky="nsew") 
forecast_frame = tk.Frame(root)
forecast_frame.grid(row=3, column=0, columnspan=4, sticky="nsew")
prevention_frame = tk.Frame(root)
prevention_frame.grid(row=4, column=0, columnspan=4, sticky="nsew")
forecast_label = tk.Label(forecast_frame, text="", font=('Helvetica', 12))
forecast_label.pack()
root.mainloop()
