import psutil, os
cpu = psutil.cpu_percent(1)
print("CPU Usage:", cpu, '%')
memorykb = psutil.virtual_memory()[3]
memorygb = (((memorykb/1024)/1024)/1024)
print('Memory Usage:', "%.2f" %memorygb, 'GB')