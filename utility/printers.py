import ctypes
import win32print
import win32ui
import win32con

comdlg32 = ctypes.windll.comdlg32


class PRINT_VIEW(ctypes.Structure):
    _fields_ = [
        ("lStructSize", ctypes.c_ulong),
        ("hwndOwner", ctypes.c_void_p),
        ("hDevMode", ctypes.c_void_p),
        ("hDevNames", ctypes.c_void_p),
        ("hDC", ctypes.c_void_p),
        ("Flags", ctypes.c_ulong),
        ("nFromPage", ctypes.c_ushort),
        ("nToPage", ctypes.c_ushort),
        ("nMinPage", ctypes.c_ushort),
        ("nMaxPage", ctypes.c_ushort),
        ("nCopies", ctypes.c_ushort),
        ("hInstance", ctypes.c_void_p),
        ("lCustData", ctypes.c_ulong),
        ("lpfnPrintHook", ctypes.c_void_p),
        ("lpfnSetupHook", ctypes.c_void_p),
        ("lpPrintTemplateName", ctypes.c_void_p),
        ("lpSetupTemplateName", ctypes.c_void_p),
        ("hPrintTemplate", ctypes.c_void_p),
        ("hSetupTemplate", ctypes.c_void_p)
    ]
    def test(self):
        dlg = PRINT_VIEW()
        dlg.lStructSize = ctypes.sizeof(PRINT_VIEW)
        dlg.Flags = 0x00000001  # PD_RETURNDC

        if comdlg32.PrintDlgW(ctypes.byref(dlg)):
            print("Printer selected!")
        else:
            print("Dialog canceled or failed.")

class Priterinfolist():
    def __init__(self):
        self.printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1)
    def print_info(self):
        try:
            print("Connected Printers (Windows):")
            for printer_info in self.printers:
                print(printer_info[2]) 
        except Exception as e:
            print(f"Error retrieving printers on Windows: {e}")
class Printer_sent():
    def __init__(self):
        self.printer_name = win32print.GetDefaultPrinter()
        self.hprinter = win32print.OpenPrinter(self.printer_name)
        self.printer_info = win32print.GetPrinter(self.hprinter, 2)
    def print_text(self,header_text,table_datas:list,footer_text):
        self.pdc = win32ui.CreateDC()
        self.pdc.CreatePrinterDC(self.printer_name)
        self.pdc.StartDoc("print kivy")
        self.pdc.StartPage()
        width = self.pdc.GetDeviceCaps(8)   # HORZRES
        height = self.pdc.GetDeviceCaps(10) # VERTRES
        header_text = header_text
        self.pdc.SetTextAlign(win32con.TA_CENTER)
        self.pdc.TextOut(width // 2, 100, header_text)
        table_data = table_datas
        cell_width = width // len(table_data[0]) - 20
        cell_height = 100
        y = 250
        margin_line=height - 100
        for row in table_data:
            x = 70
            for cell in row:
                self.pdc.TextOut(x, y, str(cell))
                x += cell_width
                #self.pdc.Rectangle((x - 5, y - 5, x + cell_width, y + cell_height))
                # if margin_line > y:
                #     break
            y += 150

        footer_text = footer_text
        self.pdc.TextOut(width // 2, height - 100, footer_text)
        self.pdc.EndPage()
        self.pdc.EndDoc()
        self.pdc.DeleteDC()