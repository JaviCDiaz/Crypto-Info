from utils.QtCore import *

class Settings ():
    def __init__(self):
        # APP SETTINGS
        self.app_settings = {
            # APP SETTINGS
            'window_title': 'Crypto Info',
            'app_logo': 'app_logo.png',
            'app_corner_radius': 10,

            # UI MAIN SETTINGS
            'start_width': 1450,
            'start_height': 850,
            'minimum_width': 1450,
            'minimum_height': 850,

            # EXCHANGE SETTINGS
            'exchange_list': ['Binance', 'KuCoin', 'GateIO', 'Kraken', 'Huobi', 'Coinbase', 'OKEx']
        }

        # TITLE BAR SETTINGS
        self.title_bar_settings = {
            # TITLE BAR (tb)
            'tb_bg_color': '#202020',
            'tb_height': 40,
            'tb_logo_size': 20,
            'tb_logo_name': 'app_logo.png',

            'tb_title': 'Crypto Info',
            'tb_title_font_weight': 800,
            'tb_title_font_size': 10,
            'tb_title_font_family': 'Segoe UI',
            'tb_title_color': '#aaaaaa',

            # ---- MINIMIZE BTN (tb_minimize_btn)
            'tb_minimize_btn_tooltip_text': 'Minimizar',
            'tb_minimize_btn_icon_path': 'icon_minimize.svg',
            
            # ---- MAXIMIZE-RESTORE BTN (tb_maximize_btn)
            'tb_maximize_btn_tooltip_text': 'Maximizar',
            'tb_maximize_btn_restore_tooltip_text': 'Minimizar tamaño',
            'tb_maximize_btn_icon_path': 'icon_maximize.svg',
            'tb_maximize_btn_restore_icon_path': 'icon_restore.svg',
            
            # ---- CLOSE BTN (tb_close_btn)
            'tb_close_btn_tooltip_text': 'Cerrar',
            'tb_close_btn_icon_path': 'icon_close.svg',

            # ---- TITLE BAR BUTTONS STYLE (tb_btn)
            'tb_btn_width': 24,
            'tb_btn_height': 24,
            'tb_btn_radius': 12,

            'tb_btn_bg_color_hover': '#404040',
            'tb_btn_bg_color_pressed': '#353535',
            'tb_btn_close_bg_color_hover': '#de1414',
            'tb_btn_close_bg_color_pressed': '#b01010',

            'tb_btn_icon_color_inactive': '#c3ccdf',
            'tb_btn_icon_color_hover': '#dce1ec',
            'tb_btn_icon_color_pressed': '#edf0f5',
        }

        # TOOLTIP SETTINGS    
        self.tooltip_settings = {
            # TOOLTIP (tt)
            'tt_bg_color': '#151515',
            'tt_border_color': '#ffc50c',
            'tt_text_color': '#aaaaaa',
        }

         # CUSTOM LINE EDIT SETTINGS
        self.custom_line_edit_settings = {
            # LINE EDIT (le)
            'le_unfocus_border_color': '#cccccc',
            'le_focus_border_color': '#ffc50c',
            'le_border_radius': 5, # 20 TO COMPLETED ROUNDED RECT

            # BG COLORS (le_bg)
            'le_bg_unfocus_color': '#ffffff',
            'le_bg_focus_color': '#ffffff',

            # TEXT COLORS (le_txt)
            'le_txt_unfocus_color': '#777777',
            'le_txt_focus_color': '#252525',
            'le_txt_unfocus_placeholder_color': '#aaaaaa',
            'le_txt_focus_placeholder_color': '#aaaaaa',

            # SEARCH ICON
            'le_search_icon_name': 'icon_search.png',
            'le_search_icon_color': '#777777'
        }

        # COIN COMPLETER
        self.coin_completer_settings = {
            # LISTVIEW (coin_comp_list)
            'coin_comp_list_bg_color': '#ffffff',
            'coin_comp_list_item_height': 30,

            # SCROLLBAR (coin_comp_scroll)
            'coin_comp_scroll_width': 10,
            'coin_comp_scroll_handler_color': '#ffc50c',

            # ITEM DELEGATE (coin_comp_item)
            'coin_comp_item_bg_color_hover': '#ffefbd',
            'coin_comp_item_default_icon_name': 'BTC_16.png',
            'coin_comp_item_text_color': '#111111'
        }

        # COMBOBOX SETTINGS
        self.combobox_settings = {
            # COMBOBOX (cbox)
            'cbox_unfocus_bg_color': '#ffffff',
            'cbox_focus_bg_color': '#ffffff',
            'cbox_unfocus_border_color': '#cccccc',
            'cbox_focus_border_color': '#ffc50c',
            'cbox_border_radius': 5, # 20 TO COMPLETED ROUNDED RECT
            
            # TEXT
            'cbox_txt_unfocus_color': '#777777',
            'cbox_txt_focus_color': '#252525',
            'cbox_font_weight': 600,
            'cbox_font_size': 12,
            'cbox_font_family': 'Segoe UI',

            # POPUP (cbox_popup)
            'cbox_popup_bg_color': '#ffffff',
            'cbox_popup_item_height': 30,

            # DROPDOWN ICON (cbox_icon)
            'cbox_icon_unfocus': 'icon_dropdown_down.png',
            'cbox_icon_unfocus_color': '#777777',
            'cbox_icon_focus': 'icon_dropdown_up.png',
            'cbox_icon_focus_color': '#252525',

            # ITEM DELEGATE (cbox_item)
            'cbox_item_bg_color_hover': '#ffefbd',
            'cbox_item_text_color': '#111111'
        }

        # TABLE CLIENTS SETTINGS
        self.table_settings = {
            # table style (table)
            'table_text_color': '#cccccc',

            'table_header_text_color': '#252525',
            'table_header_font_weight': 600,
            'table_header_font_size': 13,
            'table_header_font_family': 'Segoe UI',

            'table_Vscrollbar_bg_color': 'transparent',
            'table_Vscrollbar_width': 6,
            'table_Vscrollbar_handle_bar_color': '#ffc50c',

            # item delegate (table_item)
            'table_item_pen_color': '#cccccc'
        }

        # CLIENTS DATABASE SETTINGS
        self.coins_database_settings = {
            # DATABASE (db)
            'db_file_name': 'coins_db.db',
            'db_table_name': 'coins'
        }
    