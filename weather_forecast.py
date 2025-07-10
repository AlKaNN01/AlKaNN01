import tkinter as tk
from tkinter import messagebox
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from collections import defaultdict

API_KEY = "21***512bc99****2b91****580fb"
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"

def get_forecast():
    city = city_entry.get()
    if city == "":
        messagebox.showwarning("Uyarı", "Lütfen bir şehir adı girin!")
        return

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "tr"
    }

    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        city_name = data["city"]["name"]

        daily_temps = defaultdict(list)

        for item in data["list"]:
            date_str = item["dt_txt"].split(" ")[0]  # sadece gün
            temp = item["main"]["temp"]
            daily_temps[date_str].append(temp)

        avg_temps = {date: sum(temps)/len(temps) for date, temps in daily_temps.items()}
        draw_chart(avg_temps)
        result_label.config(text=f"{city_name} için 5 günlük sıcaklık tahmini:")
    else:
        messagebox.showerror("Hata", "Veri alınamadı. Şehir adını kontrol edin.")

def draw_chart(avg_temps):
    for widget in chart_frame.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(5, 3.5), dpi=100)
    dates = list(avg_temps.keys())[:5]
    temps = [avg_temps[date] for date in dates]

    ax.plot(dates, temps, marker='o', color='tomato', linewidth=2)
    ax.set_title("5 Günlük Ortalama Sıcaklık Tahmini (°C)")
    ax.set_ylabel("Sıcaklık (°C)")
    ax.grid(True)

    chart = FigureCanvasTkAgg(fig, master=chart_frame)
    chart.draw()
    chart.get_tk_widget().pack()

# Arayüz
root = tk.Tk()
root.title("5 Günlük Hava Tahmini")
root.geometry("500x500")
root.resizable(False, False)

city_entry = tk.Entry(root, font=("Arial", 14))
city_entry.pack(pady=15)
city_entry.insert(0, "Istanbul")

get_btn = tk.Button(root, text="5 Günlük Tahmini Getir", command=get_forecast, font=("Arial", 12))
get_btn.pack(pady=5)

result_label = tk.Label(root, text="", font=("Arial", 12), wraplength=450, justify="center")
result_label.pack(pady=10)

chart_frame = tk.Frame(root)
chart_frame.pack(pady=10)

root.mainloop()
