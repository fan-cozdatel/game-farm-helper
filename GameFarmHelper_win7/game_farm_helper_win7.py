import os
import sys
import time
import ctypes
import subprocess
from datetime import datetime

class GameFarmHelperWin7:
    def __init__(self):
        self.user32 = ctypes.windll.user32
        self.is_farming = False
        self.monitor_on = True
        self.last_cursor_pos = None
        self.last_activity_time = time.time()
        self.nircmd_path = self._find_nircmd()
    
    def _find_nircmd(self):
        """Поиск NirCmd в папке с программой"""
        # Проверяем в текущей папке
        if os.path.exists("nircmd.exe"):
            return os.path.abspath("nircmd.exe")
        
        # Проверяем в подпапке
        if os.path.exists("nircmd/nircmd.exe"):
            return os.path.abspath("nircmd/nircmd.exe")
        
        # Проверяем в System32
        if os.path.exists(r"C:\Windows\System32\nircmd.exe"):
            return r"C:\Windows\System32\nircmd.exe"
        
        # Проверяем в Windows
        if os.path.exists(r"C:\Windows\nircmd.exe"):
            return r"C:\Windows\nircmd.exe"
        
        return None
    
    def turn_off_monitor(self):
        """Выключение монитора (Win7)"""
        # Метод 1: Через SendMessage
        try:
            self.user32.SendMessageW(0xFFFF, 0x0112, 0xF170, 2)
            self.monitor_on = False
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Монитор выключен")
            return True
        except:
            pass
        
        # Метод 2: Через NirCmd
        if self.nircmd_path:
            try:
                subprocess.run([self.nircmd_path, "monitor", "off"], 
                             capture_output=True, timeout=5)
                self.monitor_on = False
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Монитор выключен (NirCmd)")
                return True
            except:
                pass
        
        # Метод 3: Через powercfg
        try:
            subprocess.run(["powercfg", "/change", "monitor-timeout-ac", "1"], 
                         capture_output=True, timeout=5)
            time.sleep(60)  # Ждем 1 минуту
            self.monitor_on = False
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Монитор выключен (powercfg)")
            return True
        except:
            pass
        
        print("Не удалось выключить монитор!")
        return False
    
    def turn_on_monitor(self):
        """Включение монитора"""
        try:
            # Имитация движения мыши через ctypes
            ctypes.windll.user32.mouse_event(1, 1, 1, 0, 0)
            time.sleep(0.1)
            ctypes.windll.user32.mouse_event(1, -1, -1, 0, 0)
            self.monitor_on = True
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Монитор включен")
            return True
        except:
            # Через NirCmd
            if self.nircmd_path:
                try:
                    subprocess.run([self.nircmd_path, "monitor", "on"], 
                                 capture_output=True, timeout=5)
                    self.monitor_on = True
                    return True
                except:
                    pass
        return False
    
    def check_user_activity(self):
        """Проверка активности пользователя (Win7)"""
        try:
            # Структура POINT для GetCursorPos
            class POINT(ctypes.Structure):
                _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]
            
            pt = POINT()
            ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
            cursor_pos = (pt.x, pt.y)
            
            # Проверяем нажатия клавиш
            for key_code in range(1, 254):
                if ctypes.windll.user32.GetAsyncKeyState(key_code) & 0x8000:
                    return True
            
            # Проверяем движение мыши
            if self.last_cursor_pos is not None:
                if cursor_pos != self.last_cursor_pos:
                    self.last_cursor_pos = cursor_pos
                    return True
            else:
                self.last_cursor_pos = cursor_pos
        except:
            pass
        
        return False
    
    def get_windows_version(self):
        """Получение версии Windows"""
        try:
            version = sys.getwindowsversion()
            if version.major == 6 and version.minor == 1:
                return f"Windows 7 (Build {version.build})"
            elif version.major == 6 and version.minor == 0:
                return f"Windows Vista (Build {version.build})"
            elif version.major == 10:
                if version.build >= 22000:
                    return f"Windows 11 (Build {version.build})"
                else:
                    return f"Windows 10 (Build {version.build})"
            else:
                return f"Windows {version.major}.{version.minor}"
        except:
            return "Windows (неопределенная версия)"
    
    def show_system_info(self):
        """Показать информацию о системе"""
        print("\n" + "=" * 50)
        print("ИНФОРМАЦИЯ О СИСТЕМЕ")
        print("=" * 50)
        
        print(f"ОС: {self.get_windows_version()}")
        
        # Процессор
        try:
            import platform
            processor = platform.processor()
            if processor:
                print(f"Процессор: {processor}")
        except:
            pass
        
        # Оперативная память
        try:
            import ctypes.wintypes
            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]
            
            memory_status = MEMORYSTATUSEX()
            memory_status.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memory_status))
            
            total_ram_gb = memory_status.ullTotalPhys / (1024**3)
            print(f"Оперативная память: {total_ram_gb:.1f} GB")
        except:
            pass
        
        # Видеокарта через WMI
        try:
            import wmi
            c = wmi.WMI()
            for gpu in c.Win32_VideoController():
                print(f"Видеокарта: {gpu.Name}")
                break
        except:
            try:
                # Через реестр
                import _winreg
                key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 
                                     r"SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}\0000")
                gpu_name = _winreg.QueryValueEx(key, "DriverDesc")[0]
                _winreg.CloseKey(key)
                print(f"Видеокарта: {gpu_name}")
            except:
                print("Видеокарта: не удалось определить")
        
        # NirCmd
        if self.nircmd_path:
            print(f"NirCmd: Установлен ({self.nircmd_path})")
        else:
            print("NirCmd: Не найден (рекомендуется установить)")
            print("Скачать: http://www.nirsoft.net/utils/nircmd.html")
    
    def start_farming_mode(self, monitor_timeout=10):
        """Запуск режима фарма"""
        print("\n" + "=" * 50)
        print("РЕЖИМ ФАРМА АКТИВИРОВАН")
        print("=" * 50)
        print(f"Монитор выключится через {monitor_timeout} сек. бездействия")
        print(f"Для выхода нажмите Ctrl+C")
        print("=" * 50 + "\n")
        
        self.monitor_timeout = monitor_timeout
        self.is_farming = True
        self.last_activity_time = time.time()
        last_status_time = 0
        
        try:
            while self.is_farming:
                current_time = time.time()
                
                if self.check_user_activity():
                    self.last_activity_time = current_time
                    if not self.monitor_on:
                        self.turn_on_monitor()
                else:
                    if self.monitor_on and current_time - self.last_activity_time > monitor_timeout:
                        self.turn_off_monitor()
                
                # Показываем статус каждые 5 секунд
                if current_time - last_status_time > 5:
                    if self.monitor_on:
                        remaining = monitor_timeout - int(current_time - self.last_activity_time)
                        if remaining > 0:
                            status = f"Монитор выключится через {remaining} сек."
                        else:
                            status = "Выключение..."
                    else:
                        status = "Монитор выключен (игра работает)"
                    
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] {status}")
                    last_status_time = current_time
                
                time.sleep(0.5)
                
        except KeyboardInterrupt:
            print("\n" + "=" * 50)
            print("ВЫХОД ИЗ РЕЖИМА ФАРМА")
            print("=" * 50)
            self.stop_farming_mode()
    
    def stop_farming_mode(self):
        """Остановка режима фарма"""
        self.is_farming = False
        
        if not self.monitor_on:
            self.turn_on_monitor()
        
        print("Режим фарма остановлен")

