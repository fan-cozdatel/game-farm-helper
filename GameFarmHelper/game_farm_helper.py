import os
import sys
import time
import ctypes
import subprocess
import platform
from datetime import datetime

try:
    import win32gui
    import win32con
    import win32api
except ImportError:
    print("Ошибка: pywin32 не установлен!")
    print("Выполните: pip install pywin32")
    input("Нажмите Enter для выхода...")
    sys.exit(1)

try:
    import psutil
except ImportError:
    print("Ошибка: psutil не установлен!")
    print("Выполните: pip install psutil")
    input("Нажмите Enter для выхода...")
    sys.exit(1)

class GameFarmHelper:
    def __init__(self):
        self.user32 = ctypes.windll.user32
        self.is_farming = False
        self.monitor_on = True
        self.last_cursor_pos = None
        self.last_activity_time = time.time()
    
    def get_windows_version(self):
        """Получение правильной версии Windows"""
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
            
            product_name = winreg.QueryValueEx(key, "ProductName")[0]
            display_version = winreg.QueryValueEx(key, "DisplayVersion")[0]
            current_build = winreg.QueryValueEx(key, "CurrentBuild")[0]
            
            winreg.CloseKey(key)
            
            # Исправляем определение Windows 11
            build_number = int(current_build)
            if build_number >= 22000:
                # Это Windows 11
                if "Home" in product_name:
                    return f"Windows 11 Home {display_version} (Build {current_build})"
                elif "Pro" in product_name:
                    return f"Windows 11 Pro {display_version} (Build {current_build})"
                else:
                    return f"Windows 11 {display_version} (Build {current_build})"
            else:
                # Это Windows 10
                return f"{product_name} {display_version} (Build {current_build})"
        except:
            # Запасной вариант
            version = sys.getwindowsversion()
            if version.build >= 22000:
                return f"Windows 11 (Build {version.build})"
            else:
                return f"Windows 10 (Build {version.build})"
    
    def turn_off_monitor(self):
        """Выключение монитора"""
        try:
            self.user32.SendMessageW(0xFFFF, 0x0112, 0xF170, 2)
            self.monitor_on = False
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Монитор выключен")
            return True
        except Exception as e:
            print(f"Ошибка выключения монитора: {e}")
            return False
    
    def turn_on_monitor(self):
        """Включение монитора"""
        try:
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 1, 1, 0, 0)
            time.sleep(0.1)
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, -1, -1, 0, 0)
            self.monitor_on = True
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Монитор включен")
            return True
        except Exception as e:
            print(f"Ошибка включения монитора: {e}")
            return False
    
    def check_user_activity(self):
        """Проверка активности пользователя"""
        try:
            cursor_pos = win32api.GetCursorPos()
            
            for key_code in range(1, 254):
                if win32api.GetAsyncKeyState(key_code) & 0x8000:
                    return True
            
            if self.last_cursor_pos is not None:
                if cursor_pos != self.last_cursor_pos:
                    self.last_cursor_pos = cursor_pos
                    return True
            else:
                self.last_cursor_pos = cursor_pos
        except:
            pass
        
        return False
    
    def disable_screensaver(self):
        """Отключение скринсейвера"""
        try:
            self.user32.SystemParametersInfoW(17, 0, None, 0)
            print("Скринсейвер отключен")
            return True
        except:
            return False
    
    def set_monitor_timeout(self, seconds=30):
        """Установка таймаута монитора в секундах"""
        try:
            minutes = max(1, seconds // 60)
            
            subprocess.run(["powercfg", "/change", "monitor-timeout-ac", str(minutes)], 
                         capture_output=True, timeout=5)
            subprocess.run(["powercfg", "/change", "monitor-timeout-dc", str(minutes)], 
                         capture_output=True, timeout=5)
            print(f"Таймаут монитора: {seconds} секунд")
            return True
        except:
            return False
    
    def show_system_info(self):
        """Показать информацию о системе"""
        print("\n" + "=" * 50)
        print("ИНФОРМАЦИЯ О СИСТЕМЕ")
        print("=" * 50)
        
        # Правильная версия Windows
        windows_version = self.get_windows_version()
        print(f"ОС: {windows_version}")
        
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
            total_ram = psutil.virtual_memory().total / (1024**3)
            print(f"Оперативная память: {total_ram:.1f} GB")
        except:
            pass
        
        # Видеокарта
        try:
            import wmi
            c = wmi.WMI()
            for gpu in c.Win32_VideoController():
                print(f"Видеокарта: {gpu.Name}")
                if hasattr(gpu, 'AdapterRAM') and gpu.AdapterRAM:
                    vram = int(gpu.AdapterRAM) / (1024**3)
                    if vram > 0:
                        print(f"Видеопамять: {vram:.1f} GB")
                break
        except:
            try:
                result = subprocess.run(['nvidia-smi', '--query-gpu=name', '--format=csv,noheader'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    gpu_name = result.stdout.strip()
                    print(f"Видеокарта: {gpu_name}")
            except:
                print("Видеокарта: не удалось определить")
        
        # Права администратора
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        print(f"Права администратора: {'Да' if is_admin else 'Нет'}")
    
    def start_farming_mode(self, monitor_timeout=10):
        """Запуск режима фарма"""
        print("\n" + "=" * 50)
        print("РЕЖИМ ФАРМА АКТИВИРОВАН")
        print("=" * 50)
        print(f"Монитор выключится через {monitor_timeout} сек. бездействия")
        print(f"Для выхода нажмите Ctrl+C")
        print("=" * 50 + "\n")
        
        self.monitor_timeout = monitor_timeout
        
        # Применяем настройки
        print("Применение настроек...")
        self.disable_screensaver()
        self.set_monitor_timeout(monitor_timeout)
        
        print("Настройки применены")
        print("Не трогайте мышь и клавиатуру!\n")
        
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
        
        print("Восстановление таймаута монитора...")
        self.set_monitor_timeout(600)  # 10 минут
        
        print("Режим фарма остановлен")
        print("Настройки восстановлены")

def main():
    print("=" * 50)
    print("GAME FARM HELPER v5.0")
    print("=" * 50)
    
    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    if not is_admin:
        print("\nВНИМАНИЕ: Программа запущена без прав администратора!")
        print("Некоторые функции могут не работать.")
        print("Рекомендуется перезапустить от имени администратора.\n")
    
    helper = GameFarmHelper()
    
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