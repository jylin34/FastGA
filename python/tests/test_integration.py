import fastga
import pytest

def test_individual_creation_and_name():
    """
    測試是否可以從 Python 成功建立 Individual 物件，
    並驗證 get_name() 方法是否如預期運作。
    """
    # 準備 (Arrange) & 執行 (Act):
    # 從 C++ 模組建立一個物件
    try:
        ind = fastga.Individual("PythonTest")
    except Exception as e:
        pytest.fail(f"Failed to create fastga.Individual object: {e}")

    # 斷言 (Assert):
    # 驗證 C++ 方法的回傳值是否正確
    assert ind.get_name() == "My name is PythonTest"
