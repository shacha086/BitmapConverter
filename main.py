import dearpygui.dearpygui as dpg
import pyperclip
import rotate_matrix

# =====================
# 常量与全局变量
# =====================
ROWS, COLS = 8, 8
CELL_SIZE = 20
matrix = [[0 for _ in range(COLS)] for _ in range(ROWS)]
row_scanning = False


def redraw_bitmap():
    """重绘位图矩阵到画布"""
    dpg.delete_item("canvas", children_only=True)
    for i in range(ROWS):
        for j in range(COLS):
            color = (0, 0, 0, 255) if matrix[i][j] else (255, 255, 255, 255)
            x0, y0 = j * CELL_SIZE, i * CELL_SIZE
            x1, y1 = x0 + CELL_SIZE, y0 + CELL_SIZE
            dpg.draw_rectangle((x0, y0), (x1, y1), fill=color, color=(200, 200, 200, 50), parent="canvas")


def set_matrix_at_mouse(value):
    """根据鼠标位置设置矩阵值"""
    if not dpg.is_item_hovered("canvas"):
        return
    local_x, local_y = dpg.get_drawing_mouse_pos()
    j = int(local_x // CELL_SIZE)
    i = int(local_y // CELL_SIZE)
    if 0 <= i < ROWS and 0 <= j < COLS:
        matrix[i][j] = value
        redraw_bitmap()


def mouse_left_press(sender, app_data):
    set_matrix_at_mouse(1)


def mouse_left_drag(sender, app_data):
    set_matrix_at_mouse(1)


def mouse_right_press(sender, app_data):
    set_matrix_at_mouse(0)


def mouse_right_drag(sender, app_data):
    set_matrix_at_mouse(0)


def clear_matrix(sender, app_data):
    global matrix
    matrix = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    redraw_bitmap()


def copy_matrix(sender, app_data):
    mat = matrix if row_scanning else rotate_matrix.clockwise(matrix)
    output = f'{{{", ".join(hex(sum(b << (len(row) - 1 - i) for i, b in enumerate(row))) for row in mat)}}}'
    pyperclip.copy(output)
    dpg.set_item_label(sender, "Copied")
    dpg.set_frame_callback(dpg.get_frame_count() + 120, lambda: dpg.set_item_label(sender, "Copy"))


def toggle_scan_mode(sender, app_data):
    global row_scanning
    row_scanning = not row_scanning
    dpg.set_item_label(sender, "Row Scanning" if row_scanning else "Column Scanning")


# =====================
# DearPyGui UI 构建
# =====================
dpg.create_context()

with dpg.window(label="Bitmap Editor"):
    with dpg.drawlist(width=COLS * CELL_SIZE, height=ROWS * CELL_SIZE, tag="canvas"):
        pass
    with dpg.handler_registry():
        dpg.add_mouse_click_handler(callback=mouse_left_press, button=dpg.mvMouseButton_Left)
        dpg.add_mouse_click_handler(callback=mouse_right_press, button=dpg.mvMouseButton_Right)
        dpg.add_mouse_drag_handler(callback=mouse_left_drag, button=dpg.mvMouseButton_Left)
        dpg.add_mouse_drag_handler(callback=mouse_right_drag, button=dpg.mvMouseButton_Right)
    with dpg.group(horizontal=True):
        clear_btn = dpg.add_button(label="Clear")
        copy_btn = dpg.add_button(label="Copy")
        dpg.set_item_callback(clear_btn, clear_matrix)
        dpg.set_item_callback(copy_btn, copy_matrix)
    scan_btn = dpg.add_button(label="Column Scanning")
    dpg.set_item_callback(scan_btn, toggle_scan_mode)

redraw_bitmap()

dpg.create_viewport(title='Bitmap Editor', width=COLS * CELL_SIZE + 40, height=ROWS * CELL_SIZE + 128)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
