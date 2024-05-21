import tkinter as tk
from tkinter import E
from tkinter import font
from tkcalendar import Calendar
import datetime

class Applicatinon(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
                
        """タイトルとサイズの設定"""
        self.master.title('在庫移動経歴自動収集アプリ')
        self.master.geometry('500x600')
        self.master.resizable(True, True)

        """フォントの設定"""
        self.font_frame = font.Font(family='Meiryo UI', size=15, weight='normal')
        self.font_btn_big = font.Font(family='Meiryo UI', size=20, weight='bold')
        self.font_btn_small = font.Font(family='Meiryo UI', size=15, weight='bold')

        self.font_lbl_bigger = font.Font(family='Meiryo UI', size=45, weight='bold')
        self.font_lbl_big = font.Font(family='Meiryo UI', size=30, weight='bold')
        self.font_lbl_middle = font.Font(family='Meiryo UI', size=15, weight='bold')
        self.font_lbl_small = font.Font(family='Meiryo UI', size=12, weight='normal')
        
        """config.txtの読み込み"""
        with open('config.txt', 'r', encoding='UTF-8') as f:
            txt_data = list(f)
            # 改行の削除
            self.metadata_list = [text.strip() for text in txt_data ]

        """日本時間の設定"""
        time_delta = datetime.timedelta(hours=9)
        jst = datetime.timezone(time_delta, 'jst')
        now = datetime.datetime.now(jst)
        self.today = now.date().strftime('%Y/%m/%d')
        self.today_1 = now.date().strftime('%Y%m%d')
        self.calender_date = now.date().strftime('%Y/%m/%d')

        """ウィジェットの配置"""
        self.create_widgets()
                
    # メインウィンドウの各種ウィジェット
    def create_widgets(self):

        # 入力項目用のフレーム
        self.frame_input = tk.Frame(self.master)
        self.frame_input.pack()

        self.add_txt = tk.Label(self.frame_input, text='対象コストセンタ', font=self.font_lbl_small)
        self.add_txt.grid(row=0, column=0, pady=10, columnspan=2)

        # コストセンタの表示
        row_index = 1
        for cost_center in self.metadata_list[1:5]:
            label = tk.Label(self.frame_input, text=cost_center, font=self.font_lbl_small)
            label.grid(row=row_index, column=0, padx=10, pady=1, columnspan=2)
            row_index += 1

        '''G.CIPログイン入力フォーム'''    
        self.add_txt_2 = tk.Label(self.frame_input, text='G.CIPログイン情報を入力してください。', font=self.font_lbl_small)
        self.add_txt_2.grid(row=5, column=0, pady=10, columnspan=2)

        self.add_txt_3 = tk.Label(self.frame_input, text='社員番号:', font=self.font_lbl_small)
        self.add_txt_3.grid(row=6, column=0, pady=10, sticky=E)

        self.user_name_input = tk.Entry(self.frame_input, width=30)
        self.user_name_input.insert(0, "")
        self.user_name_input.grid(row=6, column=1, sticky=E)

        self.add_txt_4 = tk.Label(self.frame_input, text='G.CIPパスワード:', font=self.font_lbl_small)
        self.add_txt_4.grid(row=7, column=0, pady=10, sticky=E)

        self.user_pass_input = tk.Entry(self.frame_input, width=30, show="*")
        self.user_pass_input.insert(0, "")
        self.user_pass_input.grid(row=7, column=1, sticky=E)

        # 集計期間の入力
        self.add_txt_5 = tk.Label(self.frame_input, text='ボタンから集計期間を選択してください。', font=self.font_lbl_small)
        self.add_txt_5.grid(row=10, column=0, pady=10, columnspan=2)

        self.test_btn2 = tk.Button(self.frame_input, text='開始期間を選択')
        self.test_btn2.configure(width=12, height=1, command=self.start_tarm_dialog)
        self.test_btn2.grid(row=11, column=0, pady=10, sticky=E)

        self.var = tk.StringVar()
        self.var.set(self.calender_date)
        self.start_input_tarm = tk.Label(self.frame_input,textvariable=self.var,
                                         font=self.font_lbl_small,
                                         anchor=tk.W) 
        self.start_input_tarm.grid(row=11, column=1,)

        self.test_btn3 = tk.Button(self.frame_input, text='終了期間を選択')
        self.test_btn3.configure(width=12, height=1, command=self.end_tarm_dialog)
        self.test_btn3.grid(row=12, column=0, pady=10,sticky=E)
        
        self.var2 = tk.StringVar()
        self.var2.set(self.calender_date)
        self.end_input_tarm = tk.Label(self.frame_input, textvariable=self.var2,
                                       font=self.font_lbl_small,
                                       anchor=tk.W)
        self.end_input_tarm.grid(row=12, column=1,)
        
        # 出力データ保存先
        self.save_frame = tk.Frame(self.master)
        self.save_frame.pack()

        # 出力ボタンの配置
        self.dir_button_3 = tk.Button(self.save_frame, text="出力", font=self.font_btn_big)
        self.dir_button_3.configure(width=10, height=1, command=self.get_val)
        self.dir_button_3.grid(row=2, column=0, columnspan=2)
        
        # ファイルの保存先パスをテキストで表示する
        self.add_txt_6 = tk.Label(self.save_frame, text='保存先:',)
        self.add_txt_6.grid(row=3, column=0, pady=10)

        self.var3 = tk.StringVar()
        self.var3.set(self.metadata_list[-1])
        self.data_save_path = tk.Label(self.save_frame, textvariable=self.var3,
                                       anchor=tk.W)
        self.data_save_path.grid(row=3, column=1,)

        
        
    '''日付カレンダー用関数'''
    def start_tarm_dialog(self):
        
        top = tk.Toplevel(self)
        top.title('日付の選択')
        
        def add_start_input_tarm():
            self.calender_date = str(cal.selection_get().strftime('%Y/%m/%d'))
            self.var.set(self.calender_date)
            top.destroy()

        cal = Calendar(top, font="Arial 14", selectmode='day', locale='ja',
                    cursor="hand1", year=2024, month=1, day=1, showweeknumbers=False)

        cal.pack(fill="both", expand=True)
        ok_btn = tk.Button(top, text="OK")
        ok_btn.configure(width=10, height=2, command=add_start_input_tarm)
        ok_btn.pack()
    
    def end_tarm_dialog(self):
        
        top = tk.Toplevel(self)
        top.title('日付の選択')
        
        def add_end_input_tarm():
            self.calender_date = str(cal.selection_get().strftime('%Y/%m/%d'))
            self.var2.set(self.calender_date)
            top.destroy()

        cal = Calendar(top, font="Arial 14", selectmode='day', locale='ja',
                    cursor="hand1", year=2024, month=1, day=1, showweeknumbers=False)

        cal.pack(fill="both", expand=True)
        ok_btn = tk.Button(top, text="OK")
        ok_btn.configure(width=10, height=2, command=add_end_input_tarm)
        ok_btn.pack()

    '''
    スクレイピングに必要な情報

    self.metadata_list[1:5] -> コストセンタNo
    self.user_name_input -> 社員番号
    self.user_pass_input -> G.CIPパスワード
    self.start_input_tarm -> 開始期間
    self.end_input_tarm -> 終了期間

    '''
    def get_val(self):
        """
        スクレイピングに必要な情報を確認するための関数
        """
        # コストセンタNoのリストを取得
        cost_centers = self.metadata_list[1:5]
        print(f'コストセンタ{cost_centers}')
        # 社員番号とG.CIPパスワードを取得
        employee_number = self.user_name_input.get()
        print(f'社員番号: {employee_number}')
        gcip_password = self.user_pass_input.get()
        print(f"パスワード: {gcip_password}")
        # 開始期間と終了期間を取得
        start_period = self.start_input_tarm.cget("text")
        print(f"開始期間: {start_period}")
        end_period = self.end_input_tarm.cget("text")
        print(f"終了期間: {end_period}")

# ? exe化する際に必要なオプション。テスト運用モデルはコンソールを確認できる仕様
# ! pyinstaller --hidden-import babel.numbers qa_assy_add_cal.py --onefile --noconsole
def main():
    root = tk.Tk()
    app = Applicatinon(master=root)

    # ループ処理
    app.mainloop()


if __name__ == '__main__':
    main()



