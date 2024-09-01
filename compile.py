import os
import subprocess
import time

sys = os.system('ollama pull llama3.1')
time.sleep(0.5)
print('pull complite', sys)
process = subprocess.Popen(['ollama', 'serve'])
time.sleep(12)
print('ollama serve complite')
sys = os.system('ollama pull llama3.1')
time.sleep(0.5)
print('pull complite', sys)
