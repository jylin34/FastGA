#include <gtest/gtest.h>
#include "individual.hpp"

// 測試套件名稱：IndividualTest
// 測試案例名稱：InitialAgeIsZero
TEST(IndividualTest, InitialAgeIsZero) {
    // 準備 (Arrange): 建立一個 Individual 物件
    Individual ind(10);

    // 斷言 (Assert): 驗證物件的初始年齡是否為 0
    EXPECT_EQ(ind.fitness(), 0.0);
}