def main():
    print("=" * 50)
    print("GAME FARM HELPER Win7")
    print("=" * 50)
    
    helper = GameFarmHelperWin7()
    
    while True:
        print("\n" + "=" * 50)
        print("МЕНЮ:")
        print("=" * 50)
        print("1. Запустить фарм (монитор выключится через 10 сек)")
        print("2. Запустить фарм (монитор выключится через 30 сек)")
        print("3. Запустить фарм (своё время выключения монитора)")
        print("4. Тест: выключить монитор")
        print("5. Информация о системе")
        print("6. Выход")
        print("=" * 50)
        
        choice = input("\nВыберите действие (1-6): ").strip()
        
        if choice == "1":
            print("\nЗапуск режима фарма...")
            print("Монитор выключится через 10 секунд бездействия")
            helper.start_farming_mode(monitor_timeout=10)
            
        elif choice == "2":
            print("\nЗапуск режима фарма...")
            print("Монитор выключится через 30 секунд бездействия")
            helper.start_farming_mode(monitor_timeout=30)
            
        elif choice == "3":
            try:
                print("\nНАСТРОЙКА ВРЕМЕНИ ВЫКЛЮЧЕНИЯ МОНИТОРА")
                print("-" * 40)
                timeout = int(input("Через сколько секунд бездействия выключить монитор? (5-600): "))
                timeout = max(5, min(timeout, 600))
                print(f"\nМонитор выключится через {timeout} секунд бездействия")
                helper.start_farming_mode(monitor_timeout=timeout)
            except ValueError:
                print("Ошибка: введите числовое значение!")
                
        elif choice == "4":
            print("\nВыключение монитора через 3 секунды...")
            for i in range(3, 0, -1):
                print(f"   {i}...")
                time.sleep(1)
            helper.turn_off_monitor()
            print("\nПодвигайте мышкой, чтобы включить монитор")
            
        elif choice == "5":
            helper.show_system_info()
            
        elif choice == "6":
            print("\nДо свидания!")
            break
            
        else:
            print("Неверный выбор!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nПрограмма остановлена пользователем")
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        input("Нажмите Enter для выхода...")