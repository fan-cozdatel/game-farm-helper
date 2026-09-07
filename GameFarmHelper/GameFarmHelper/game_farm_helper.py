import os
import sys
import time
import ctypes
import subprocess
import platform
import json
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
        
        # Загрузка конфигурации
        self.config = self._load_config()
        
        # Поиск программ для подсветки
        self.keyboard_software = self._find_keyboard_software()
    
    def _load_config(self):
        """Загрузка конфигурации из файла"""
        config_file = "config.json"
        default_config = {
            "keyboard_manufacturer": "unknown",
            "keyboard_model": "unknown",
            "backlight_method": "auto",
            "backlight_hotkey": "F12",
            "monitor_timeout": 10
        }
        
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Обновляем значения по умолчанию
                    for key, value in default_config.items():
                        if key not in config:
                            config[key] = value
                    return config
            except:
                pass
        
        return default_config
    
    def _save_config(self):
        """Сохранение конфигурации"""
        try:
            with open("config.json", 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            return True
        except:
            return False
    
    def _find_keyboard_software(self):
        """Поиск установленного ПО для клавиатуры"""
        software = {}
        
        # Logitech G Hub
        logitech_paths = [
            r"C:\Program Files\LGHUB\lghub.exe",
            r"C:\Program Files\Logitech\G HUB\lghub.exe",
            r"C:\Program Files\Logitech Gaming Software\LCore.exe"
        ]
        for path in logitech_paths:
            if os.path.exists(path):
                software['logitech'] = path
                break
        
        # Razer Synapse
        razer_paths = [
            r"C:\Program Files\Razer\Razer Synapse\Razer Synapse.exe",
            r"C:\Program Files (x86)\Razer\Razer Synapse\Razer Synapse.exe"
        ]
        for path in razer_paths:
            if os.path.exists(path):
                software['razer'] = path
                break
        
        # Corsair iCUE
        corsair_paths = [
            r"C:\Program Files\Corsair\CORSAIR iCUE Software\iCUE.exe",
            r"C:\Program Files (x86)\Corsair\CORSAIR iCUE Software\iCUE.exe"
        ]
        for path in corsair_paths:
            if os.path.exists(path):
                software['corsair'] = path
                break
        
        # SteelSeries GG
        steelseries_paths = [
            r"C:\Program Files\SteelSeries\SteelSeries Engine\SteelSeriesEngine.exe",
            r"C:\Program Files\SteelSeries\GG\SteelSeriesGG.exe"
        ]
        for path in steelseries_paths:
            if os.path.exists(path):
                software['steelseries'] = path
                break
        
        # HyperX NGenuity
        hyperx_paths = [
            r"C:\Program Files\HyperX\NGenuity\NGenuity.exe",
            r"C:\Program Files (x86)\HyperX\NGenuity\NGenuity.exe"
        ]
        for path in hyperx_paths:
            if os.path.exists(path):
                software['hyperx'] = path
                break
        
        # OpenRGB (если установлен)
        openrgb_paths = [
            r"C:\Program Files\OpenRGB\OpenRGB.exe",
            r"C:\Program Files (x86)\OpenRGB\OpenRGB.exe"
        ]
        for path in openrgb_paths:
            if os.path.exists(path):
                software['openrgb'] = path
                break
        
        return software
    
    def get_windows_version(self):
        """Получение версии Windows"""
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
            product_name = winreg.QueryValueEx(key, "ProductName")[0]
            display_version = winreg.QueryValueEx(key, "DisplayVersion")[0]
            current_build = winreg.QueryValueEx(key, "CurrentBuild")[0]
            winreg.CloseKey(key)
            
            build_number = int(current_build)
            if build_number >= 22000:
                if "Home" in product_name:
                    return f"Windows 11 Home {display_version} (Build {current_build})"
                elif "Pro" in product_name:
                    return f"Windows 11 Pro {display_version} (Build {current_build})"
                else:
                    return f"Windows 11 {display_version} (Build {current_build})"
            else:
                return f"{product_name} {display_version} (Build {current_build})"
        except:
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
        """Установка таймаута монитора"""
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
    
    def turn_off_keyboard_backlight(self):
        """Выключение подсветки клавиатуры (универсальный метод)"""
        method = self.config.get('backlight_method', 'auto')
        
        if method == 'none':
            print("ℹ️ Подсветка отключена в настройках")
            return True
        
        # Пробуем программные методы
        if method in ['auto', 'software']:
            if self.keyboard_software:
                for software_name, path in self.keyboard_software.items():
                    if self._turn_off_via_software(software_name, path):
                        return True
        
        # Пробуем горячую клавишу
        if method in ['auto', 'hotkey']:
            hotkey = self.config.get('backlight_hotkey', 'F12')
            if self._turn_off_via_hotkey(hotkey):
                return True
        
        # Если ничего не сработало
        print("⚠️ Не удалось выключить подсветку автоматически")
        print("💡 Варианты решения:")
        print("1. Нажмите Fn+" + self.config.get('backlight_hotkey', 'F12') + " вручную")
        print("2. Или настройте программу под свою клавиатуру")
        print("3. Или отключите управление подсветкой в настройках")
        return False
    
    def _turn_off_via_software(self, software_name, path):
        """Выключение через ПО производителя"""
        try:
            if software_name == 'logitech':
                subprocess.run([path, '--backlight=off'], capture_output=True, timeout=5)
                print("✅ Подсветка выключена (Logitech G Hub)")
                return True
            elif software_name == 'razer':
                subprocess.run([path, '--brightness=0'], capture_output=True, timeout=5)
                print("✅ Подсветка выключена (Razer Synapse)")
                return True
            elif software_name == 'corsair':
                subprocess.run([path, '--brightness=0'], capture_output=True, timeout=5)
                print("✅ Подсветка выключена (Corsair iCUE)")
                return True
            elif software_name == 'steelseries':
                subprocess.run([path, '--brightness=0'], capture_output=True, timeout=5)
                print("✅ Подсветка выключена (SteelSeries GG)")
                return True
            elif software_name == 'hyperx':
                subprocess.run([path, '--brightness=0'], capture_output=True, timeout=5)
                print("✅ Подсветка выключена (HyperX NGenuity)")
                return True
            elif software_name == 'openrgb':
                subprocess.run([path, '--mode', 'off'], capture_output=True, timeout=5)
                print("✅ Подсветка выключена (OpenRGB)")
                return True
        except:
            pass
        return False
    
    def _turn_off_via_hotkey(self, hotkey):
        """Выключение через горячую клавишу"""
        # F1-F12 клавиши
        hotkeys = {
            'F1': 0x70, 'F2': 0x71, 'F3': 0x72, 'F4': 0x73,
            'F5': 0x74, 'F6': 0x75, 'F7': 0x76, 'F8': 0x77,
            'F9': 0x78, 'F10': 0x79, 'F11': 0x7A, 'F12': 0x7B
        }
        
        if hotkey in hotkeys:
            try:
                vk_code = hotkeys[hotkey]
                # Пытаемся отправить нажатие
                ctypes.windll.user32.keybd_event(vk_code, 0, 0, 0)
                time.sleep(0.05)
                ctypes.windll.user32.keybd_event(vk_code, 0, 2, 0)
                print(f"✅ Отправлена клавиша {hotkey} (проверьте подсветку)")
                return True
            except:
                pass
        return False
    
    def turn_on_keyboard_backlight(self):
        """Включение подсветки"""
        method = self.config.get('backlight_method', 'auto')
        
        if method == 'none':
            return True
        
        # Пробуем программные методы
        if self.keyboard_software:
            for software_name, path in self.keyboard_software.items():
                try:
                    if software_name == 'logitech':
                        subprocess.run([path, '--backlight=100'], capture_output=True, timeout=5)
                        print("✅ Подсветка включена (Logitech)")
                        return True
                    elif software_name == 'razer':
                        subprocess.run([path, '--brightness=100'], capture_output=True, timeout=5)
                        print("✅ Подсветка включена (Razer)")
                        return True
                    elif software_name == 'openrgb':
                        subprocess.run([path, '--mode', 'static', '--color', 'ffffff'], 
                                     capture_output=True, timeout=5)
                        print("✅ Подсветка включена (OpenRGB)")
                        return True
                except:
                    pass
        
        return False
    
    def show_keyboard_info(self):
        """Информация о клавиатуре"""
        print("\n" + "=" * 50)
        print("ИНФОРМАЦИЯ О КЛАВИАТУРЕ")
        print("=" * 50)
        
        print(f"Производитель: {self.config.get('keyboard_manufacturer', 'Неизвестно')}")
        print(f"Модель: {self.config.get('keyboard_model', 'Неизвестно')}")
        print(f"Метод управления: {self.config.get('backlight_method', 'auto')}")
        print(f"Горячая клавиша: Fn+{self.config.get('backlight_hotkey', 'F12')}")
        
        if self.keyboard_software:
            print("\n✅ Найдено ПО:")
            for name, path in self.keyboard_software.items():
                print(f"   - {name.upper()}: {path}")
        else:
            print("\n❌ ПО не найдено")
        
        print("\n💡 Поддерживаемые клавиатуры:")
        print("1. Logitech (G Hub)")
        print("2. Razer (Synapse)")
        print("3. Corsair (iCUE)")
        print("4. SteelSeries (GG)")
        print("5. HyperX (NGenuity)")
        print("6. OpenRGB (универсальное)")
        print("7. Любые клавиатуры (Fn+F1-F12)")
    
    def show_system_info(self):
        """Информация о системе"""
        print("\n" + "=" * 50)
        print("ИНФОРМАЦИЯ О СИСТЕМЕ")
        print("=" * 50)
        
        windows_version = self.get_windows_version()
        print(f"ОС: {windows_version}")
        
        try:
            processor = platform.processor()
            if processor:
                print(f"Процессор: {processor}")
        except:
            pass
        
        try:
            total_ram = psutil.virtual_memory().total / (1024**3)
            print(f"Оперативная память: {total_ram:.1f} GB")
        except:
            pass
        
        try:
            import wmi
            c = wmi.WMI()
            for gpu in c.Win32_VideoController():
                print(f"Видеокарта: {gpu.Name}")
                break
        except:
            pass
        
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        print(f"Права администратора: {'Да' if is_admin else 'Нет'}")
    
    def start_farming_mode(self, monitor_timeout=10, disable_backlight=True):
        """Запуск режима фарма"""
        print("\n" + "=" * 50)
        print("РЕЖИМ ФАРМА АКТИВИРОВАН")
        print("=" * 50)
        print(f"Монитор выключится через {monitor_timeout} сек. бездействия")
        if disable_backlight and self.config.get('backlight_method') != 'none':
            print("Подсветка клавиатуры будет выключена")
        print(f"Для выхода нажмите Ctrl+C")
        print("=" * 50 + "\n")
        
        self.monitor_timeout = monitor_timeout
        
        print("Применение настроек...")
        self.disable_screensaver()
        self.set_monitor_timeout(monitor_timeout)
        
        if disable_backlight:
            self.turn_off_keyboard_backlight()
        
        print("Настройки применены")
        print("Не трогайте мышь и клавиатуру!\n")
        
        self.is_farming = True
        self.last_activity_time = time.time()
        last_status_time = 0
        backlight_on = not disable_backlight
        
        try:
            while self.is_farming:
                current_time = time.time()
                
                if self.check_user_activity():
                    self.last_activity_time = current_time
                    if not self.monitor_on:
                        self.turn_on_monitor()
                        if disable_backlight and not backlight_on:
                            self.turn_on_keyboard_backlight()
                            backlight_on = True
                else:
                    if self.monitor_on and current_time - self.last_activity_time > monitor_timeout:
                        self.turn_off_monitor()
                        if disable_backlight and backlight_on:
                            self.turn_off_keyboard_backlight()
                            backlight_on = False
                
                if current_time - last_status_time > 5:
                    if self.monitor_on:
                        remaining = monitor_timeout - int(current_time - self.last_activity_time)
                        if remaining > 0:
                            status = f"Монитор выключится через {remaining} сек."
                        else:
                            status = "Выключение..."
                    else:
                        status = "Монитор выключен (игра работает)"
                        if not backlight_on:
                            status += " | Подсветка выключена"
                    
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
        
        self.turn_on_keyboard_backlight()
        
        print("Восстановление таймаута монитора...")
        self.set_monitor_timeout(600)
        
        print("Режим фарма остановлен")
        print("Настройки восстановлены")

def main():
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
        print("3. Запустить фарм (своё время)")
        print("4. Тест: выключить монитор")
        print("5. Тест: выключить подсветку клавиатуры")
        print("6. Настройки клавиатуры")
        print("7. Информация о системе")
        print("8. Выход")
        print("=" * 50)
        
        choice = input("\nВыберите действие (1-8): ").strip()
        
        if choice == "1":
            helper.start_farming_mode(monitor_timeout=10, disable_backlight=True)
        elif choice == "2":
            helper.start_farming_mode(monitor_timeout=30, disable_backlight=True)
        elif choice == "3":
            try:
                timeout = int(input("Через сколько секунд выключить монитор? (5-600): "))
                timeout = max(5, min(timeout, 600))
                helper.start_farming_mode(monitor_timeout=timeout, disable_backlight=True)
            except ValueError:
                print("Ошибка: введите число!")
        elif choice == "4":
            print("\nВыключение монитора через 3 секунды...")
            for i in range(3, 0, -1):
                print(f"   {i}...")
                time.sleep(1)
            helper.turn_off_monitor()
        elif choice == "5":
            print("\nВыключение подсветки...")
            helper.turn_off_keyboard_backlight()
        elif choice == "6":
            print("\nНастройки клавиатуры:")
            print("В разработке...")
            helper.show_keyboard_info()
        elif choice == "7":
            helper.show_system_info()
        elif choice == "8":
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